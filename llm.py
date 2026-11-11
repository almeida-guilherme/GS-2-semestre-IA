import os

# PROVEDOR=ollama (padrão, roda local) ou openai (só se o professor liberar)
PROVEDOR = os.getenv("PROVEDOR", "ollama")
MODELO = os.getenv("MODELO", "qwen3.5:9b")


def criar_llm(modelo=None, temperatura=0, saida_json=False):
    modelo = modelo or MODELO
    if PROVEDOR == "openai":
        from langchain_openai import ChatOpenAI
        extra = {"response_format": {"type": "json_object"}} if saida_json else {}
        return ChatOpenAI(model=modelo, temperature=temperatura, model_kwargs=extra)

    from langchain_ollama import ChatOllama
    # reasoning=False desliga o "pensamento" do qwen, que deixa tudo bem mais lento
    return ChatOllama(model=modelo, temperature=temperatura, reasoning=False, num_ctx=8192,
                      format="json" if saida_json else None)
