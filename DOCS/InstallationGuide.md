# Please follow the instructions to setup the server for “AI Research Helper”.

## Minimum System Requirements:
1. The server should atleast have a memory of 20GB and RAM of 4GB. The program takes space upto around 3GB minimum.
2. A good internet connection is also recommended as large chunk of data is downloaded while server configuration.
3. We recommend Ubuntu 16.04 servers on AWS.

## Installing Python(2.7)
### NOTE : Make sure you are using python 2.7.
1. First check if python is already installed on the server or not. (Sometimes it is pre-installed).
2. If not use the command “sudo apt-get install python2.7”.
3. To check the successful installation type “python2.7”.
4. Install python package manager “pip” by entering the command “sudo apt-get install python-pip”.
5. Confirm pip installation .Run “pip -V”

## Importing Code from a remote git server:
1. Clone code using the command “git clone (git repository url)”.
2. Move to the code directory using “cd text-classifier”.

## Installing MONGODB for data storage:
1. Move back to root folder using  “cd ..”.
2. To install mongodb type “sudo apt-get install mongodb”.

## Installing dependency python packages:
1. First we need to install the enchant library using the command “sudo apt-get install libenchant1c2a”.
2. Now for the package installations we need to set the locale settings to use pip. Enter command “export LC_ALL=C”.
3. Now move to the folder that contains the code using “cd text-classifier”.
4. Now we install all the pre-requisite libraries already listed in the “requirements.txt” file.
5. Do this by typing “sudo pip install -r requirements.txt”. This step will take some time, as it installs all the required libraries.
6. Now we need to download the english data on spacy. Use the command “sudo python -m spacy download en”.
7. Next we need to download the nltk data. We perform this action using python.
8. Open python using “python2.7”.
9. Then import the nltk and load the data using the following commands:
-->>>import nltk
-->>>nltk.download('all')
10. This will take some time and download all the nltk. Depending on the internet connection, this action varies from 5 mins to couple of hours.

We have downloaded all the required dependencies and can start the server. We will need to start a bunch of files for the system to work.

## Server Startup:
1. First we install screen using the command “sudo apt-get install screen”.
2. Next we create a screen for the main templating file.
3. Create a screen using “screen” command.
4. We rename the screen by command “screen -S main”.
5. We start the main file that allows us to view the UI in web browser. Enter the command “python main.py”.
6. Now we cannot quit the code here, and we have to detach the screen. We perform this task by combination of keys. Press Ctrl+A, and then Ctrl + D.
7. This will detach the screen. You can confirm this by using the command to list all screens “screen -ls”. The screen named “main” must have the status “(Detached)”.
8. Now we create a screen for data collection processor.
9. Repeat the steps 3 and 4 to create a new screen, but this time instead of “main” name it “data_collection_processor”.
10. Here we will start the data collection file.
11. Enter “python processor.py”. Then detach this screen using the same method described above.
12. Similarly create a new screen named “summary_processor” and run command “python summary_processor.py” and then detach it.
13. Now check for all the running screen using “screen -ls”. It will be something like this.
14. The server is up and running now.
15. On the same machine it is accessible using “localhost:5000”.
16. For remote access specify the ip address along with the port e.g “http://127.0.0.1:5000”.

## Note: The ip address must be external ip of the VM and port 5000 must be allowed in the firewall.
