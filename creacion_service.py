from pymongo import MongoClient
import pandas as pd
import json
import os
import datetime

# importar las variables de entorno
os.environ['DECLARA_DB_NAME'] = 'declaranet'
os.environ['DECLARA_HOST'] = "148.216.25.182"
os.environ['DECLARA_PASSWORD'] = "c0ntr4l0r14"
os.environ['DECLARA_PORT'] = '27017'
os.environ['DECLARA_USERNAME'] = 'declaranetusr'

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

# conexion con la bd de mongo 
DB_NAME = os.environ.get('DECLARA_DB_NAME') #nombre de la base de datos
HOST = os.environ.get('DECLARA_HOST') #dirección del host donde se encuentra la base de datos
PASSWORD = os.environ.get('DECLARA_PASSWORD') #contraseña para autenticarse en la base de datos
PORT = int(os.environ.get('DECLARA_PORT')) #puerto por defecto para MongoDB
USERNAME = os.environ.get('DECLARA_USERNAME') #nombre de usuario para autenticarse en la base de datos

