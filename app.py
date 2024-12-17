from pymongo import MongoClient
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import sys

# Variables globales
false = False

# Creacion de el archivo y la ruta de la carpeta
fecha_actual = datetime.now()
nombre_carpeta = fecha_actual.strftime("%d_%m_%Y")
ruta_actual = os.getcwd()

# Ruta completa
ruta_completa = os.path.join(ruta_actual, nombre_carpeta)

# Crear la carpeta si no existe
if not os.path.exists(ruta_completa):
    os.makedirs(ruta_completa)

nombre_no_t = "archivo1.csv"
ruta_no_t = os.path.join(ruta_completa, nombre_no_t)

if not os.path.exists(ruta_no_t):
    print(f"")

# Define el orden de los niveles académicos para despues buscar el mas alto
nivel_academico_orden = {
    'PRIMARIA': 1,
    'SECUNDARIA': 2,
    'BACHILLERATO': 3,
    'LICENCIATURA': 4,
    'ESPECIALIDAD': 5,
    'MAESTRIA': 6,
    'DOCTORADO': 7
}

# Clase para redirigir la salida de la consola a un widget Text de Tkinter
class ConsoleRedirector: # clase para redirigir la salida de la consola a un widget Text de Tkinter
    def __init__(self, consola): # constructor de la clase
        self.consola = consola # inicializa el atributo consola con el widget Text de Tkinter

    def write(self, text): # método para escribir en el widget Text de Tkinter
        self.consola.insert(tk.END, text) # inserta el texto en el widget Text de Tkinter
        self.consola.see(tk.END)      # hace que el widget Text de Tkinter muestre el texto al final

    def flush(self):  # método para vaciar el buffer de salida
        pass

# Función para "aplanar" un diccionario anidado
def flat_dict(d, parent_key='', sep='_'): # función para "aplanar" un diccionario anidado, convirtiendo las claves anidadas en claves únicas
    items = {} # diccionario para almacenar los elementos aplanados
    for k, v in d.items(): # itera sobre los elementos del diccionario
        new_key = parent_key + sep + k if parent_key else k # genera una nueva clave combinando la clave actual con la clave del padre usando el separador
        if isinstance(v, dict): # si el valor es otro diccionario, llama a la función recursivamente
            items.update(flat_dict(v, new_key, sep=sep)) # actualiza el diccionario con los elementos aplanados
        else: # si no es un diccionario, añade el valor al nuevo diccionario
            items[new_key] = v # añade el valor al diccionario
    return items # retorna el diccionario con las claves aplanadas

# Función para manejar el clic del botón
def on_button_click(): # función para manejar el clic del botón
    global fechas # indica que vamos a modificar la variable global
    start_month = int(start_month_combobox.get()) # obtiene el mes de inicio
    start_year = int(start_year_combobox.get()) # obtiene el año de inicio

    # Calcula los meses consecutivos
    fechas = [] # lista para almacenar las fechas
    for i in range(3):  # Cambia este valor si necesitas más meses
        month = start_month + i # suma el índice al mes de inicio
        year = start_year + (month - 1) // 12 # calcula el año
        month = (month - 1) % 12 + 1 # calcula el mes
        fechas.append(f"{year}-{str(month).zfill(2)}") # añade la fecha a la lista
    print(f"Fechas generadas: {fechas}") # imprime las fechas generadas
    realizar_consulta() # llama a la función para realizar la consulta

