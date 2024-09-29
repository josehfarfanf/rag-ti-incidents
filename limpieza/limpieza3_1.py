# Instalación de la versión específica de googletrans (3.1.0a0)
# Nota: Esta línea instala la versión 3.1.0a0 de googletrans.
# Puedes comentarla si ya tienes la librería instalada o si prefieres utilizar una versión diferente.
# pip install googletrans==3.1.0a0

# Importación de las librerías necesarias
import pandas as pd  # Pandas para manipulación y análisis de datos
import numpy as np  # Librería NumPy para cálculos numéricos
import re  # Librería para trabajar con expresiones regulares
import datetime  # Librería para operaciones relacionadas con fechas y horas
import time  # Librería para medir el tiempo de ejecución

# Importación de la clase Translator de googletrans
from googletrans import Translator

# --------------------------------------------
# VALIDAR TIEMPO DE EJECUCIÓN DEL CÓDIGO
# Definición de la función convertir_tiempo


def convertir_tiempo(segundos):
    # Calcula las horas completas en base a los segundos proporcionados
    horas = segundos // 3600
    # Calcula los minutos completos después de restar las horas
    minutos = (segundos % 3600) // 60
    # Calcula los segundos restantes después de obtener las horas y minutos
    segundos = segundos % 60
    # Devuelve una tupla con los valores de horas, minutos y segundos
    return horas, minutos, segundos


# Registro del tiempo actual en la variable inicio
inicio = time.time()
# --------------------------------------------

# Definición de las rutas de los archivos CSV
nombre_archivo1 = r'data\Nuevo\export_hd_v1_a_2020-02-11.csv'
nombre_archivo2 = r'data\Nuevo\export_hd_v1_b_2020-02-11.csv'

# ------------------------ (UN SOLO GRUPO) ------------------------
# Lectura de los archivos CSV en DataFrames utilizando Pandas
df1 = pd.read_csv(nombre_archivo1, encoding='UTF-8', low_memory=False)
df2 = pd.read_csv(nombre_archivo2, encoding='UTF-8', low_memory=False)
# -----------------------------------------------------------------

# ------------------------ (VALIDAR SI SIRVE) ------------------------
# Identificación de columnas con valores faltantes en el DataFrame df1
# columns_with_missing_values = df1.columns[df1.isnull().any()]

# Eliminación de las columnas con valores faltantes en el DataFrame df1
# df1.drop(columns_with_missing_values, axis=1, inplace=True)

# Identificación de columnas con valores faltantes en el DataFrame df2
# columns_with_missing_values = df2.columns[df2.isnull().any()]

# Eliminación de las columnas con valores faltantes en el DataFrame df2
# df2.drop(columns_with_missing_values, axis=1, inplace=True)
# --------------------------------------------------------------------

# Eliminación de columnas específicas del DataFrame df1
df1 = df1.drop(["DIRECT_CONTACT_LOGIN_ID",
               "DIRECT_CONTACT_INTERNET_E_MAIL"], axis=1)

# LIMPIEZA 01
# Imprime la forma (número de filas y columnas) del DataFrame df1
print(f"df1: {df1.shape}")

# Imprime la forma del DataFrame df2
print(f"df2: {df2.shape}")

# Concatena los DataFrames df1 y df2 en un nuevo DataFrame llamado df_merged
df_merged = pd.concat([df1, df2])

# Imprime la forma del DataFrame df_merged después de la concatenación
print(f"df_merged: {df_merged.shape}")


# Lista de columnas deseadas en el DataFrame df_merged
columnas_deseadas = [
    "ENTRY_ID",
    "STAGECONDITION",
    "DESCRIPTION_CLEAN",
    "DETAILED_DECRIPTION_CLEAN",
    "RESOLUTION_CLEAN",
    "URGENCY",
    "IMPACT",
    "PRIORITY",
    "PRIORITY_WEIGHT",
    "RESOLUTION_CATEGORY",
    "RESOLUTION_METHOD",
    "RESOLUTION_CATEGORY_TIER_2",
    "RESOLUTION_CATEGORY_TIER_3"
]

# Filtra el DataFrame df_merged para incluir solo las columnas deseadas
df_merged = df_merged[columnas_deseadas]

# Imprime la forma del DataFrame df_merged
print(f"df_merged: {df_merged.shape}")


