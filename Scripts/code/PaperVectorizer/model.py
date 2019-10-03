import multiprocessing
from gensim.models.doc2vec import Doc2Vec

MAX_EPOCHS = 100
VEC_SIZE = 100
ALPHA = 0.025
MIN_ALPHA = 0.00025
MIN_COUNT = 20
WINDOW = 8
DM = 0
DBOW_WORDS = 1
HS = 1
NEGATIVE = 10
cores = multiprocessing.cpu_count()

class Doc2VecModel():
	def __init__(self):
		self.model = Doc2Vec(
			vector_size = VEC_SIZE,
			alpha = ALPHA,
			min_alpha = MIN_ALPHA,
			min_count = MIN_COUNT,
			window = WINDOW,
			dm = DM,
			dbow_words = DBOW_WORDS,
			workers = cores,
			hs = HS,
			negative = NEGATIVE
		)

	def fit(self, tag_data):
		print("Building Vocab")
		self.model.build_vocab(tag_data)

		print("Start training")
		for epoch in range(MAX_EPOCHS):
			print('iteration {0}'.format(epoch))
			self.model.train(tag_data,
				total_examples=self.model.corpus_count,
				epochs=self.model.epochs)
			self.model.alpha -= 0.0002
			self.model.min_alpha = self.model.alpha

	def save_model(self, filename):
		self.model.save(filename)
		print("Model saved")

	def load_model(self, filename):
		self.model = Doc2Vec.load(filename)
