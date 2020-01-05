import csv
import string
from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def data_loader(paper_dir):
	aaai_paper_list = []
	with open("./data/AAAI_2019.csv", 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		aaai_paper_list = list(reader)

	print(len(aaai_paper_list))
	aies19_paper_list = []
	with open("./data/AIES_2019_info.tsv", 'r', encoding='CP949') as f:
		reader = csv.reader(f, delimiter='\t')
		aies19_paper_list = list(reader)

	print(len(aies19_paper_list))
	aies18_paper_list = []
	with open("./data/AIES_2018_info.tsv", 'r', encoding='CP949') as f:
		reader = csv.reader(f, delimiter='\t')
		aies18_paper_list = list(reader)

	print(len(aies18_paper_list))
	paper_list = aaai_paper_list+aies18_paper_list+aies19_paper_list
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
	for i, paper in enumerate(paper_list):
		a = 3
		b = 5
		if i > 1343:
			a = 2
			b = 4
		title = paper[a].lower()
		abstract = paper[b].lower()
		tokenized_words = tokenize_string(abstract)
		tagged_token = TaggedDocument(words=tokenized_words, tags=[title])
		tagged_data.append(tagged_token)

	return tagged_data

# data_loader('asdfasd')