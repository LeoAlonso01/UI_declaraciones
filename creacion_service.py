from pymongo import MongoClient
import pandas as pd
import json
import os
import datetime

#
from conexion import uri
DB_NAME = os.environ.get("DB_NAME")

# Creación de la URI de conexión para MongoDB
# uri = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# Función para "aplanar" un diccionario anidado, convirtiendo las claves anidadas en claves únicas
def flat_dict(d, parent_key='',sep='_'):
    items = {} #diccionario para almacenar los elementos aplanados
    for k, v in d.items(): #itera sobre los elementos del diccionario
        new_key = parent_key + sep + k if parent_key else k #genera una nueva clave combinando la clave actual con la clave del padre usando el separador
        if isinstance(v, dict): #si el valor es otro diccionario, llama a la función recursivamente
            items.update(flat_dict(v, new_key, sep=sep)) #actualiza el diccionario con los elementos aplanados
        else: #si no es un diccionario, añade el valor al nuevo diccionario
            items[new_key] = v #añade el valor al diccionario
    return items #retorna el diccionario con las claves aplanadas

# selecciona la bd y la coleccion
client = MongoClient(uri)
db = client[DB_NAME]
collection = db['datosPublicos100']  # Nombre de la colección donde se realizará la consulta

# Ejecuta la consulta de agregación en la colección usando con el json en crudo para modificar sus variables
with open('pipeline.json', 'r') as file: # Abre el archivo JSON en modo de lectura
    pipeline = json.load(file) # Carga el archivo JSON con el pipeline de agregación
cursor = collection.aggregate(pipeline) # Ejecuta la consulta de agregación en la colección

# Convierte los resultados de la consulta en una lista]
lista = list(cursor) # Convierte los resultados de la consulta en una lista
df = pd.DataFrame(lista) # Convierte la lista de resultados en un DataFrame de pandas
print(df) # Imprime el DataFrame