from gensim.summarization import keywords
from gensim.summarization import summarize

for sentence in summarizer(parser.document,1):
	print(sentence)