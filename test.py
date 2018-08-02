from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from unidecode import unidecode
import sys, traceback
import unicodedata
import codecs
import requests
import unicodedata
import spacy
from spacy.lang.en import English #update for python 3
nlp = spacy.load('en')
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import nltk, re, pprint
from nltk import word_tokenize
from nltk import sent_tokenize
from gensim.summarization import keywords
from gensim.summarization import summarize
from gensim import corpora, models, similarities
from collections import defaultdict
from nltk.tokenize import sent_tokenize
import os
import tempfile
from pprint import pprint

LANGUAGE = "english"
textss = "Type II markets tend to share two major features. First, banks are deeply rooted in the economy and are strong contenders to become leaders in mobile financial services in their respective countries. Second, mobile operators and retailers have achieved high penetration levels and built strong customer relationships in their core business. Multiple strong contenders have emerged to provide financial services and, in some markets, mobile operators, banks, and retailers have partnered to leverage each other's assets. In others, entrenched interests or regulatory restrictions have resulted in partnership models that not all parties approve of. Regardless of the market dynamics, however, Type II markets tend to be more integrated with existing financial and retail infrastructure, often including access to national clearing and settlement systems. These markets include Brazil, Mexico and Panama."

output_sentences = []
hold=''
truecount=0
store=''
store=keywords(textss,ratio=0.05)#extracts most relevant words from full text
store1=str(store)
holdfirst=nltk.word_tokenize(store1)#Tokenize a string (keywords) to split off punctuation other than periods 
nparser = PlaintextParser.from_string(textss,Tokenizer(LANGUAGE)) #parser is an object that represents the full text
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)
print('summarizer_stopwords')
print(type(summarizer.stop_words))
print(summarizer.stop_words)
sentencess=[]
compare=[]
TEMP_FOLDER = tempfile.gettempdir()
documents=sent_tokenize(textss)#full text into sentences
summalen=len(documents)#number of sentences
stoplist = set('for a of the and to in'.split())
print(stoplist)
    
texts = [[word for word in document.lower().split() if word not in stoplist]
              for document in documents]#texts is an array of sentences where each sentence is a list of words without stopwords
frequency = defaultdict(int)#dict subclass that calls a factory function to supply missing values
    
for text in texts:
	for token in text:
		frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]#array of words that occur more than once