import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pandas as pd

import sys 

# Clase para redirigir la salida de la consola a un widget Text de Tkinter
class ConsoleRedirector: # clase para redirigir la salida de la consola a un widget Text de Tkinter
    def __init__(self, consola): # constructor de la clase
        self.consola = consola # inicializa el atributo consola con el widget Text de Tkinter

    def write(self, text): # método para escribir en el widget Text de Tkinter
        self.consola.insert(tk.END, text) # inserta el texto en el widget Text de Tkinter
        self.consola.see(tk.END)       # hace que el widget Text de Tkinter muestre el texto al final

    def flush(self):   # método para vaciar el buffer de salida
        pass           # no hace nada

# Variable global para almacenar las fechas
fechas = []

def on_button_click():
    global fechas  # Indica que vamos a modificar la variable global
    start_month = int(start_month_combobox.get())
    start_year = int(start_year_combobox.get())

    # Calcula los meses consecutivos
    fechas = []
    for i in range(3):  # 3 meses consecutivos
        month = start_month + i
        year = start_year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        fechas.append(f"{year}-{str(month).zfill(2)}")

    print(fechas)

    # Puedes usar la lista `fechas` para un JSON o consulta
    generar_json()

# Función para simular la creación de un JSON
def generar_json():
    datos_json = {
        "fechas": fechas
    }
    df = pd.DataFrame(datos_json)
# Crear la ventana principal
root = tk.Tk()
# cambiar el tamañio de la ventana
root.geometry("400x400")
root.title("Rango de Fechas con Tkinter")

# Crear una etiqueta para la fecha de inicio
start_label = tk.Label(root, text="Fecha de inicio:")
start_label.grid(row=0, column=0, padx=10, pady=10)

# Crear un campo de entrada para el mes de inicio
start_month_combobox = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(1, 13)], width=5)
start_month_combobox.grid(row=0, column=1, padx=10, pady=10)
start_month_combobox.set(datetime.now().strftime("%m"))

# Crear un campo de entrada para el año de inicio
start_year_combobox = ttk.Combobox(root, values=[str(i) for i in range(2000, 2031)], width=5)
start_year_combobox.grid(row=0, column=2, padx=10, pady=10)
start_year_combobox.set(datetime.now().strftime("%Y"))

# Crear un botón
button = tk.Button(root, text="Mostrar Fechas:", command=on_button_click)
button.grid(row=2, column=0, columnspan=3, pady=10)

#widget consola 
consola = tk.Text(root, width=49, height=10)
consola.grid(row=4, column=0, columnspan=3, pady=10)
sys.stdout = ConsoleRedirector(consola)

# Iniciar el bucle principal de la aplicación
root.mainloop()
