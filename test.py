from gensim.summarization import keywords
from gensim.summarization import summarize
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
summarizer = Summarizer(stemmer)

for sentence in summarizer(parser.document,1):
	print(sentence)