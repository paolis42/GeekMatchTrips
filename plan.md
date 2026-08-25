# GeekMatch Trips

## 1. NEGOCIO

### Problema

Al planificar un viaje, las personas pueden encontrar muchos lugares y actividades interesantes, pero no siempre es fácil decidir cuáles conviene incluir considerando sus gustos y el presupuesto disponible.

La información suele estar distribuida en diferentes sitios, lo que puede dificultar la organización y hacer que el viajero priorice actividades que no se ajustan realmente a sus intereses o presupuesto.

### Solución

GeekMatch Trips busca apoyar la planificación de viajes personalizados.

En esta primera versión, el programa evaluará un lugar turístico a la vez según el nivel de interés del usuario, el precio del lugar y su presupuesto disponible. Como resultado, indicará si el lugar es recomendado o no y explicará el motivo de la decisión.

### Alcance

En esta versión se podrá:

* Ingresar información de un lugar.
* Evaluar si conviene incluirlo en el viaje.
* Mostrar el motivo de la decisión.
* Guardar las evaluaciones en un archivo JSON.
* Mostrar un resumen de los lugares evaluados.

El proyecto completo de GeekMatch Trips contempla a futuro la generación de itinerarios reales, horarios, reservas, entradas oficiales, comidas, descansos, tiempos de traslado, mapas y otras preferencias del viajero.

Estas funciones no se implementarán durante esta primera versión.

### MoSCoW

#### Must

1. Solicitar los datos necesarios para evaluar un lugar.
2. Decidir si el lugar es recomendado utilizando el interés, precio y presupuesto.
3. Mostrar el resultado y el motivo de la decisión.
4. Guardar cada evaluación en `datos.json`.
5. Mostrar las evaluaciones guardadas en una tabla.

#### Should

* Informar si una actividad es gratuita o pagada.
* Informar si necesita reserva o tiene distintas formas de acceso.
* Incorporar categorías de intereses del viajero.
* Mostrar información sobre cuándo conviene reservar.

#### Could

* Generar un itinerario completo por días y horarios.
* Considerar desayuno, almuerzo, once y cena.
* Agregar pausas breves de descanso.
* Considerar tiempos de traslado.
* Personalizar el ritmo del viaje.
* Incorporar mapas.
* Mostrar páginas oficiales para comprar entradas o realizar reservas.

#### Won't

* Base de datos en esta versión.
* Inicio de sesión.
* API o MCP.
* Compra directa de entradas.
* Pagos dentro de la aplicación.
* Generación automática del viaje completo.

---

## 2. TÉCNICO

### Datos de entrada

El programa solicitará:

* `nombre_lugar`: texto (`str`).
* `nivel_interes`: número entero (`int`) entre 1 y 5.
* `precio`: número entero (`int`).
* `presupuesto`: número entero (`int`).

### Regla de decisión

El programa tendrá cuatro resultados posibles:

#### 1. Dato inválido

Ocurre si:

* el nivel de interés es menor que 1 o mayor que 5;
* el precio es negativo;
* o el presupuesto es negativo.

Resultado:

**Dato inválido. Revisa la información ingresada.**

#### 2. Recomendado

Ocurre cuando:

* el nivel de interés es igual o mayor a 4;
* y el precio es menor o igual al presupuesto disponible.

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

### Paquete externo

Se utilizará el paquete `tabulate` para mostrar en consola una tabla ordenada con los lugares evaluados y sus resultados.

Los registros serán almacenados en el archivo `datos.json`.

### Pantalla web

Se utilizará Django para mostrar los datos almacenados en `datos.json`.

La dirección de la página será:

`/resumen/`

La pantalla mostrará los lugares evaluados, nivel de interés, precio, presupuesto y resultado obtenido.

Esta primera versión utilizará una sola vista Django y no utilizará base de datos.
