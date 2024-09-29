import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os

from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from util import *

max_len_text=2000

# Inicializamos una variable de sesión para controlar el estado
if 'page' not in st.session_state:
    st.session_state['page'] = 'welcome'

# Inicializamos los chunks en la sesión si no están ya inicializados
if 'chunks' not in st.session_state:
    st.session_state['chunks'] = []

# Inicializamos la respuesta a la pregunta
if 'respuesta' not in st.session_state:
    st.session_state['respuesta'] = None

# Función para procesar la pregunta
def procesar_pregunta():
    pregunta = st.session_state['pregunta']
    if (len(pregunta)>max_len_text):
        pregunta=process_incident_description(pregunta)
    if pregunta:
        # Simulamos el procesamiento de la pregunta y la recuperación de chunks
        handle_userinput(pregunta)
    else:
        st.write("No ha ingresado una descripción válida de un problema.")

# Función para previsualizar los datos del CSV cargado
def previsualizar_csv(archivo_csv):
    if archivo_csv is not None:
        # Leemos el CSV
        df = pd.read_csv(archivo_csv)
        if df.shape[1] != 2:
            st.write("El fichero seleccionado debe contener solo las dos columnas requeridas (incidente y solución)")
            return None
        else:
            # Mostramos una vista previa de los datos
            st.write("Previsualización de los datos cargados:")
            st.dataframe(df)
            return df
    else:
        st.write("No se ha subido ningún archivo.")
        return None

# Pantalla de bienvenida
if st.session_state['page'] == 'welcome':
    st.title('¡Bienvenido al sistema de apoyo de análisis de incidentes de TI!')
    st.write("""
    Esta aplicación le permite buscar soluciones a incidentes de TI. 
    Simplemente describa su problema, y el sistema le ayudará a encontrar posibles soluciones basadas en casos anteriores. 
    Además, también podrá contribuir añadiendo información sobre incidentes resueltos para mejorar la capacidad de búsqueda y resolución de problemas futuros.
    """)
    # Usamos on_click para cambiar de pantalla en el mismo ciclo de renderizado
    st.button('CONTINUAR', on_click=lambda: st.session_state.update(page='main'))

# Pantalla principal
elif st.session_state['page'] == 'main':
    # Título de la aplicación
    st.title("Apoyo al análisis de incidentes de TI")
    
    # Crear las pestañas
    tab1, tab2 = st.tabs(["Análisis de incidentes","Actualizar base de conocimiento"])
    # Contenido de la pestaña 2 - Ingresar texto
    with tab1:
        st.header("Descripción del incidente")

        # Creamos un formulario para que soporte Control + Enter
        with st.form(key='form_pregunta', clear_on_submit=False):
            st.text_area("Ingrese la descripción del incidente que desea resolver. Recuerde ingresar detalles relevantes del problema que tiene actualmente.", key='pregunta', height=100)
            # Botón para procesar la pregunta
            submit_button = st.form_submit_button(label="Procesar pregunta")

        # Procesar la pregunta si se presiona el botón o si se usa Ctrl+Enter
        if submit_button:
            procesar_pregunta()

        if st.session_state['respuesta']:
            st.subheader("Respuesta")
            st.write(st.session_state['respuesta'])

        # Mostrar los chunks recuperados si existen resultados
        if st.session_state['chunks']:
            st.subheader("Referencias consultadas:")
            for index, chunk in enumerate(st.session_state['chunks']):
                with st.expander(f"referencia {index+1}"):
                    st.write(chunk)
            
    # Contenido de la pestaña 1 - Cargar archivo CSV
    with tab2:
        st.header("Seleccione un archivo CSV")
        uploaded_file = st.file_uploader("Recuerde que el archivo CSV debe contener dos columnas: la descripción del problema y su resolución", type=["csv"])
        
        if uploaded_file is not None:
            # Leer el archivo CSV
            # Previsualizamos los datos del archivo subido
            df = previsualizar_csv(uploaded_file)
            if df is not None:
                if st.button("Cargar Registros"):
                    insert_documents(df)
                
            


