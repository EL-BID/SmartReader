
from flask import Flask, render_template, request, send_from_directory, Response, send_file, jsonify
model = '1-test, 2018-08-02 18:44:07'
model_name = " ".join(model.split(",")[:-1]).strip()
model_file_name = model.split(",")[-1].strip()
file = request.files['file']
print(file)