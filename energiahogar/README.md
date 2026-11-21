# EnergiaHogar

## 1. Presentacion del proyecto

EnergiaHogar es una aplicacion web que estima el consumo electrico mensual de los equipos de un hogar, calcula su costo y simula cuanto se ahorraria al reducir el tiempo de uso.

**Problema que resuelve:** muchas personas no saben que equipos pesan mas en su factura de energia ni cuanto ahorrarian cambiando sus habitos.

**Funcionalidad principal:** el usuario ingresa equipos (nombre, potencia en W y horas de uso diario), la tarifa por kWh y un porcentaje de reduccion. La aplicacion devuelve el consumo y costo mensual, el aporte de cada equipo, el mayor consumidor y el ahorro del escenario simulado.

## 2. Tecnologias utilizadas

| Tecnologia | Funcion | Motivo |
|---|---|---|
| Python | Lenguaje de la logica de calculo | Requisito del curso y claridad para operaciones numericas |
| FastAPI | Rutas, recepcion de formularios y respuestas | Framework moderno, rapido y facil de probar |
| Jinja2 | Plantillas HTML dinamicas | Permite mostrar resultados sin JavaScript pesado |
| python-multipart | Lectura de formularios HTML en FastAPI | Necesario para `Form` |
| Uvicorn | Servidor de desarrollo | Servidor ASGI estandar para FastAPI |
| pytest + httpx | Pruebas automatizadas con `TestClient` | Requisito del curso |

## 3. Arquitectura y organizacion

```
energiahogar/
  app/
    main.py            rutas de FastAPI
    logic.py           validacion y calculos
    templates/
      base.html        diseno comun
      index.html       formulario
      resultado.html   resultados
  tests/
    test_app.py        pruebas con pytest
  requirements.txt
  pytest.ini
  README.md
```

- Las rutas estan en `app/main.py` (`GET /` y `POST /analizar`).
- La logica esta en `app/logic.py`, separada de la web, por lo que se puede probar sin servidor.
- Las plantillas heredan de `base.html` y reciben el diccionario de resultados desde la ruta.

## 4. Funcionamiento de la aplicacion

1. El usuario llena el formulario en `/` y lo envia por POST a `/analizar`.
2. FastAPI recibe las listas de nombres, potencias y horas, mas la tarifa y la reduccion.
3. `logic.py` convierte y valida los datos, calcula `kWh = W x horas x 30 / 1000`, ordena los equipos por consumo y simula el escenario de ahorro.
4. FastAPI entrega el resultado a `resultado.html`, donde Jinja2 genera la tabla, las barras de participacion y el resumen.
5. Si hay datos incorrectos (texto en vez de numero, potencia menor o igual a cero, horas fuera de 0 a 24, tarifa invalida o formulario vacio), se lanza `EntradaInvalida`; la ruta responde con codigo 400 y muestra el mensaje en el formulario.

## 5. Instalacion y ejecucion

Requisitos: Python 3.10 o superior.

```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abrir `http://127.0.0.1:8000` en el navegador. Agregar los equipos, escribir la tarifa por kWh (por ejemplo 800), elegir el porcentaje de reduccion y pulsar **Analizar consumo**.

## 6. Pruebas automatizadas

Ejecutar desde la raiz del proyecto:

```bash
pytest -v
```

| Prueba | Que comprueba | Datos | Esperado | Obtenido | Exito |
|---|---|---|---|---|---|
| test_consumo_mensual_kwh | Formula de consumo | 100 W, 5 h | 15.0 kWh | 15.0 kWh | Si |
| test_analizar_totales_y_ahorro | Funcionalidad principal | Nevera 150 W 24 h, TV 100 W 5 h, tarifa 800, reduccion 10% | 123 kWh, 98400 de costo, ahorro 9840 | Igual | Si |
| test_ruta_inicio_responde | Ruta GET / | Peticion simple | Codigo 200 y titulo | Igual | Si |
| test_ruta_analizar_muestra_resultado | Ruta POST /analizar | Formulario valido | Codigo 200, "Nevera" y "123.00 kWh" en la pagina | Igual | Si |
| test_potencia_negativa_devuelve_error | Entrada invalida | Potencia -5 | Codigo 400 con mensaje | Igual | Si |
| test_horas_fuera_de_rango | Caso limite | 30 horas | Codigo 400 | Igual | Si |
| test_tarifa_invalida_lanza_excepcion | Validacion en la logica | Tarifa 0 | `EntradaInvalida` | Igual | Si |

Resultado de la ejecucion: 7 pruebas aprobadas.

## 7. Evidencias de funcionamiento

**Interfaz principal**

![Interfaz principal](evidencias/interfaz.png)

**Aplicacion en ejecucion (formulario con datos)**

![Formulario](evidencias/formulario.png)

**Resultado del procesamiento**

![Resultado](evidencias/resultado.png)

**Manejo de una entrada invalida (potencia negativa)**

![Validacion](evidencias/validacion.png)

**Ejecucion de las pruebas con pytest**

![pytest](evidencias/pytest.png)

## 8. Conclusiones

El principal reto fue mantener la logica independiente de la capa web para poder probarla directamente y, ademas, probar las rutas con `TestClient`. Separar las excepciones propias del calculo del manejo de errores HTTP permitio mostrar mensajes claros en la plantilla. Se aprendio como FastAPI recibe formularios con campos repetidos, como Jinja2 reutiliza un diseno base y como pytest verifica tanto funciones como rutas completas.
