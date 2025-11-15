from __future__ import absolute_import, division, print_function, unicode_literals

import re
import os
import pickle
from collections import Counter

import nltk
from nltk import sent_tokenize, word_tokenize

import spacy
from spacy.lang.en import English

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Carregando modelo do spaCy
nlp = spacy.load("en_core_web_sm")

LANGUAGE = "english"

# ---------------------------------------------------
# Utilidades básicas (tokenização, salvamento, etc.)
# ---------------------------------------------------

def save_corpus(path, corpus):
    """Mantida por compatibilidade, caso queira reutilizar depois."""
    with open(path, "wb") as f:
        pickle.dump(corpus, f)


def load_corpus(path):
    """Mantida por compatibilidade, caso queira reutilizar depois."""
    with open(path, "rb") as f:
        return pickle.load(f)


def tokenize(text):
    """Tokenização simples em palavras alfanuméricas, minúsculas."""
    return re.findall(r"\b\w+\b", text.lower())


# ---------------------------------------------------
# Palavras-chave (substituindo gensim.summarization.keywords)
# ---------------------------------------------------

def get_keywords(text: str, topn: int = 10, language: str = LANGUAGE):
    """
    Extrai palavras-chave por frequência (bem simples), removendo
    algumas stopwords comuns em inglês.
    Retorna uma lista de strings.
    """
    if not text or not text.strip():
        return []

    # stopwords bem simples para não depender de downloads do NLTK
    basic_stopwords = {
        "the", "and", "to", "of", "in", "a", "is", "it", "for", "on", "that",
        "this", "with", "as", "by", "an", "be", "are", "at", "from", "or",
        "was", "were", "has", "have", "had", "but", "not", "can", "will",
        "would", "should", "could", "about", "into", "than", "then",
        "there", "their", "they", "them", "these", "those", "its", "we",
        "you", "your", "our", "us"
    }

    tokens = tokenize(text)
    tokens = [t for t in tokens if t not in basic_stopwords]
    freq = Counter(tokens)
    keywords_list = [w for w, _ in freq.most_common(topn)]
    return keywords_list


def keywords(text, words=10, split=True, language: str = LANGUAGE, **kwargs):
    """
    Wrapper compatível com a antiga gensim.summarization.keywords.
    Aceita 'words' (número de palavras) e ignora silenciosamente 'ratio',
    se alguém ainda passar.
    """
    # suporte opcional a ratio, apenas para não quebrar chamadas antigas
    ratio = kwargs.get("ratio", None)
    if ratio is not None:
        # heurística: número de palavras-chave em função do tamanho do texto
        approx_words = max(1, int(len(tokenize(text)) * ratio))
        words = approx_words

    kws = get_keywords(text, topn=words, language=language)
    return kws if split else "\n".join(kws)


# ---------------------------------------------------
# Similaridade por TF-IDF (substituindo MatrixSimilarity / LSI)
# ---------------------------------------------------

def build_model(texts):
    """
    Constrói um modelo TF-IDF para uma lista de textos.
    Retorna: vectorizer, tfidf_matrix
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix


def query_with_cosine(query_vec, docs_matrix, topn=10):
    """
    query_vec: (1, dim)
    docs_matrix: (n_docs, dim)
    Retorna lista [(idx, similaridade), ...] ordenada desc.
    """
    sims = cosine_similarity(query_vec, docs_matrix)[0]  # (n_docs,)
    top_idx = sims.argsort()[::-1][:topn]
    return list(zip(top_idx, sims[top_idx]))


# ---------------------------------------------------
# Função principal: get_summary (reimplementada)
# ---------------------------------------------------

def get_summary(textss, truereq, numofsent):
    """
    Gera resumo de `textss` retornando uma lista de frases.
    - truereq: número final de frases no resumo
    - numofsent: parâmetro mantido por compatibilidade (não é usado
      exatamente como antes, mas pode ser usado para ajustar tamanho).
    """

    # Garantir que temos texto utilizável
    if not textss or not textss.strip():
        return []

    # 1) Extrair frases do texto
    documents = sent_tokenize(textss)
    if len(documents) == 0:
        return []

    # 2) Extrair palavras-chave do texto completo
    #    (comportamento inspirado no gensim.summarization.keywords)
    kw_list = keywords(textss, words=20, split=True)
    kw_set = set(kw_list)

    # 3) Se quiser, também podemos usar um resumo inicial do SUMY
    #    como "filtro" de frases mais importantes
    parser = PlaintextParser.from_string(textss, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    # Pega algumas frases iniciais com SUMY (limitadas por numofsent)
    initial_candidates = [str(s) for s in summarizer(parser.document, numofsent)]
    candidate_set = set(initial_candidates)

    # 4) Montar listas de frases + pontuações (compare)
    sentencess = []
    compare = []

    for sent in documents:
        # Se SUMY foi usado, podemos priorizar frases que ele já sugeriu
        base_score = 1 if sent in candidate_set else 0

        # Overlap com palavras-chave
        tokens = tokenize(sent)
        overlap = sum(1 for t in tokens if t in kw_set)

        score = base_score + overlap
        sentencess.append(sent)
        compare.append(score)

    # 5) Selecionar as melhores `truereq` frases,
    #    aplicando o mesmo filtro de sujeito que você já usava.
    output_sentences = []
    i = 0

    # Evita loop infinito se truereq > número de frases
    truereq = min(truereq, len(sentencess))

    while i < truereq and sentencess:
        # índice da frase com maior score
        idx = compare.index(max(compare))

        sentence_candidate = sentencess[idx]
        doc_spacy = nlp(sentence_candidate)

        # Coletar sujeitos gramaticais (nsubj)
        subjects = [w.text.lower() for w in doc_spacy if w.dep_ == "nsubj"]

        use_sentence = True
        if subjects:
            bad_pronouns = {"they", "their", "both", "these", "this"}
            if subjects[0] in bad_pronouns:
                use_sentence = False

        if use_sentence:
            # Filtra frases exageradamente longas por número de vírgulas
            if sentence_candidate.count(",") < 7:
                output_sentences.append(sentence_candidate)
                i += 1

        # Remove essa frase das listas para não ser escolhida de novo
        del sentencess[idx]
        del compare[idx]

    return output_sentences