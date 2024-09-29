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
nombre_archivo1 = r'data\nuevo-dataset03_20240704_final.csv'

# ------------------------ (UN SOLO GRUPO) ------------------------
# Lectura de los archivos CSV en DataFrames utilizando Pandas
df1 = pd.read_csv(nombre_archivo1, encoding='UTF-8')
# -----------------------------------------------------------------

print(f"df1: {df1.shape}")

# ----------------------------------------------------------------------------------------------------
# >>> NOMBRE COLUMNAS
# ENTRY_ID
# STAGECONDITION_TRAD
# DESCRIPTION_NEW
# RESOLUTION_CLEAN_TRAD
# URGENCY
# IMPACT
# PRIORITY
# PRIORITY_WEIGHT
# RESOLUTION_CATEGORY_TRAD
# RESOLUTION_METHOD_TRAD
# RESOLUTION_CATEGORY_TIER_2_TRAD
# RESOLUTION_CATEGORY_TIER_3_TRAD


df1.drop_duplicates(subset='ENTRY_ID', keep=False, inplace=True)

df1['DESCRIPTION_NEW'] = df1['DESCRIPTION_NEW'].apply(
    lambda x: str(x))
df1['DESCRIPTION_NEW'] = df1['DESCRIPTION_NEW'].apply(
    lambda x: re.sub(r'[^a-zA-Z0-9.@:/áéíóúÁÉÍÓÚñÑ]', ' ', x))
df1['DESCRIPTION_NEW'] = df1['DESCRIPTION_NEW'].apply(
    lambda x: re.sub(r'\s+', ' ', x))
df1['DESCRIPTION_NEW'] = df1['DESCRIPTION_NEW'].apply(
    lambda x: re.sub(r'^\d+\s*', '', x))
df1['DESCRIPTION_NEW'] = df1['DESCRIPTION_NEW'].apply(
    lambda x: re.sub(r'^\W+', '', x))
df1['DESCRIPTION_NEW'] = df1['DESCRIPTION_NEW'].astype(str)


df1['RESOLUTION_CLEAN_TRAD'] = df1['RESOLUTION_CLEAN_TRAD'].astype(str)
df1['RESOLUTION_CLEAN_TRAD'] = df1['RESOLUTION_CLEAN_TRAD'].str.normalize('NFKD').str.encode(
    'ascii', errors='ignore').str.decode('utf-8')
# df1['RESOLUTION_CLEAN_TRAD'] = df1['RESOLUTION_CLEAN_TRAD'].apply(
#     lambda x: re.sub(r'[^a-zA-Z0-9.@:/áéíóúÁÉÍÓÚñÑ]', ' ', x))
df1['RESOLUTION_CLEAN_TRAD'] = df1['RESOLUTION_CLEAN_TRAD'].apply(
    lambda x: re.sub(r'\s+', ' ', x))
df1['RESOLUTION_CLEAN_TRAD'] = df1['RESOLUTION_CLEAN_TRAD'].apply(
    lambda x: re.sub(r'^\d+\s*', '', x))
df1['RESOLUTION_CLEAN_TRAD'] = df1['RESOLUTION_CLEAN_TRAD'].apply(
    lambda x: re.sub(r'^\W+', '', x))


print(f"df1: {df1.shape}")


translator = Translator()
df1['DESCRIPTION_NEW_TRAD'] = df1['DESCRIPTION_NEW'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna DESCRIPTION_NEW_TRAD")

df1['RESOLUTION_CLEAN_TRAD_TRAD'] = df1['RESOLUTION_CLEAN_TRAD'].apply(
    lambda x: translator.translate(x, dest='es').text)
print("COMPLETA columna RESOLUTION_CLEAN_TRAD_TRAD")

print(f"df1: {df1.shape}")

# **********************************************
# Seleccionar las columnas deseadas
columnas_deseadas = [
    'ENTRY_ID',
    'STAGECONDITION_TRAD',
    'DESCRIPTION_NEW_TRAD',
    'RESOLUTION_CLEAN_TRAD_TRAD',
    'URGENCY',
    'IMPACT',
    'PRIORITY',
    'PRIORITY_WEIGHT',
    'RESOLUTION_CATEGORY_TRAD',
    'RESOLUTION_METHOD_TRAD',
    'RESOLUTION_CATEGORY_TIER_2_TRAD',
    'RESOLUTION_CATEGORY_TIER_3_TRAD'
]

df1 = df1[columnas_deseadas]

print(f"df1: {df1.shape}")

# df1['Longitud_DESCRIPCION'] = df1['DESCRIPCION_NUEVO_TRAD'].str.len()

# df1 = df1[(df1['Longitud_DESCRIPCION'] >= 10) &
#           (df1['Longitud_DESCRIPCION'] <= 20)]

# print(f"df1: {df1.shape}")
# **********************************************

# ----------------------------------------------------------------------------------------------------

# --------- OBTENER FECHA ACTUAL ---------
# Obtener la fecha y hora actual
now = datetime.datetime.now()

# ----------------------------------------
# Nombre del archivo final
nombre_final = 'nuevo-dataset03_20240704_final_trad'

# Guardar el DataFrame df1 en un archivo CSV con el nombre deseado
df1.to_csv(fr'data\{nombre_final}.csv',
           index=False, encoding='UTF-8')

# Obtener la fecha y hora actual en un formato legible
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

# Imprimir un mensaje de éxito con la fecha y el nombre del archivo
print(f"[{formatted_date}] [{nombre_final}.csv] Limpieza finalizada con éxito...")

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
