import tkinter as tk
from tkinter import ttk
from datetime import datetime

def on_button_click():
    start_month = start_month_combobox.get()
    start_year = start_year_combobox.get()
    end_month = end_month_combobox.get()
    end_year = end_year_combobox.get()
    label.config(text=f"Fecha de inicio: {start_year}-{start_month}\n Fecha de fin: {end_year}-{end_month}")

# Crear la ventana principal
root = tk.Tk()
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

# Crear una etiqueta para la fecha de fin
end_label = tk.Label(root, text="Fecha de fin:")
end_label.grid(row=1, column=0, padx=10, pady=10)

# Crear un campo de entrada para el mes de fin
end_month_combobox = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(1, 13)], width=5)
end_month_combobox.grid(row=1, column=1, padx=10, pady=10)
end_month_combobox.set(datetime.now().strftime("%m"))

# Crear un campo de entrada para el año de fin
end_year_combobox = ttk.Combobox(root, values=[str(i) for i in range(2000, 2031)], width=5)
end_year_combobox.grid(row=1, column=2, padx=10, pady=10)
end_year_combobox.set(datetime.now().strftime("%Y"))

# Crear un botón
button = tk.Button(root, text="Mostrar Fechas", command=on_button_click)
button.grid(row=2, column=0, columnspan=3, pady=10)

# Crear una etiqueta para mostrar las fechas seleccionadas
label = tk.Label(root, text="")
label.grid(row=3, column=0, columnspan=3, pady=10)

# Iniciar el bucle principal de la aplicación
root.mainloop()