# ESTANDARIZAR DATOS
df_merged.drop_duplicates(subset='ENTRY_ID', keep=False, inplace=True)
# Imprime la forma del DataFrame df_merged
print(f"df_merged: {df_merged.shape}")

# # Convertir la columna 'RESOLUTION_CLEAN' a tipo de dato string
df_merged['ENTRY_ID'] = df_merged['ENTRY_ID'].astype(str)
# Convertir a mayúsculas y eliminar espacios en blanco alrededor de la columna 'ENTRY_ID'
df_merged['ENTRY_ID'] = df_merged['ENTRY_ID'].str.upper()
df_merged['ENTRY_ID'] = df_merged['ENTRY_ID'].str.strip()

# # Convertir la columna 'RESOLUTION_CLEAN' a tipo de dato string
df_merged['STAGECONDITION'] = df_merged['STAGECONDITION'].astype(str)
# Convertir a mayúsculas y eliminar espacios en blanco alrededor de la columna 'STAGECONDITION'
df_merged['STAGECONDITION'] = df_merged['STAGECONDITION'].str.upper()
df_merged['STAGECONDITION'] = df_merged['STAGECONDITION'].str.strip()

# # Convertir la columna 'RESOLUTION_CLEAN' a tipo de dato string
df_merged['DESCRIPTION_CLEAN'] = df_merged['DESCRIPTION_CLEAN'].astype(str)
# Convertir a mayúsculas y eliminar espacios en blanco alrededor de la columna 'DESCRIPTION_CLEAN'
df_merged['DESCRIPTION_CLEAN'] = df_merged['DESCRIPTION_CLEAN'].str.upper()
df_merged['DESCRIPTION_CLEAN'] = df_merged['DESCRIPTION_CLEAN'].str.strip()
# Eliminar el punto final
df_merged['DESCRIPTION_CLEAN'] = df_merged['DESCRIPTION_CLEAN'].apply(
    lambda x: x[:-1] if x.endswith('.') else x)

# # Convertir la columna 'RESOLUTION_CLEAN' a tipo de dato string
df_merged['DETAILED_DECRIPTION_CLEAN'] = df_merged['DETAILED_DECRIPTION_CLEAN'].astype(
    str)
# Convertir a mayúsculas y eliminar espacios en blanco alrededor de la columna 'DETAILED_DECRIPTION_CLEAN'
df_merged['DETAILED_DECRIPTION_CLEAN'] = df_merged['DETAILED_DECRIPTION_CLEAN'].str.upper()
df_merged['DETAILED_DECRIPTION_CLEAN'] = df_merged['DETAILED_DECRIPTION_CLEAN'].str.strip()
# Eliminar el punto final
df_merged['DETAILED_DECRIPTION_CLEAN'] = df_merged['DETAILED_DECRIPTION_CLEAN'].apply(
    lambda x: x[:-1] if x.endswith('.') else x)

# # Convertir la columna 'RESOLUTION_CLEAN' a tipo de dato string
df_merged['RESOLUTION_CLEAN'] = df_merged['RESOLUTION_CLEAN'].astype(str)
# Convertir a mayúsculas y eliminar espacios en blanco alrededor de la columna 'RESOLUTION_CLEAN'
df_merged['RESOLUTION_CLEAN'] = df_merged['RESOLUTION_CLEAN'].str.upper()
df_merged['RESOLUTION_CLEAN'] = df_merged['RESOLUTION_CLEAN'].str.strip()
# Eliminar el punto final
df_merged['RESOLUTION_CLEAN'] = df_merged['RESOLUTION_CLEAN'].apply(
    lambda x: x[:-1] if x.endswith('.') else x)
# --------------------------------------------------------------
# # Convertir la columna 'RESOLUTION_CLEAN' a tipo de dato string
df_merged['RESOLUTION_CATEGORY'] = df_merged['RESOLUTION_CATEGORY'].astype(str)
# Convertir a mayúsculas y eliminar espacios en blanco alrededor de la columna 'RESOLUTION_CATEGORY'
df_merged['RESOLUTION_CATEGORY'] = df_merged['RESOLUTION_CATEGORY'].str.upper()
df_merged['RESOLUTION_CATEGORY'] = df_merged['RESOLUTION_CATEGORY'].str.strip()

