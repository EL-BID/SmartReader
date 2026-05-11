import pickle
from collections import defaultdict

class SimpleDictionary:
    def __init__(self, docs=None):
        self.token2id = {}
        self.id2token = {}
        self.doc_freq = defaultdict(int)

        if docs:
            self.build(docs)

    def build(self, docs):
        # docs = lista de listas: [[word1, word2], [word3, word1], ...]
        for doc in docs:
            for token in set(doc):
                self.doc_freq[token] += 1
            for token in doc:
                if token not in self.token2id:
                    idx = len(self.token2id)
                    self.token2id[token] = idx
                    self.id2token[idx] = token

    def doc2bow(self, words):
        """Converte lista de palavras para Bag-of-Words: [(id, freq)]"""
        freq = defaultdict(int)
        for w in words:
            if w in self.token2id:
                freq[self.token2id[w]] += 1
        return list(freq.items())

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump((self.token2id, self.id2token, dict(self.doc_freq)), f)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            token2id, id2token, doc_freq = pickle.load(f)
        dic = SimpleDictionary()
        dic.token2id = token2id
        dic.id2token = id2token
        dic.doc_freq = defaultdict(int, doc_freq)
        return dic
