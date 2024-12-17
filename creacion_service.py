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

# variables del pipeline
fechas = ["2024-12", "2024-11"]
false = False

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
cursor = collection.aggregate([
    {
      "$lookup":
        {
          "from": "declaracion100",
          "localField": "idUsrDecnet",
          "foreignField": "encabezado.usuario.idUsuario",
          "as": "declaracion"
        }
    },
    {
      "$sort":
        {
          "nombre": 1
        }
    },
    {
      "$unwind":
        {
          "path": "$declaracion",
          "preserveNullAndEmptyArrays": false
        }
    },
    {
      "$addFields":
        {
          "mes": {
            "$dateToString": {
              "format": "%Y-%m",
              "date": {
                "$toDate":"$declaracion.encabezado.fechaActualizacion"
              }
            }
          }
        }
    },
    {
      "$match":
        {
          "mes": {
            "$in": fechas
          }
        }
    },
    {
      "$sort":
        {
          "rfc": 1
        }
    },
    {
      "$project":
        {
          "declaracion.encabezado.tipoDeclaracion": 1,
          "nombre": 1,
          "declaracion._id": 1,
          "declaracion.declaracion.datosEmpleoCargoComision.empleoCargoComision.areaAdscripcion": 1,
          "declaracion.declaracion.datosEmpleoCargoComision.empleoCargoComision.empleoCargoComision": 1,
          "declaracion.declaracion.datosEmpleoCargoComision.empleoCargoComision.fechaEncargo": 1,
          "declaracion.declaracion.inversionesCuentasValores.ninguno": 1,
          "declaracion.declaracion.bienesInmuebles.ninguno": 1,
          "declaracion.declaracion.vehiculos.ninguno": 1,
          "declaracion.declaracion.bienesInmuebles.bienesInmuebles.domicilio.domicilioExtranjero": 1,
          "declaracion.declaracion.bienesInmuebles.bienesInmuebles.transmisores.tipoPersona": 1,
          "declaracion.declaracion.ingresos.ingresoNetoParejaDependiente.remuneracion.monto": 1,
          "declaracion.declaracion.ingresos.otrosIngresosTotal.monto": 1,
          "declaracion.declaracion.datosDependientesEconomicos.ninguno": 1,
          "declaracion.declaracion.datosCurricularesDeclarante.escolaridad.nivel.valor": 1,
          "declaracion.encabezado.fechaActualizacion": 1,
          "declaracion.encabezado.anio": 1
        }
    }
  ]) # Ejecuta la consulta de agregación en la colección

# Convierte los resultados de la consulta en una lista]
lista = list(cursor) # Convierte los resultados de la consulta en una lista
df = pd.DataFrame(lista) # Convierte la lista de resultados en un DataFrame de pandas
print(df) # Imprime el DataFrame
# imprime el datafgrame con todas las columnas y filas
df.all()
# Aplana la columna 'declaracion' del DataFrame para convertir los datos anidados en un formato plano
df_flat = df['declaracion'].apply(lambda x: flat_dict(x)).apply(pd.Series)
# Concatena el DataFrame original sin la columna 'declaracion' con el DataFrame aplanado
df = pd.concat([df.drop(['declaracion'], axis=1), df_flat], axis=1)

# Obtiene la fecha y hora actuales
fecha_actual = datetime.datetime.now()
# Formatea la fecha actual para usarla como nombre de carpeta
nombre_carpeta = fecha_actual.strftime("%d_%m_%Y")
# Obtiene la ruta del directorio actual
ruta_actual = os.getcwd()

# Crea la ruta completa donde se guardará el archivo CSV
ruta_completa = os.path.join(ruta_actual, nombre_carpeta)

# Verifica si la carpeta existe; si no, la crea
if not os.path.exists(ruta_completa):
    os.makedirs(ruta_completa)

print("Listo")  # Imprime un mensaje indicando que el proceso ha finalizado

# Define el nombre del archivo CSV que se va a guardar
nombre_archivo_csv = "archivo1.csv"
# Crea la ruta completa para el archivo CSV
ruta_archivo_csv = os.path.join(ruta_completa, nombre_archivo_csv)

# Guarda el DataFrame en un archivo CSV en la ubicación especificada
df.to_csv(ruta_archivo_csv, index=False)
