from django.contrib import admin
from .models import Registro


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_lugar",
        "nivel_interes",
        "precio",
        "presupuesto",
        "resultado",
        "fecha",
    )

    list_filter = (
        "resultado",
        "eliminado",
    )

    search_fields = (
        "nombre_lugar",
    )

    readonly_fields = (
        "fecha",
        "fecha_eliminacion",
    )

