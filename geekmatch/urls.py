from django.contrib import admin
from django.urls import path

from core import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("registros/", views.lista, name="lista"),
    path("registros/crear/", views.crear, name="crear"),
    path("registros/<int:pk>/editar/", views.editar, name="editar"),
    path("registros/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]
