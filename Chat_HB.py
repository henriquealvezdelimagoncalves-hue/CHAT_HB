# Streamlit e openai 

# Título 
# Input de mensagem cliente 
    # Salvar as mensagem que foram enviadas pelo usuario 
    # usar essas mensagem para a a Ia Responder 
    # aparecer a mensagem da IA na tela 
    # pegar chave api e modelo de ia 
    # editar streamlit para formatacao amigavel 
 
import streamlit as st 
from openai import OpenAI 
from PIL import Image
import hmac


def autenticar():
    if st.session_state.get("autenticado", False):
        return True

    st.title("Acesso ao sistema")

    with st.form("login", clear_on_submit=True):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar")

    if entrar:
        usuarios = st.secrets["usuarios"]

        senha_correta = False

        if usuario in usuarios:
            senha_correta = hmac.compare_digest(
                senha.encode("utf-8"),
                usuarios[usuario].encode("utf-8"),
            )

        if senha_correta:
            st.session_state["autenticado"] = True
            st.session_state["usuario_logado"] = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    return False


if not autenticar():
    st.stop()

if st.sidebar.button("Sair"):
    st.session_state.clear()
    st.rerun()

modelo_IA = OpenAI(
    api_key=st.secrets["gemini"]["api_key"].strip(),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

logo = Image.open("Logo_Hesselbach.png")
logo = logo.resize((300, 100),
    Image.Resampling.LANCZOS)

st.sidebar.image(logo, width=350)
# st.sidebar.image("logo_Hesselbach.png", width= 350)

st.html("""
    <h1 style="
        color: #f8fff7;
        font-size: 20px;
        font-family: Arial, sans-serif;
        text-align: center;
        font-weight: bold;
        background-color:;
        padding: 20px;
        border-radius: 12px;
    ">
        Chat AI
    </h1>
""")



# histórico temporário do streamlit
if not "lista_mensagens" in  st.session_state:
    st.session_state["lista_mensagens"] = []

mensagem_usuario = st.chat_input(" Escreva sua mensagem ...")

# mostrar as mensagens
for mensagem in st.session_state["lista_mensagens"]:
    quem_enviou = mensagem["role"]
    texto_mensagem = mensagem["content"]
    st.chat_message(quem_enviou).write(texto_mensagem)

if mensagem_usuario:
    # mensagem na tela 
    st.chat_message("user").write(mensagem_usuario)
    mensagem_X = {"role": "user", "content": mensagem_usuario}
    #adicionando a mensagem na lista 
    st.session_state["lista_mensagens"].append(mensagem_X)

    # Resposta da IA 
    #mensagem_IA = "Voce perguntou: " + mensagem_usuario
    resposta_modelo = modelo_IA.chat.completions.create(
        messages= st.session_state["lista_mensagens"], 
        model = "gemini-flash-lite-latest"
    )
    resposta_IA = resposta_modelo.choices[0].message.content

    # enviar mensagem da IA 
    st.chat_message("assistant").write(resposta_IA)
    mensagem_Y = {"role": "assistant", "content": resposta_IA}
    st.session_state["lista_mensagens"].append(mensagem_Y)


