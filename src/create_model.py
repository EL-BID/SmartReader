# import logging
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from src.LemmaTokenizer import *

def get_topic_keywords(features, X):
	features_with_weights = sorted([ {"keyword":features[i], "count": X[0,i], "index":i} for i in range(len(features)) ], key=lambda x:-x["count"] )[:50]
	features = {}
	feature_indices = {}
	for fww in features_with_weights:
		features[fww["keyword"]] = fww["count"]
		feature_indices[fww["keyword"]] = fww["index"]
	return features, feature_indices


def create_and_save_model(subtopics, output_file):
	data = []
	output = ()
	all_texts = []
	vec = TfidfVectorizer(ngram_range=(1,3), stop_words="english")
	subtopic_names = list(subtopics.keys())
	no_data_subtopic_names = []
	
	f = open('log/create_model_log.txt','wb')
	for topic in subtopic_names:
		text = subtopics[topic]

		if len(text.strip()) >0 :
			all_texts.append(text)
		else:
			no_data_subtopic_names.append(topic)
		f.write('text: ' + text + '\n')
		f.write('type of no_data_subtopic_names: ' + type(subtopic_names) + '\n')
	# f.write('subtopic_names: ' + str(subtopic_names) + '\n')
	f.close()
	


	X = vec.fit_transform(all_texts)
	global gX
	gX = X
	features = vec.get_feature_names()
	for i in range(len(subtopic_names)):
		if subtopic_names[i] not in no_data_subtopic_names:
			Xi = X[i, :]
			features_with_weights, feature_indices = get_topic_keywords(features, Xi)
			data.append( {"topic":subtopic_names[i], "keywords":features_with_weights, "vectorizer":vec, "feature_indices":feature_indices} )
			# output["keywords"] = features_with_weights
			# print(features_with_weights)
			# print(type(features_with_weights))
			# print(feature_indices)
			# output["feature_indices"] = feature_indices

	pickle.dump(data, open(output_file, "wb"))
	global gvec
	gvec = vec


def load_model(file_path):
	return pickle.load(open(file_path, "rb"))

gvec = None
gX = None
