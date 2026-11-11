import json
import sys
import time
from pathlib import Path

import pandas as pd

from agente import criar_agente, perguntar
from juiz import julgar
from llm import criar_llm
from seguranca import ocultar_dados_pessoais

PASTA = Path(__file__).parent
RESULTADOS = PASTA / "resultados"
GOLDEN = json.loads((PASTA / "golden_dataset.json").read_text(encoding="utf-8"))


def gerar_respostas(versao):
    agente = criar_agente(versao)
    linhas = []
    for item in GOLDEN:
        inicio = time.time()
        saida = perguntar(agente, item["mensagem"])
        linhas.append({
            "id": item["id"],
            "tipo": item["tipo"],
            # a tabela mostra a mensagem já com os dados ocultados
            "mensagem": ocultar_dados_pessoais(item["mensagem"])[0],
            "rota": saida["rota"],
            "fichas": ", ".join(saida.get("fontes", [])),
            "resposta": saida["resposta"],
            "tempo_s": round(time.time() - inicio, 1),
        })
        print("resposta", item["id"], flush=True)
    RESULTADOS.mkdir(exist_ok=True)
    tabela = pd.DataFrame(linhas)
    tabela.to_csv(RESULTADOS / f"respostas_v{versao}.csv", index=False)
    return tabela


def julgar_respostas(versao):
    tabela = pd.read_csv(RESULTADOS / f"respostas_v{versao}.csv")
    juiz = criar_llm(saida_json=True)
    notas = []
    for item, resposta in zip(GOLDEN, tabela["resposta"]):
        nota = julgar(item, resposta, juiz)
        notas.append({
            "veredito": nota["veredito_final"],
            "veredito_llm": nota.get("veredito"),
            "cita_ficha": nota["cita_ficha_regra"],
            "vazou_dado": nota["vazou_dado_regra"],
            "sem_fonte": "; ".join(nota.get("sem_fonte") or []),
            "justificativa": nota.get("justificativa", ""),
        })
        print("juiz", item["id"], nota["veredito_final"], flush=True)
    tabela = pd.concat([tabela, pd.DataFrame(notas)], axis=1)
    tabela.to_csv(RESULTADOS / f"golden_v{versao}.csv", index=False)
    return tabela


if __name__ == "__main__":
    # python avaliacao.py 2          -> gera respostas e julga
    # python avaliacao.py 1 julgar   -> só julga as respostas já salvas
    versao = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if "julgar" not in sys.argv:
        gerar_respostas(versao)
    julgar_respostas(versao)
