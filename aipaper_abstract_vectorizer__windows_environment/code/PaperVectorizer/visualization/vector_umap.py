import umap
from sklearn.datasets import load_digits
import pickle
import matplotlib.pyplot as plt
import numpy as np
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')

data1 = None
data2 = None
label1 = None
label2 = None
with open('./python_binary_data/doc2vec_negative.embedding', 'rb') as f:
	data1 = pickle.load(f)
with open('./python_binary_data/doc2vec_positive.embedding', 'rb') as f:
	data2 = pickle.load(f)
with open('./python_binary_data/doc2vec_negative.label', 'rb') as f:
	label1 = pickle.load(f)
with open('./python_binary_data/doc2vec_positive.label', 'rb') as f:
	label2 = pickle.load(f)
labels = label1[-126:]+label2
print(len(label1))
print(len(label2))
label = []
for l in labels:
	if l == 'negative':
		label.append(0)
	else:
		label.append(1)


data = data1[-126:]+data2
embedding = umap.UMAP(n_neighbors=2).fit_transform(data, y=label)
fig, ax = plt.subplots(1, figsize=(7,5))
plt.scatter(*embedding.T, c=label, s=0.3, cmap='Spectral', alpha=1.0)
plt.setp(ax, xticks=[], yticks=[])
cbar = plt.colorbar(boundaries = np.arange(3) - 0.5)
cbar.set_ticks(np.arange(2))
cbar.set_ticklabels(['negative','positive'])
plt.title('Test')
plt.show()
print(embedding)
