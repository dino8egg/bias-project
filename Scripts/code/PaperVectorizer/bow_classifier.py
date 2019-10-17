import itertools
import os
import csv
import random

import numpy as np

from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from sklearn.metrics import confusion_matrix

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.preprocessing import text, sequence
from keras import utils

negative = []
with open("./data/negative_labels.tsv", 'r', encoding='UTF8') as f:
	reader = csv.reader(f, delimiter='\t')
	for line in reader:
		if len(line) > 0:
			negative.append(line)

positive = []
with open("./data/positive_labels.tsv", 'r', encoding='UTF8') as f:
	reader = csv.reader(f, delimiter='\t')
	for line in reader:
		if len(line) > 0:
			positive.append(line)

random.shuffle(negative)
random.shuffle(positive)

length = len(positive)
negative_data = negative[:length]

train_data = negative_data[:length//5*4]+positive[:length//5*4]
test_data = negative_data[length//5*4:]+positive[length//5*4:]

train_X = [s[1] for s in train_data]
train_y = [s[2] for s in train_data]
test_X = [s[1] for s in test_data]
test_y = [s[2] for s in test_data]

# train_size = int(len(df) * .7)
# train_posts = df['post'][:train_size]
# train_tags = df['tags'][:train_size]

# test_posts = df['post'][train_size:]
# test_tags = df['tags'][train_size:]

max_words = 10000
tokenize = text.Tokenizer(num_words=max_words, char_level=False)
tokenize.fit_on_texts(train_X) # only fit on train

x_train = tokenize.texts_to_matrix(train_X)
x_test = tokenize.texts_to_matrix(test_X)

encoder = LabelEncoder()
encoder.fit(train_y)
y_train = encoder.transform(train_y)
y_test = encoder.transform(test_y)

num_classes = np.max(y_train) + 1
y_train = utils.to_categorical(y_train, num_classes)
y_test = utils.to_categorical(y_test, num_classes)

batch_size = 32
epochs = 2

# Build the model
model = Sequential()
model.add(Dense(512, input_shape=(max_words,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
              
history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_split=0.1)

score = model.evaluate(x_test, y_test,
                       batch_size=batch_size, verbose=1)
print('Test accuracy:', score[1])