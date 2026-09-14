# GeekMatch Trips

## 1. NEGOCIO

### Problema

Al planificar un viaje, las personas pueden encontrar muchos lugares y actividades interesantes, pero no siempre es fácil decidir cuáles conviene incluir considerando sus gustos y el presupuesto disponible.

La información suele estar distribuida en diferentes sitios, lo que puede dificultar la organización y hacer que el viajero priorice actividades que no se ajustan realmente a sus intereses o presupuesto.

### Solución

GeekMatch Trips busca apoyar la planificación de viajes personalizados.

La aplicación permite evaluar lugares turísticos según el nivel de interés del usuario, el precio de la actividad y su presupuesto disponible.

Como resultado, el sistema indica si el lugar es recomendado o no y explica el motivo de la decisión.

La regla de decisión está implementada en Python dentro de `solucion.py` y es reutilizada por la aplicación Django, evitando duplicar la lógica de negocio.

En esta segunda etapa, GeekMatch Trips incorpora persistencia mediante SQLite, operaciones CRUD, inicio de sesión y control de acceso mediante roles.

---

### Alcance actual

En esta versión se puede:

- Iniciar sesión en la aplicación.
- Consultar los lugares evaluados.
- Ingresar un nuevo lugar turístico.
- Indicar un nivel de interés entre 1 y 5.
- Ingresar el precio de la actividad.
- Ingresar el presupuesto disponible.
- Evaluar si el lugar es recomendado.
- Mostrar el motivo de la decisión.
- Guardar las evaluaciones en una base de datos SQLite.
- Editar registros existentes.
- Recalcular automáticamente el resultado cuando un registro es editado.
- Realizar borrado lógico de registros.
- Administrar registros mediante Django Admin.
- Utilizar diferentes niveles de acceso según el rol del usuario.

El proyecto completo de GeekMatch Trips contempla a futuro la generación de itinerarios reales, horarios, reservas, entradas oficiales, comidas, descansos, tiempos de traslado, mapas y otras preferencias del viajero.

Estas funciones todavía no forman parte del alcance actual.

---

### MoSCoW

#### Must

1. Solicitar los datos necesarios para evaluar un lugar.

2. Decidir si el lugar es recomendado utilizando el nivel de interés, precio y presupuesto.

3. Mostrar el resultado y el motivo de la decisión.

4. Reutilizar la función `decidir()` de `solucion.py` desde Django.

5. Guardar las evaluaciones en una base de datos SQLite.

6. Mostrar los registros almacenados.

7. Permitir crear nuevos registros.

8. Permitir editar registros existentes.

9. Recalcular el resultado al editar un registro.

10. Implementar borrado lógico para evitar eliminar físicamente los registros.

11. Implementar inicio y cierre de sesión.

12. Utilizar roles para controlar las acciones permitidas a cada usuario.

13. Proteger las rutas desde el servidor para impedir accesos no autorizados.

14. Utilizar Django Admin para administrar los registros.

#### Should

- Informar si una actividad es gratuita o pagada.
- Informar si necesita reserva o tiene distintas formas de acceso.
- Incorporar categorías de intereses del viajero.
- Mostrar información sobre cuándo conviene reservar.
- Mejorar el diseño visual de la aplicación.
- Mostrar mensajes más amigables cuando un usuario no tiene permisos.

#### Could

- Generar un itinerario completo por días y horarios.
- Considerar desayuno, almuerzo, once y cena.
- Agregar pausas breves de descanso.
- Considerar tiempos de traslado.
- Personalizar el ritmo del viaje.
- Incorporar mapas.
- Mostrar páginas oficiales para comprar entradas o realizar reservas.
- Permitir que cada usuario tenga sus propios viajes.
- Incorporar una base de datos más robusta para una futura publicación en internet.

#### Won't

- API o MCP en esta versión.
- Compra directa de entradas.
- Pagos dentro de la aplicación.
- Generación automática del viaje completo.
- Reservas automáticas.
- Integración con servicios externos de transporte o mapas.

---

## 2. TÉCNICO

### Tecnologías utilizadas

El proyecto utiliza:

- Python para la lógica de programación.
- Django para la aplicación web.
- SQLite como base de datos.
- Django ORM para consultar y modificar los registros.
- Django Authentication para usuarios y sesiones.
- Django Groups para implementar roles.
- `python-decouple` para manejar variables sensibles desde `.env`.
- Git y GitHub para control de versiones.
- `tabulate` como paquete externo utilizado en la etapa inicial del proyecto para mostrar datos en consola.

---

### Datos de entrada

El sistema utiliza los siguientes datos para evaluar un lugar:

- `nombre_lugar`: texto (`str`).
- `nivel_interes`: número entero (`int`) entre 1 y 5.
- `precio`: número entero (`int`).
- `presupuesto`: número entero (`int`).

Los campos numéricos son convertidos utilizando `int()` y se utiliza manejo de excepciones para evitar errores cuando el usuario ingresa datos que no son números enteros.

---

### Regla de decisión

La regla principal se mantiene dentro de la función `decidir()` de `solucion.py`.

Esta función no se copia dentro de las vistas Django, sino que se importa y reutiliza.

El programa tiene cuatro resultados posibles:

#### 1. Dato inválido

