"""Lê resultados.csv, confere os dados e atualiza a seção de testes do README.

Uso: python testes_usuarios/indicadores.py
"""
import re
import sys
from pathlib import Path

import pandas as pd

PASTA = Path(__file__).parent
PLANILHA = Path(sys.argv[1]) if len(sys.argv) > 1 else PASTA / "resultados.csv"
README = Path(sys.argv[2]) if len(sys.argv) > 2 else PASTA.parent / "README.md"

INICIO = "<!-- testes:inicio -->"
FIM = "<!-- testes:fim -->"

TAREFAS = {
    "t1": "T1: o que levar para a 2ª via do RG (perda)",
    "t2": "T2: preço e prazo da certidão pelo portal",
    "t3": "T3: atendimento aos sábados",
}
PERGUNTAS = {
    "q1": "Foi fácil encontrar a informação",
    "q2": "Linguagem fácil de entender",
    "q3": "Confiaria nas orientações",
    "q4": "Ficou claro de onde vinha a informação",
    "q5": "Usaria de novo",
}


def br(numero):
    return f"{numero:.1f}".replace(".", ",")


def conferir(dados):
    erros = []
    for i, linha in dados.iterrows():
        # só códigos P1, P2... para não guardar nome de ninguém
        if not re.fullmatch(r"P\d+", str(linha["participante"])):
            erros.append(f"linha {i + 2}: participante deve ser P1, P2... (sem nome)")
        for t in TAREFAS:
            if linha[f"{t}_acertou"] not in (0, 1):
                erros.append(f"linha {i + 2}: {t}_acertou deve ser 0 ou 1")
            if not linha[f"{t}_tempo_s"] > 0:
                erros.append(f"linha {i + 2}: {t}_tempo_s deve ser um número de segundos")
        for q in PERGUNTAS:
            if linha[q] not in (1, 2, 3, 4, 5):
                erros.append(f"linha {i + 2}: {q} deve ser uma nota de 1 a 5")
    return erros


def montar_secao(dados):
    n = len(dados)
    if n == 0:
        return "**Aguardando os testes.** Os resultados entram aqui quando `resultados.csv` for preenchido."

    linhas = [f"Participantes: **{n}** pessoas de fora do grupo, identificadas só como P1 a P{n}.", ""]
    if n < 5:
        linhas += [f"> O enunciado pede pelo menos 5 pessoas. Conseguimos {n}; os resultados valem como indicação, não como medida firme.", ""]

    linhas += ["**Tempo para encontrar a informação e acerto**", "",
               "| Tarefa | Tempo médio | Mediana | Mín–máx | Acertos |", "|---|---|---|---|---|"]
    for t, nome in TAREFAS.items():
        tempo = dados[f"{t}_tempo_s"]
        acertos = int(dados[f"{t}_acertou"].sum())
        linhas.append(f"| {nome} | {tempo.mean():.0f} s | {tempo.median():.0f} s | "
                      f"{tempo.min():.0f}–{tempo.max():.0f} s | {acertos}/{n} |")

    total = sum(int(dados[f"{t}_acertou"].sum()) for t in TAREFAS)
    linhas += ["", f"Acerto geral nas tarefas: **{total}/{3 * n} ({total / (3 * n):.0%})**.", ""]

    linhas += ["**Facilidade de uso** (1 = discordo totalmente, 5 = concordo totalmente)", "",
               "| Afirmação | Média | Notas |", "|---|---|---|"]
    for q, frase in PERGUNTAS.items():
        notas = ", ".join(str(int(x)) for x in dados[q])
        linhas.append(f"| {frase} | {br(dados[q].mean())} | {notas} |")
    media = dados[list(PERGUNTAS)].values.mean()
    linhas += ["", f"Média geral: **{br(media)} de 5**.", ""]

    # frases tiradas direto dos números; a interpretação o grupo escreve depois
    mais_lenta = max(TAREFAS, key=lambda t: dados[f"{t}_tempo_s"].mean())
    pior_nota = min(PERGUNTAS, key=lambda q: dados[q].mean())
    usou = dados["usou"].value_counts()
    linhas.append("**Destaques**")
    linhas.append("")
    linhas.append(f"- Tarefa mais demorada: {TAREFAS[mais_lenta]} (média de {dados[f'{mais_lenta}_tempo_s'].mean():.0f} s).")
    linhas.append(f"- Afirmação com a menor nota: \"{PERGUNTAS[pior_nota]}\" ({br(dados[pior_nota].mean())}).")
    linhas.append("- Como usaram: " + ", ".join(f"{k} ({v})" for k, v in usou.items()) + ".")

    comentarios = [c for c in dados["comentario"].dropna() if str(c).strip()]
    if comentarios:
        linhas += ["", "**Comentários dos participantes**", ""]
        linhas += [f"- \"{c}\"" for c in comentarios]

    if "observacao" in dados:
        obs = [f"{p}: {o}" for p, o in zip(dados["participante"], dados["observacao"]) if pd.notna(o) and str(o).strip()]
        if obs:
            linhas += ["", "**Observações do facilitador**", ""]
            linhas += [f"- {o}" for o in obs]
    return "\n".join(linhas)


def atualizar_readme(secao):
    texto = README.read_text(encoding="utf-8")
    if INICIO not in texto:
        raise SystemExit(f"Não achei {INICIO} no README.")
    antes, resto = texto.split(INICIO)
    _, depois = resto.split(FIM)
    README.write_text(f"{antes}{INICIO}\n{secao}\n{FIM}{depois}", encoding="utf-8")


if __name__ == "__main__":
    dados = pd.read_csv(PLANILHA)
    erros = conferir(dados)
    if erros:
        print("Corrija a planilha antes de continuar:")
        print("\n".join(f"- {e}" for e in erros))
        raise SystemExit(1)
    secao = montar_secao(dados)
    print(secao)
    atualizar_readme(secao)
    print(f"\nREADME atualizado ({len(dados)} participantes).")
