*Esta herramienta digital forma parte del catálogo de herramientas del **Banco Interamericano de Desarrollo**. Puedes conocer más sobre la iniciativa del BID en [code.iadb.org](code.iadb.org)*

## *SmartReader*

### Descripción y contexto
---

*SmartReader* es una herramienta que utiliza técnicas de Procesamiento de Lenguaje Natural para proporcionar una nueva perspectiva a tu investigación (pregunta de investigación y literatura recopilada); esto lo hace a través de consultar a Google y recuperar información actualizada y relacionada con tu pregunta de investigación. *SmartReader* es una alternativa para hacerle frente a la necesidad que tienen los trabajadores de conocimiento de mantener el ritmo a la cantidad exponencial de información que se genera todos los días.

El Departamento de Conocimiento Innovación y Comunicación del Banco Interamericano de Desarrollo creó esta herramienta luego de reconocer esta necesidad además de querer explorar tecnologías como la Inteligencia Artificial y el Procesamiento del Lenguaje Natural para asistir en el proceso de Gestión del Conocimiento.

La herramienta consta de cuatro interfaces: 1) *Definición del modelo*, 2) *Estado del modelo*, 3) *Aplicación del modelo*, e 4) *Interfaz de resultados*. El siguiente diagrama de flujo explica el funcionamiento de la herramienta:


