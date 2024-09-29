import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os

from langchain_openai import OpenAIEmbeddings
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone.grpc import PineconeGRPC as Pinecone
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document 

from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import ServerlessSpec

load_dotenv()

openai_api_key =  os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.environ["PINECONE_API_KEY"]
cohere_api_key=os.environ["COHERE_API_KEY"]
max_len_text=2000

#Index y namspace de la base de datos
index_name='tfm-rag-cohere'#'tfm-rag-preprocessed-2000'#'tfm-rag-preprocessed'#index_name='tfm-rag'
namespace ='tfm-rag-cohere'#'incidents-preprocessed-2000'# "incidents-preprocessed"#namespace = "incidents"
dimension=1024 #1536

#prompt para preprocesar incidente
incident_template = """
Eres un asistente inteligente especializado en la gestión de incidentes de sistemas de información.

**Reporte del incidente:**
{incident_report}

**Solución propuesta:**
###
{support_solution}
###
**Instrucciones:**
1. Analiza rigurosamente el reporte del incidente. Si no se trata de un incidente real, devuelve un texto vacío.
2. Analiza rigurosamente la solución proporcionada, la cual se encuentra delimitada por el triple simbolo numeral (###). Asegúrate que la solución propuesta incluye detalles claros sobre el proceso seguido para resolver el incidente, este paso es muy IMPORTANTE, devuelve un texto vacío.
3. Corrige cualquier error de digitación y ortografía en el reporte y la solución. Elimina redundancias y conserva detalles técnicos importantes como mensajes de error y componentes afectados.
4. Describe el problema de manera concisa y técnica, sin agregar información adicional.
5. Explica los pasos seguidos por el soporte para resolver el incidente, incluyendo herramientas utilizadas, configuraciones verificadas, y acciones realizadas. Sé específico y detallado.
6. Proporciona la respuesta en español, manteniendo en inglés los nombres de componentes y mensajes de error.

Presenta la respuesta en un máximo de 2000 caracteres de manera que se pueda identificar fácilmete los problemas que que generaron el incidente y el proceso de resolución del mismo
IMPORTANTE:** Si no se cumplen las condiciones (no es un incidente real o la solución no contiene detalles del proceso seguido), **DEVUELVE ESTRICTAMENTE** un texto vacío. Evita usar símbolos en la respuesta
"""
#Prompt para resumir descripciones de incidentes
description_template = """
Eres un asistente inteligente especializado en la gestión de incidentes de sistemas de información y un usuario presenta el siguiente incidente

**Reporte del incidente:**
{incident_report}

**Instrucciones:**
1. Analiza rigurosamente el reporte del incidente. Si no se trata de un incidente real, devuelve un texto vacío.
2. Corrige cualquier error de digitación y ortografía en el reporte del incidente. Elimina redundancias y conserva detalles técnicos importantes como mensajes de error y componentes afectados.
3. Describe el problema de manera concisa y técnica, sin agregar información adicional.
4. Proporciona la respuesta en español, manteniendo en inglés los nombres de componentes y mensajes de error.

IMPORTANTE:** recuerda, si no se describe un incidente, **DEVUELVE ESTRICTAMENTE** un texto vacío.
"""
####Modelo de embeddings a usar en el modelo
#embeddings = OpenAIEmbeddings()
embeddings=CohereEmbeddings(
    model="embed-multilingual-v3.0",cohere_api_key=cohere_api_key
)
####Base de conocimiento
   
pc = Pinecone(api_key=pinecone_api_key)
with st.spinner('Verficando base de conocimeinto...'):
    if index_name in pc.list_indexes().names():
        vstore=PineconeVectorStore.from_existing_index(
            index_name=index_name,
            namespace=namespace,
            embedding=embeddings)

###LLM para generación de respuestas
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)

def insert_documents(df):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 200
    )
    final_incident=(get_incident_text(''.join(df.iloc[:, 0].astype(str)),''.join(df.iloc[:, 1].astype(str))))
    doc_chunks = text_splitter.split_text(str(final_incident))
    print("numero chuncks "+str(len(doc_chunks)))
    print(doc_chunks)
    documents = [Document(page_content=text) for text in doc_chunks]
    if index_name not in pc.list_indexes().names():
        with st.spinner('Creando base de conocimeinto...'):
            pc.create_index(
                name=index_name,
                dimension=dimension, 
                metric="cosine", 
                spec=ServerlessSpec(
                    cloud="aws", 
                    region="us-east-1"
                ) 
            ) 

    with st.spinner('Actualizando base de conocimeinto...'):
        vectorstore_from_docs = PineconeVectorStore.from_documents(
            documents,
            index_name=index_name,
            embedding=embeddings,
            namespace=namespace
        )
    with st.spinner('Conectando con base de conocimeinto...'):    
        vstore=PineconeVectorStore.from_existing_index(
            index_name=index_name,
            namespace=namespace,
            embedding=embeddings)

def handle_userinput(user_question):
    if index_name in pc.list_indexes().names():
        process_question(user_question)
    else:
        st.write("No existe el index: "+index_name)

def process_question(user_question):
    prompt_template = PromptTemplate(
    input_variables=["incident"],
    template="""
    Eres un experto en sistemas de información.
    Genera una solución al incidente descrito a continuación, basado únicamente en el contexto previo. Si dentro del contexto compartido no se presentan incidentes similares responde que no conoces como resolver el incidente
    Descripción del incidente: {incident}
    """
    )
    prompt = prompt_template.format(incident=user_question)
    
    with st.spinner('Consultando base de conocimeinto...'):
        docs = vstore.similarity_search(user_question)  
        
    st.session_state['chunks'] = docs
    chain = load_qa_chain(llm, chain_type="stuff")
    with st.spinner('Generando posibles soluciones para el incidente...'):
        response = chain.run(input_documents=docs, question=prompt)
    st.session_state['respuesta'] = response

def get_incident_text(description, solution):
    result="Descripción del incidente: "+description+ ". Solución del incidente: "+solution
    if (len(result)>max_len_text):
        return process_incident(description, solution)
    else:
        return result

def process_incident(description, solution):
    # Crear una plantilla de prompt
    prompt_template = PromptTemplate(input_variables=["incident_report", "support_solution"], template=incident_template)
    
    # Crear una cadena LLM con la plantilla de prompt
    chain = LLMChain(prompt=prompt_template, llm=llm)
    final_text=''
    try:
        final_text = chain.run(incident_report=description, support_solution=solution)
    except:
        final_text=''
    return final_text

def process_incident_description(description):
    # Crear una plantilla de prompt
    prompt_template = PromptTemplate(input_variables=["incident_report"], template=description_template)
    
    # Crear una cadena LLM con la plantilla de prompt
    chain = LLMChain(prompt=prompt_template, llm=llm)
    final_text=''
    try:
        final_text = chain.run(incident_report=description)
    except:
        final_text=''
    return final_text