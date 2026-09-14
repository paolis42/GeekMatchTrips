# Uso de Inteligencia Artificial - GeekMatch Trips

## Herramientas utilizadas

Durante el desarrollo de GeekMatch Trips utilicé las siguientes herramientas de apoyo:

- ChatGPT, para realizar consultas, recibir explicaciones, revisar código y comprender los pasos necesarios para implementar la evaluación.
- GitHub Copilot, como apoyo dentro de Visual Studio Code mediante sugerencias de código.

La IA fue utilizada como apoyo durante el desarrollo, pero cada cambio fue incorporado y probado manualmente dentro del proyecto antes de continuar con la siguiente etapa.

---

## Trabajo realizado y comprobado durante el desarrollo

Durante la evaluación trabajé directamente desde Visual Studio Code y fui probando el funcionamiento de cada parte del proyecto.

Entre las tareas realizadas y verificadas se encuentran:

- configuración del entorno virtual;
- instalación y uso de Django;
- creación y modificación del modelo `Registro`;
- creación de migraciones;
- ejecución de las migraciones sobre SQLite;
- comprobación del estado de las migraciones;
- configuración de Django Admin;
- creación de un superusuario;
- prueba del buscador y los filtros del administrador;
- implementación y prueba del CRUD;
- creación de registros;
- edición de registros;
- comprobación de que el resultado se recalcula al editar;
- implementación del borrado lógico;
- comprobación desde Django Admin de que un registro eliminado sigue existiendo en la base de datos;
- implementación del inicio y cierre de sesión;
- creación de los grupos `admin`, `normal` y `viewer`;
- creación de usuarios de prueba;
- comprobación manual de las restricciones de cada rol;
- prueba de acceso directo mediante URLs;
- comprobación de respuestas `403 Forbidden`;
- actualización del repositorio GitHub durante el desarrollo.

---

## Consultas realizadas a la IA

### Consulta sobre el modelo y SQLite

Una de las consultas realizadas fue:

> ¿Cómo adapto el modelo de la guía a GeekMatch Trips para guardar nombre del lugar, nivel de interés, precio, presupuesto, resultado y motivo en SQLite?

La respuesta sirvió como referencia para crear el modelo `Registro`.

La propuesta fue adaptada a los datos que realmente utiliza GeekMatch Trips y se agregaron también campos para implementar el borrado lógico:

- `eliminado`
- `fecha_eliminacion`

Después de realizar el cambio ejecuté:

`python manage.py makemigrations`

y:

`python manage.py migrate`

Posteriormente comprobé el estado de las migraciones mediante:

`python manage.py makemigrations --check --dry-run`

El resultado fue:

`No changes detected`

Esto permitió comprobar que el modelo y las migraciones estaban sincronizados.

---

### Consulta sobre la reutilización de la regla de decisión

Otra consulta realizada fue:

> ¿Debo copiar los if y elif de la función decidir() dentro de las vistas de Django?

Se revisó que esto no era necesario.

La función `decidir()` se mantuvo dentro de `solucion.py` y las vistas Django la importan mediante:

`from solucion import decidir`

De esta forma se evita mantener dos versiones de la misma regla de negocio.

También comprobé que al editar un registro se vuelva a ejecutar `decidir()`, ya que cambiar el interés, precio o presupuesto puede cambiar el resultado de la evaluación.

---

### Consulta sobre el cambio desde JSON a SQLite

Durante el desarrollo detecté que `views.py` todavía contenía código de la evaluación anterior que utilizaba:

- `import json`
- `datos.json`
- `settings.BASE_DIR`

La consulta realizada fue si ese código debía mantenerse o reemplazarse.

Se determinó que las vistas de Eva 2 debían trabajar con el modelo `Registro` y SQLite.

Por lo tanto se eliminó de las vistas el almacenamiento mediante JSON y se reemplazó por operaciones utilizando Django ORM.

`datos.json` dejó de ser el sistema principal de persistencia.

---

### Consulta sobre CRUD

También utilicé IA como apoyo para organizar las cuatro operaciones requeridas:

- CREATE
- READ
- UPDATE
- DELETE

Las vistas finalmente implementadas fueron:

- `lista`
- `crear`
- `editar`
- `eliminar`

Durante las pruebas comprobé manualmente cada operación.

Para CREATE agregué un nuevo lugar desde la página web.

Para READ comprobé que los registros almacenados en SQLite aparecieran en la lista.

Para UPDATE modifiqué el nivel de interés de un registro y confirmé que el resultado cambiara automáticamente.

Para DELETE comprobé que el registro desapareciera de la lista normal, pero continuara existiendo dentro de Django Admin.

Esto confirmó que se estaba utilizando borrado lógico y no eliminación física.

---