![flujograma_en](https://code.iadb.org/sites/default/files/inline-images/chart_es.png "Flow Chart SmartReader")

Como se muestra en la gráfica, de izquierda a derecha y de arriba a abajo, el proceso comienza cuando el usuario crea un modelo al ingresar un conjunto de temas y subtemas que son relevantes a una determinada pregunta de investigación. Con este conjunto de palabras, la herramienta generará cadenas de consulta utilizadas para recuperar los datos más relevantes disponibles en Google. Luego, al aplicar sklearn.TfidfVectorizer, se creará un modelo con términos ponderados. Posteriormente, se aplica un modelo al corpus de documentos que el usuario carga en un archivo comprimido de archivos .txt. El proceso ocurre al calificar los párrafos de cada documento, extraer sus entidades y ubicaciones correspondientes y ordenar estos párrafos en orden descendente. Después de elegir los párrafos con mayor calificación (se seleccionó un número aleatorio de 50 párrafos), la herramienta procederá a seleccionar las oraciones más relevantes. Los cálculos dará como resultado un archivo .json y la visualización de las palabras clave, entidades, ubicaciones y frases más relevantes de nuestro corpus de documentos. Para obtener más información sobre cómo contribuir a este proyecto, consulta la siguiente entrada en nuestro blog Abierto al Público.
 	
### Guía de instalación
---

#### Requerimientos mínimos del sistema
1.	El servidor deberá contar con al menos 20GB de espacio en disco y un RAM de 4GB. La herramienta ocupa un espacio de mínimo 3GB.
2.	Se recomienda una buena conexión a Internet, ya que una gran cantidad de datos se descargan durante la configuración del servidor.
3.	Recomendamos instalar la aplicación en una distribución de CentOS.

#### Instalación de Python (3.\*)
NOTA: asegúrese de estar usando python3
Primero compruebe si python3 ya está instalado en el servidor. Si no, siga los siguientes pasos:
```
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
```

#### Instalación de pip
```
sudo yum -y install python36u-pip
sudo pip install –upgrade pip
```
Confirme la instalación de con: `pip -V`

#### Instalación de MongoDB para el almacenamiento de datos:
1.	Navega a la carpeta madre (home)
2.	Haga clic [aquí](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-centos-7) para ver los pasos de instalación de MongoDB. Si el enlace no funciona, copia y pega la siguiente url en tu navegador https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-centos-7 

#### Clonar el Código desde un servidor remoto de git:
Clona el repositorio usando el comando: `git clone https://github.com/EL-BID/*SmartReader*.git`.

#### Crea un entorno:
1.	Crea una nueva carpeta para el proyecto y navega a esa carpeta
2.	Crea un entorno virtual e instala python3 en el entorno con el siguiente comando: `python3.6 -m venv my_env` (donde my_env es el nombre del entorno)
3.	Activa el entorno recién creado con el siguiente comando: `source my_env/bin/activate`  
4.	Para desactivar el entorno usa el siguiente comando: `deactivate`  

#### Installing dependencies:
1.	Activa el entorno que creaste en el paso anterior 
2.	Navega hacia la carpeta con la herramienta clonada 
3.	Instala la librería *enchant* con el siguiente comando `sudo yum install enchant`.
4.	Para instalar el resto de los paquetes deberás modificar tu configuración local usando la siguiente línea: `export LC_ALL=C`.
5.	Instala todas las librerías que están en el archivo “requirements.txt” usando el siguiente comando: `sudo pip install -r requirements.txt`.
6.	Descarga los datos en inglés de la librería *spacy* así:  `sudo python -m spacy download en`.
7.	La librería *nltk* deberá usarse utilizando python. Para esto, activa `python` en la línea de comandos.
8.	Importa *nltk* y descarga todos los datos usando los siguientes comandos:

```
>>> import nltk
>>> nltk.download('all')
```

### User Guide
---

#### Server Startup:
1.	Instala  *screen* con el siguiente comando: `sudo yum install screen`
2.	Crea una pantalla para el archivo principal usando el siguiente comando: `screen -S main`.
3.	Al iniciar el archivo principal podrás visualizar la interfaz de la aplicación. Para esto, ejecuta la siguiente línea: `python run.py`
4.	4.	Desconecta la pantalla con Ctrl + A y luego Ctrl + D. Para confirmar que la pantalla fue desconectada puedes enlistar todas las pantallas disponibles usando `screen -ls`. . La pantalla con nombre “main” deberá tener el estado de “Desconectado”.
5.	Now we create a screen for data collection processor. Repeat the steps to create a new screen by choosing an arbitrary name such as “data_collection_processor”. 
6.	Start the data collection file by typing `python processor.py`. Then detach this screen using the same method described above.
7.	Similarly create a new screen for the summary_processor which can be named “summary_processor” and run command `python summary_processor.py` and detach it.
8.	Check for all the running screen using `screen -ls`.
9.	The server is up and running now. To access the application in the server, browse “localhost:8080”. For remote access specify the public IP address along with the port.

### How to Contribute
---

This section explains to developers the most useful ways to send “pull requests”, how to declare any bugs found in the tool, and which style guides should be followed when contributing new lines of code.

### Code of Conduct 
---

The Code of Conduct establishes the social norms, rules, and responsibility that individuals and organizations are expected to follow when interacting in any way with the digital tool and its respective community. It is considered a best practice to actively encourage an environment of respect and inclusion for making contributions to the project. The Github platform awards and supports the repositories which provide this specific section. As soon as you create *CODE_OF_CONDUCT.md* you can access the specific recommended template created by Github. 

### Authors
---

BID

### Additional Information
---

Blog en Abierto al Público

### License 
---

The license specifies the permission and the conditions for use that the developer authorizes to others who wish to use or modify the digital tool.

Include a note in this section with the type of license that has been assigned to the digital tool. The text of this license should be included in a specific file named *LICENSE.md* or *LICENSE.txt* in the main folder.

If you are unsure about what kinds of licenses exist and which would be the best for your case, we recommend visiting the following page: https://choosealicense.com/.

### Limitation of responsibilities
---

The IDB is not responsible, under any circumstance, for damage or compensation, moral or patrimonial; direct or indirect; accessory or special; or by way of consequence, foreseen or unforeseen, that could arise:

i. Under any concept of intellectual property, negligence or detriment of another part theory;

ii. Following the use of the Digital Tool, including, but not limited to defects in the Digital Tool, or the loss or inaccuracy of data of any kind. The foregoing includes expenses or damages associated with communication failures and / or malfunctions of computers, linked to the use of the Digital Tool.

