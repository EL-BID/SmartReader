from pymongo import MongoClient
import traceback
import os

try:

    if os.system("grep mongod") != 256:
        pass
    else:
        os.system("service mongod start")
    client = MongoClient()
    db = client.classifier_database
    collection = db.model_jobs
    summary_collection = db.summary_jobs

except Exception as e:
    print(traceback.format_exc())
