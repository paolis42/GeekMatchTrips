import json

from django.conf import settings
from django.shortcuts import render

from solucion import decidir


def resumen(request):
    ruta_datos = settings.BASE_DIR / "datos.json"

    registros = []

    # Leer los registros que ya existen
    if ruta_datos.exists():
        with open(ruta_datos, "r", encoding="utf-8") as archivo:
            registros = json.load(archivo)

    resultado_actual = None

    # Si el usuario envía el formulario
    if request.method == "POST":
        nombre_lugar = request.POST.get("nombre_lugar")
        nivel_interes = int(request.POST.get("nivel_interes"))
        precio = int(request.POST.get("precio"))
        presupuesto = int(request.POST.get("presupuesto"))

        # Reutiliza la misma regla de solucion.py
        resultado, motivo = decidir(
            nivel_interes,
            precio,
            presupuesto
        )

        registro = {
            "lugar": nombre_lugar,
            "interes": nivel_interes,
            "precio": precio,
            "presupuesto": presupuesto,
            "resultado": resultado,
            "motivo": motivo
        }

        registros.append(registro)

        # Guardar nuevamente en datos.json
        with open(ruta_datos, "w", encoding="utf-8") as archivo:
            json.dump(
                registros,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        resultado_actual = registro

    return render(
        request,
        "resumen.html",
        {
            "registros": registros,
            "resultado_actual": resultado_actual
        }
    )
