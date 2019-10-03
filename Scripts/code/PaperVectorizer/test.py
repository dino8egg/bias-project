import sys
import time
from gensim.models.doc2vec import Doc2Vec
from dataloader import tokenize_string

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


if __name__=='__main__':
	test(sys.argv[1], sys.argv[2])
