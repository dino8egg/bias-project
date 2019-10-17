# -*- coding: euc-kr -*-
import sys
import csv
import time
from gensim.models.doc2vec import Doc2Vec
from dataloader import data_loader, tokenize_string
import operator

TSV_DIR = './data/positive_labels.tsv'

def test2(modelfile):
	paper_list = data_loader('asfd')
	with open(TSV_DIR, 'wt', encoding='UTF8') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')
		for paper in paper_list[1344:]:
			title = paper[2].lower()
			abstract = paper[4].lower()
			tokenized_words = tokenize_string(abstract)
			abstract = ' '.join(tokenized_words)
			tsv_writer.writerow([title, abstract, 'positive', 0])

def test(modelfile):
	paper_list = data_loader('asfd')
	paper_dic = {}
	for i, paper in enumerate(paper_list):
		print(i)
		a = 3
		b = 5
		if i > 1343:
			a = 2
			b = 4
		title = paper[a].lower()
		abstract = paper[b].lower()
		tokenized_words = tokenize_string(abstract)
		paper_dic[title] = ' '.join(tokenized_words)
	print("dic complete")

	start = time.time()
	model = Doc2Vec.load(modelfile)

	print(model.docvecs.index_to_doctag(1344))
	print(len(model.docvecs))
	similarities = {}
	for s in range(1344):
		similarities[model.docvecs.index_to_doctag(s)] = 0

	all_papers = [model.docvecs.index_to_doctag(s) for s in range(1344)]
	ethics = [model.docvecs.index_to_doctag(s) for s in range(1344, len(model.docvecs))]
	for ethic_paper in ethics:
		for paper in all_papers:
			similarities[paper] += model.docvecs.similarity(ethic_paper, paper)

	sorted_papers = sorted(similarities.items(), key=operator.itemgetter(1))
	print("sort complete")
	print(sorted_papers)
	with open(TSV_DIR, 'wt', encoding='UTF8') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')
		for paper in sorted_papers:
			tsv_writer.writerow([paper[0], paper_dic[paper[0]], 'negative', paper[1]])


if __name__=='__main__':
	test2(sys.argv[1])
