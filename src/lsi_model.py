import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    return " ".join(re.findall(r"\b\w+\b", text.lower()))

class LSIModel:
    def __init__(self, num_topics=100, language="english"):
        self.num_topics = num_topics
        self.language = language

        # pipeline TF-IDF → SVD → Normalização (igual ao gensim)
        self.vectorizer = TfidfVectorizer(stop_words=language)
        self.svd = TruncatedSVD(n_components=num_topics)
        self.pipeline = make_pipeline(self.svd, Normalizer(copy=False))

        self.lsi_matrix = None
        self.documents = None

    def fit(self, documents):
        cleaned = [clean_text(d) for d in documents]
        self.documents = cleaned

        tfidf = self.vectorizer.fit_transform(cleaned)
        self.lsi_matrix = self.pipeline.fit_transform(tfidf)

    def transform(self, text):
        clean_t = clean_text(text)
        vec = self.vectorizer.transform([clean_t])
        return self.pipeline.transform(vec)[0]

    def similarity(self, query):
        q_vec = self.transform(query)
        sims = cosine_similarity([q_vec], self.lsi_matrix)[0]
        return sims

    def most_similar(self, query, topn=5):
        scores = self.similarity(query)
        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )
        return ranked[:topn]