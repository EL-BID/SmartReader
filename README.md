*Esta herramienta digital forma parte del catálogo de herramientas del **Banco Interamericano de Desarrollo**. Puedes conocer más sobre la iniciativa del BID en [code.iadb.org](code.iadb.org)*

## Smart Reader

### Descripción y contexto
---

AI Research helper is a tool that uses NLP techniques to give you a fresh insight of your research (research question and literature) by querying Google and retrieving related up-to-date information. It was created to tackle the challenge that knowledge workers experience when coping with the exponential amount of information generated every day. 


The Knowledge Innovation and Communication Department of the Inter-American Development Bank created this tool after acknowledging this need and the latency of technologies such as Artificial Intelligence and Natural language Processing, to assist the Knowledge creation process.  


The tool comprises four interfaces: 1) Model Definition, 2) Model Status, 3) Model Application, and 4) Results interfaces. The following flow chart explain the mechanics of the tool.  

![flujograma](https://code.iadb.org/sites/default/files/inline-images/flujograma.jpg "Logo Title Text 1")

As depicted in the chart, from left to right and from top to bottom, the process starts with the user creating a model by entering a set of topic and subtopics that match a determined research question. Afterwards, the model will generate query strings used to retrieve the most relevant data available online, this means querying Google. Afterwards, by applying the sklearn.TfidfVectorizer, a model with weighted terms will be created. In the Model Application interface, a model is applied to the corpus of documents that the user uploads in a zipped file of .txt files. The application process occurs by first scoring the paragraphs from each document, extracting their corresponding entities and locations and ordering these paragraphs in descending order. After picking the top paragraphs (a random number of 50 paragraphs was selected), the tool will proceed to select the most relevant sentences. The calculations will result in a json file and visualization of the most relevant keywords, entities, locations and sentences of our corpus of documents. For more information about how to contribute to this project please refer to the following blog post in Abierto al Público.
 	
### Guía de instalación
---
Minimum System Requirements:
1.	The server should at least have a memory of 20GB and RAM of 4GB. The program takes space up to around 3GB minimum.
2.	A good internet connection is also recommended as large chunk of data is downloaded during the server configuration.
3.	We recommend installing the application on a CentOS distribution.
Installing Python (3.*)
NOTE: Make sure you are using python3.
First check if python3 is already installed on the server. If not, please follow the following steps:
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
Installing pip
sudo yum -y install python36u-pip
sudo pip install –upgrade pip
Confirm the pip installation with pip -V
Installing MongoDB for data storage:
1.	Navigate to the home folder
2.	Click here for MongoDB installation steps. If link doesn’t work, copy and paste the following url  into your browser https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-centos-7 
Importing Code from a remote git server:
Clone the repository using the command git clone (git repository url).
Create an environment
1.	Create a new folder for the project and navigate to that folder
2.	Create virtual environment and install python3 in the environment using the following command:
python3.6 -m venv my_env (where my_env is the name of environment)   
3.	Activate the newly created environment by typing: source my_env/bin/activate  
4.	To deactivate the environment type: deactivate  
Installing dependencies:
1.	Activate the newly created virtual environment 
2.	Navigate to cloned repository 
3.	Install enchant library by typing sudo yum install enchant.
4.	For installing the remaining packages, set the locale settings to use pip. Enter the following in the command line: export LC_ALL=C.
5.	Install all libraries contained in the “requirements.txt” by typing sudo pip install -r requirements.txt.
6.	Download the English data on spacy using the command: sudo python -m spacy download en.
7.	The nltk library needs to be downloaded using python. Type python in the command line.
8.	Then import the nltk and load the data using the following commands:
-->>>import nltk
-->>>nltk.download('all')


### Guía de usuario
---Server Startup:
1.	Install screen using the command sudo yum install screen
2.	Create a screen for the main templating file by typing:  screen -S main in the command line.
3.	Start the main file that allows us to view the UI in web browser by entering the following command: python run.py
4.	Detach the screen by pressing Ctrl + A, and then Ctrl + D. To confirm whether a screen was detached list all screens using screen -ls. The screen named “main” must have the status “(Detached)”.
5.	Now we create a screen for data collection processor.
6.	Repeat the steps to create a new screen by choosing an arbitrary name such as “data_collection_processor”. 
7.	Start the data collection file by typing “python processor.py”. Then detach this screen using the same method described above.
8.	Similarly create a new screen for the summary_processor which can be named “summary_processor” and run command “python summary_processor.py” and detach it.
9.	Check for all the running screen using screen -ls.
10.	The server is up and running now. To access the application in the server, browse “localhost:8080”. For remote access specify the public IP address along with the port e.g. http://127.0.0.1:8080
 

### Cómo contribuir
---
Si deseas contribuir con este proyecto, por favor lee las siguientes guías que establece el [BID](https://www.iadb.org/es "BID"):

* [Guía para Publicar Herramientas Digitales](https://el-bid.github.io/guia-de-publicacion/ "Guía para Publicar") 
* [Guía para la Contribución de Código](https://github.com/EL-BID/Plantilla-de-repositorio/blob/master/CONTRIBUTING.md "Guía de Contribución de Código")

### Código de conducta 
---
Puedes ver el código de conducta para este proyecto en el siguiente archivo [CODE*OF*CONDUCT.md](CODEOFCONDUCT.md).

### Información adicional
---
Appendix
Knowledge creation is often done through research, a researcher typically begins by establishing a broad research topic then from this topic, develop more narrow topics or subtopics that will help define the outline for the research. The next step usually is the literature review process, often during this process as more knowledge is acquired the subtopics are redefined or remodeled. The issue is the amount of time it will take. Another issue is that new ideas for focus areas or subtopics may not be developed until far into the research. The AI Research Helper is a tool that uses natural language processing techniques to gather intelligence that can provide an insight on what may be the most appropriate focus areas that is relevant to the research. This can help you, for instance, to quickly guide your research process and extract relevant insights in no time.
Model Application:  This interface allows a user to select a model and upload a corpus of documents onto which this model will be applied. The application of this model to the corpus involves analyzing the documents to identify and sort the most relevant paragraphs in ascending order. Once this process is completed the first 50 paragraphs which would be deemed the most relevant paragraphs are analyzed and the model is used to determine the most unique and most representative sentences to the topic. The locations and the entities associated with these sentences are identified and extrapolated.  
Results: This interface displays the information regarding the status of the application of the model to the corpus and the result after the process is completed. The various status for this process is the same as the status mentioned for the model. This interface allows a user to visualize the summary of all the model application that was successfully processed and, download a json file with the processed data. 
View Summaries: This interface can be access by selecting the “Visualize summaries” button from the result interface. On this interface are word clouds showing the keywords, locations and entities that were most relevant to the corpus of documents. A count of the occurrence of each keyword, entity and location within the identified documents is performing to determine the font size of the word in the word clouds, the higher number of occurrences yields the largest font. For each subtopic the most unique and highly representative sentences are displayed. A link to the document in which these sentences are found for are also displayed. Within these documents all relevant sentences to the topic are highlighted. 
Note: original Lucidchart graph accessible here (https://www.lucidchart.com/documents/edit/bdce92fe-b473-4d0a-9fb4-0300b4561dd0/0 ). You need to have an account there.
### Autor
---
BID

### Licencias
---
Los detalles de licencia para este código fuente se encuentran en el archivo [LICENSE.md](LICENSE.md).

La Documentación de Soporte y Uso del software se encuentra licenciada bajo Creative Commons IGO 3.0 Atribución-NoComercial-SinObraDerivada (CC-IGO 3.0 BY-NC-ND)

## Limitación de responsabilidades

El BID no será responsable, bajo circunstancia alguna, de daño ni indemnización, moral o patrimonial; directo o indirecto; accesorio o especial; o por vía de consecuencia, previsto o imprevisto, que pudiese surgir:

i. Bajo cualquier teoría de responsabilidad, ya sea por contrato, infracción de derechos de propiedad intelectual, negligencia o bajo cualquier otra teoría; y/o

ii. A raíz del uso de la Herramienta Digital, incluyendo, pero sin limitación de potenciales defectos en la Herramienta Digital, o la pérdida o inexactitud de los datos de cualquier tipo. Lo anterior incluye los gastos o daños asociados a fallas de comunicación y/o fallas de funcionamiento de computadoras, vinculados con la utilización de la Herramienta Digital.

