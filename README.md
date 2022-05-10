# Houm Backend Tech Lead Challenge

## 1. Problema

### 1.1 Requisitos

Crear un servicio REST que:

- Permita que la aplicación móvil mande las coordenadas del Houmer
- Para un día retorne todas las coordenadas de las propiedades que visitó y cuánto tiempo se quedó en cada una
- Para un día retorne todos los momentos en que el houmer se trasladó con una velocidad superior a cierto parámetro

### 1.2 Observaciones

- El lenguaje de programación debe ser Python
- La solución debe ser de calidad de producción
- Incluir instrucciones de cómo ejecutar el código localmente
- Cualquier supuesto que se haya realizado tiene que ser documentado y justificado
- Tienes 5 días para entregar tu respuesta

## 2. Solución implementada

### 2.1. Supuestos de la solución
- Cada Houmer tiene una aplicación encargada de autenticarlo y enviar periodicamente su ubicación
- Existe un Api Gateway entre la aplicación y los servicios aquí implementados que se encarga de autenticar los requests
- Existe una DB con la información de los Houmers y las Propiedades a visitar, la cual se extenderá para almacenar los datos de ubicación.
- Una Visita es un periodo de tiempo en el cual el Houmer permanece al menos 5 minutos en un lugar cuyas coordenadas coinciden con las de una propiedad.
- Un Movimiento es el periodo de tiempo en el que un Houmer se desplaza entre dos visitas consecutivas.
- La distancia recorrida en un movimiento es la distancia entre el punto inicial y el punto final.
- El sistema de posicionamiento es "ideal". Para más simplicidad en el cálculo, se asume que cuando un Houmer se encuentra en una propiedad, las coordenadas de ambos serán idénticas. También se asume que mientras el Houmer no se mueva, su posición será constante.


### 2.2. Diseño de la solución
- La solución implementada consta de **3 microservicios, una cola de trabajo y una base de datos relacional**.
- El microservicio **Location** recibe los requests enviados periódicamente por la aplicación de los Houmers y los encola en la cola de trabajo.
- El microservicio **ETL** escucha los mensajes de la cola de trabajo, procesa los datos enviados por la aplicación y los persiste en la base de datos.
- El microservicio **Query** ejecuta las consultas sobre las visitas y los movimientos de los Houmers a partir de la información contenida en la base de datos.

#### 2.2.1. Diagrama del sistema
![Diagrama del sistema]("diagram.png")

#### 2.2.2. Justificación del diseño
- Dependiendo de la cantidad de Houmers activos, la cantidad de llamadas al endpoint que recibe sus ubicaciones puede ser muy grande. Al mover el trabajo de procesar e insertar los datos en la DB a una cola de trabajo, se disminuye el costo en tiempo y recursos de cada request, disminuyendo las probabilidades de que estos terminen en un timeout.
- Tener el procesamiento de datos en un pipeline de ETL dedicado permite realizar operaciones de mayor costo sin ralentizar el funcionamiento del resto del sistema. Además, se puede extender fácilmente para almacenar los datos de ubicación en un data warehouse, audit log, etc., aplicar transformaciones más complejas, pre-calcular respuestas, etc.
- Al tener los endpoints de escritura y lectura separados en dos microservicios distintos (Location y Query, respectivamente), podemos escalar ambos independientemente según sus propios requerimientos. Es decir, no necesitamos escalar los recursos destinados a las operaciones de consulta cuando hay muchos Houmers enviando su ubicación, ni tampoco le quitamos recursos valiosos al servicio de escritura cuando se hacen muchas consultas de visitas y movimientos.
- Además, se aumenta la independencia de los componentes del sistema, ya que al servicio de escritura no le importa (ni conoce) el estado de la base de datos, y el servicio de lectura tampoco necesita la cola de trabajos para funcionar.

### 2.3. Documentación de la API

Los microservicios **Location** y **Query** exponen la documentación de sus APIs en http://localhost:8081/docs y http://localhost:8082/docs respectivamente

## 3. Instrucciones

### 3.1 Setup

El setup consiste en la inicialización de la base de datos. El directorio **setup** implementa un contenedor que define los modelos **User**, **Property** y **Location**, crea las tablas respectivas, e inserta datos de prueba.

Para ejecutar la inicialización, primero se debe crear un archivo `.env` a partir del template `.env.template`. Una vez creado, se pueden cambiar los valores por defecto por el valor que se desee utilizar

```sh
cp .env.template .env
```

Una vez creado y llenado el archivo, se deben ejecutar los siguientes comandos. Estos crearán el contenedor y ejecutarán el script que llenará la base de datos.
```
docker compose -f docker-compose.setup.yaml build setup
docker compose -f docker-compose.setup.yaml up setup
```

Una vez completado el script, podemos eliminar el contenedor de setup con el siguiente comando:
```
docker compose -f docker-compose.setup.yaml down
```

### 3.2 Ejecución

Para levantar el sistema, una vez realizado el setup, basta ejecutar el comando `docker compose up`


## 4. Posibles mejoras

- Uso de postgis en la base de datos para el manejo de coordenadas y el cálculo de distancias
- Agregar márgenes de tolerancia a las consultas que utilizan las coordenadas (por ejemplo, considerar que un Houmer se encuentra en una propiedad si está ubicado a menos de X metros de distancia de dicha propiedad)
- Cálculo de distancia de ruta.
- Un cuarto microservicio que actúe de intermediario entre la base de datos y los otros microservicios (Para mantener la definición de los modelos y tablas en un único lugar)
- Tests. Los microservicios tienen abstracciones implementadas para facilitar la generación de mocks en los tests, pero éstos no se pudieron implementar por falta de tiempo.
- Hacer más robusta la conexión a la DB y a la cola de trabajos (manejar desconexiones, reconexiones, reintentos, etc.)
