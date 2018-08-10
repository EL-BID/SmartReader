import json
import os
import time
from src.database_connectivity import *
from datetime import datetime
from src.process import *
from src.convert_dataset import *


def getJob():

    result = summary_collection.find( { 'status': "Queued" } ).limit( 1 )
    return result

def updateJobStatus(jobid, status):

    summary_collection.update(
        {"_id": jobid},
        {
            "$set": {
                "status": status
            }
        }
    )

def run_job(job):
    jobid = ""
    for document in job:
        try:
            jobid = document["_id"]
            updateJobStatus(jobid, "Processing")
            output_json = create_summary(document["file_path"], document["model_file_name"])
            print("XXXXXXXXXXXXXXX")
            print(output_json)
            convert_txt_html(output_json)
            if not os.path.isdir('Summaries'):
                os.mkdir('Summaries')
            json.dump(output_json, open("Summaries/" + document["summary_filename"], "w"))
            updateJobStatus(jobid, "Done")

        except Exception as e:
            print (e)
            updateJobStatus(jobid, "Error")


def processNextJob():
    print('fetching job')
    job = getJob()
    jobs_len = job.count()

    if jobs_len == 0:
        print('no more jobs to process')
        return jobs_len
    else:
        run_job(job)
        return jobs_len

while(True):
    jobs_check = processNextJob()
    if jobs_check == 0:
        time.sleep(10)
