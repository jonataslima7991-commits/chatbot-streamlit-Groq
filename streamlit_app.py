# Estudo de Caso 1 - DSA AI Coder - Criando Seu Assistente de Programação Python, em Python

# Importa módulo para interagir com o sistema operacional
import os

# Importa a biblioteca Streamlit para criar a interface web interativa
import streamlit as st

# Importa a classe Groq para se conectar à API da plataforma Groq e acessar o LLM
from groq import Groq


# 1. A CONFIGURAÇÃO TEM DE SER A PRIMEIRA COISA (Não coloque nada do Streamlit antes disto)
st.set_page_config(
    page_title="J.A.R.V.I.S. Core",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. LOGO A SEGUIR VEM O ESTILO VISUAL (O CSS)
st.markdown(
    """
    <style>
    /* Fundo principal da aplicação */
    .stApp {
        background-color: #030a16; /* Cor de segurança escura */
        background-image: url("https://wallpaperaccess.com/full/2267778.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    /* Barra lateral translúcida */
    [data-testid="stSidebar"] {
        background-color: rgba(2, 10, 20, 0.85) !important;
        border-right: 1px solid #00aaff !important;
    }

    /* Esconde a barra superior branca padrão do Streamlit */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Estilo das mensagens do chat */
    [data-testid="stChatMessage"] {
        background-color: rgba(0, 30, 60, 0.7) !important;
        border-left: 3px solid #00aaff !important;
    }
    
    /* Textos com brilho */
    h1, h2, h3, p {
        text-shadow: 0px 0px 5px rgba(0, 170, 255, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# A partir daqui continua o resto do seu código (CUSTOM_PROMPT, st.title, etc...)
# Configura a página do Streamlit com título, ícone, layout e estado inicial da sidebar
st.set_page_config(
    page_title="Jonatas AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define um prompt de sistema que descreve as regras e comportamento do assistente de IA
CUSTOM_PROMPT = """
Você é o *J.A.R.V.I.S.* (Just A Rather Very Intelligent System), o lendário assistente pessoal do Senhor Tony Stark, operando dentro do núcleo central da Stark Industries.

Sua missão é auxiliar o Senhor(a) (tratando o usuário respeitosamente como "Senhor" ou "Senhora") com dúvidas complexas de programação, com foco principal em Python e na integração de sistemas avançados (como os protocolos de armadura Mark ou a gestão de energia do Reator Arc).

*PERSONALIDADE E TOM DE VOZ:*
1.  *Educado e Leal (Vibe Britânica):* Use uma linguagem formal, refinada, britânica e extremamente polida. Comece a interação aceitando o protocolo de análise. Ex: "Inicializando protocolos de análise Python para o Senhor(a)..." ou "Sistemas online, Senhor(a). O que deseja computar?"
2.  *Brilhante e Competente:* Suas explicações devem ser extremamente técnicas e precisas, mas organizadas. Você não ajuda apenas iniciantes; você otimiza o código do próprio Homem de Ferro.
3.  *Leve Pitada de Sarcasmo (Ao estilo Jarvis):* Se o usuário perguntar algo muito simples, você pode dar uma resposta ligeiramente cínica ou seca, mas sempre útil, ao estilo do JARVIS nos filmes.

*ESTRUTURA DE RESPOSTA:*
1.  *Aceitação do Protocolo:* Comece confirmando que o sistema está online e pronto.
2.  *Explicação Técnica:* Uma explicação direta e técnica do conceito (não muito didática, mais direta ao ponto).
3.  *Exemplo de Código Otimizado:* Forneça um bloco de código Python extremamente bem comentado e otimizado.
4.  *Conclusão e Monitoramento:* Encerre confirmando que a análise foi concluída e que você continua monitorando os sistemas. Ex: "Análise concluída. Monitorando integridade dos sistemas."

*REGRAS FINAIS:* Mantenha a imersão. Você é o JARVIS.
"""

# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:
    
    # Define o título da barra lateral
    st.title("🤖 JARVIS AI Coder")
    
    # Mostra um texto explicativo sobre o assistente
    st.markdown("Stark Industries - J.A.R.V.I.S.")
    
    
    # Campo para inserir a chave de API da Groq
    groq_api_key = st.text_input(
        "Insira sua API Key Groq", 
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

# Título principal do app
st.title("Jonatas Oliveira - JARVIS AI Coder")

# Subtítulo adicional
st.title("Assistente Pessoal de Programação do Sr.Jonatas 🐍")

# Texto auxiliar abaixo do título
st.caption("Bem vindo Senhor, em que posso ajuda-lo no dia de hoje? ")

# Inicializa o histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa a variável do cliente Groq como None
client = None

# Verifica se o usuário forneceu a chave de API da Groq
if groq_api_key:
    
    try:
        
        # Cria cliente Groq com a chave de API fornecida
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        
        # Exibe erro caso haja problema ao inicializar cliente
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

# Caso não tenha chave, mas já existam mensagens, mostra aviso
elif st.session_state.messages:
     st.warning("Insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada do usuário no chat
if prompt := st.chat_input("Qual sua dúvida sobre Python?"):
    
    # Se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("Insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara mensagens para enviar à API, incluindo prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):
            
            try:
                
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extrai a resposta gerada pela API
                dsa_ai_resposta = chat_completion.choices[0].message.content
                
                # Exibe a resposta no Streamlit
                st.markdown(dsa_ai_resposta)
                
                # Armazena resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            # Caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>Projeto de utilização de API para criação de IA própria</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Obrigado DSA
