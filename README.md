*Esta herramienta digital forma parte del catálogo de herramientas del **Banco Interamericano de Desarrollo**. Puedes conocer más sobre la iniciativa del BID en: [code.iadb.org](https://code.iadb.org/es)*

*Versión en inglés [aquí](https://github.com/EL-BID/SmartReader/blob/master/README-EN.md)*

## *SmartReader*

### Descripción y contexto
---

*SmartReader* es una herramienta que utiliza técnicas de Procesamiento de Lenguaje Natural para proporcionar una nueva perspectiva a tu investigación (pregunta de investigación y literatura recopilada). Esto lo hace a través de consultar a Google y recuperar información actualizada y relacionada con tu pregunta de investigación. *SmartReader* es una alternativa para hacerle frente a la necesidad que tienen los trabajadores de conocimiento de mantener el ritmo a la cantidad exponencial de información que se genera todos los días y que se comparte en el internet.

El Departamento de Conocimiento Innovación y Comunicación del **Banco Interamericano de Desarrollo** creó esta herramienta luego de reconocer esta necesidad además de querer explorar tecnologías como la Inteligencia Artificial y el Procesamiento del Lenguaje Natural para asistir en el proceso de Gestión del Conocimiento.

La herramienta consta de cuatro interfaces: 1) *Definición del modelo*, 2) *Estado del modelo*, 3) *Aplicación del modelo*, e 4) *Interfaz de resultados*. El siguiente diagrama de flujo explica el funcionamiento de la herramienta:


![flujograma_en](https://code.iadb.org/sites/default/files/inline-images/chart_es.png "Flow Chart SmartReader")  

<img   src="https://code.iadb.org/sites/default/files/inline-images/keys_es.png" 
alt="keys!" width="50%" style="float:right;"/>


Como se muestra en la gráfica, de izquierda a derecha y de arriba a abajo, el proceso comienza cuando el usuario crea un modelo al ingresar un conjunto de temas y subtemas que son relevantes a una determinada pregunta de investigación. Con este conjunto de palabras, la herramienta generará cadenas de consulta utilizadas para recuperar los datos más relevantes disponibles en Google. Luego, al aplicar *sklearn.TfidfVectorizer*, se creará un modelo con términos ponderados. Posteriormente, se aplica un modelo al corpus de documentos que el usuario carga en un archivo comprimido de archivos *.txt*. El proceso ocurre al calificar los párrafos de cada documento, extraer sus entidades y ubicaciones correspondientes y ordenar estos párrafos en orden descendente. Después de elegir los párrafos con mayor calificación (se seleccionó un número aleatorio de 50 párrafos), la herramienta procederá a seleccionar las oraciones más relevantes. Los cálculos dará como resultado un archivo *.json* y la visualización de las palabras clave, entidades, ubicaciones geográficas y frases más relevantes de nuestro corpus de documentos. Para obtener más información sobre cómo contribuir a este proyecto, consulta la [siguiente entrada](https://www.google.com/) en nuestro blog Abierto al Público.
 	
### Guía de instalación
---

#### Requerimientos mínimos del sistema
1.	El servidor deberá contar con al menos 20GB de espacio en disco y un RAM de 4GB. La herramienta ocupa un espacio de mínimo 3GB.
2.	Se recomienda una buena conexión a Internet dado que una gran cantidad de datos se descarga durante la configuración del servidor.
3.	Recomendamos instalar la aplicación en una distribución de CentOS.

#### Instalación de Python (3.\*)
NOTA: asegúrate de estar usando python3
Primero comprueba si python3 ya está instalado en el servidor. Caso contrario, sigue los siguientes pasos:
```
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
```

#### Instalación de pip
```
sudo yum -y install python36u-pip
sudo pip install –upgrade pip
```
Confirma la instalación con: `pip -V`

#### Instalación de MongoDB para el almacenamiento de datos:
1.	Navega a la carpeta madre (home)
2.	Haz clic [aquí](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-centos-7) para ver los pasos de instalación de MongoDB. Si el enlace no funciona, copia y pega la siguiente url en tu navegador https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-centos-7 

#### Clonar el Código desde un servidor remoto de git:
Clona el repositorio usando el comando: `git clone https://github.com/EL-BID/SmartReader.git`.

#### Crea un entorno:
1.	Crea una nueva carpeta para el proyecto y navega a esa carpeta
2.	Crea un entorno virtual e instala python3 en el entorno con el siguiente comando: `python3.6 -m venv my_env` (donde `my_env` es el nombre del entorno)
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
4.	Desconecta la pantalla con Ctrl + A y luego Ctrl + D. Para confirmar que la pantalla fue desconectada puedes enlistar todas las pantallas disponibles usando `screen -ls`. La pantalla con nombre “main” deberá tener el estado de “Desconectado”.
5.	Crea la pantalla que va a albergar el procesador de los datos. Repite los pasos para crear una nueva pantalla. Puedes elegir un nombre arbitrario como “data_collection_processor”. 
6.	Inicia el archivo para esta pantalla ejecutando: `python processor.py`. Luego desconecta esta pantalla usando el mismo método mencionado anteriormente.
7.	Finalmente, crea una pantalla para el proceso que llamaremos summary_processor y ejecuta el correspondiente archivo con esta línea: `python summary_processor.py`. Desconecta la pantalla.
8.	Chequea todas las pantallas en ejecución usando: `screen -ls`.
9.	El servidor estará funcionando. Para acceder a la aplicación, utilizando tu navegador de preferencia, navega a localhost:8080. Para acceso remoto, deberás especificar una IP pública como por ejemplo: http://127.0.0.1:8080

### Cómo funciona
---
1.	Ir a la pestaña "Model Definition" y crear un nombre aleatorio para el modelo.
2.	Pensar en una lista de tópicos y subtópicos que describan la pregunta de investigación sobre la que quieres trabajar. Por ejemplo con la pregunta: "How will technology impact the economy of the future?", se podría decir que dos ejemplos de sub-tópicos podrían ser 1)"Technology" y 2)"Economics". Asismismo las palabras claves que corresponden a estos subtópicos serían 1)"artificial intelligence, machine learning, natural language processing" y 2)"behavioral economics" respectivamente. Toma en cuenta que las palabras clave deben estar separadas por coma. Una vez creado el modelo, hacer click submit.
3.  Luego en la pestaña de "Model Status" podrás chequear el estado de la creación del modelo.
4.  En la pestaña de "Model Aplication" selecciona el modelo que acabaste de crear. Seguidamente carga una carpeta comprimida zip que contiene el corpus de tus documentos en formato .txt (hemos adjuntado una muestra). Finalmente, envía el formulario.
5.  En la pestaña "Results" es donde podrás descargarte los resúmenes y formato json y visualizar los resultados.

