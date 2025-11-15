from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from unidecode import unidecode

import sys, traceback, unicodedata, codecs, requests
import unicodedata
import spacy
from spacy.lang.en import English
nlp = spacy.load('en_core_web_sm')

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

from src.lsi_model import LSIModel
from src.SimpleDictionary import SimpleDictionary

import pickle

import logging
import nltk, re, os
from nltk import word_tokenize
from nltk import sent_tokenize


#from gensim.summarization import keywords
#from gensim.summarization import summarize
#from gensim import corpora, models, similarities
from collections import defaultdict, Counter
import tempfile

sentencess=[]
compare=[]
LANGUAGE = "english"

###### PARTE UM DO AJUSTE
def save_corpus(path, corpus):
    with open(path, "wb") as f:
        pickle.dump(corpus, f)

def load_corpus(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def query_with_cosine(query_vec, docs_matrix, topn=10):
    # query_vec: (1, dim) | docs_matrix: (n_docs, dim)
    sims = cosine_similarity(query_vec, docs_matrix)[0]  # (n_docs,)
    top_idx = np.argsort(-sims)[:topn]
    return list(zip(top_idx, sims[top_idx]))

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

###### REMOÇÃO DO GENSIM
def get_keywords(text: str, topn: int = 10, language: str = LANGUAGE):
    """
    Extrai palavras-chave usando TF-IDF em um único documento.
    Retorna lista de strings (keywords).
    """
    if not text or not text.strip():
        return []

    vectorizer = TfidfVectorizer(stop_words=language)
    tfidf = vectorizer.fit_transform([text])
    scores = tfidf.toarray()[0]
    terms = np.array(vectorizer.get_feature_names_out())

    if len(terms) == 0:
        return []

    topn = min(topn, len(terms))
    top_idx = np.argsort(-scores)[:topn]
    return terms[top_idx].tolist()

def keywords(text, words=10, split=True, language: str = LANGUAGE):
    kws = get_keywords(text, topn=words, language=language)
    return kws if split else "\n".join(kws)

#def build_model(texts):
#    vectorizer = TfidfVectorizer(stop_words='english')
#    tfidf_matrix = vectorizer.fit_transform(texts)
#    return vectorizer, tfidf_matrix

#def build_index(matrix):
#    """
#    matrix: ndarray (n_docs, dim)
#    retorna matriz normalizada igual ao MatrixSimilarity
#    """
#    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
#    return matrix / (norms + 1e-10)
'''
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


    dictionary = tokenize(texts)#storing a map of words
    dictionary.save(os.path.join(TEMP_FOLDER, 'deerwester.dict'))
    new_doc = str(textss.encode('utf-8'))#storing the utf-8 version of textss (original)
    new_vec = dictionary.doc2bow(new_doc.lower().split())#converting the utf-8 econded textss into a bag-of-words format = list of (token_id, token_count) 2-tuples. Each word is assumed to be a tokenized and normalized string (either unicode or utf8-encoded).

    corpus = [dictionary.doc2bow(text) for text in texts]#applying doc2bow to texts(list of  words that occur more than once) save into an array
    save_corpus(os.path.join(TEMP_FOLDER, 'deerwester.mm'), corpus)
    dictionary = tokenize.load( os.path.join(TEMP_FOLDER,  'deerwester.dict'))
    corpus = load_corpus(os.path.join(TEMP_FOLDER,  'deerwester.mm'))
    lsi = LSIModel(corpus, id2word=dictionary, num_topics=2)
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
'''
###### PRIMEIRA TENTATIVA DE CORREÇÃO
'''
def get_summary(textss, truereq, numofsent):
    """
    textss   : texto completo
    truereq  : número de sentenças que você realmente quer no resultado final
    numofsent: número de sentenças que o Sumy vai gerar como candidatos
    """
    if not textss or not textss.strip():
        return []

    # 1) Keywords do texto inteiro
    #    (ajuste 'words' se quiser mais/menos keywords)
    kw_list = keywords(textss, words=20, split=True)
    kw_set = set(kw_list)

    # 2) Candidatos iniciais com Sumy (LSA)
    parser = PlaintextParser.from_string(textss, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    # Sentenças originais
    documents = sent_tokenize(textss)
    summalen = len(documents)

    candidate_sentences = []
    candidate_scores = []

    for sentence in summarizer(parser.document, numofsent):
        s_text = str(sentence)
        tokens = [t.lower() for t in word_tokenize(s_text)]
        score = sum(1 for t in tokens if t in kw_set)
        candidate_sentences.append(s_text)
        candidate_scores.append(score)

    # 3) Complementar com sentenças mais similares ao texto completo via TF-IDF
    #    (sem LSI, sem MatrixSimilarity)
    if summalen > 0:
        # TF-IDF por sentença
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(documents)  # (n_docs, dim)

        # Vetor do documento completo
        full_doc_vec = vectorizer.transform([textss])       # (1, dim)

        # Similaridade de cosseno texto completo x sentenças
        sims = cosine_similarity(full_doc_vec, tfidf_matrix)[0]  # (n_docs,)

        # Pega as top sentenças mais similares
        order = np.argsort(-sims)
        extra_sentences = []
        extra_scores = []

        for idx in order:
            s_text = documents[idx]
            if s_text in candidate_sentences:
                continue  # já está nos candidatos Sumy

            tokens = [t.lower() for t in word_tokenize(s_text)]
            kw_score = sum(1 for t in tokens if t in kw_set)
            extra_sentences.append(s_text)
            extra_scores.append(kw_score)

            if len(extra_sentences) >= numofsent:
                break

        candidate_sentences.extend(extra_sentences)
        candidate_scores.extend(extra_scores)

    # 4) Agora faz o filtro gramatical com spaCy,
    #    priorizando sentenças com mais overlap de keywords
    output_sentences = []
    i = 0

    while i < truereq and candidate_sentences:
        # acha sentença com maior score
        best_idx = int(np.argmax(candidate_scores))
        best_sentence = candidate_sentences[best_idx]
        best_score = candidate_scores[best_idx]

        # se score é 0, provavelmente o resto não é tão relevante
        if best_score == 0 and output_sentences:
            break

        # Analisa sujeito com spaCy
        doc = nlp(best_sentence)
        subjects = [w.text.lower() for w in doc if w.dep_ == "nsubj"]

        # Regras parecidas com o seu código original
        if subjects:
            subj = subjects[0]
            if subj not in ("they", "their", "both", "these", "this"):
                if best_sentence.count(",") < 7:
                    output_sentences.append(best_sentence)
                    i += 1

        # remove a sentença usada
        del candidate_sentences[best_idx]
        del candidate_scores[best_idx]

    return output_sentences
'''
###### SEGUNDA TENTATIVA DE CORREÇÃO
