from pymongo import MongoClient
import traceback
import os

try:
    MONGO_URL = os.environ.get("MONGO_URL", "mongodb://mongo:27017/meu_banco")

    if os.system("grep mongod") != 256:
        pass
    else:
       # os.system("service mongod start")
       print("Falha no acesso ao mongo DB")
    client = MongoClient(MONGO_URL)
    db = client.classifier_database
    collection = db.model_jobs
    summary_collection = db.summary_jobs

except Exception as e:
    print(traceback.format_exc())