# Función para realizar la consulta y guardar los resultados
def realizar_consulta(): # función para realizar la consulta y guardar los resultados
    # Configuración de MongoDB
    from conexion import uri # importa la URI de conexión a MongoDB
    DB_NAME = os.environ.get("DB_NAME") # obtiene el nombre de la base de datos
    client = MongoClient(uri) # crea el cliente de MongoDB
    db = client[DB_NAME]    # selecciona la base de datos
    collection = db['datosPublicos100'] # selecciona la colección

    # Ejecutar el pipeline de agregación
    try:    # intenta ejecutar la consulta
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
  ]
)

        # Convertir resultados a DataFrame
        lista = list(cursor) # convierte el cursor a una lista
        df = pd.DataFrame(lista) # convierte la lista a un DataFrame
        if df.empty: # si el DataFrame está vacío, imprime un mensaje
            print("No se encontraron resultados para las fechas proporcionadas.") # imprime un mensaje
            return # termina la función

        # Aplana la columna 'declaracion'
        df_flat = df['declaracion'].apply(lambda x: flat_dict(x)).apply(pd.Series) # aplica la función flat_dict a la columna 'declaracion' y convierte el resultado en un DataFrame
        df = pd.concat([df.drop(['declaracion'], axis=1), df_flat], axis=1) # concatena el DataFrame original sin la columna 'declaracion' con el DataFrame aplanado

        # Crear carpeta para guardar resultados
        fecha_actual = datetime.now() # obtiene la fecha y hora actuales
        nombre_carpeta = fecha_actual.strftime("%d_%m_%Y") # formatea la fecha actual para usarla como nombre de carpeta
        ruta_actual = os.getcwd() # obtiene la ruta del directorio actual
        ruta_completa = os.path.join(ruta_actual, nombre_carpeta) # crea la ruta completa donde se guardará el archivo CSV
        os.makedirs(ruta_completa, exist_ok=True) # crea la carpeta si no existe

        # Guardar DataFrame como CSV
        ruta_archivo_csv = os.path.join(ruta_completa, "archivo1.csv") # crea la ruta del archivo CSV
        df.to_csv(ruta_archivo_csv, index=False) # guarda el DataFrame como un archivo CSV
        print(f"Archivo CSV guardado en: {ruta_archivo_csv}") # imprime la ruta del archivo CSV

    except Exception as e: # si ocurre un error, imprime un mensaje
        print(f"Error durante la consulta: {e}") # imprime un mensaje

def convert_to_dict(val):
    if isinstance(val, str):
        val = val.replace('"', '$').replace("'", '"').replace('$', "'").replace("None", "null")
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            return np.nan
    return val

def get_persona_type(x):
    if isinstance(x, list):
        for dic in x:
            transmisores = dic.get('transmisores', [])
            if any(item.get('tipoPersona') == 'PERSONA_MORAL' for item in transmisores):
                return 'PERSONA_MORAL'
        return 'PERSONA_FISICA' if any(dic.get('transmisores') for dic in x) else np.nan
    return np.nan

def get_domicilioExtranjero(x):
    if isinstance(x, list):
        for dic in x:
            domicilio = dic.get('domicilio', {}).get('domicilioExtranjero')
            if domicilio is not None:
                return 'SI'
        return 'NO'
    return np.nan

def get_areaAdscripcion(x):
    if isinstance(x, list) and len(x) > 0 and isinstance(x[0], dict):
        return x[0].get('areaAdscripcion', np.nan)
    return np.nan

def get_empleoCargoComision(x):
    if isinstance(x, list) and len(x) > 0 and isinstance(x[0], dict):
        return x[0].get('empleoCargoComision', np.nan)
    return np.nan

def get_fechaEncargo(x):
    if isinstance(x, list) and len(x) > 0 and isinstance(x[0], dict):
        return x[0].get('fechaEncargo', np.nan)
    return np.nan

def get_max_nivel_academico(x):
    if isinstance(x, list):
        max_nivel = 0
        max_nivel_nombre = np.nan
        for dic in x:
            nivel = dic.get('nivel', {}).get('valor')
            if nivel and nivel in nivel_academico_orden and nivel_academico_orden[nivel] > max_nivel:
                max_nivel = nivel_academico_orden[nivel]
                max_nivel_nombre = nivel
        return max_nivel_nombre
    return np.nan

def convertir_a_si_no(valor):
    return 'SI' if valor != 0 else 'NO'