### Consulta sobre login y roles

Una de las consultas realizadas fue:

> ¿Cómo puedo utilizar los grupos de Django para tener los roles admin, normal y viewer sin crear mi propio sistema de contraseñas?

La respuesta fue utilizar el sistema de autenticación y los grupos incluidos en Django.

Se crearon los siguientes grupos:

- `admin`
- `normal`
- `viewer`

Se definió el siguiente comportamiento:

#### Viewer

Puede:

- iniciar sesión;
- ver registros.

No puede:

- crear;
- editar;
- eliminar.

#### Normal

Puede:

- iniciar sesión;
- ver registros;
- crear registros.

No puede:

- editar;
- eliminar.

#### Admin

Puede:

- ver;
- crear;
- editar;
- eliminar.

El superusuario de Django también puede realizar todas las acciones.

---

## Correcciones y ajustes realizados durante el uso de IA

Las respuestas generadas por IA no fueron utilizadas sin revisión.

Durante el desarrollo se realizaron varias correcciones y adaptaciones.

### Adaptación del modelo

Los ejemplos generales de la guía y de la IA podían utilizar nombres de campos diferentes.

El modelo final se adaptó específicamente a GeekMatch Trips utilizando:

- `nombre_lugar`
- `nivel_interes`
- `precio`
- `presupuesto`
- `resultado`
- `motivo`

---

### Corrección de un nombre de campo

Durante la preparación de la vista de edición apareció una referencia incorrecta:

`nivel_interres`

Se corrigió por:

`nivel_interes`

Esto era necesario para que el nombre coincidiera con el campo enviado por el formulario.

---

### Mantener una sola regla de negocio

Se comprobó que la regla de decisión no quedara copiada dentro de `views.py`.

La versión final reutiliza la función de `solucion.py`.

Esto permite que la misma lógica sea utilizada por la aplicación sin mantener dos reglas diferentes.

---

### Recalcular el resultado durante UPDATE

Se verificó que la edición no modificara solamente los datos ingresados.

Después de cambiar:

- nivel de interés;
- precio;
- presupuesto;

se vuelve a ejecutar `decidir()`.

De esta manera también se actualizan:

- `resultado`;
- `motivo`.

---

### Validación de números

Se incorporó manejo de excepciones mediante `try/except` para los campos que deben convertirse a números enteros.

Esto evita que la aplicación termine en un error si se intenta ingresar texto en un valor que debe ser numérico.

---

### Seguridad de los roles

Inicialmente ocultar botones podía parecer suficiente para diferenciar los roles.

Sin embargo, se comprobó que eso no protege realmente una aplicación.

Por este motivo las restricciones se implementaron también dentro de las vistas Django.

Después realicé pruebas escribiendo directamente las URLs protegidas.

Por ejemplo, utilizando un usuario sin permisos se intentó acceder directamente a rutas de creación, edición o eliminación.

Django respondió con:

`403 Forbidden`

Esto permitió comprobar que las restricciones funcionan del lado del servidor y no dependen solamente de la interfaz.

---

## Pruebas realizadas

Las funcionalidades fueron probadas manualmente durante el desarrollo.

### Base de datos

Se comprobó:

- creación de migraciones;
- ejecución de migraciones;
- almacenamiento en SQLite;
- ausencia de migraciones pendientes.

### Django Admin

Se comprobó:

- visualización del modelo `Registro`;
- columnas personalizadas;
- buscador por nombre;
- filtros por resultado;
- filtro por estado de eliminación.

### CRUD

Se comprobó:

- creación de registros;
- visualización de registros;
- edición;
- recálculo del resultado;
- borrado lógico.

### Autenticación

Se comprobó:

- inicio de sesión;
- cierre de sesión;
- acceso solo para usuarios autenticados.

### Roles

Se probaron usuarios con diferentes permisos.

Se comprobó que `viewer` no pudiera crear.

También se comprobó que `normal` pudiera crear, pero recibiera `403 Forbidden` al intentar editar o eliminar mediante una URL directa.

---

## Conclusión sobre el uso de IA

La inteligencia artificial fue utilizada como una herramienta de apoyo durante el desarrollo de GeekMatch Trips.

Se utilizó principalmente para:

- resolver dudas;
- explicar conceptos de Django;
- proponer estructuras de código;
- revisar posibles errores;
- comprender migraciones;
- organizar el CRUD;
- implementar autenticación;
- comprender el uso de grupos y permisos.

Las propuestas fueron revisadas, adaptadas al proyecto y probadas manualmente antes de ser incorporadas.

El proyecto evolucionó desde una primera versión que almacenaba información en `datos.json` hacia una aplicación Django que utiliza SQLite, CRUD, borrado lógico, autenticación y control de acceso mediante roles.