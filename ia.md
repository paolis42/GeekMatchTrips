## Trabajo realizado personalmente

Durante el desarrollo fui creando y ejecutando el proyecto desde Visual Studio Code, realizando las pruebas de consola y web de forma manual.

Entre las tareas realizadas estuvieron:

- creación y organización de los archivos del proyecto;
- pruebas de los cuatro resultados del programa;
- instalación y prueba de `tabulate`;
- comprobación de los registros de `datos.json`;
- creación del entorno virtual;
- instalación de Django;
- creación de la aplicación `core`;
- prueba de la ruta `/resumen/`;
- configuración de `.env` y `.gitignore`;
- creación y actualización del repositorio GitHub.

## Decisiones y correcciones realizadas por mí

Durante el desarrollo utilicé la IA principalmente como apoyo para resolver dudas y revisar partes del código, pero fui probando y ajustando personalmente el funcionamiento del proyecto.

Una de las primeras decisiones fue mantener el alcance de esta entrega enfocado en el MVP. GeekMatch Trips es una idea más amplia que contempla itinerarios completos, reservas, horarios, descansos y otras funciones, pero decidí implementar solamente las funciones necesarias para esta evaluación y dejar las demás como desarrollo futuro en el MoSCoW.

Realicé manualmente las pruebas de los cuatro resultados definidos para la regla de decisión:

- Recomendado.
- No recomendado por presupuesto.
- No recomendado por baja afinidad.
- Dato inválido.

Durante estas pruebas detecté que al escribir valores como `40.000` en un campo convertido mediante `int()` el programa generaba un error. Después de revisar el problema comprendí que `int()` esperaba un número sin separadores de miles, por lo que para esta versión decidí solicitar valores como `40000`.

También revisé y corregí la indentación del código al incorporar el almacenamiento JSON. Inicialmente algunas instrucciones relacionadas con `registro` y `registros` podían quedar dentro de una condición, lo que habría impedido que se ejecutaran para todos los resultados. La estructura final quedó fuera de los bloques `if`, `elif` y `else`.

Probé personalmente que `datos.json` no reemplazara las evaluaciones anteriores, sino que agregara nuevos lugares al historial.

GitHub Copilot sugirió utilizar más funciones, `try/except` y validaciones adicionales. Decidí no incorporar todas esas sugerencias porque agregaban complejidad que no era necesaria para el MVP solicitado en esta evaluación.

Posteriormente se reorganizó la regla de decisión dentro de la función `decidir()`. Revisé que el programa de consola siguiera funcionando después de este cambio y que Django pudiera reutilizar la misma regla sin duplicar los `if`, `elif` y `else`.

También realicé manualmente la configuración del entorno virtual, la instalación de las dependencias, el archivo `requirements.txt` y las pruebas del servidor Django.

Durante la configuración de Django comprobé desde el navegador que la ruta `/resumen/` mostrara correctamente los registros almacenados en `datos.json` y que al enviar un nuevo lugar desde el formulario este quedara agregado al historial.

Finalmente configuré `.env` para sacar la `SECRET_KEY` de `settings.py`, manteniendo este archivo fuera del repositorio mediante `.gitignore`, y creé `.env.example` sin incluir información privada.

La IA fue utilizada como herramienta de consulta, explicación y revisión, pero el programa fue probado durante cada etapa y las decisiones sobre el alcance y las funciones que finalmente quedaron en el proyecto fueron tomadas de acuerdo con los requisitos de la evaluación.