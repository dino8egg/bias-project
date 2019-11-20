import csv
import random
import sys
import pickle

# negative = []
# with open("./negative_labels.tsv", 'r', encoding='UTF8') as f:
# 	reader = csv.reader(f, delimiter='\t')
# 	for line in reader:
# 		if len(line) > 0:
# 			negative.append(line)

# positive = []
# with open("./positive_labels.tsv", 'r', encoding='UTF8') as f:
# 	reader = csv.reader(f, delimiter='\t')
# 	for line in reader:
# 		if len(line) > 0:
# 			positive.append(line)

# size = len(positive)
# negative = negative[:size]
# random.shuffle(negative)
# random.shuffle(positive)
# train = positive[:size//5*4]+negative[:size//5*4]
# test = positive[size//5*4:]+negative[size//5*4:]
# random.shuffle(train)
# random.shuffle(test)

# with open("./train_1.tsv", 'wt', encoding='UTF8') as f:
# 	writer = csv.writer(f, delimiter='\t')
# 	for line in train:
# 		writer.writerow(line)

# with open("./test_1.tsv", 'wt', encoding='UTF8') as f:
# 	writer = csv.writer(f, delimiter='\t')
# 	for line in test:
# 		writer.writerow(line)

negative = []
with open("./fat.csv", 'r', encoding='UTF8',  errors='ignore') as f:
	while True:
		# try:
		line = f.readline()
		print(line)
		if len(line) > 0:
			negative.append(line)
		else:
			break
		# except ValueError:
		# 	pass

print(len(negative))
with open("./fat_test.tsv", 'wt', encoding='UTF8') as f:
	writer = csv.writer(f, delimiter='\t')
	for line in negative:
		writer.writerow([line, 'positive'])