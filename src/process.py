import numpy as np
import os
import pickle
import spacy
from collections import defaultdict
from geopy.geocoders import Nominatim
from nltk.tokenize import sent_tokenize
from scipy.spatial.distance import cdist

from src import create_model
from src import dataset_reader
from src import spell_check
from src.sumytest import *

geolocator = Nominatim()

nlp = spacy.load('en')
a, b = None, None
entity_types_non_loc = ['PERSON', "ORG", "PRODUCT", "EVENT", "WORK_OF_ART", "LANGUAGE", "NORP"]
entity_types_loc = ["LOC", "GPE"]


def get_entities(nlp, text):
	entities = defaultdict(lambda:[])
	doc = nlp(text)
	for ent in doc.ents:
		entities[ent.label_].append( {"type":ent.label_, "text":ent.text} )
	return entities

def score_doc(model, doc):
	texts = [par.text for par in doc.paragraphs]#generating a list of paragraphs per document. So len(texts) will return the number of paragraphs in a document
	for topic in model:
		vec = topic['vectorizer']#vec returns the TfidfVectorizer function of the model with its corresponding parameters
		X = vec.transform(texts)#vec.transform would transform documents(text) to a document-term matrix. It returns X which is a sparse matrix, [n_samples, n_features]
		feature_indices = topic["feature_indices"]
		for i in range(X.shape[0]):#X.shape[0] is the number of rows, e.g.: 126 rows or paragraphs. From now, "topic" refers to the information in the model and "X" refers to text file
			score = 0#scores[i, 0]
			hits = []
			for feat in feature_indices:#feat returns the keyword itself
				# print("feat in feature_indices: ", feat)
				j = feature_indices[feat]#j returns the index of the keyword
				if feat in topic["keywords"] and X[i,j] > 0: # iterate through keywords and weights ?????
					sc = (X[i,j] * topic["keywords"][feat])
					hits.append( {"keyword":feat, "count": sc } )
					score = score + sc
			doc.paragraphs[i].classification[ topic["topic"] ] = score
			doc.paragraphs[i].topic_keywords[topic["topic"]] = hits
			entities = get_entities(nlp, u'%s' % texts[i])
			doc.paragraphs[i].locations = []
			for et in entity_types_loc:
				doc.paragraphs[i].locations.extend(entities[et])
			doc.paragraphs[i].entities = []
			for et in entity_types_non_loc:
				doc.paragraphs[i].entities.extend(entities[et])
	for i in range(len(doc.paragraphs)):
		sm = 1.0*sum( doc.paragraphs[i].classification.values() )
		if sm == 0 or True:
			sm = 1
		for topic_name in doc.paragraphs[i].classification:
			doc.paragraphs[i].classification[topic_name] /= sm

para_g = None
def consolidate_data(dataset, model):
	output_prelim = defaultdict(lambda:[])
	global para_g
	for doc in dataset:
		for para in doc.paragraphs:
			para_g = para
			best_topic = max( para.classification, key=para.classification.get )
			output_prelim[best_topic].append( { "para":para, "score":para.classification[best_topic] } )
	output = []
	for topic in output_prelim:
		d = {"topic":topic, "paragraphs": sorted( output_prelim[topic]  , key=lambda x:-x[ "score" ]) }
		output.append(d)
	return output

def create_summary(dataset_location, model_name):

	#dataset_location = "refined_ocred_data"
	#model_name = "models/informal_economy_new.pkl"
	#print (os.getcwd())
	model_name = "models/" + model_name
	print (model_name)

	dataset = dataset_reader.read_dataset_text(dataset_location)
	# print ("Number of files: ", len(dataset))
	model = create_model.load_model(model_name)
	# print("Model loaded", model)
	i = 0
	# limit = 2
	for doc in dataset:
		#print(i)
		i = i + 1
		score_doc(model, doc)
	output = consolidate_data(dataset, model)
	pickle.dump(output, open("prelim_output_informal_economy_new.bin", "wb"))

	get_lat_lng = False
	location_history = {}
	js = []
	for topic in output:
		topic_name = topic["topic"]
		d = {"topic":topic_name}
		all_keywords = defaultdict(lambda:0)
		all_locations = defaultdict(lambda:0)
		all_entities = defaultdict(lambda:0)
		all_entities_type = defaultdict(lambda:0)
		summary_points = []
		paragraphs = topic["paragraphs"]

		for p in paragraphs[0:50]:
			try:
				full_text = p["para"].text
				sentences = sent_tokenize(full_text)
				print('XXXXXXXXXXXXXXXXXXXXXXXXX')
				print(sentences)
				print('YYYYYYYYYYYYYYYYYYYYYYY')
				summary = get_summary( full_text, 1, len(sentences) )[0]
				# original_sentence = summary
				# summary_index = sentences.index(summary)
				# summary = spell_check.check_spelling(summary)
				# context = sentences[summary_index-1] + sentences[summary_index] + sentences[summary_index+1]
				# context = spell_check.check_spelling(context)

				# summary_points.append({ "summary":summary, "context": context, "original_sentence": original_sentence ,"text":full_text, "doc_id":p["para"].document.name.split('/')[-1], "para_id":p["para"].para_id, "score":p["score"]})
				# for kwo in p["para"].topic_keywords[topic_name]:
				# 	kw = kwo["keyword"]
				# 	all_keywords[kw] += kwo["count"]
				# for eto in p["para"].locations:
				# 	all_locations[ eto["text"] ] += 1
				# for eto in p["para"].entities:
				# 	all_entities[ eto["text"] ] += 1
				# 	all_entities_type[eto["text"]] = eto["type"]

			except:
				pass
		# d['summary_points'] = summary_points
		# d["keywords"] = [ {"keyword":k, "count":all_keywords[k]} for k in all_keywords]
		# sm = np.sum( [kw["count"] for kw in d["keywords"]] )
		# for kw in d["keywords"]:
		# 	kw["count"] = int(1000*kw["count"]/sm)

		# d["locations"] = [ {"keyword":k, "count":all_locations[k], "type":"LOCATION"} for k in all_locations if len(k) > 1]
		# if get_lat_lng == True:
		# 	for l in d["locations"]:
		# 		count = 0
		# 		while count <= 3:
		# 			count = count + 1
		# 			#print(count)
		# 			try:
		# 				if l['keyword']  in location_history:
		# 					latlng = location_history[ l['keyword'] ]
		# 				else:
		# 					latlng = geolocator.geocode(l['keyword'])
		# 					location_history[ l['keyword'] ] = latlng

		# 				break
		# 				if latlng:
		# 					l["lat"] = latlng.latitude
		# 					l["lng"] = latlng.longitude
		# 			except:
		# 				pass
		# d["entities"] = [ {"keyword":k, "count":all_entities[k] , "type":all_entities_type[k]} for k in all_entities if len(k) > 1]
		# d["folder"] = dataset_location
		# d["folder_name"] = dataset_location.split("/")[-1]
		# #print (d["folder_name"])
		# js.append(d)
		# print ("***********", js)

	# os.remove("prelim_output_informal_economy_new.bin")
	return js
