import re
import unicodedata
from pathlib import Path

PASTA_FICHAS = Path(__file__).parent / "fichas"

# a FC-07 não tem linha de palavras-chave, então definimos aqui
PALAVRAS_FC07 = [
    "horario", "sabado", "domingo", "feriado", "atendem", "funciona",
    "agendar", "agendamento", "marcar", "procuracao", "outra pessoa", "terceiro",
    "filho", "filha", "crianca", "menor", "sozinho", "responsavel",
    "pagamento", "pagar", "pix", "boleto", "guia", "prioritario", "prioridade",
    "libras", "interprete", "deficiencia", "gestante", "idoso", "boletim",
    "privacidade", "dados pessoais",
]

# palavras que aparecem em várias fichas e sozinhas não definem o assunto
GENERICAS = {"segunda via", "2a via", "digital", "cadastro", "comprovante", "inscricao", "trabalho"}

CATEGORIAS = {
    "FC-01": "RG (Carteira de Identidade)",
    "FC-02": "CPF",
    "FC-03": "Título de eleitor",
    "FC-04": "Carteira de Trabalho",
    "FC-05": "Certidões",
    "FC-06": "CNH (renovação)",
    "FC-07": "Atendimento e regras gerais",
}


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.replace("ª", "a")


def carregar_fichas(pasta=PASTA_FICHAS):
    fichas = {}
    for arquivo in sorted(Path(pasta).glob("FC-*.md")):
        texto = arquivo.read_text(encoding="utf-8")
        codigo = arquivo.name[:5]
        titulo = texto.splitlines()[0].lstrip("# ").strip()

        achou = re.search(r"\*\*Palavras-chave:\*\*(.+)", texto)
        palavras = [p.strip() for p in achou.group(1).split(",")] if achou else []
        if codigo == "FC-07":
            palavras = PALAVRAS_FC07

        data = re.search(r"vers[aã]o de (\d{2}/\d{2}/\d{4})", texto)
        fichas[codigo] = {
            "codigo": codigo,
            "titulo": titulo,
            "palavras": [normalizar(p) for p in palavras],
            "texto": texto,
            "data": data.group(1) if data else "sem data",
        }
    return fichas


def pontuar(pergunta, ficha):
    pergunta = normalizar(pergunta)
    pontos = 0
    for palavra in ficha["palavras"]:
        # \b só no começo para aceitar plural (sabado -> sabados)
        if re.search(r"\b" + re.escape(palavra), pergunta):
            pontos += 1 if palavra in GENERICAS else 3
    return pontos


def buscar(pergunta, fichas, minimo=3):
    """Devolve os códigos das fichas relevantes, da mais para a menos pontuada."""
    notas = {cod: pontuar(pergunta, f) for cod, f in fichas.items()}
    maior = max(notas.values())
    if maior < minimo:
        return []

    escolhidas = [cod for cod, n in notas.items() if n >= maior / 2 and n >= minimo and cod != "FC-07"]
    escolhidas.sort(key=lambda c: -notas[c])
    # FC-07 complementa as outras fichas (horário, terceiros, pagamento...)
    if notas["FC-07"] >= minimo:
        escolhidas.append("FC-07")
    return escolhidas[:3]


if __name__ == "__main__":
    fichas = carregar_fichas()
    for pergunta in ["Quanto custa a segunda via do RG?", "Vocês atendem aos sábados?",
                     "Quanto custa tirar o passaporte?"]:
        print(pergunta, "->", buscar(pergunta, fichas))
