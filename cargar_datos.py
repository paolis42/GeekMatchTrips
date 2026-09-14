import json

from core.models import Registro


with open("datos.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)


for dato in datos:
    registro, creado = Registro.objects.get_or_create(
        nombre_lugar=dato["lugar"],
        nivel_interes=dato["interes"],
        precio=dato["precio"],
        presupuesto=dato["presupuesto"],
        resultado=dato["resultado"],
        motivo=dato["motivo"],
    )

    if creado:
        print(f"Agregado: {registro.nombre_lugar}")
    else:
        print(f"Ya existía: {registro.nombre_lugar}")