Ocurre si:

- el nivel de interés es menor que 1 o mayor que 5;
- el precio es negativo;
- o el presupuesto es negativo.

Resultado:

**Dato inválido. Revisa la información ingresada.**

#### 2. Recomendado

Ocurre cuando:

- el nivel de interés es igual o mayor a 4;
- y el precio es menor o igual al presupuesto disponible.

Resultado:

**Recomendado. El lugar tiene alta afinidad con tus intereses y está dentro de tu presupuesto.**

#### 3. No recomendado por presupuesto

Ocurre cuando el precio del lugar es mayor que el presupuesto disponible.

Resultado:

**No recomendado por presupuesto. El lugar supera el monto disponible para esta actividad.**

#### 4. No recomendado por baja afinidad

Ocurre cuando el presupuesto alcanza para realizar la actividad, pero el nivel de interés es menor que 4.

Resultado:

**No recomendado por baja afinidad. El lugar no tiene suficiente relación con tus intereses.**

---

### Base de datos

La aplicación utiliza SQLite, incluida con Django.

La información deja de almacenarse en `datos.json`.

El modelo principal se llama `Registro` y contiene información como:

- nombre del lugar;
- nivel de interés;
- precio;
- presupuesto;
- resultado;
- motivo;
- fecha de creación;
- estado de eliminación;
- fecha de eliminación.

Django ORM permite trabajar con estos datos sin escribir consultas SQL manualmente.

Las modificaciones realizadas al modelo se controlan mediante migraciones de Django.

---

### CRUD

La aplicación implementa las cuatro operaciones principales sobre los registros.

#### CREATE

Permite crear una nueva evaluación.

El usuario ingresa:

- nombre del lugar;
- nivel de interés;
- precio;
- presupuesto.

Antes de guardar el registro, la aplicación utiliza `decidir()` para calcular el resultado y el motivo.

#### READ

La página principal muestra los registros que se encuentran activos.

Los registros marcados como eliminados no se muestran en la lista normal.

#### UPDATE

Permite modificar un registro existente.

Cuando se cambia el interés, precio o presupuesto, se vuelve a ejecutar `decidir()` para actualizar también el resultado y el motivo.

De esta forma, el resultado almacenado siempre corresponde a los datos actuales del registro.

#### DELETE

Se utiliza borrado lógico.

El registro no se elimina físicamente de SQLite.

En su lugar, se modifica el campo `eliminado` para indicar que el registro ya no debe aparecer en la lista principal.

También se registra la fecha de eliminación.

---

### Rutas principales

Las rutas principales de la aplicación son:

- `/login/` → inicio de sesión.
- `/logout/` → cierre de sesión.
- `/registros/` → listado de registros.
- `/registros/crear/` → creación de un registro.
- `/registros/<id>/editar/` → edición de un registro.
- `/registros/<id>/eliminar/` → borrado lógico.
- `/admin/` → administración de Django.

---

### Inicio de sesión

La aplicación utiliza el sistema de autenticación incluido en Django.

Las contraseñas no se almacenan manualmente en el proyecto.

Django se encarga de administrar los usuarios, las contraseñas y las sesiones.

Cuando una persona intenta acceder a la aplicación sin haber iniciado sesión, debe autenticarse antes de acceder a las vistas protegidas.

---

### Roles y permisos

Se utilizan los grupos de Django para manejar los roles.

Los roles definidos son:

#### Viewer

Puede:

- iniciar sesión;
- ver los registros.

No puede:

- crear;
- editar;
- eliminar.

#### Normal

Puede:

- iniciar sesión;
- ver los registros;
- crear nuevos registros.

No puede:

- editar;
- eliminar.

#### Admin

Puede:

- ver;
- crear;
- editar;
- eliminar.

El superusuario de Django también tiene acceso completo.

Las restricciones no dependen solamente de ocultar botones en la interfaz.

Las vistas verifican los permisos en el servidor, por lo que un usuario sin autorización recibe una respuesta `403 Forbidden` aunque intente ingresar manualmente a una URL restringida.

---

### Django Admin

El modelo `Registro` está registrado en Django Admin.

El administrador permite:

- visualizar los registros;
- buscar registros por nombre del lugar;
- filtrar por resultado;
- filtrar por estado de eliminación;
- revisar registros que fueron eliminados lógicamente.

Esto también permite comprobar que un registro eliminado desde la aplicación sigue almacenado en SQLite.

---

### Seguridad

El proyecto utiliza:

- autenticación de Django;
- control de acceso mediante grupos;
- decorador `login_required`;
- validación de permisos en el servidor;
- protección CSRF en formularios POST;
- variables sensibles almacenadas en `.env`;
- `.env.example` como ejemplo de configuración;
- `.gitignore` para evitar subir información sensible y archivos locales al repositorio.

La clave secreta real de Django no se almacena directamente en `settings.py`.

---

### Persistencia

En la primera etapa del proyecto los registros se almacenaban en `datos.json`.

En Eva 2, SQLite reemplaza a JSON como sistema principal de persistencia.

`datos.json` deja de ser utilizado por las vistas Django para almacenar nuevas evaluaciones.

La lógica de decisión de `solucion.py` se mantiene y es reutilizada por la aplicación web.