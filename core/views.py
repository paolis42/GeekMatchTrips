from django.shortcuts import render, redirect, get_object_or_404

from solucion import decidir
from .models import Registro


# READ - mostrar registros
def lista(request):
    registros = Registro.objects.filter(eliminado=False)

    return render(
        request,
        "lista.html",
        {"registros": registros}
    )


# CREATE - crear registro
def crear(request):
    error = None

    if request.method == "POST":
        nombre_lugar = request.POST.get("nombre_lugar", "").strip()

        try:
            nivel_interes = int(request.POST.get("nivel_interes", ""))
            precio = int(request.POST.get("precio", ""))
            presupuesto = int(request.POST.get("presupuesto", ""))

        except ValueError:
            error = "Interés, precio y presupuesto deben ser números enteros."

        else:
            resultado, motivo = decidir(
                nivel_interes,
                precio,
                presupuesto
            )

            Registro.objects.create(
                nombre_lugar=nombre_lugar,
                nivel_interes=nivel_interes,
                precio=precio,
                presupuesto=presupuesto,
                resultado=resultado,
                motivo=motivo,
            )

            return redirect("lista")

    return render(
        request,
        "form.html",
        {
            "accion": "Crear",
            "error": error
        }
    )


# UPDATE - editar registro
def editar(request, pk):
    registro = get_object_or_404(
        Registro,
        pk=pk,
        eliminado=False
    )

    error = None

    if request.method == "POST":
        nombre_lugar = request.POST.get("nombre_lugar", "").strip()

        try:
            nivel_interes = int(request.POST.get("nivel_interes", ""))
            precio = int(request.POST.get("precio", ""))
            presupuesto = int(request.POST.get("presupuesto", ""))

        except ValueError:
            error = "Interés, precio y presupuesto deben ser números enteros."

        else:
            resultado, motivo = decidir(
                nivel_interes,
                precio,
                presupuesto
            )

            registro.nombre_lugar = nombre_lugar
            registro.nivel_interes = nivel_interes
            registro.precio = precio
            registro.presupuesto = presupuesto
            registro.resultado = resultado
            registro.motivo = motivo

            registro.save()

            return redirect("lista")

    return render(
        request,
        "form.html",
        {
            "accion": "Editar",
            "registro": registro,
            "error": error
        }
    )


# DELETE lógico
def eliminar(request, pk):
    registro = get_object_or_404(
        Registro,
        pk=pk,
        eliminado=False
    )

    if request.method == "POST":
        registro.soft_delete()
        return redirect("lista")

    return render(
        request,
        "confirmar.html",
        {"registro": registro}
    )