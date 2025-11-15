import glob
import json
import os
import re
#import pprint
import traceback
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
        form = request.form.to_dict()
        print("DEBUG form recebido:", form)
        print("CWD:", os.getcwd())

        json_obj = {}

        # Campos obrigatórios
        model_name = form.get('model')
        topic1 = form.get('topic')

        if not model_name:
            return jsonify({"error": True, "message": "Campo 'model' é obrigatório"}), 400
        if not topic1:
            return jsonify({"error": True, "message": "Campo 'topic' é obrigatório"}), 400

        json_obj['model_name'] = model_name
        json_obj["topic_name"] = [topic1]
        json_obj["subtopics"] = []

        # Campos opcionais: topic2 e topic3
        topic2 = form.get('topic2')
        if topic2:
            json_obj["topic_name"].append(topic2)

        topic3 = form.get('topic3')
        if topic3:
            json_obj["topic_name"].append(topic3)

        # Quantidade de subtopics
        raw_num = form.get('youcantseeme', '0')
        try:
            num_subtopics = int(raw_num)
        except ValueError:
            return jsonify({"error": True, "message": "Campo 'youcantseeme' deve ser um inteiro"}), 400

        # Monta lista de subtopics
        for i in range(num_subtopics):
            sub_name = form.get(f"subtopic{i}")
            keywords_raw = form.get(f"keywords{i}")

            if sub_name and keywords_raw:
                subtopic_i = {
                    "subtopic_name": sub_name,
                    "keywords": [
                        re.sub(r'[^A-Za-z0-9 ]+', '', x.strip())
                        for x in keywords_raw.split(',')
                        if x.strip()
                    ]
                }
                json_obj["subtopics"].append(subtopic_i)

        print("JSON de entrada montado:", json_obj)

        # Gera nome do arquivo do modelo
        output_model_file_name = "model_" + json_obj["topic_name"][0].replace(" ", "_") + \
            "_" + datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + ".pkl"
        timestamp = datetime.now()

        # IMPORTANTE: garantir que 'collection' está definido antes
        # Exemplo:
        # from pymongo import MongoClient
        # client = MongoClient("mongodb://mongo:27017/")
        # db = client["seu_banco"]
        # collection = db["sua_colecao"]

        result = collection.insert_one({
            "input": json_obj,
            "model_name": model_name,
            "output_model_file": output_model_file_name,
            "timestamp": timestamp,
            "status": "Queued"
        })

        print("all working done, inserted id:", result.inserted_id)

        return Response(json.dumps({'success': True}), 200, {'contentType': 'application/json'})

    except:
        traceback.print_exc()
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
#def get_models():
#    models = []
#    cursor = collection.find({"status": "Done"})
#    for document in cursor:
#        ts = document.get('timestamp')
#        ts_str = ts.strftime('%Y-%m-%d %H:%M:%S') if ts else None
#
#        models.append({
#            "label": document["model_name"],
#            # É ISSO que o /create_summary vai receber em request.form['model']
#            "value": f'{document["model_name"]}, {document["output_model_file"]}',
#            "file": document["output_model_file"],
#            "timestamp": ts_str
#        })

def get_models():
    try:
        models = []
        cursor = collection.find({"status": "Done"}).sort("timestamp", -1)

        for document in cursor:
            models.append([
                document.get("model_name", ""),
                document.get("output_model_file", ""),
                document.get("timestamp", datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S')
            ])

        # SEMPRE retorna alguma coisa (nem que seja lista vazia)
        return jsonify(models)
    except Exception as e:
        # loga pra você ver no container
        print("Erro em /get_models:", e)
        # ainda assim devolve JSON válido
        return jsonify([]), 500

@app.route('/create_summary',methods = ['POST'])
def upload_file():
    try:
        # --------- MODEL ----------
        raw_model = request.form.get('model', '').strip()
        if not raw_model:
            print('Campo "model" veio vazio ou não foi enviado')
            return Response(
                json.dumps({'error': True, 'message': 'Campo "model" é obrigatório.'}),
                400,
                {'contentType': 'application/json'}
            )

        parts = [p.strip() for p in raw_model.split(',') if p.strip()]
        if len(parts) < 2:
            print('Formato de "model" inválido:', raw_model)
            return Response(
                json.dumps({'error': True, 'message': 'Formato de "model" inválido. Use: "nome do modelo, arquivo.pkl".'}),
                400,
                {'contentType': 'application/json'}
            )

        model_name = " ".join(parts[:-1])
        model_file_name = parts[-1]

        # --------- ARQUIVO ----------
        if 'file' not in request.files:
            print('Nenhum arquivo "file" enviado no form')
            return Response(
                json.dumps({'error': True, 'message': 'Nenhum arquivo enviado.'}),
                400,
                {'contentType': 'application/json'}
            )

        file = request.files['file']
        filename = secure_filename(file.filename or '')

        if not filename:
            print('Filename vazio')
            return Response(
                json.dumps({'error': True, 'message': 'Nome de arquivo inválido.'}),
                400,
                {'contentType': 'application/json'}
            )

        if not filename.endswith('.zip'):
            print('Arquivo não é zip:', filename)
            return Response(
                json.dumps({'error': True, 'message': 'Apenas arquivos .zip são aceitos.'}),
                400,
                {'contentType': 'application/json'}
            )

        # --------- PROCESSA ZIP ----------
        if not os.path.isdir('Data'):
            os.mkdir('Data')

        summary_filename = "summary_json_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
        folder_name = "text_files_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(os.getcwd(), "Data", folder_name)
        os.mkdir(file_path)

        file.save(filename)
        upload_input_files(filename, file_path)

        timestamp = datetime.now()
        result = summary_collection.insert_one({
            "file_path": file_path,
            "summary_filename": summary_filename,
            "model_name": model_name,
            "model_file_name": model_file_name,
            "status": "Queued",
            "timestamp": timestamp
        })
        print("Job de summary criado, _id:", result.inserted_id)

        return Response(json.dumps({'success': True}), 200, {'contentType': 'application/json'})

    except Exception as e:
        import traceback
        print('Erro em /create_summary:', e)
        traceback.print_exc()
        return Response(
            json.dumps({'error': True, 'message': str(e)}),
            500,
            {'contentType': 'application/json'}
        )

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