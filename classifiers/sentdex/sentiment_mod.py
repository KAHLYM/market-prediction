import pickle

from statistics import mode

from nltk.classify import ClassifierI
from nltk.tokenize import word_tokenize

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for classifier in self._classifiers:
            vote = classifier.classify(features)
            votes.append(vote)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for classifier in self._classifiers:
            vote = classifier.classify(features)
            votes.append(vote)
        choice_votes = votes.count(mode(votes))
        confidence = choice_votes / len(votes)
        return confidence

# Word features
word_features5k_f = open('pickled_algos/data/word_features5k.pickle', 'rb')
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

# NaiveBayesClassifier
open_file = open('pickled_algos/classifiers/NaiveBayes_classifier5k.pickle', 'rb')
NaiveBayes_classifier  = pickle.load(open_file)
open_file.close()

# MultinomialNB
open_file = open('pickled_algos/classifiers/MNB_classifier5k.pickle', 'rb')
MNB_classifier = pickle.load(open_file)
open_file.close()

# BernoulliNB
open_file = open('pickled_algos/classifiers/BernoulliNB_classifier5k.pickle', 'rb')
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

# LogisticRegression
open_file = open('pickled_algos/classifiers/LogisticRegression_classifier5k.pickle', 'rb')
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

# LinearSVC
open_file = open('pickled_algos/classifiers/LinearSVC_classifier5k.pickle', 'rb')
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

# SGDClassifier
open_file = open('pickled_algos/classifiers/SGDC_classifier5k.pickle', 'rb')
SGDC_classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VoteClassifier(NaiveBayes_classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

def sentiment(text):
    features = find_features(text)
    return voted_classifier.classify(features), voted_classifier.confidence(features)
