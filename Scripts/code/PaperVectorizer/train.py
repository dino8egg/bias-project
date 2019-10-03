import sys
import time
from model import Doc2VecModel
from dataloader import data_tagger

PAPER_DIR = "/Users/hyungjun/Documents/2019_DSLAB/Bias/data/AAAI_2019_info.tsv"

def train(modelfile):
	model = Doc2VecModel()
	tagged_data = data_tagger(PAPER_DIR)

	start = time.time()
	model.fit(tagged_data)
	model.save_model(modelfile)
	print("Execution Time: {:.3} sec".format(time.time() - start))


if __name__=='__main__':
	train(sys.argv[1])
