<img  align="left" width="150" style="float: left;" src="https://www.upm.es/sfs/Rectorado/Gabinete%20del%20Rector/Logos/UPM/CEI/LOGOTIPO%20leyenda%20color%20JPG%20p.png">
<img  align="right" width="60" style="float: right;" src="http://www.dit.upm.es/figures/logos/ditupm-big.gif">


<br/><br/>


# Práctica ODM con PYTHON-FLASK y MONGOENGINE

## 1. Objetivo

- Desarrollar las 4 operaciones CRUD (Create, Read, Update and Delete) a través de un ODM
- Practicar con un ODM para realizar queries
- Afianzar las ventajas de usar ODMs en el desarrollo de aplicaciones
- Realizar consultas semánticas usando SPARQL

## 2. Dependencias

Para realizar la práctica el alumno deberá tener instalado en su ordenador:
- Herramienta GIT para gestión de repositorios [Github](https://git-scm.com/downloads)
- Entorno de ejecución de Python 3 [Python](https://www.python.org/downloads/)
- Base de datos MongoDB [MongoDB](https://www.mongodb.com/try/download/community)
- Base de datos [Fuseki](https://jena.apache.org/documentation/fuseki2/)

## 3. Descripción de la práctica

La práctica simula una aplicación de gestión de pacientes basada en el patron MVC (Modelo-Vista-Controlador) utlizando la librería Flask de python. La práctica tambien usa MongoEngine como ODM para poder almacenar los datos de la aplicación en MongoDB.

La **vista** es una interfaz web basada en HTML y CSS que permite realizar diversas acciones sobre los pacientes como crear, editar, buscar, filtrar, listar o eliminar. La vista esta incluida ya en el codigo descargado.

El **modelo** es la representación de la información de los pacientes. En esta aplicación se van a usar tres modelos: doctor, hospital y patient. Un ejemplo de como están definidos los modelos en esta práctica es el siguiente (la definición de todos los modelos se encuentra en `models.py`):

```
class Patient(db.Document):
    id = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    surname = db.StringField(required=True)
    dni = db.StringField(required=True)
    hospital = db.ReferenceField(Hospital)
    doctors = db.ListField(db.ReferenceField("Doctor")) 
```
Por sencillez se ha relacionado el paciente con el hospital y con el doctor. Y el doctor no tiene relación con el hospital más que a través de sus pacientes. Es decir en este modelo de uso el doctor puede atender en cualquier hospital. Es el paciente el que se asigna a un hospital (el que le corresponda por ejemplo por distrito) y luego se le asigna cualquier doctor.

El **controlador** ejecuta acciones sobre los modelos. El alumno deberá desarrollar varias funciones del controlador para que las acciones que se realicen a través de la página web funcionen correctamente. Para ello, desarrollara las operaciones correspondientes con MongoEngine implementando las operaciones CRUD sobre los objetos patiente, hospital y doctor, así como otra serie de queries.

En el siguiente video puede observar cuál sería el funcionamiento normal de la aplicación [link](https://youtu.be/8xXaFCRxMXE)

## 4. Descargar e instalar el código del proyecto

Abra un terminal en su ordenador y siga los siguientes pasos.

Clone el repositoro de GitHub
```
git clone https://github.com/BBDD-ETSIT/MASTER_PRACTICA_ODM_PYTHON.git
```

Navegue a través de un terminal a la carpeta MASTER_PRACTICA_ODM_PYTHON.
```
> cd MASTER_PRACTICA_ODM_PYTHON
```

Una vez dentro de la carpeta, se instalan las dependencias. Para ello debe crear un virtual environment de la siguiente manera:

```
[LINUX/MAC] > python3 -m venv venv
[WINDOWS] > py.exe -m venv env
```

Si no tiene instalado venv, Lo puede instalar de la siguiente manera:

```
[LINUX/MAC] > python3 -m pip install --user virtualenv
[WINDOWS] > py.exe -m pip install --user virtualenv
```

Una vez creado el virtual environment lo activamos para poder instalar las dependencias:

```
[LINUX/MAC] > source venv/bin/activate
[WINDOWS] > .\env\Scripts\activate
```

Instalamos las dependencias con pip:

```
> pip3 install -r flaskr/requirements.txt 
```

Indicamos a Flask el fichero con el que arrancar el servidor:

```
[LINUX/MAC] >  export FLASK_APP=flaskr/run.py
[WINDOWS] > $env:FLASK_APP = "flaskr/run.py"
```
Debemos tener arrancado MongoDB. Dependiendo de cómo lo hayamos instalado arrancará solo al iniciar la máquina o tendremos que ir a ejecutar el programa "mongod" a la carpeta bin donde hayamos realizado la instalación.

Podemos arrancar el servidor con el siguiente comando. Hasta que no realize el primer ejercicio sobre la configuración de la URI, el servidor no arrancara.

```
$ flask run
```


Abra un navegador y vaya a la url "http://localhost:5000" para ver la aplicación de gestión de pacientes.

Si necesita arrancar la aplicación en un puerto diferente al predeterminado puede usar el sigiuente comando (reemplazando el 5002 por el puerto correspondiente):

```
flask run --port=5002
```

**NOTA: Cada vez que se quiera realizar una prueba del código desarrollado, debemos parar y arrancar de nuevo la practica. Para ello, desde el terminal pulse ctrl+c para parar y arranque de nuevo con flask run**

**NOTA2: Si ha modificado algun documento de manera indeseada y se quiere volver a restablecer los valores por defecto, borre la base de datos que ha creado y vuelva a arrancar el servidor con flask.**

## 5. Tareas a realizar

La primera tarea es inspeccionar todo el código provisto y entender donde están los modelos, las vistas y los controladores, asi como la semilla o seeders.



### 5.1 Conectar a la base de datos adecuada y añadir en el seed un nuevo médico
 Primero hay que conseguir conectar a la base de datos, deberá definir la URI de Conexión a la base de datos con nombre **hospitales_NOMBREALUMNO** por ejemplo para Enrique Barra la base de datos se llamaría **hospitales_Enrique**

 Diríjase al fichero db.py e identifique las siguientes líneas y añada la infomación correspondiente para conectarse a la base de datos (una vez completada la información se deben borrar los <>)

```
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "<nombre_bddd>",
        "host": "<nombre_host>",
        "port": <27017>,
        "alias": "default",
    }
]
```
En este punto podremos comprobar que la aplicación funciona con 
```
$ flask run
```
Al hacer esto veremos que nos llena la base de datos con los seed (semilla), que son los datos iniciales de la aplicación. 
Una vez hecho esto tendremos que entrar con mongosh y borrar la base de datos **hospitales_NOMBREALUMNO**, para que así podamos hacer el siguiente paso, que es añadir datos al seed y que al arrancar la aplicación los cree porque detectará que no existe la base de datos (ver primeras líneas del método seeder de `flaksr/run.py`)

En este momento tendremos que editar el fichero `flaksr/seeders/seeders.json` y añadir un nuevo doctor con nuestros datos, nos inventamos el id y la especialidad. 
Una vez hecho esto al volver a arrancar la aplicación con "flask run" cargará este nuevo doctor en la base de datos con el seeder.
En este momento accedemos a la base de datos con mongosh y hacemos una query para buscar este nuevo doctor. Y hacemos una captura de pantalla (CAPTURA1) donde se vean sus datos en la mongo shell.


### 5.2 Rellenar las funciones del controlador que atacan a la base de datos usando los modelos

Se provee un esqueleto con todas los funciones que deberá rellenar. El alumno deberá editar el fichero `flaksr/controllers/patientController.py`.
En cada una de estas funciones se deberá hacer uso del ODM MongoEngine para realizar operaciones con la base de datos y devolver un resultado de la operación.


Las funciones son las siguientes:

### show_hospitals()

**Descripción:** Busca en la base de datos todos los hospitales existentes en la coleccion "Hospital"

**Parametros:** Ninguno

**Returns:** Un array de objetos de hospitales

### filterHospitalsByCity(city)

**Descripción:** 

- Busca en la colección "Hospital" filtrando por ciudad
- Para acceder a la ciudad debe usar :

**Parametros:** city - Nombre de la ciudad

**Returns:** Un array de objetos de hospitales

### list_hospital_patients(hospital_id)

**Descripción:** Busca todos los pacientes correspondientes a un hospital ordenados por el nombre (de la A a la Z)

**Parametros:** hospital_id - Id del hospital

**Returns:** Un array de objetos de pacientes

### read_patient(patient_id)

**Descripción:** Busca los datos de un paciente

**Parametros:**

- patient_id - Id del paciente a actualizar

**Returns:** Un objeto paciente

### create_patient(hospital_id, body)

**Descripción:** Crea un paciente dentro de un hospital

**Parametros:** 
- hospital_id - Id del hospital
- body - Objeto json con todos los datos del formulario de crear paciente (name, surname, dni)

Para acceder a cada una de los valores del formulario usar:
```
body["name"]
```
- id - id del Paciente, debe generarse con:
```
id = uuid.uuid4()
```
**Returns:** El objeto paciente creado

### update_patient(patient_id, body)

**Descripción:** Actualiza los datos del paciente identificado por patient_id

**Parametros:**

- patient_id - Id del paciente
- body - Objeto json con todos los datos del formulario de crear paciente (name, surname, dni)


**Returns:** El objeto paciente actualizado

### delete_patient(patient_id)

**Descripción:** Borra un paciente de la base de datos

**Parametros:** patient_id - Id del paciente

**Returns:** El resultado de la operación de borrado

### assignDoctor(patient_id, doctor_id)

**Descripción:**

- Asigna un medico a un paciente en la base de datos.

**Parametros:**

- patient_id - Id del paciente
- doctor_id - Id del doctor

**Returns:** Devuelve los datos del paciente al que se le ha asignado el medico

### show_patient_doctors(patient_id)

**Descripción:** Devuelve los doctores que estan asignados a un paciente.

**Parametros:**

- patient_id - Id del paciente

**Returns:** Un array de objetos de doctores 

### show_hospital(hospital_id)

Esta función será la encargada de mostrar información sobre un hospital en particular.
A diferencia del resto de apartados, en este caso la información se conseguirá de una fuente semántica: DBpedia.

Para ello, primero deberá recuperar el hospital (usando el ODM), para de esa forma acceder a su IRI.
Mediante la función `sparql` (importada de `models`), debe realizar una consulta SPARQL a DBpedia, conteniendo al menos:

- La página web del hospital (en la variable `?homepage`)
- La descripción del hospital en español (en la variable `?descripcion`)
- El nombre del hospital en español (variable `?nombre`)
- Número de camas en el hospital (en la variable `?camas`), debe tener un valor en blanco si no se encuentra

Adicionalmente, se puede añadir más información, tal como el código postal, la región de referencia, o el número de habitantes de la ciudad en la que se encuentra el hospital.

Se proporciona una consulta de prueba en la que se muestra el nombre (etiqueta) del hospital, y que deberá modificar.



### 5.3 Añadir un campo nuevo al modelo paciente y usarlo al asignar doctor

En este momento queremos añadir un campo tipo booleano al modelo paciente, el campo se llama `premium` y tiene que ser `db.BooleanField()` (no ponga required=True porque los pacientes existentes no tienen este campo).

- Edite `flaskr/models.py` para añadir este campo.

- Compruebe el contenido de `flaskr/templates/show.html` y vea que sobre la línea 90 hay una condición que si el paciente tiene el campo premium a true muestra dicha información.

- Edite `flaksr/controllers/patientController.py` para que cuando el doctor asignado es el nuevo que añadimos en el seed ponga el campo premium a true (y por lo tanto al visualizar el paciente saldrá la fila adecuada). 

En este punto hay que realizar una captura de pantalla (CAPTURA2) donde se muestre que en primer lugar ha añadido un paciente nuevo inventado por usted, con datos inventados, le asigna el doctor que añadió al seeder y muestra el paciente.

## 6. Almacenar los datos de DBpedia

En la última función de la tarea 5.2, estamos consultando DBpedia, un servicio externo.
Para evitar que nuestra aplicación deje de funcionar si el servicio deja de estar disponible, vamos a descargar los datos en un grafo, que posteriormente podremos cargar en nuestra base de datos Fuseki.
También adaptaremos el código para que la consulta se realice a nuestro servidor, en lugar de a DBpedia.

Para ello, debemos seguir los siguientes pasos:

* Descargar la información necesaria sobre los hospitales desde DBpedia. La descarga se puede realizar desde la página de DBpedia de cada hospital.
* Exportar toda la información descargada en un solo fichero en formato Turtle, `hospitales.ttl`.

El fichero resultante (`hospitales.ttl`) se subirá a la tarea de Moodle.

Finalmente, se comprobará que la información descargada es correcta siguiendo estos pasos:

* Lanzar una instancia local de Fuseki, usando la versión standalone o la imagen de docker (ver transparencias).
* Crear un dataset nuevo en la instancia local (p.e., `hospitales`).
* Cargar la información descargada en la instancia local de Fuseki.
* En este punto, realizar una captura de pantalla (CAPTURA3) mostrando la página del dataset creado, y el número de triplas contenidas
* Modificar la llamada a `sparql` dentro de `run.py` para que use el endpoint de la instancia local (p.e. `sparql(query=query, endpoint='http://localhost:3000/hospitales/sparql')`.
* Comprobar que las consultas siguen funcionando correctamente (es decir, la página se muestra igual que apuntando a DBpedia directamente)

Una vez realizado estos pasos, se  añadirá el fichero CAPTURA3 a la entrega de moodle.

## 7. Instrucciones para la Entrega y Evaluación.

NOTA: Se han includo una suite de tests para determinar si se han implementado de forma correcta cada una de las funciones y obtener una nota orientativa de acuerdo a la rúbrica. Para poder ejecutar los tests debe ejecutar el siguiente comando:

```
python -m pytest -v --disable-warnings
```
Y obtendrá una salida similar a la siguiente:

```
================================== test session starts ===================================
platform darwin -- Python 3.11.3, pytest-7.4.2, pluggy-1.3.0 -- /Users/admin/PX_ODM_FLASK/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/admin/PX_ODM_FLASK
plugins: harvest-1.10.4, mocha-0.4.0
collected 11 items                                                                       

flaskr/tests/test_check.py::test_list_hospitals PASSED                             [  9%]
flaskr/tests/test_check.py::test_filterHospitalsByCity PASSED                      [ 18%]
flaskr/tests/test_check.py::test_list_hospital_patients PASSED                     [ 27%]
flaskr/tests/test_check.py::test_show_hospital PASSED                              [ 36%]
flaskr/tests/test_check.py::test_read_patient PASSED                               [ 45%]
flaskr/tests/test_check.py::test_create_patient PASSED                             [ 54%]
flaskr/tests/test_check.py::test_update_patient PASSED                             [ 63%]
flaskr/tests/test_check.py::test_delete_patient PASSED                             [ 72%]
flaskr/tests/test_check.py::test_assign_doctor PASSED                              [ 81%]
flaskr/tests/test_check.py::test_show_patient_doctors PASSED                       [ 90%]
flaskr/tests/test_check.py::test_show_score 

La nota orientativa obtenida en la práctica es:


-----------------
| Score: 9.5 /9.5|
-----------------

PASSED                                 [100%]

============================ 11 passed, 47 warnings in 1.08s =============================

```

El alumno deberá subir a Moodle las **capturas** solicitadas y los ficheros *patientController.py*, *seeders.json* y *models.py* con las modificaciones realizadas, además del fichero `hospitales.ttl` (en total 7 ficheros incluyendo las capturas). 

**RÚBRICA**: Cada método que se pide resolver de la practica se puntuara de la siguiente manera:
-  **0.5 puntos por añadir en el seeder el doctor con sus datos personales y conectar a la base de datos con su nombre.**
-  **0.5 puntos por cada uno de las siguientes funciones realizadas:**  `list_hospitals`, `filterHospitalsByCity`, `list_hospital_patients`, `read`, `showPatientDoctors` y `delete`.
-  **1 puntos por cada uno de las siguientes funciones realizadas:**  `create_patient` y `update_patient`
-  **2 puntos por la función `assignDoctor` con la funcionalidad requerida en el punto 5.2**
-  **1.5 puntos** por la función `show_hospital`.
-  **1 punto** por capturar la información adecuada en el fichero `hospitales.ttl`.
