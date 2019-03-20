gimport os
import time
from src.database_connectivity import *
from src.search_data import *
from src.create_model import *

cursor = collection.find()

for document in cursor:
    print ("this is the status", document["status"])
def getJob():
    result = collection.find( { 'status': "Queued" } ).limit(1)#retrieving what is in the database with the status 'Queued'. e.g.: topics, subtopics, model_name, ect. result is a dictionary
    return result

def updateJobStatus(jobid, status):

    collection.update(
        {"_id": jobid},
        {
            "$set": {
                "status": status
            }
        }
    )


def run_job(job):
    #Group of 'Queued' jobs retrieved from the database
    for document in job:
        try:
            print (document["model_name"])
            jobid = document["_id"]
            updateJobStatus(jobid, "Processing")
            topic_text = get_data(document["input"])
            #joined text from the results of querying the topics on the internet
            all_text = " ".join([topic_text[text] for text in topic_text])
            if len(all_text.strip()) > 0:
                print("Creating Model")
                create_and_save_model(topic_text, os.path.join(os.getcwd(),"models",document["output_model_file"]))
                print ("Model Created")
                updateJobStatus(jobid, "Done")
            else:
                updateJobStatus(jobid, "No data")
        except Exception as e:
            print (e)
            updateJobStatus(jobid, "Error")


def processNextJob():
    print('fetching job')
    job = getJob()#job is a group of jobs that have the 'Queued' status in the database
    jobs_len = job.count()

    if jobs_len == 0:#excecuted once there are no more 'Queued' jobs in the database
        print('no more jobs to process')
        return jobs_len
    else:
        run_job(job)
        return jobs_len


while(True):
    jobs_check = processNextJob()
    if jobs_check == 0:
        time.sleep(10)
