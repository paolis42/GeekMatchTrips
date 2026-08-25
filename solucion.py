import json
import os
from tabulate import tabulate


nombre_lugar = input("Nombre del lugar: ")
nivel_interes = int(input("Nivel de interés (1 a 5): "))
precio = int(input("Precio del lugar: "))
presupuesto = int(input("Presupuesto disponible: "))


if nivel_interes < 1 or nivel_interes > 5 or precio < 0 or presupuesto < 0:
    resultado = "Dato inválido"
    motivo = "Revisa la información ingresada."

elif nivel_interes >= 4 and precio <= presupuesto:
    resultado = "Recomendado"
    motivo = "El lugar tiene alta afinidad con tus intereses y está dentro de tu presupuesto."

elif precio > presupuesto:
    resultado = "No recomendado por presupuesto"
    motivo = "El precio del lugar supera tu presupuesto disponible."

else:
    resultado = "No recomendado por baja afinidad"
    motivo = "El lugar no tiene suficiente relación con tus intereses."


registro = {
    "lugar": nombre_lugar,
    "interes": nivel_interes,
    "precio": precio,
    "presupuesto": presupuesto,
    "resultado": resultado,
    "motivo": motivo
}


registros = []


if os.path.exists("datos.json"):
    with open("datos.json", "r", encoding="utf-8") as archivo:
        registros = json.load(archivo)


registros.append(registro)


with open("datos.json", "w", encoding="utf-8") as archivo:
    json.dump(registros, archivo, indent=4, ensure_ascii=False)


print("\n--- Resultado GeekMatch ---")
print("Lugar:", nombre_lugar)
print("Resultado:", resultado)
print("Motivo:", motivo)


print("\n--- Lugares evaluados ---")
print(tabulate(registros, headers="keys", tablefmt="grid"))