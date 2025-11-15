from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from unidecode import unidecode
import sys, traceback
import unicodedata
import codecs
import requests
import unicodedata
import spacy
from spacy.lang.en import English
nlp = spacy.load('en_core_web_sm')
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

sentencess=[]
compare=[]
LANGUAGE = "english"

def get_summary(textss , truereq, numofsent):
    output_sentences = []
    hold=''
    truecount=0
    store=''
    store=keywords(textss,ratio=0.05)#extracting the most relevant words from full text
    store1=str(store)
    holdfirst=nltk.word_tokenize(store1)#storing the tokenized string (keywords) to remove punctuation
    parser = PlaintextParser.from_string(textss,Tokenizer(LANGUAGE))#storing the full text into an object
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    sentencess=[]
    compare=[]
    TEMP_FOLDER = tempfile.gettempdir()
    documents=sent_tokenize(textss)#storing sentences of full text
    summalen=len(documents)#storing the number of sentences
    stoplist = set('for a of the and to in'.split())

    for sentence in summarizer(parser.document,numofsent):
        hold=str(sentence)
        ttt=nltk.word_tokenize(hold)
        count=0
        for i in range(0, len(ttt)):
            for j in range(0,len(holdfirst)):
                if ttt[i]==holdfirst[j]:
                    count+=1
        compare.append(count)
        sentencess.append(str(sentence))

    texts = [[word for word in document.lower().split() if word not in stoplist]
              for document in documents]#storing an array of sentences where each sentence is a list of words without stopwords
    frequency = defaultdict(int)#storing a subclass that calls a factory function to supply missing values

    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
              for text in texts]#storing an array of words that occur more than once


    dictionary = corpora.Dictionary(texts)#storing a map of words
    dictionary.save(os.path.join(TEMP_FOLDER, 'deerwester.dict'))
    new_doc = str(textss.encode('utf-8'))#storing the utf-8 version of textss (original)
    new_vec = dictionary.doc2bow(new_doc.lower().split())#converting the utf-8 econded textss into a bag-of-words format = list of (token_id, token_count) 2-tuples. Each word is assumed to be a tokenized and normalized string (either unicode or utf8-encoded).

    corpus = [dictionary.doc2bow(text) for text in texts]#applying doc2bow to texts(list of  words that occur more than once) save into an array
    corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER, 'deerwester.mm'), corpus)
    dictionary = corpora.Dictionary.load( os.path.join(TEMP_FOLDER,  'deerwester.dict'))
    corpus = corpora.MmCorpus(os.path.join(TEMP_FOLDER,  'deerwester.mm'))
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
    doc = str(textss.encode('utf-8'))
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow]#converting the query to LSI space
    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save( os.path.join(TEMP_FOLDER,  'deerwester.index') )
    index = similarities.MatrixSimilarity.load( os.path.join(TEMP_FOLDER,  'deerwester.index') )
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    newlist=[]

    for i in range(0,summalen):
        newlist.append(documents[sims[i][0]])
        if i==4:
            break

    for sentencez in newlist:
        hold=str(sentencez)
        ttt=nltk.word_tokenize(hold)
        count=0

        for i in range(0, len(ttt)):
            for j in range(0,len(holdfirst)):
                if ttt[i]==holdfirst[j]:
                    count+=1
        compare.append(count)
        sentencess.append(str(sentencez))
    i=0
    while i<truereq:
        holdsubs=[]
        indexes=compare.index(max(compare))
        doc1=nlp( u'%s' %  str(sentencess[indexes]))
        parse=doc1
        for word in parse:
            if word.dep_ == 'nsubj':
                holdsubs.append(word.text.lower())
        if holdsubs:
            if holdsubs[0]!='they' and holdsubs[0]!='their' and holdsubs[0]!='both' and holdsubs[0]!='these' and holdsubs[0]!='this':
                countcomma=str(sentencess[indexes]).count(',')
                if countcomma<7:
                    output_sentences.append(sentencess[indexes])
                    i+=1
        del sentencess[indexes]
        del compare[indexes]
    return output_sentences
