class Document:
	def __init__(self):
		self.paragraphs = []
		self.keywords = []
		self.locations = []
		self.name = None

	def read_text(self, file_name):
		self.name = file_name
		f = open(file_name, "r")
		for para_text in f.read().split("\n"):
			paragraph = Paragraph(self, para_text)
			self.paragraphs.append(paragraph)
			paragraph.para_id = len(self.paragraphs)-1

	def get_text(self):
		return [ paragraph.text for paragraph in self.paragraphs ]

	def get_keywords(self):
		all_keywords = []
		for para in self.paragraphs:
			kws = [ kw for kw in para.keywords ]
			all_keywords.extend(kws)
		return sorted(all_keywords, key =lambda x: -x["count"])

	def get_locations(self):
		all_locations = []
		for para in self.paragraphs:
			kws = [ kw for kw in para.locations ]
			all_locations.extend(kws)
		return sorted(all_locations, key =lambda x: -x["count"])

class Paragraph:
	def __init__(self, document, text):
		self.document = document
		self.text = text
		self.classification = {}
		self.keywords = []
		self.locations = []
		self.topic_keywords = {}
		self.entities = {}
		self.para_id = -1