# # Convertir la columna 'RESOLUTION_CLEAN' a tipo de dato string
df_merged['RESOLUTION_METHOD'] = df_merged['RESOLUTION_METHOD'].astype(str)
# Convertir a mayúsculas y eliminar espacios en blanco alrededor de la columna 'RESOLUTION_METHOD'
df_merged['RESOLUTION_METHOD'] = df_merged['RESOLUTION_METHOD'].str.upper()
df_merged['RESOLUTION_METHOD'] = df_merged['RESOLUTION_METHOD'].str.strip()

# # Convertir la columna 'RESOLUTION_CLEAN' a tipo de dato string
df_merged['RESOLUTION_CATEGORY_TIER_2'] = df_merged['RESOLUTION_CATEGORY_TIER_2'].astype(
    str)
# Convertir a mayúsculas y eliminar espacios en blanco alrededor de la columna 'RESOLUTION_CATEGORY_TIER_2'
df_merged['RESOLUTION_CATEGORY_TIER_2'] = df_merged['RESOLUTION_CATEGORY_TIER_2'].str.upper()
df_merged['RESOLUTION_CATEGORY_TIER_2'] = df_merged['RESOLUTION_CATEGORY_TIER_2'].str.strip()

# # Convertir la columna 'RESOLUTION_CLEAN' a tipo de dato string
df_merged['RESOLUTION_CATEGORY_TIER_3'] = df_merged['RESOLUTION_CATEGORY_TIER_3'].astype(
    str)
# Convertir a mayúsculas y eliminar espacios en blanco alrededor de la columna 'RESOLUTION_CATEGORY_TIER_3'
df_merged['RESOLUTION_CATEGORY_TIER_3'] = df_merged['RESOLUTION_CATEGORY_TIER_3'].str.upper()
df_merged['RESOLUTION_CATEGORY_TIER_3'] = df_merged['RESOLUTION_CATEGORY_TIER_3'].str.strip()

df_merged['Longitud_RESOLUTION_CLEAN'] = df_merged['RESOLUTION_CLEAN'].str.len()

df_merged = df_merged[(df_merged['Longitud_RESOLUTION_CLEAN'] <= 5948)]

# Imprime la forma del DataFrame df_merged
print(f"df_merged: {df_merged.shape}")
# --------------------------------------------------------------

# Imprime la forma del DataFrame df_merged después de la concatenación
print("Empieza la traducción de las columnas...")

# df_merged = df_merged.sample(n=10, random_state=42)

