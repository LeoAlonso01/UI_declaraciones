from pymongo import MongoClient
import os

# conexion con la bd de mongo 
DB_NAME = os.environ.get('DB_NAME') #nombre de la base de datos
HOST = os.environ.get('HOST') #dirección del host donde se encuentra la base de datos
PASSWORD = os.environ.get('PASSWORD') #contraseña para autenticarse en la base de datos
PORT = os.environ.get('PORT') #puerto por defecto para MongoDB
USERNAME = os.environ.get('USERNAME') #nombre de usuario para autenticarse en la base de datos

print(PORT)
# intenton de conexion a la bd
try:
    uri = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}" #crea la URI de conexión para MongoDB
    client = MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD) #crea una instancia de MongoClient
    client2 = MongoClient(uri) #crea una instancia de MongoClient
    db = client[DB_NAME] #selecciona la base de datos
    print("Conexión exitosa")
except Exception as e:
    print("Error de conexión:", e)