import csv
import random
import sys
import os
import time
import operator

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


AAAI_DIR = './data/data1'

def test(modelfile):
  start = time.time()

  train_data = []
  with open("./data/train_1.tsv", 'r', encoding='UTF8') as f:
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
      if len(line) > 0:
        train_data.append(line)

  random.shuffle(train_data)

  train_X = [s[1] for s in train_data]
  train_y = [s[2] for s in train_data]

  model = Doc2Vec.load(modelfile)
  train_X_doc2vec = [model.infer_vector(tokenize_string(s)) for s in train_X]

  sgd_doc2vec = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)
  # logreg_doc2vec = LogisticRegression(n_jobs=1, C=1e5)

  sgd_doc2vec.fit(train_X_doc2vec, train_y)
  # logreg_doc2vec.fit(train_X_doc2vec, train_y)

  filenames = os.listdir(AAAI_DIR)
  for filename in filenames:
    fullname = AAAI_DIR+'/'+filename

    aaai_info = []
    with open(fullname, 'r', encoding='UTF8') as tf:
      reader = csv.reader(tf)
      for line in reader:
        aaai_info.append(line)

    aaai_vectors = [model.infer_vector(tokenize_string(s[5])) for s in aaai_info]
    pred_sgd_doc2vec2 = sgd_doc2vec.predict(aaai_vectors)
    # pred_logreg_doc2vec2 = logreg_doc2vec.predict(test_X_doc2vec)

    with open("./labeled_data/"+filename, 'wt') as out_file:
      csv_writer = csv.writer(out_file)
      for i, paper in enumerate(aaai_info):
        csv_writer.writerow(paper+[pred_sgd_doc2vec2[i]])


if __name__=='__main__':
  # Use models/aaai_aies.model for labeling
  test('./models/aaai_aies2.model')