# Procesar el archivo CSV
df = pd.read_csv(ruta_no_t)
df['declaracion_bienesInmuebles_bienesInmuebles'] = df['declaracion_bienesInmuebles_bienesInmuebles'].apply(convert_to_dict)
df['moral_o_fisica'] = df['declaracion_bienesInmuebles_bienesInmuebles'].apply(get_persona_type)
df['domicilioExtranjero'] = df['declaracion_bienesInmuebles_bienesInmuebles'].apply(get_domicilioExtranjero)

df['declaracion_datosEmpleoCargoComision_empleoCargoComision'] = df['declaracion_datosEmpleoCargoComision_empleoCargoComision'].apply(convert_to_dict)
df['areaAdscripcion'] = df['declaracion_datosEmpleoCargoComision_empleoCargoComision'].apply(get_areaAdscripcion)
df['empleoCargoComision'] = df['declaracion_datosEmpleoCargoComision_empleoCargoComision'].apply(get_empleoCargoComision)
df['fechaEncargo'] = df['declaracion_datosEmpleoCargoComision_empleoCargoComision'].apply(get_fechaEncargo)

df['declaracion_datosCurricularesDeclarante_escolaridad'] = df['declaracion_datosCurricularesDeclarante_escolaridad'].apply(convert_to_dict)
df['max_nivel_academico'] = df['declaracion_datosCurricularesDeclarante_escolaridad'].apply(get_max_nivel_academico)

df.drop(columns=[
    'declaracion_bienesInmuebles_bienesInmuebles',
    'declaracion_datosEmpleoCargoComision_empleoCargoComision',
    'declaracion_datosCurricularesDeclarante_escolaridad'
], inplace=True)

df['declaracion_ingresos_ingresoNetoParejaDependiente_remuneracion_monto'] = df['declaracion_ingresos_ingresoNetoParejaDependiente_remuneracion_monto'].apply(convertir_a_si_no)
df['declaracion_ingresos_otrosIngresosTotal_monto'] = df['declaracion_ingresos_otrosIngresosTotal_monto'].apply(convertir_a_si_no)

# Guardar el archivo final
nombre_archivo_csv = "declaraciones_publicas.csv"
ruta_archivo_csv = os.path.join(ruta_completa, nombre_archivo_csv)

df.to_csv(ruta_archivo_csv, index=False)
print(f'Archivo guardado en: {ruta_archivo_csv}')

# Crear la interfaz gráfica
root = tk.Tk() # crea la ventana principal
root.geometry("400x400") # cambia el tamaño de la ventana
root.title("Declaraciones Públicas") # cambia el título de la ventana

# Etiqueta y campos para la fecha de inicio
start_label = tk.Label(root, text="Fecha de inicio:") # crea una etiqueta
start_label.grid(row=0, column=0, padx=10, pady=10) # coloca la etiqueta en la ventana
start_month_combobox = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(1, 13)], width=5) # crea un campo de entrada para el mes
start_month_combobox.grid(row=0, column=1, padx=10, pady=10) # coloca el campo de entrada en la ventana
start_month_combobox.set(datetime.now().strftime("%m")) # establece el mes actual como valor predeterminado
start_year_combobox = ttk.Combobox(root, values=[str(i) for i in range(2000, 2031)], width=5) # crea un campo de entrada para el año
start_year_combobox.grid(row=0, column=2, padx=10, pady=10) # coloca el campo de entrada en la ventana
start_year_combobox.set(datetime.now().strftime("%Y")) # establece el año actual como valor predeterminado

# Botón para generar fechas y realizar la consulta
button = tk.Button(root, text="Consultar", command=on_button_click) # crea un botón
button.grid(row=2, column=0, columnspan=3, pady=10) # coloca el botón en la ventana

# Consola para mostrar resultados
consola = tk.Text(root, width=49, height=10) # crea un widget Text para la consola
consola.grid(row=4, column=0, columnspan=3, pady=10) # coloca la consola en la ventana
sys.stdout = ConsoleRedirector(consola) # redirige la salida estándar a la consola

# Iniciar el loop de la interfaz gráfica
root.mainloop() # inicia el bucle principal de la aplicación
