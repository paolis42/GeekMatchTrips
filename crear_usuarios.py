from django.contrib.auth.models import User, Group
from decouple import config


# Crear los grupos si todavía no existen
for nombre_grupo in ("admin", "normal", "viewer"):
    Group.objects.get_or_create(name=nombre_grupo)


usuarios = [
    ("admin", "admin", config("PASS_ADMIN", default="")),
    ("normal", "normal", config("PASS_NORMAL", default="")),
    ("viewer", "viewer", config("PASS_VIEWER", default="")),
]


for username, grupo, password in usuarios:

    if not password:
        raise ValueError(
            f"Falta configurar PASS_{username.upper()} en el archivo .env"
        )

    usuario, creado = User.objects.get_or_create(
        username=username
    )

    usuario.set_password(password)
    usuario.is_active = True
    usuario.save()

    usuario.groups.clear()
    usuario.groups.add(
        Group.objects.get(name=grupo)
    )

    if creado:
        print(f"Usuario creado: {username} -> {grupo}")
    else:
        print(f"Usuario actualizado: {username} -> {grupo}")