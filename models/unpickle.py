import pickle
import json
import re

def transformer(model_path:str):
	with open(model_path, 'rb') as f:
		data = pickle.load(f)
		data =  re.sub(r"\n"," ",data)
		data =  re.sub(r"\s{2,}"," ",data)
		data = re.sub(r"\'","\"",data)
		print(data)
		

		with open('result.json','w') as fp:
			json.dump(data,fp)

			keys = ('topic','keywords', 'feature_indices')

		# with open("data.json","w") as outfile:
		# 	json.dump(data, outfile)
		    

if __name__ == "__main__":
	model_path = "model_Artificial_Intelligence_2019-03-25_14_38_33.pkl"
	transformer(model_path)