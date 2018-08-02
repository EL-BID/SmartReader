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
textss = "Type II markets tend to share two major features. First, banks are deeply rooted in the economy and are strong contenders to become leaders in mobile financial services in their respective countries. Second, mobile operators and retailers have achieved high penetration levels and built strong customer relationships in their core business. Multiple strong contenders have emerged to provide financial services and, in some markets, mobile operators, banks, and retailers have partnered to leverage each other's assets. In others, entrenched interests or regulatory restrictions have resulted in partnership models that not all parties approve of. Regardless of the market dynamics, however, Type II markets tend to be more integrated with existing financial and retail infrastructure, often including access to national clearing and settlement systems. These markets include Brazil, Mexico and Panama."

nparser = PlaintextParser.from_string(textss,Tokenizer(LANGUAGE))

for sentence in summarizer(parser.document,1):
	print(sentence)