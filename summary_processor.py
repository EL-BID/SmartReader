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
    summary_collection.update_one(
        {"_id": jobid},
        {"$set": {"status": status}}
    )

def run_job(job):
    jobid = ""
    '''
    A document is an object of this form:
    {'_id': ObjectId('5c9b842ea1c0a02dea101856'), 
    'file_path': '/app/AIResearchHelper/SmartReader/Data/text_files_2019-03-27_10-09-50',
    'summary_filename': 'summary_json_2019-03-27_10-09-50.json',
    'model_name': 'test_1', 'model_file_name': 'model_Artificial_Intelligence_2019-03-25_14_38_33.pkl',
    'status': 'Queued', 'timestamp': datetime.datetime(2019, 3, 27, 10, 9, 50, 24000)}
    '''
    for document in job:
        jobid = document["_id"]
        try:
            updateJobStatus(jobid, "Processing")
            output_json = create_summary(document["file_path"], document["model_file_name"])
            convert_txt_html(output_json)

            os.makedirs("Summaries", exist_ok=True)

            with open(os.path.join("Summaries", document["summary_filename"]), "w") as f:
                json.dump(output_json, f)

            updateJobStatus(jobid, "Done")

        except Exception as e:
            print("Erro ao processar job", jobid, "->", e)
            updateJobStatus(jobid, "Error")

def processNextJob():
    print('fetching job')
    #job = getJob() #job is a group of jobs that have the 'Queued' status in the database
    job_cursor = getJob()          # ainda é um Cursor
    jobs = list(job_cursor)        # transforma em lista
    #jobs_len = job.count()
    jobs_len = len(jobs)

    if jobs_len == 0:
        print('no more jobs to process')
        return jobs_len
    else:
        run_job(jobs)
        return jobs_len

while(True):
    jobs_check = processNextJob()
    if jobs_check == 0:
        time.sleep(10)