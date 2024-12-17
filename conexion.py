
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from urllib.parse import quote_plus

# Cargar el archivo .env.local
load_dotenv(dotenv_path=".env.local")

# Obtener variables de entorno
DB_NAME = os.getenv("DB_NAME")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

try:
    # Asegurarse de que PORT es un número válido
    if not PORT.isdigit():
        raise ValueError(f"PORT contiene caracteres no válidos: {PORT}")
    PORT = int(PORT)

    # Codificar USERNAME y PASSWORD
    USERNAME_ESCAPED = quote_plus(USERNAME)
    PASSWORD_ESCAPED = quote_plus(PASSWORD)

    # Crear la URI de conexión
    uri = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    
    # Conectar a MongoDB
    client = MongoClient(uri)
    db = client[DB_NAME]  # Seleccionar la base de datos
    collection = db['datosPublicos100']  # Nombre de la colección
    print("Conexión exitosa")
except Exception as e:
    print("Error de conexión:", e)
