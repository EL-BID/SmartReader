import pickle
import json
import re
import ast
def transformer(model_path:str):
	with open(model_path, 'rb') as f:
		file_name = model_path[0:-4]
		data = str(pickle.load(f))
		data = re.sub(r"\n"," ",data)
		data = re.sub(r"\s{2,}"," ",data) 
		data = data.replace("'vectorizer': TfidfVectorizer(analyzer='word', binary=False, decode_error='strict', dtype=<class 'numpy.int64'>, encoding='utf-8', input='content', lowercase=True, max_df=1.0, max_features=None, min_df=1, ngram_range=(1, 3), norm='l2', preprocessor=None, smooth_idf=True, stop_words='english', strip_accents=None, sublinear_tf=False, token_pattern='(?u)\\\\b\\\\w\\\\w+\\\\b', tokenizer=None, use_idf=True, vocabulary=None),","")
		data = data.replace("[","")
		data = data.replace("]","")
		data = ast.literal_eval(data)
		
		with open(file_name + '.json','w') as fp:
			json.dump(data, fp, ensure_ascii=False, sort_keys=True, indent=4)
		    

if __name__ == "__main__":
	model_path = "model_Future_of_Government_Work_2019-03-29_17_05_40.pkl"
	transformer(model_path)