import sys
import time
from gensim.models.doc2vec import Doc2Vec
from dataloader import tokenize_string
import operator

TSV_DIR = './data/negative_labels.tsv'

def test(modelfile, testfile):
	start = time.time()
	model = Doc2Vec.load(modelfile)

	tokens = []
	with open(testfile) as tf:
		test_txt = tf.read().lower()
		tokens = tokenize_string(test_txt)

	test_vec = model.infer_vector(tokens)
	similar_doc = model.docvecs.most_similar([test_vec])
	print("Similar Documents")
	print(similar_doc)
	print("Execution Time: {:.3} sec".format(time.time() - start))

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
	with open(TSV_DIR, 'wt') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')
		for paper in sorted_papers:
			tsv_writer.writerow(['2019', paper_section, paper_title, paper_authors, paper_abstract, pdf_url, '', paper_publish_date])


if __name__=='__main__':
	test(sys.argv[1], sys.argv[2])
