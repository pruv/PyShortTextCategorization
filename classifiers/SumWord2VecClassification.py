from collections import defaultdict

import numpy as np
from nltk import word_tokenize
from scipy.spatial.distance import cosine

from utils.classification_exceptions import ModelNotTrainedException


class SumEmbeddedVecClassifier:
    def __init__(self, wvmodel, classdict, vecsize=300):
        self.wvmodel = wvmodel
        self.classdict = classdict
        self.vecsize = vecsize
        self.trained = False

    def train(self):
        self.addvec = defaultdict(lambda : np.zeros(self.vecsize))
        for classtype in self.classdict:
            for shorttext in self.classdict[classtype]:
                self.addvec[classtype] += self.shorttext_to_embedvec(shorttext)
            self.addvec[classtype] /= np.linalg.norm(self.addvec[classtype])
        self.addvec = dict(self.addvec)
        self.trained = True

    def shorttext_to_embedvec(self, shorttext):
        vec = np.zeros(self.vecsize)
        tokens = word_tokenize(shorttext)
        for token in tokens:
            if token in self.wvmodel:
                vec += self.wvmodel[token]
        vec /= np.linalg.norm(vec)
        return vec

    def score(self, shorttext):
        if not self.trained:
            raise ModelNotTrainedException()
        vec = self.shorttext_to_embedvec(shorttext)
        scoredict = {}
        for classtype in self.classdict:
            scoredict[classtype] = 1 - cosine(vec, self.addvec[classtype])
        return scoredict