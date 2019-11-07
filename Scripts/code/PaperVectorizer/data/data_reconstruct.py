import pandas as pd
import csv

positive = []
with open("./positive_labels.tsv", 'r', encoding='UTF8') as f:
	reader = csv.reader(f, delimiter='\t')
	for line in reader:
		if len(line) > 0:
			positive.append(line)

negative = []
with open("./negative_labels.tsv", 'r', encoding='UTF8') as f:
	reader = csv.reader(f, delimiter='\t')
	for line in reader:
		if len(line) > 0:
			negative.append(line)

print(len(positive))
with open("./bert/train.tsv", 'wt', encoding='UTF8') as f:
	writer = csv.writer(f, delimiter='\t')
	# writer.writerow(['id', 'label', 'alpha', 'text'])
	for line in positive[:90]:
		writer.writerow([line[0], 1, 'a', line[1]])
	for line in negative[:90]:
		writer.writerow([line[0], 0, 'a', line[1]])

with open("./bert/dev.tsv", 'wt', encoding='UTF8') as f:
	writer = csv.writer(f, delimiter='\t')
	# writer.writerow(['id', 'label', 'alpha', 'text'])
	for line in positive[90:100]:
		writer.writerow([line[0], 1, 'a', line[1]])
	for line in negative[90:100]:
		writer.writerow([line[0], 0, 'a', line[1]])

with open("./bert/test.tsv", 'wt', encoding='UTF8') as f:
	writer = csv.writer(f, delimiter='\t')
	writer.writerow(['id', 'text'])
	for line in positive[100:126]:
		writer.writerow([line[0], line[1]])
	for line in negative[100:126]:
		writer.writerow([line[0], line[1]])