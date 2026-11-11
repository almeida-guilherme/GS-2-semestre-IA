import subprocess

from agente import criar_agente

# llm=1 só para montar o grafo, sem carregar o modelo
grafo = criar_agente(llm=1).get_graph()

nomes = {
    "__start__": "Mensagem do usuário",
    "proteger": "proteger\n(valida, oculta dados pessoais,\ndetecta injeção)",
    "buscar_fichas": "buscar_fichas\n(palavras-chave nas 7 fichas)",
    "gerar_resposta": "gerar_resposta\n(LLM só com as fichas encontradas)",
    "resposta_fixa": "resposta_fixa\n(inválida, fora do escopo,\ninjeção, canal oficial)",
    "finalizar": "finalizar\n(aviso, fonte e data,\noculta dados de novo)",
    "__end__": "Resposta",
}

linhas = ['digraph G {', 'rankdir=TB; node [shape=box, style="rounded,filled", fillcolor="#eef3fb", fontname="Helvetica"];',
          '"gerar_resposta" [fillcolor="#ffe9b3"];']
for no in grafo.nodes:
    linhas.append(f'"{no}" [label="{nomes.get(no, no)}"];')
for aresta in grafo.edges:
    estilo = ' [style=dashed]' if aresta.conditional else ''
    linhas.append(f'"{aresta.source}" -> "{aresta.target}"{estilo};')
linhas.append("}")

subprocess.run(["dot", "-Tpng", "-Gdpi=130", "-o", "diagrama_arquitetura.png"], input="\n".join(linhas).encode(), check=True)
print(grafo.draw_mermaid())
