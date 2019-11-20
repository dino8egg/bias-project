import csv
import random
import sys

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

# random.shuffle(negative)
# random.shuffle(positive)

# length = len(positive)
# negative_data = negative[:length]

# train_data = negative_data[:length//5*4]+positive[:length//5*4]
# test_data = negative_data[length//5*4:]+positive[length//5*4:]

train_data = []
with open("./data/train_1.tsv", 'r', encoding='UTF8') as f:
  reader = csv.reader(f, delimiter='\t')
  for line in reader:
    if len(line) > 0:
      train_data.append(line)

random.shuffle(train_data)

test_data = []
with open("./data/test_1.tsv", 'r', encoding='UTF8') as f:
  reader = csv.reader(f, delimiter='\t')
  for line in reader:
    if len(line) > 0:
      test_data.append(line)

random.shuffle(test_data)

target_data = positive+negative
target_x = [s[1] for s in target_data]

train_X = [s[1] for s in train_data]
train_y = [s[2] for s in train_data]
test_X = [s[1] for s in test_data]
test_y = [s[2] for s in test_data]

model = Doc2Vec.load(sys.argv[1])
train_X_doc2vec = [model.infer_vector(tokenize_string(s)) for s in train_X]
test_X_doc2vec = [model.infer_vector(tokenize_string(s)) for s in test_X]

sgd_doc2vec = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)
logreg_doc2vec = LogisticRegression(n_jobs=1, C=1e5)

sgd_doc2vec.fit(train_X_doc2vec, train_y)
logreg_doc2vec.fit(train_X_doc2vec, train_y)

target_X_doc2vec = [model.infer_vector(tokenize_string(s[0])) for s in target_x]
pred_y_sgd_target = sgd_doc2vec.predict(target_X_doc2vec)
pred_y_logreg_target = logreg_doc2vec.predict(target_X_doc2vec)

nb = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', MultinomialNB()),
              ])
sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
               ])
logreg = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', LogisticRegression(n_jobs=1, C=1e5)),
               ])

nb.fit(train_X, train_y)
sgd.fit(train_X, train_y)
logreg.fit(train_X, train_y)
pred_y_nb = nb.predict(target_x)
pred_y_sgd = sgd.predict(target_x)
pred_y_logreg = logreg.predict(target_x)

with open("./data/doc2vec_labeled_sgd.tsv", 'wt', encoding='UTF8') as f:
  writer = csv.writer(f, delimiter='\t')
  positive = 0
  negative = 0
  for i, line in enumerate(target_data):
    if pred_y_sgd_target[i] == "positive": positive += 1
    else: negative += 1
    writer.writerow([line[0], line[1], pred_y_sgd_target[i]])
  print("doc2vec sgd positive: "+str(positive))
  print("doc2vec sgd negative: "+str(negative))

with open("./data/doc2vec_labeled_logreg.tsv", 'wt', encoding='UTF8') as f:
  writer = csv.writer(f, delimiter='\t')
  positive = 0
  negative = 0
  for i, line in enumerate(target_data):
    if pred_y_logreg_target[i] == "positive": positive += 1
    else: negative += 1
    writer.writerow([line[0], line[1], pred_y_logreg_target[i]])
  print("doc2vec logreg positive: "+str(positive))
  print("doc2vec logreg negative: "+str(negative))

with open("./data/bow_labeled_nb.tsv", 'wt', encoding='UTF8') as f:
  writer = csv.writer(f, delimiter='\t')
  positive = 0
  negative = 0
  for i, line in enumerate(target_data):
    if pred_y_nb[i] == "positive": positive += 1
    else: negative += 1
    writer.writerow([line[0], line[1], pred_y_nb[i]])
  print("bow nb positive: "+str(positive))
  print("bow nb negative: "+str(negative))

with open("./data/bow_labeled_sgd.tsv", 'wt', encoding='UTF8') as f:
  writer = csv.writer(f, delimiter='\t')
  positive = 0
  negative = 0
  for i, line in enumerate(target_data):
    if pred_y_sgd[i] == "positive": positive += 1
    else: negative += 1
    writer.writerow([line[0], line[1], pred_y_sgd[i]])
  print("bow sgd positive: "+str(positive))
  print("bow sgd negative: "+str(negative))

with open("./data/bow_labeled_logreg.tsv", 'wt', encoding='UTF8') as f:
  writer = csv.writer(f, delimiter='\t')
  positive = 0
  negative = 0
  for i, line in enumerate(target_data):
    if pred_y_logreg[i] == "positive": positive += 1
    else: negative += 1
    writer.writerow([line[0], line[1], pred_y_logreg[i]])
  print("bow logreg positive: "+str(positive))
  print("bow logreg negative: "+str(negative))