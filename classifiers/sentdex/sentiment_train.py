import pickle
import random

from statistics import mode

import nltk
from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.tokenize import word_tokenize

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import LinearSVC

from processor import Processor

# Dataset(s)
print('Loading short_reviews')
short_pos = open('short_reviews/positive.txt','r').read()
short_neg = open('short_reviews/negative.txt','r').read()

documents = []
all_words = []

# Positive
print('Processing positive reviews')
pp_pos = Processor(data=short_pos.split('\n'), valid_word_tags=['J'], tag='pos')
pp_pos.run()
documents.extend(pp_pos.documents)
all_words.extend(pp_pos.tokenized_data)

# Negative
print('Processing negative reviews')
pp_neg = Processor(data=short_neg.split('\n'), valid_word_tags=['J'], tag='neg')
pp_neg.run()
documents.extend(pp_neg.documents)
all_words.extend(pp_neg.tokenized_data)

print('Pickling documents')
save_documents = open('pickled_algos/data/documents.pickle','wb')
pickle.dump(documents, save_documents)
save_documents.close()

word_features = list(nltk.FreqDist(all_words).keys())[:5000]

print('Pickling features')
save_word_features = open('pickled_algos/data/word_features5k.pickle','wb')
pickle.dump(word_features, save_word_features)
save_word_features.close()

print('Processing features')

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]

random.shuffle(featuresets)

training_set = featuresets[:10000]
testing_set = featuresets[10000:]

print('Training various classifiers')

# NaiveBayesClassifier
NaiveBayes_classifier = nltk.NaiveBayesClassifier.train(training_set)
print(f'{"NaiveBayes_classifier accuracy:":<40}{(nltk.classify.accuracy(NaiveBayes_classifier, testing_set)*100):<.2f}%')

save_classifier = open('pickled_algos/classifiers/NaiveBayes_classifier5k.pickle','wb')
pickle.dump(NaiveBayes_classifier, save_classifier)
save_classifier.close()

# MultinomialNB
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print(f'{"MNB_classifier accuracy:":<40}{(nltk.classify.accuracy(MNB_classifier, testing_set)*100):<.2f}%')

save_classifier = open('pickled_algos/classifiers/MNB_classifier5k.pickle','wb')
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

# BernoulliNB
BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print(f'{"BernoulliNB_classifier accuracy:":<40}{(nltk.classify.accuracy(BernoulliNB_classifier, testing_set)*100):<.2f}%')

save_classifier = open('pickled_algos/classifiers/BernoulliNB_classifier5k.pickle','wb')
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

# LogisticRegression
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print(f'{"LogisticRegression_classifier accuracy:":<40}{(nltk.classify.accuracy(LogisticRegression_classifier, testing_set)*100):<.2f}%')

save_classifier = open('pickled_algos/classifiers/LogisticRegression_classifier5k.pickle','wb')
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

# LinearSVC
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print(f'{"LinearSVC_classifier accuracy:":<40}{(nltk.classify.accuracy(LinearSVC_classifier, testing_set)*100):<.2f}%')

save_classifier = open('pickled_algos/classifiers/LinearSVC_classifier5k.pickle','wb')
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

# NuSVC
# NuSVC_classifier = SklearnClassifier(NuSVC())
# NuSVC_classifier.train(training_set)
# print(f'{"NuSVC_classifier accuracy:":<40}{(nltk.classify.accuracy(NuSVC_classifier, testing_set)*100):<.2f}%')

# save_classifier = open('pickled_algos/NuSVC_classifier5k.pickle','wb')
# pickle.dump(NuSVC_classifier, save_classifier)
# save_classifier.close()

# SGDClassifier
SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print(f'{"SGDC_classifier accuracy:":<40}{(nltk.classify.accuracy(SGDC_classifier, testing_set)*100):<.2f}%')

save_classifier = open('pickled_algos/classifiers/SGDC_classifier5k.pickle','wb')
pickle.dump(SGDC_classifier, save_classifier)
save_classifier.close()
