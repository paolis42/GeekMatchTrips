from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from solucion import decidir
from .models import Registro


# -------------------------------------------------
# ROLES Y PERMISOS
# -------------------------------------------------

def es_admin(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.groups.filter(name="admin").exists()
    )


def puede_crear(user):
    return user.is_authenticated and (
        es_admin(user)
        or user.groups.filter(name="normal").exists()
    )


# -------------------------------------------------
# READ - MOSTRAR REGISTROS
# viewer, normal y admin pueden ver
# -------------------------------------------------

@login_required(login_url="login")
def lista(request):
    registros = Registro.objects.filter(eliminado=False)

    return render(
        request,
        "lista.html",
        {
            "registros": registros,
            "puede_crear": puede_crear(request.user),
            "es_admin": es_admin(request.user),
        }
    )


# -------------------------------------------------
# CREATE - CREAR REGISTRO
# admin y normal pueden crear
# -------------------------------------------------

@login_required(login_url="login")
def crear(request):

    if not puede_crear(request.user):
        raise PermissionDenied

    error = None

    if request.method == "POST":
        nombre_lugar = request.POST.get(
            "nombre_lugar",
            ""
        ).strip()

        try:
            nivel_interes = int(
                request.POST.get("nivel_interes", "")
            )

            precio = int(
                request.POST.get("precio", "")
            )

            presupuesto = int(
                request.POST.get("presupuesto", "")
            )

        except ValueError:
            error = (
                "Interés, precio y presupuesto "
                "deben ser números enteros."
            )

        else:
            # Reutilizamos la regla de negocio
            # definida en solucion.py
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


# -------------------------------------------------
# UPDATE - EDITAR REGISTRO
# solo admin puede editar
# -------------------------------------------------

@login_required(login_url="login")
def editar(request, pk):

    if not es_admin(request.user):
        raise PermissionDenied

    registro = get_object_or_404(
        Registro,
        pk=pk,
        eliminado=False
    )

    error = None

    if request.method == "POST":
        nombre_lugar = request.POST.get(
            "nombre_lugar",
            ""
        ).strip()

        try:
            nivel_interes = int(
                request.POST.get("nivel_interes", "")
            )

            precio = int(
                request.POST.get("precio", "")
            )

            presupuesto = int(
                request.POST.get("presupuesto", "")
            )

        except ValueError:
            error = (
                "Interés, precio y presupuesto "
                "deben ser números enteros."
            )

        else:
            # Se vuelve a calcular el resultado
            # al editar los datos
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


# -------------------------------------------------
# DELETE LÓGICO
# solo admin puede eliminar
# -------------------------------------------------

@login_required(login_url="login")
def eliminar(request, pk):

    if not es_admin(request.user):
        raise PermissionDenied

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
        {
            "registro": registro
        }
    )


# -------------------------------------------------
# LOGIN
# -------------------------------------------------

def iniciar_sesion(request):
    error = None

    if request.method == "POST":
        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            auth_login(request, usuario)
            return redirect("lista")

        error = "Usuario o contraseña incorrectos."

    return render(
        request,
        "login.html",
        {
            "error": error
        }
    )


# -------------------------------------------------
# LOGOUT
# -------------------------------------------------

def cerrar_sesion(request):
    auth_logout(request)
    return redirect("login")