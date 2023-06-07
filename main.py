import random
import time
from tkinter import ttk
import tkinter as tk
import pandas as pd

# Semilla aleatoria timestamp
resultados = []

def update_results(dato):
    if len(dato) < 10:
        result.configure(text=f'RESULTADOS:\n{dato}')
    else:
        result.configure(text='RESULTADOS:\nLos resultados se guardaron en el archivo "resultados.xlsx"')


# Animación del dado
def drop_animation(frame_index=0):
    if frame_index < len(spritesheet):
        dice.configure(image=spritesheet[frame_index])
        frame_index += 1
        dice.after(100, lambda: drop_animation(frame_index))

def toogle_seed():
    global custom_random_seed
    if custom_seed.get() == 1:
        if timestamp_seed.get() == 1:
            print("asignar semilla timestamp")
            timestamp = time.time()
            custom_random_seed = timestamp
            random.seed(timestamp)
        elif seed_entry.get() != '':
            if seed_entry.get() != custom_random_seed:
                print("semilla asignada")
                custom_random_seed = seed_entry.get()
                random.seed(seed_entry.get())
        elif custom_random_seed != None and seed_entry.get() != '' and timestamp_seed.get() == 0:
            print("asignar vacio -- sin semilla ")
            custom_random_seed = None
            random.seed(None)
    else:
        if custom_random_seed != None:
            print("se cambio la configuracion a sin semilla personzalida")
            custom_random_seed = None
            random.seed(None)

# Función de lanzamiento simple
def lanzamiento_simple():
    toogle_seed()
    resultados.clear()
    resultados.append(random.randrange(1,6,1))
    dice.configure(image=spritesheet[resultados[0]-1])
    update_results(resultados)
    print(resultados)
    dt = pd.DataFrame(resultados)
    dt.to_excel('resultados.xlsx', engine = 'openpyxl')

def new_lanzamiento(n):
    drop_animation()
    root.after(1000, lanzamiento_n_veces(n))

def lanzamiento_n_veces():
    try:
        resultados.clear()
        toogle_seed()
        for i in range(int(entry.get())):
            resultado = random.randrange(1,6,1)  #aleatoriedad de numeros en un rango del 1 a 6
            print(f"El resultado es: {resultado}")
            resultados.append(resultado)
        else:
            update_results(resultados)
            print(f"Lista de resultados: {resultados}")
            dt = pd.DataFrame(resultados)
            dt.to_excel('resultados.xlsx', engine = 'openpyxl')
    except Exception as e:
        print("ocurrio un eeror")


def lanzamiento_simple_wrapper():
    drop_animation()
    root.after(800, lanzamiento_simple)


def lanzamiento_n_wrapper():
    drop_animation()
    root.after(800, lanzamiento_n_veces)


# Iinicalización de tkinter y renderización gráfica
root = tk.Tk()
custom_seed = tk.IntVar()
timestamp_seed = tk.IntVar()
custom_random_seed = None
root.geometry('1200x720') # Tamaño de pantalla de la app
title = ttk.Label(text="Lanzamiento aleatorio de un dado.")
checkbutton = tk.Checkbutton(root, text='Con semilla personalizada', variable=custom_seed,
                             onvalue=1, offvalue=0)
timestamp_checkbutton = tk.Checkbutton(root, text='Con semilla timestamp', variable=timestamp_seed,
                             onvalue=1, offvalue=0)
seed_entry = tk.Entry(root)
simple_drop_btn = ttk.Button(text="Lanzar", command=lanzamiento_simple_wrapper) # Botón para lanzamiento simple
entry = ttk.Entry(root) # Entrada para el numero de n veces a lanzar el dado
complex_drop_btn = ttk.Button(text="Lanzar n veces", command=lanzamiento_n_wrapper) # Botón para lanzar n veces. Requiere entry
spritesheet = [
    tk.PhotoImage(file="assets/1.png"),
    tk.PhotoImage(file="assets/2.png"),
    tk.PhotoImage(file="assets/3.png"),
    tk.PhotoImage(file="assets/4.png"),
    tk.PhotoImage(file="assets/5.png"),
    tk.PhotoImage(file="assets/6.png")
]
dice = ttk.Label(image=spritesheet[0]) # Crear un label y cargar la imagen del dado
result = ttk.Label(text="RESULTADOS:")
# INICIO Organización y distribución de elementos en la app
title.pack(pady=20)
checkbutton.pack()
timestamp_checkbutton.pack()
seed_entry.pack()
dice.pack(pady=30)
simple_drop_btn.pack(pady=10)
complex_drop_btn.pack(pady=10)
entry.pack()
result.pack(pady=30)
# FIN de Organización y distribución de elementos en la app
root.mainloop() # Correr la interfaz y la app mientras este abierta o activa

