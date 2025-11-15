import glob
import json
import os
import re
import pprint
import zipfile
from collections import defaultdict
from src.database_connectivity import *
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory, Response, send_file, jsonify
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/GenerateDataCollection',methods=['GET'])
def data_collection_page():
    return render_template('data_collection.html')


@app.route('/GenerateSummary',methods=['GET'])
def generate_summary_page():
    return render_template('generate_summary.html')


@app.route('/ModelsStatus')
def get_model_status_page():
    print ("get_model_status_page is being called")
    return render_template('models_status.html')


@app.route('/SummariesStatus')
def get_summary_status_page():
    return render_template('summaries_status.html')


@app.route('/VisualizeSummary', methods=['GET'])
def visualize_summary():
    summary_filename = request.args['summary_filename']
    with open(("Summaries/" + summary_filename), "r") as sj:
        output_json = json.load(sj)

    summary_json = json.dumps(output_json)
    return render_template('visualize_summary.html', summary_json=summary_json)


@app.route('/DownloadSummary', methods=['GET'])
def download_summary():
    print ("in download function")
    summary_filename = request.args['summary_filename']
    print (os.getcwd())
    with open(("Summaries/" + summary_filename), "r") as sj:
        summary_json = json.load(sj)

    summary_json = json.dumps(summary_json)
    return Response(
        summary_json,
        mimetype="application/json",
        headers={"Content-disposition":
                     "attachment; filename=" + summary_filename})


@app.route('/returnjson')
def return_json():
    print (os.getcwd())
    filename = request.args['filename']
    with open(("Summaries/" + filename), "r") as sj:
        summary_json = json.load(sj)
    summary_json = json.dumps(summary_json)
    return summary_json


@app.route('/generate_data_model', methods=['POST'])
def get_data():

    print ("get_data is being called")
    try:
        json_obj = {}

        json_obj['model_name'] = request.form['model']
        json_obj["topic_name"] = [request.form['topic']]
        json_obj["subtopics"] = []
        if request.form['topic2']:
            json_obj["topic_name"].append(request.form['topic2'])
        if request.form['topic3']:
            json_obj["topic_name"].append(request.form['topic3'])

        num_subtopics = int(request.form['youcantseeme'])
        for i in range(num_subtopics):
            subtopic_i = {}
            if request.form["subtopic"+str(i)]:
                subtopic_i["subtopic_name"] = request.form["subtopic"+str(i)]
                subtopic_i["keywords"] = [re.sub('[^A-Za-z0-9 ]+', '', x.strip()) for x in request.form["keywords"+str(i)].split(',')]
                json_obj["subtopics"].append(subtopic_i)

        print (os.getcwd())
        model_name = json_obj["model_name"]
        output_model_file_name = "model_"+json_obj["topic_name"][0].replace(" ","_")+"_"+datetime.now().strftime('%Y-%m-%d_%H_%M_%S')+".pkl"
        timestamp = datetime.now()
        collection.insert({"input": json_obj, "model_name": model_name, "output_model_file":  output_model_file_name , "timestamp" : timestamp, "status": "Queued"})

        print ("all working done")

        return Response(json.dumps({'success':True}),200,{'contentType' : 'application/json'})

    except:
        return json.dumps({'error': False}), 500, {'contentType': 'application/json'}


@app.route('/get_status')
def get_status():
    models = []
    cursor = collection.find({}).sort([("timestamp",-1)])
    for document in cursor:
        models.append([document["model_name"], document["status"], document['timestamp'].strftime('%Y-%m-%d %H:%M:%S')])
    model_json = json.dumps(models)
    return model_json


@app.route('/get_models')
def get_models():
    models = []
    cursor = collection.find({"status": "Done"})
    for document in cursor:
        models.append([document["model_name"], document["output_model_file"], document['timestamp'].strftime('%Y-%m-%d %H:%M:%S')])

    model_json = json.dumps(models)
    return model_json

@app.route('/create_summary',methods = ['POST'])
def upload_file():
    try:
        try:
            model = request.form.get('model')
            model_name = " ".join(model.split(",")[:-1]).strip()
            model_file_name = model.split(",")[-1].strip()#storing the model name with the model's creation date
            file = request.files['file']#storing the zipped files
            filename = secure_filename(file.filename)#storing the name of the zipped folder

        except Exception as e:
            print (e)
        if filename.endswith('.zip'):
            if not os.path.isdir('Data'):
                os.mkdir('Data')
            summary_filename = "summary_json_"+ datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +".json"
            folder_name = "text_files_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(os.getcwd(),"Data",folder_name)
            os.mkdir(file_path)
            file.save(filename)
            upload_input_files(filename, file_path)
            timestamp = datetime.now()
            summary_collection.insert({"file_path": file_path, "summary_filename": summary_filename, "model_name": model_name, "model_file_name": model_file_name , "status": "Queued", "timestamp": timestamp})

            return Response(json.dumps({'success': True}), 200, {'contentType': 'application/json'})
        else:
            return Response(json.dumps({'error': False}),400 , {'contentType': 'application/json'})
    except:

        return Response(json.dumps({'error': False}), 500, {'contentType': 'application/json'})


@app.route('/summary_status')
def get_summary_status():
    summary = []
    cursor = summary_collection.find({}).sort([("timestamp",-1)])
    for document in cursor:
        summary.append([document["summary_filename"],document["model_name"],document["status"],document['timestamp'].strftime("%Y-%m-%d %H:%M:%S")])

    summary_json = json.dumps(summary)
    return summary_json


@app.route('/download', methods=['GET', 'POST'])
def download():
    summary_filename = request.form.get('summary_filename')

    with open (("Summaries/"+summary_filename), "r") as sj:
        summary_json = json.load(sj)

    summary_json = json.dumps(summary_json)
    return Response(
        summary_json,
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=" + summary_filename})


def upload_input_files(filename, file_path):

    try:
        with zipfile.ZipFile(os.path.join(filename), "r") as zip_ref:
            zip_ref.extractall(file_path)
    except Exception as e:
        print (e)
    try:#removing original name of zip file
        for root, dirs, files in os.walk(file_path, topdown=False):
            if root != file_path:
                for name in files:
                    source = os.path.join(root, name)
                    target = os.path.join(file_path, name)
                    os.rename(source, target)
    except Exception as e:
        print (e)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
        os.remove(filename)


# if __name__ == '__main__':
#     app.run(debug=True, port=8080, host='0.0.0.0', use_reloader=False)
