import csv
import string
import multiprocessing
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# Data loading
PAPER_DIR = "/Users/hyungjun/Documents/2019_DSLAB/Bias/data/AAAI_2019_info.tsv"

paper_list = []
with open(PAPER_DIR, 'r', encoding='utf-8') as f:
	reader = csv.reader(f, delimiter='\t')
	paper_list = list(reader)

# Preprocessing
# tagged_data = [TaggedDocument(words=word_tokenize(paper[4].lower()), tags=paper[2]) for paper in paper_list]
tagged_data = []
cnt = 1
for paper in paper_list[:500]:
	title = paper[2].lower()
	abstract = paper[4].lower()

	tokens = word_tokenize(abstract)
	tokens = list(filter(lambda token: token not in string.punctuation, tokens))
	tokens = list(filter(lambda token: token not in stopwords.words('english'), tokens))
	
	tagged_token = TaggedDocument(words=tokens, tags=[title])
	cnt += 1
	tagged_data.append(tagged_token)

# Document Embedding
max_epochs = 100
vec_size = 100
alpha = 0.025
window = 8
cores = multiprocessing.cpu_count()

model = Doc2Vec(vector_size=vec_size,
	alpha=alpha,
	min_alpha=0.00025,
	min_count=20,
	window=8,
	dm=0,
	dbow_words=1,
	workers=cores,
	hs=1,
	negative=10)
  
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
	print('iteration {0}'.format(epoch))
	model.train(tagged_data,
		total_examples=model.corpus_count,
		epochs=model.epochs)
	model.alpha -= 0.0002
	model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")

# Testing
model= Doc2Vec.load("d2v.model")
test_data = word_tokenize("Research related to Image processing with GAN".lower())
v1 = model.infer_vector(test_data)
print("V1_infer", v1)

similar_doc = model.docvecs.most_similar([v1])
print(similar_doc)

