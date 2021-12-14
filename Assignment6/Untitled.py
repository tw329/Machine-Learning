import sys
import numpy as np

def bootstrap(train_data, train_label):
	boot_data = np.zeros(train_data.shape)
	boot_label = np.zeros(train_label.shape)
	rows = len(train_data)
	for i in range(rows):
		ran = np.random.randint(0, rows-1)
		boot_data[i] = train_data[ran]
		boot_label[i] = train_label[ran]
	return boot_data, boot_label

def stump(data, labels):
	rows = len(data)
	cols = len(data[0])
	ret = np.zeros((cols, 3))
	for i in range(cols):
		tmplabel = np.concatenate((data.T[i].reshape(rows,1), labels.reshape(rows,1)), axis = 1)
		tmplabel = tmplabel[tmplabel[:,0].argsort()]
		for j in range(1, max(1, rows-1)):
			lsize = j
			lp = 0
			for k in range (j):
				if tmplabel[k][1] == -1:
					lp += 1
			rsize = rows - j
			rp = 0 
			for k in range (j, rows):
				if tmplabel[k][1] == -1:
					rp += 1
			gini =	(lsize/rows)*(lp/lsize)*(1-lp/lsize)+(rsize/rows)*(rp/rsize)*(1-rp/rsize)
			if j == 1:
				ret[i][0] = gini
				ret[i][1] = j
				ret[i][2] = (tmplabel[j-1][0]+tmplabel[j][0])/2
			else:
				if ret[i][0] > gini:
					ret[i][0] = gini
					ret[i][1] = j
					ret[i][2] = (tmplabel[j-1][0]+tmplabel[j][0])/2
	ans = np.zeros(4)
	ans = np.concatenate((ret[0],[0]))
	for i in range(1, cols):
		if ans[0] > ret[i][0]:
			ans = np.concatenate((ret[i],[i]))
	
	# gini, row, threshold, column
	print('gini', ans[0], 'col', ans[3], 'thres', ans[2])
	return ans[3], ans[2]

def majority(data, label, c, t):
	majority = np.zeros(2)
	for i in range(len(data)):
		if data[i][int(c)] < t:
			if label[i] == -1:
				majority[0] += 1
			else:
				majority[1] += 1
	if majority[0] > majority[1]:
		return -1 # -1 is more than 1
	else:
		return 1
#--------------------------------
# input data
f= open(sys.argv[1], 'r')
train_data = np.loadtxt(f)
f.close()
rows = len(train_data)
cols = len(train_data[0])

#--------------------------------
# input labels
train_labels = np.full(rows, None)
f= open(sys.argv[2], 'r')
l = f.readline()
while(l != ''):
	a = l.split()
	if int(a[0]) == 0:
		train_labels[int(a[1])] = -1
	else:
		train_labels[int(a[1])] = int(a[0])
	l = f.readline()
f.close()

#--------------------------------
# input labels
test_labels = np.full(rows, None)
f= open(sys.argv[3], 'r')
l = f.readline()
while(l != ''):
	a = l.split()
	if int(a[0]) == 0:
		test_labels[int(a[1])] = -1
	else:
		test_labels[int(a[1])] = int(a[0])
	l = f.readline()
f.close()

#--------------------------------
test_prediction = np.zeros(rows)
test_data = train_data
for k in range(100):
	boot_data, boot_label = bootstrap(train_data, train_labels)
	c, t = stump(boot_data, boot_label)  # best colm and threshold k s
	# c < t, majority
	maj = majority(train_data, train_labels, c, t)  # return after split is -1 more or 1 more
	for j in range(len(test_data)):
		if test_data[j][int(c)] < t:
			test_prediction[j] += maj      # For same test data test against every bootstarp result 
		else:
			test_prediction[j] -= maj

for j in range(len(test_labels)):
	if test_labels[j] == None:
		if test_prediction[j] > 0:
			print(1, j)
		else:
			print(0, j)