### Cómo contribuir
---

Hemos puesto a disposción el código de esta herramienta y nos encataría escuchar tu experiencia con ella. Para ver un listado de posibles mejoras que podrías hacer a *SmartReader* consulta la pestaña *Issues* de este repositorio y el [CONTRIBUTING.md](https://github.com/EL-BID/SmartReader/blob/master/CONTRIBUTING.md).  
Finalmente, te comentamos que escribimos una entrada sobre *SmartReader* en *Abierto al Público*. El enlace al blog está en la sección de [Información Adicional](#información-adicional) de este documento. ¡Quedamos atentos!


### Código de Conducta 
---

Puedes ver el código de conducta [aquí](https://github.com/EL-BID/SmartReader/blob/master/CODE-OF-CONDUCT.md)

### Autores
---
© 2017 Banco Interamericano de Desarrollo e Instituto para el Futuro.
Este software es el resultado de una asociación entre el Banco Interamericano de Desarrollo y el [Instituto para el Futuro](http://www.iftf.org/).
Los derechos de autor del software son compartidos por ambas organizaciones, incluso si el licenciante es únicamente el Banco Interamericano de Desarrollo.

Banco Interamericano de Desarrollo  
Involucrados:

- [Daniela Collaguazo](mailto:danielaco@iadb.org)
- [Kyle Strand](mailto:kyles@iadb.org)
- Seaford Bacchas

### Información Adicional
---

[Blog en Abierto al Público](https://blogs.iadb.org/abierto-al-publico/2018/09/07/smartreader-herramienta-de-analisis-de-texto/)

### Licencia
---

Puedes ver la licencia del código fuente [aquí](https://github.com/EL-BID/SmartReader/blob/master/LICENSE.md)

La Documentación de Soporte y Uso del software se encuentra licenciada bajo Creative Commons IGO 3.0 Atribución-NoComercial-SinObraDerivada (CC-IGO 3.0 BY-NC-ND)

## Limitación de responsabilidades
---

El BID no será responsable, bajo circunstancia alguna, de daño ni indemnización, moral o patrimonial; directo o indirecto; accesorio o especial; o por vía de consecuencia, previsto o imprevisto, que pudiese surgir:

i. Bajo cualquier teoría de responsabilidad, ya sea por contrato, infracción de derechos de propiedad intelectual, negligencia o bajo cualquier otra teoría; y/o

ii. A raíz del uso de la Herramienta Digital, incluyendo, pero sin limitación de potenciales defectos en la Herramienta Digital, o la pérdida o inexactitud de los datos de cualquier tipo. Lo anterior incluye los gastos o daños asociados a fallas de comunicación y/o fallas de funcionamiento de computadoras, vinculados con la utilización de la Herramienta Digital.
