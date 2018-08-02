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

stemmer = Stemmer("english")
summarizer = Summarizer(stemmer)
nparser = PlaintextParser.from_string(textss,Tokenizer(LANGUAGE))

for sentence in summarizer(parser.document,1):
	print(sentence)