
# from flask import Flask, render_template, request, send_from_directory, Response, send_file, jsonify
# app = Flask(__name__)
#
# model = '1-test, 2018-08-02 18:44:07'
# model_name = " ".join(model.split(",")[:-1]).strip()
# model_file_name = model.split(",")[-1].strip()
#
# @app.route('/create_summary',methods = ['POST'])
# def upload_file():
# 	print('getting here')
# 	try:
# 		print('')
# 		file = request.files['file']
# 		print(file)
# 	except Exception as e:
# 		print (e)
#
