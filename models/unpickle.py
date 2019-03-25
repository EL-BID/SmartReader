import pickle
import json

def transformer(model_path:str):
	with open(model_path, 'rb') as f:
		data = str(pickle.load(f))
		data = re.sub(r"","",data)
		    

if __name__ == "__main__":
	model_path = "model_Future_of_Government_Work_2019-03-22_11_37_37.pkl"
	transformer(model_path)