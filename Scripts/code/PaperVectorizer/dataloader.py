import csv
import string
from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def data_loader(paper_dir):
	paper_list = []
	with open(paper_dir, 'r', encoding='utf-8') as f:
		reader = csv.reader(f, delimiter='\t')
		paper_list = list(reader)

	return paper_list


def tokenize_string(text):
	tokens = word_tokenize(text)
	tokens = list(filter(lambda token: token not in string.punctuation, tokens))
	tokens = list(filter(lambda token: token not in stopwords.words('english'), tokens))

	return tokens


def data_tagger(paper_dir):
	paper_list = data_loader(paper_dir)

	# deactivated code: without tokenize_string preprocessing
	# tagged_data = [TaggedDocument(words=word_tokenize(paper[4].lower()), tags=paper[2]) for paper in paper_list]
	tagged_data = []
	for paper in paper_list:
		title = paper[2].lower()
		abstract = paper[4].lower()
		tokenized_words = tokenize_string(abstract)
		tagged_token = TaggedDocument(words=tokenized_words, tags=[title])
		tagged_data.append(tagged_token)

	return tagged_data