import sys
import time
from gensim.models.doc2vec import Doc2Vec
from dataloader import data_loader, tokenize_string
import operator

TSV_DIR = './data/negative_labels.tsv'

def test(modelfile):
	paper_list = data_loader('asfd')
	paper_dic = {}
	for paper in paper_list:
		a = 3
		b = 5
		if i > 1343:
			a = 2
			b = 4
		title = paper[a].lower()
		abstract = paper[b].lower()
		tokenized_words = tokenize_string(abstract)
		paper_dic[title] = tokenized_words
	print("dic complete")

	start = time.time()
	model = Doc2Vec.load(modelfile)

	print(model.docvecs.index_to_doctag(1344))
	print(len(model.docvecs))
	similarities = {}
	for s in range(len(model.docvecs)):
		similarities[model.docvecs.index_to_doctag(s)] = 0

	all_papers = [model.docvecs.index_to_doctag(s) for s in range(1344)]
	ethics = [model.docvecs.index_to_doctag(s) for s in range(1344, len(model.docvecs))]
	for ethic_paper in ethics:
		for paper in all_papers:
			similarities[paper] += model.docvecs.similarity(ethic_paper, paper)

	sorted_papers = sorted(similarities.items(), key=operator.itemgetter(1))
	print("sort complete")
	with open(TSV_DIR, 'wt') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')
		for paper in sorted_papers:
			tsv_writer.writerow(['2019', paper_section, paper_title, paper_authors, paper_abstract, pdf_url, '', paper_publish_date])


if __name__=='__main__':
	test(sys.argv[1])