# TRADUCIR LOS DATOS DE LAS COLUMNAS
# Creación de una instancia del traductor de googletrans
translator = Translator()
# Traducción de la columna 'DESCRIPTION_CLEAN' al español
df_merged['STAGECONDITION_TRAD'] = df_merged['STAGECONDITION'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna STAGECONDITION_TRAD")
# Traducción de la columna 'DESCRIPTION_CLEAN' al español
df_merged['DESCRIPTION_CLEAN_TRAD'] = df_merged['DESCRIPTION_CLEAN'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna DESCRIPTION_CLEAN_TRAD")
# Traducción de la columna 'DETAILED_DECRIPTION_CLEAN' al español
df_merged['DETAILED_DECRIPTION_CLEAN_TRAD'] = df_merged['DETAILED_DECRIPTION_CLEAN'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna DETAILED_DECRIPTION_CLEAN_TRAD")
# Traducción de la columna 'RESOLUTION_CLEAN' al español
df_merged['RESOLUTION_CLEAN_TRAD'] = df_merged['RESOLUTION_CLEAN'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna RESOLUTION_CLEAN_TRAD")
# --------------------------------------------------------------
# Traducción de la columna 'RESOLUTION_CATEGORY' al español
df_merged['RESOLUTION_CATEGORY_TRAD'] = df_merged['RESOLUTION_CATEGORY'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna RESOLUTION_CATEGORY_TRAD")

# Traducción de la columna 'RESOLUTION_METHOD' al español
df_merged['RESOLUTION_METHOD_TRAD'] = df_merged['RESOLUTION_METHOD'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna RESOLUTION_METHOD_TRAD")

# Traducción de la columna 'RESOLUTION_CATEGORY_TIER_2' al español
df_merged['RESOLUTION_CATEGORY_TIER_2_TRAD'] = df_merged['RESOLUTION_CATEGORY_TIER_2'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna RESOLUTION_CATEGORY_TIER_2_TRAD")

# Traducción de la columna 'RESOLUTION_CATEGORY_TIER_3' al español
df_merged['RESOLUTION_CATEGORY_TIER_3_TRAD'] = df_merged['RESOLUTION_CATEGORY_TIER_3'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna RESOLUTION_CATEGORY_TIER_3_TRAD")
# # --------------------------------------------------------------

# Imprime la forma del DataFrame df_merged
print(f"df_merged: {df_merged.shape}")


# LIMPIEZA 02
# Crear la columna DESCRIPTION_NEW
df_merged['DESCRIPTION_NEW'] = df_merged['DESCRIPTION_CLEAN_TRAD'] + \
    '-' + df_merged['DETAILED_DECRIPTION_CLEAN_TRAD']

# Seleccionar las columnas deseadas
columnas_deseadas = [
    'ENTRY_ID',
    'STAGECONDITION_TRAD',
    'DESCRIPTION_NEW',
    'RESOLUTION_CLEAN_TRAD',
    'URGENCY',
    'IMPACT',
    'PRIORITY',
    'PRIORITY_WEIGHT',
    # --------------------------------------------------------------
    'RESOLUTION_CATEGORY_TRAD',
    'RESOLUTION_METHOD_TRAD',
    'RESOLUTION_CATEGORY_TIER_2_TRAD',
    'RESOLUTION_CATEGORY_TIER_3_TRAD'
    # --------------------------------------------------------------
]

df_merged = df_merged[columnas_deseadas]

# # Renombrar columnas
# df_merged.rename(columns={
#     'ENTRY_ID': 'ENTRADA_ID',
#     'STAGECONDITION': 'CONDICION_ESCENARIO',
#     'DESCRIPTION_NEW': 'DESCRIPCION_NUEVO',
#     'RESOLUTION_CLEAN': 'RESOLUCION_NUEVO',
#     'URGENCY': 'URGENCIA',
#     'IMPACT': 'IMPACTO',
#     'PRIORITY': 'PRIORIDAD',
#     'PRIORITY_WEIGHT': 'PRIORIDAD_PESO'
# }, inplace=True)

# Reordenar columnas
columnas_ordenadas = [
    'ENTRY_ID',
    'STAGECONDITION_TRAD',
    'DESCRIPTION_NEW',
    'RESOLUTION_CLEAN_TRAD',
    'URGENCY',
    'IMPACT',
    'PRIORITY',
    'PRIORITY_WEIGHT',
    # --------------------------------------------------------------
    'RESOLUTION_CATEGORY_TRAD',
    'RESOLUTION_METHOD_TRAD',
    'RESOLUTION_CATEGORY_TIER_2_TRAD',
    'RESOLUTION_CATEGORY_TIER_3_TRAD'
    # --------------------------------------------------------------
]

df_merged = df_merged[columnas_ordenadas]

# Imprime la forma del DataFrame df_merged
print(f"df_merged: {df_merged.shape}")


# --------- OBTENER FECHA ACTUAL ---------
# Obtener la fecha y hora actual
now = datetime.datetime.now()

# Formatear la fecha como "YYYYMMDD"
formatted_date1 = now.strftime("%Y%m%d")
# ----------------------------------------
# Nombre del archivo final
nombre_final = 'nuevo_dataset03'

# Guardar el DataFrame df_merged en un archivo CSV con el nombre deseado
df_merged.to_csv(fr'data\{nombre_final}_{formatted_date1}.csv',
                 index=False, encoding='UTF-8')

# Obtener la fecha y hora actual en un formato legible
formatted_date2 = now.strftime("%Y-%m-%d %H:%M:%S")

# Imprimir un mensaje de éxito con la fecha y el nombre del archivo
print(f"[{formatted_date2}] [{nombre_final}_{
      formatted_date1}.csv] Limpieza finalizada con éxito...")

# --------------------------------------------
# VALIDAR TIEMPO DE EJECUCIÓN DEL CÓDIGO
# Calcula el tiempo de finalización de la ejecución
fin = time.time()

# Calcula el tiempo total de ejecución
tiempo_total = fin - inicio

# Convierte el tiempo total a horas, minutos y segundos
horas, minutos, segundos = convertir_tiempo(tiempo_total)

# Imprime el tiempo de ejecución en un formato legible
print(f"El tiempo de ejecución fue de {horas} horas, {
      minutos} minutos y {segundos} segundos.")
# --------------------------------------------
