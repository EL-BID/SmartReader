*Visit the [Publication Guide](el-bid.github.io/guia-de-publicacion/) (currently available in Spanish) for more information about how to publish digital tools.
To learn more about the Code for Development initiative, visit: [code.iadb.org](https://code.iadb.org/es)*

## *SmartReader*

### Description and Context
---

*SmartReader* is a tool that uses NLP techniques to give you a fresh insight of your research (research question and literature) by querying Google and retrieving related up-to-date information. It was created to tackle the challenge that knowledge workers experience when coping with the exponential amount of information generated every day. 


The Knowledge Innovation and Communication Department of the **Inter-American Development Bank** created this tool after acknowledging this need and the latency of technologies such as Artificial Intelligence and Natural language Processing, to assist the Knowledge creation process.  


The tool comprises four interfaces: 1) *Model Definition*, 2) *Model Status*, 3) *Model Application*, and 4) *Results interfaces*. The following flow chart explain the mechanics of the tool.  

![flujograma_en](https://code.iadb.org/sites/default/files/inline-images/flujograma.jpg "Flow Chart SmartReader English Version")
<img   src="https://code.iadb.org/sites/default/files/inline-images/keys_en.png" 
alt="keys!" width="50%" style="float:right;"/>

As depicted in the chart, from left to right and from top to bottom, the process starts with the user creating a model by entering a set of topic and subtopics that match a determined research question. Afterwards, the model will generate query strings used to retrieve the most relevant data available online, this means querying Google. Afterwards, by applying the *sklearn.TfidfVectorizer*, a model with weighted terms will be created. In the Model Application interface, a model is applied to the corpus of documents that the user uploads in a zipped file of *.txt* files. The application process occurs by first scoring the paragraphs from each document, extracting their corresponding entities and locations and ordering these paragraphs in descending order. After picking the top paragraphs (a random number of 50 paragraphs was selected), the tool will proceed to select the most relevant sentences. The calculations will result in a *json* file and visualization of the most relevant keywords, entities, locations and sentences of our corpus of documents. For more information about how to contribute to this project please refer to the following [blog post](https://www.google.com/) in Abierto al Público.
 	
### Installation Guide
---

#### Minimum System Requirements:
1.	The server should at least have a memory of 20GB and RAM of 4GB. The program takes space up to around 3GB minimum.
2.	A good internet connection is also recommended as large chunk of data is downloaded during the server configuration.
3.	We recommend installing the application on a CentOS distribution.

#### Installing Python (3.\*)
NOTE: Make sure you are using python3.
First check if python3 is already installed on the server. If not, please follow the following steps:
```
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
```

#### Installing pip
```
sudo yum -y install python36u-pip
sudo pip install –upgrade pip
```
Confirm the pip installation with `pip -V`


#### Installing MongoDB for data storage:
1.	Navigate to the home folder
2.	Click [here](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-centos-7) for MongoDB installation steps. If link doesn’t work, copy and paste the following url  into your browser https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-centos-7 

#### Importing Code from a remote git server:
Clone the repository using the command `git clone https://github.com/EL-BID/SmartReader.git`.

#### Create an environment
1.	Create a new folder for the project and navigate to that folder
2.	Create virtual environment and install python3 in the environment using the following command: `python3.6 -m venv my_env` (where `my_env` is the name of environment)
3.	Activate the newly created environment by typing: `source my_env/bin/activate`  
4.	To deactivate the environment type: `deactivate`  

#### Installing dependencies:
1.	Activate the newly created virtual environment 
2.	Navigate to cloned repository 
3.	Install *enchant* library by typing `sudo yum install enchant`.
4.	To install the remaining packages, set the locale settings to use pip. Enter the following in the command line: `export LC_ALL=C`.
5.	Install all libraries contained in the “requirements.txt” by typing `sudo pip install -r requirements.txt`.
6.	Download the English data on *spacy* using the command: `sudo python -m spacy download en`.
7.	The *nltk* library needs to be downloaded using python. Type `python` in the command line.
8.	Then import the *nltk* and load the data using the following commands:

```
>>> import nltk
>>> nltk.download('all')
```

### User Guide
---

#### Server Startup:
1.	Install *screen* using the command `sudo yum install screen`
2.	Create a screen for the main templating file by typing:  `screen -S main` in the command line.
3.	Start the main file that allows us to view the UI in web browser by entering the following command: `python run.py`
4.	Detach the screen by pressing Ctrl + A, and then Ctrl + D. To confirm whether a screen was detached list all screens using `screen -ls`. The screen named “main” must have the status “(Detached)”.
5.	Now we create a screen for data collection processor. Repeat the steps to create a new screen by choosing an arbitrary name such as “data_collection_processor”. 
6.	Start the data collection file by typing `python processor.py`. Then detach this screen using the same method described above.
7.	Similarly create a new screen for the summary_processor which can be named “summary_processor” and run command `python summary_processor.py` and detach it.
8.	Check for all the running screen using `screen -ls`.
9.	The server is up and running now. To access the application in the server, browse “localhost:8080”. For remote access specify the public IP address along with the port.

### How to Contribute
---

We have made this code available to you and we could not be more eager to hear about your experience with it. Please refer to the *Issues* tab of this repository to find some examples on how you can contribute to the improvement of *SmartReader*. Furthermore in the section [Additional Information](#additional-information) of this document you will find a link to a blogpost about *SmartReader* in *Abierto al Público*.

### Code of Conduct 
--- 

You can see the code of conduct [here](https://github.com/EL-BID/SmartReader/blob/master/CODE-OF-CONDUCT.md)

### Authors
---
© 2017 Inter-American Development Bank and Institute for the Future.
This software is the result of a partnership between the Inter-American Development Bank and the [Institute for the Future] (http://www.iftf.org/).
The copyright on the software is shared by both organizations, even if your licensor is the Inter-American Development Bank only.


Inter-american Development Bank  
Involved:

- [Daniela Collaguazo](mailto:danielaco@iadb.org)
- [Kyle Strand](mailto:kyles@iadb.org)
- Seaford Bacchas

### Additional Information
---

[Blog en Abierto al Público](https://blogs.iadb.org/abierto-al-publico/2018/09/07/smartreader-open-source-text-analytics-tool/?lang=en)

### License 
---

You can see the source code license [here](https://github.com/EL-BID/SmartReader/blob/master/LICENSE.md)

The Documentation of Support and Use of the software is licensed under Creative Commons IGO 3.0 Attribution-NonCommercial-NoDerivative (CC-IGO 3.0 BY-NC-ND)

### Limitation of responsibilities
---

The IDB is not responsible, under any circumstance, for damage or compensation, moral or patrimonial; direct or indirect; accessory or special; or by way of consequence, foreseen or unforeseen, that could arise:

i. Under any concept of intellectual property, negligence or detriment of another part theory;

ii. Following the use of the Digital Tool, including, but not limited to defects in the Digital Tool, or the loss or inaccuracy of data of any kind. The foregoing includes expenses or damages associated with communication failures and / or malfunctions of computers, linked to the use of the Digital Tool.

