from gensim.summarization import keywords
from gensim.summarization import summarize
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.parsers.html import HtmlParser

stemmer = Stemmer("english")
summarizer = Summarizer(stemmer)

for sentence in summarizer(parser.document,1):
	print(sentence)