#lanzar con streamlit run c_front_end.py en el terminal


import streamlit as st
from streamlit_chat import message

# 1. Cargar la bbdd con langchain

from langchain.sql_database import SQLDatabase
from langchain.llms import OpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_experimental.sql import SQLDatabaseChain
import os
db = SQLDatabase.from_uri("sqlite:///T1ChatBot.db")


os.environ["OPEN_API_KEY"] = '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'

# 3. Crear el LLM
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0.3,model_name='gpt-4')


# 4. Crear la cadena
from langchain_experimental.sql import SQLDatabaseChain
cadena = SQLDatabaseChain(llm=llm, database= db, verbose=False)

# 5. Formato personalizado de respuesta
formato = """
Dada una pregunta del usuario: (Responde y actua como un asistente amigable virtual)
1. crea una consulta de sqlite3 o para sql server
2. revisa los resultados
3. devuelve el dato exacto
4. si tienes que hacer alguna aclaración o devolver cualquier texto que sea siempre en español y
limitate a responder puntualmente 
#{question}
"""

# 6. Función para hacer la consulta

def consulta(input_usuario):
    consulta = formato.format(question = input_usuario)
    resultado = cadena.run(consulta)
    return(resultado)



st.title("GadgetBot")
st.write("Preguntas, dudas, consultas...")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if 'preguntas' not in st.session_state:
    st.session_state.preguntas = []
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []

def click():
    if st.session_state.user != '':
        pregunta = st.session_state.user
        respuesta = consulta(pregunta)

        st.session_state.preguntas.append(pregunta)
        st.session_state.respuestas.append(respuesta)

        # Limpiar el input de usuario después de enviar la pregunta
        st.session_state.user = pregunta


with st.form('my-form'):
   query = st.text_input('¿En qué te puedo ayudar?:', key='user', help='Pulsa Enviar para hacer la pregunta')
   submit_button = st.form_submit_button('Enviar',on_click=click)

if st.session_state.preguntas:
    for i in range(len(st.session_state.respuestas)-1, -1, -1):
        message(st.session_state.respuestas[i], key=str(i))

    # Opción para continuar la conversación
    continuar_conversacion = st.checkbox('Quieres hacer otra pregunta?')
    if not continuar_conversacion:
        st.session_state.preguntas = []
        st.session_state.respuestas = []









