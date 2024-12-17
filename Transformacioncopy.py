import pandas as pd #Importacion de pandas
import numpy as np
import json
import os
import datetime

fecha_actual = datetime.datetime.now()
nombre_carpeta = fecha_actual.strftime("%d_%m_%Y")
ruta_actual = os.getcwd()

ruta_completa = os.path.join(ruta_actual, nombre_carpeta)

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

def convert_to_dict(val):
    
    if isinstance(val, str):
        val = val.replace('"', '$')
        # Segundo: Reemplazar las comillas simples por dobles
        val = val.replace("'", '"')
        # Tercero: Reemplazar el marcador temporal por comillas simples
        val = val.replace('$', "'")
        val = val.replace("None", "null")
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            return np.nan
    else:
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

# Definir funciones para extraer cada campo de interés
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
    if valor != 0:
        return 'SI'
    else:
        return 'NO'
nombre_no_t = "archivo1.csv"
ruta_no_t = os.path.join(ruta_completa, nombre_no_t)
df=pd.read_csv(ruta_no_t)
df.head()
print(df.columns)
df['declaracion_bienesInmuebles_bienesInmuebles'] = df['declaracion_bienesInmuebles_bienesInmuebles'].apply(convert_to_dict)

df['moral_o_fisica'] = df['declaracion_bienesInmuebles_bienesInmuebles'].apply(get_persona_type)
df['domicilioExtranjero'] = df['declaracion_bienesInmuebles_bienesInmuebles'].apply(get_domicilioExtranjero)

# Primero, convertir la cadena JSON a una estructura de lista/diccionario
df['declaracion_datosEmpleoCargoComision_empleoCargoComision'] = df['declaracion_datosEmpleoCargoComision_empleoCargoComision'].apply(convert_to_dict)

# Crear nuevas columnas aplicando estas funciones
df['areaAdscripcion'] = df['declaracion_datosEmpleoCargoComision_empleoCargoComision'].apply(get_areaAdscripcion)
df['empleoCargoComision'] = df['declaracion_datosEmpleoCargoComision_empleoCargoComision'].apply(get_empleoCargoComision)
df['fechaEncargo'] = df['declaracion_datosEmpleoCargoComision_empleoCargoComision'].apply(get_fechaEncargo)

df['declaracion_datosCurricularesDeclarante_escolaridad'] = df['declaracion_datosCurricularesDeclarante_escolaridad'].apply(convert_to_dict)
df['max_nivel_academico'] = df['declaracion_datosCurricularesDeclarante_escolaridad'].apply(get_max_nivel_academico)

df.drop(columns=['declaracion_bienesInmuebles_bienesInmuebles'], inplace=True)
df.drop(columns=['declaracion_datosEmpleoCargoComision_empleoCargoComision'], inplace=True)
df.drop(columns=['declaracion_datosCurricularesDeclarante_escolaridad'], inplace=True)

#Cambia los valores numericos por si o no.
df['declaracion_ingresos_ingresoNetoParejaDependiente_remuneracion_monto'] = df['declaracion_ingresos_ingresoNetoParejaDependiente_remuneracion_monto'].apply(convertir_a_si_no)
df['declaracion_ingresos_otrosIngresosTotal_monto'] = df['declaracion_ingresos_otrosIngresosTotal_monto'].apply(convertir_a_si_no)


nombre_archivo_csv = "declaraciones_publicas.csv"
ruta_archivo_csv = os.path.join(ruta_completa, nombre_archivo_csv)

df.to_csv(ruta_archivo_csv, index=False)
print('LISTO')
# df.to_csv('declaraciones_publicas_31_09_23.csv', index=False)