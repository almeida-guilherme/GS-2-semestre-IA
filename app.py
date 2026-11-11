import streamlit as st

from agente import FICHAS, criar_agente, perguntar
from fichas import CATEGORIAS
from seguranca import LIMITE_CARACTERES

PERGUNTAS_MENU = {
    "FC-01": ["Quanto custa a segunda via do RG?", "Que documentos preciso para a segunda via do RG?",
              "Em quanto tempo fica pronto o RG?"],
    "FC-02": ["Como faço para me inscrever no CPF?", "Quanto custa tirar o CPF presencialmente?"],
    "FC-03": ["O título de eleitor é pago?", "Votar é obrigatório para quem tem 17 anos?"],
    "FC-04": ["Quanto custa e quanto demora a carteira de trabalho digital?"],
    "FC-05": ["Quanto custa a certidão de nascimento pelo portal?", "Posso pedir a certidão de outra pessoa?"],
    "FC-06": ["Com quanto tempo de antecedência posso renovar a CNH?", "Quanto custa renovar a CNH?"],
    "FC-07": ["Qual o horário de atendimento?", "Preciso de intérprete de Libras. Como faço?"],
}

st.set_page_config(page_title="Citizen Assist AI", page_icon="🪪")

# fonte maior e foco bem visível para quem usa só o teclado
st.markdown("""
<style>
html, body, [class*="css"] { font-size: 19px; }
button:focus-visible, input:focus-visible, textarea:focus-visible, [role="radio"]:focus-visible {
    outline: 3px solid #ffbf00 !important; outline-offset: 2px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def carregar_agente():
    return criar_agente(versao=4)


agente = carregar_agente()

st.title("Citizen Assist AI")
st.write("Tire dúvidas sobre RG, CPF, título de eleitor, carteira de trabalho, certidões e CNH.")
st.warning("**Não escreva dados pessoais** (CPF, RG, telefone, endereço, e-mail). "
           "Eu não preciso deles. Este é um protótipo educacional, não um canal oficial.")

if "resposta" not in st.session_state:
    st.session_state.resposta = None


def responder(texto):
    with st.spinner("Procurando nas fichas..."):
        saida = perguntar(agente, texto)
    # guardamos só a última resposta, sem histórico e sem a pergunta original
    st.session_state.resposta = saida["resposta"]


st.header("1. Escolha um assunto")
codigo = st.radio("Assunto", list(CATEGORIAS), format_func=lambda c: CATEGORIAS[c], horizontal=True)
for i, pergunta in enumerate(PERGUNTAS_MENU[codigo]):
    if st.button(pergunta, key=f"{codigo}-{i}"):
        responder(pergunta)
with st.expander("Ver a ficha completa"):
    st.markdown(FICHAS[codigo]["texto"])

st.header("2. Ou escreva sua pergunta")
with st.form("pergunta", clear_on_submit=True):
    texto = st.text_input("Sua pergunta (aperte Enter para enviar)", max_chars=LIMITE_CARACTERES + 50,
                          placeholder="Ex.: Perdi meu RG. Preciso levar boletim de ocorrência?")
    if st.form_submit_button("Perguntar"):
        responder(texto)

if st.session_state.resposta:
    st.header("Resposta")
    st.markdown(st.session_state.resposta)
