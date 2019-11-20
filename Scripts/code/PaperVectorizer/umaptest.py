import csv
import random
import sys
import pickle

from gensim.models.doc2vec import Doc2Vec
from dataloader import tokenize_string

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer

negative = []
with open("./data/negative_labels.tsv", 'r', encoding='UTF8') as f:
	reader = csv.reader(f, delimiter='\t')
	for line in reader:
		if len(line) > 0:
			negative.append(line)

positive = []
with open("./data/positive_labels.tsv", 'r', encoding='UTF8') as f:
	reader = csv.reader(f, delimiter='\t')
	for line in reader:
		if len(line) > 0:
			positive.append(line)

model = Doc2Vec.load(sys.argv[1])
print(len(negative), len(positive))

# positive_vectors = [model.infer_vector(tokenize_string(s[1])) for s in positive]
# negative_vectors = [model.infer_vector(tokenize_string(s[1])) for s in negative]
# positive_labels = [0 for s in positive]
# negative_labels = [1 for s in negative]

# nb = Pipeline([('vect', CountVectorizer()),
#                ('tfidf', TfidfTransformer()),
#               ])

# positive_vectors = [s[1] for s in positive]
# negative_vectors = [s[1] for s in negative]
# cv = CountVectorizer()
# tfid = TfidfVectorizer(use_idf=True)
# positive_vectors = tfid.fit_transform(positive_vectors)
# negative_vectors = tfid.fit_transform(negative_vectors)
# print(type(positive_vectors[1]))

# model = TSNE(learning_rate=100)
# transformed = model.fit_transform(positive_vectors+negative_vectors)
# xs = transformed[:,0]
# ys = transformed[:,1]
# plt.scatter(xs, ys, c=positive_labels+negative_labels)
# plt.show()