import csv
import random
import sys

from gensim.models.doc2vec import Doc2Vec
from dataloader import tokenize_string

negative = []
with open("./data/negative_labels.tsv", 'r', encoding='UTF8') as f:
  reader = csv.reader(f, delimiter='\t')
  for line in reader:
    if len(line) > 0:
      negative.append(line[0])

positive = []
with open("./data/positive_labels.tsv", 'r', encoding='UTF8') as f:
  reader = csv.reader(f, delimiter='\t')
  for line in reader:
    if len(line) > 0:
      positive.append(line[0])

negative = negative[:len(positive)]

model = Doc2Vec.load(sys.argv[1])
positive_vecs = [model.docvecs[v] for v in positive]
negative_vecs = [model.docvecs[v] for v in negative]
a = [model.docvecs[model.docvecs.index_to_doctag(i)] for i in range(1344, len(model.docvecs))]
print(model.most_similar(positive=positive_vecs, negative=negative_vecs, topn=50))
print(model.most_similar(positive=positive_vecs, topn=50))