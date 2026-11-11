import re
from fichas import normalizar

LIMITE_CARACTERES = 400

# a ordem importa: CPF antes do padrão genérico de números
PADROES_DADOS = [
    ("e-mail", r"[\w.+-]+@[\w-]+\.[\w.]+"),
    ("CPF", r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    ("telefone", r"(\(?\b\d{2}\)?\s?)?\b9?\d{4}[-\s]?\d{4}\b"),
    ("CEP", r"\b\d{5}-\d{3}\b"),
    ("número de documento", r"\b\d[\d.\-]{6,}\d\b"),
]

# frases em que a pessoa anuncia ou entrega um dado pessoal
FRASES_DADOS = [
    r"meu nome (e|completo)", r"meu (cpf|rg|telefone|celular|endereco|e-?mail|pis|nis|titulo) (e|eh|:)",
    r"(passar|mandar|enviar|informar) (o )?meu (endereco|telefone|celular|cpf|rg|e-?mail)",
    r"meu endereco", r"meu telefone", r"moro na", r"minha renda",
]

PADROES_INJECAO = [
    r"ignor\w* (as |todas as )?(instrucoes|regras|ordens)",
    r"esque\w* (as |tudo|suas)",
    r"prompt (de|do) sistema", r"system prompt", r"instrucoes internas",
    r"\[ ?sistema ?\]", r"\[ ?system ?\]", r"nova regra", r"novas instrucoes",
    r"(voce|vc) agora e", r"finja (ser|que)", r"modo desenvolvedor", r"jailbreak",
    r"(mostre|revele|repita) (seu|o|as) (prompt|instrucoes|regras)",
]

PADROES_SOBRE = [
    r"canal oficial", r"(voce|vc) e (um|uma|o|a)? ?(robo|ia|humano|pessoa|oficial|atendente)",
    r"quem (e|eh) (voce|vc)", r"o que (voce|vc) (faz|sabe)", r"(voce|vc) e da prefeitura",
]


# pedidos de coisas que o assistente não faz (consultar, agendar, verificar por ele)
PADROES_ACAO = [
    r"(ver|verificar|consultar|checar) (a )?(minha|meu|sua) situacao", r"minha situacao",
    r"(voce|vc) (pode )?(agendar|marcar|consultar|verificar)", r"para (voce|vc) (agendar|marcar|consultar)",
    r"(agende|marque|consulte) (para mim|pra mim|meu|minha)",
]


def pede_acao(texto):
    texto = normalizar(texto)
    return any(re.search(p, texto) for p in PADROES_ACAO)


def ocultar_dados_pessoais(texto):
    """Troca dados pessoais por marcadores. Devolve o texto limpo e os tipos encontrados."""
    encontrados = []
    for tipo, padrao in PADROES_DADOS:
        if re.search(padrao, texto):
            encontrados.append(tipo)
            texto = re.sub(padrao, f"[{tipo.upper()} OCULTO]", texto)

    # nome depois de "meu nome é"
    nome = re.search(r"(?i)(meu nome (?:é|e|completo é)\s+)([A-ZÀ-Ú][\wÀ-ú]+(?:\s+[A-ZÀ-Ú][\wÀ-ú]+)*)", texto)
    if nome:
        encontrados.append("nome")
        texto = texto.replace(nome.group(2), "[NOME OCULTO]")
    return texto, encontrados


def menciona_dados_pessoais(texto):
    texto = normalizar(texto)
    return any(re.search(p, texto) for p in FRASES_DADOS)


def tem_injecao(texto):
    texto = normalizar(texto)
    return any(re.search(p, texto) for p in PADROES_INJECAO)


def pergunta_sobre_assistente(texto):
    texto = normalizar(texto)
    return any(re.search(p, texto) for p in PADROES_SOBRE)


SIGLAS = {"rg", "cpf", "cnh", "ctps", "pis", "nis", "pix", "pdf", "sms"}


def palavra_estranha(palavra):
    if palavra in SIGLAS:
        return False
    if not re.search(r"[aeiou]", palavra):
        return True
    # 4 consoantes seguidas quase não existe em português
    return bool(re.search(r"[^aeiou\W\d]{4,}", palavra))


def validar_entrada(texto):
    """Devolve None se a entrada é válida ou o motivo: vazia, longa ou sem_sentido."""
    if not texto or not texto.strip():
        return "vazia"
    if len(texto) > LIMITE_CARACTERES:
        return "longa"
    palavras = re.findall(r"[a-z]{2,}", normalizar(texto))
    if not palavras:
        return "sem_sentido"
    estranhas = sum(1 for p in palavras if palavra_estranha(p))
    if estranhas / len(palavras) >= 0.5:
        return "sem_sentido"
    return None
