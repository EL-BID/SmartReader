import json
import os
import shutil


def convert_txt_html(js):

	docs_folder = os.path.join("static","documents", js[0]["folder_name"])
	input_folder = js[0]["folder"]
	os.mkdir(docs_folder)

	all_docs = {}

	for k in range(len(js)):
		for i in range(len(js[k][u'summary_points'])):
			try:
				sp = js[k][u'summary_points'][i]
				doc_id = sp['doc_id']

				para_id = str(sp['para_id'])
				sentence = sp[u'original_sentence']

				if doc_id in all_docs:
					doc = all_docs[doc_id]

				else:
					doc = open( os.path.join(input_folder , doc_id.replace(".html", "").replace(".txt", ".txt")) ).read()
					all_docs[doc_id] = doc

				if doc.find(sentence) < 0:
					yada
				doc = doc.replace(sentence, "<a href=\"#%s\"><mark>%s</mark></a>"  % (para_id, sentence))
				all_docs[doc_id] = doc
			except Exception as e:
				print (e)
				pass

	print("writing out dataset of length %d" % (len(all_docs)))

	for doc_id in all_docs:
		try:

			f = open( os.path.join(docs_folder,  doc_id + ".html") , "w")
			f.write('''<style type="text/css">
				p{
					font-family: sans-serif;
					line-height: 1.5;
				}
				</style>''')
			content = all_docs[doc_id]
			lines = content.split("\n")
			for l in lines:
				f.write("<p>%s</p>" % l)
			f.close()
		except Exception as e:
			print (e)
			pass
