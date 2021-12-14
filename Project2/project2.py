from sklearn.svm import LinearSVC
import sys
import random
import math
import numpy as np
from  warnings import simplefilter
from sklearn.exceptions import ConvergenceWarning
simplefilter("ignore", category=ConvergenceWarning)

## input data
datafile = sys.argv[1]
f = open(datafile, 'r')
data = []
l = f.readline()

while (l != '') :
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()
f.close()
rows = len(data)
cols = len(data[0])

## input label
labelfile = sys.argv[2]
f = open(labelfile)
trainlabels = {}
l = f.readline()
while(l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    if(trainlabels.get(int(a[1])) == -1):
        trainlabels[int(a[1])] = 0

train = []
trainlabel =[]
for i in range(0, rows, 1):
    if trainlabels.get(i) != None:
        train.append(data[i])
        trainlabel.append(trainlabels[i])

newtrain = []
newtrainlabels = []
newtest = []
newtestlabels = []
rowID = []
for i in range(0, len(train), 1):
    rowID.append(i)
random.shuffle(rowID)
for i in rowID[:int(.9*len(rowID))]:
    newtrain.append(train[i])
    newtrainlabels.append(trainlabel[i])
for i in rowID[int(.9*len(train)):]:
    newtest.append(train[i])
    newtestlabels.append(trainlabel[i])



## dot
def dot(u, v):
    rows_u = len(u)
    rows_v = len(v)

    if rows_u != rows_v:
        raise ArithmeticError('Error')
    
    sum_dot = 0.0
    for i in range(0, rows_u, 1):
        sum_dot += u[i]*v[i]
    return sum_dot

## create classifier
clf = LinearSVC(max_iter=10000)

## predict

clf.fit(newtrain, newtrainlabels)
prediction = clf.predict(newtest)

error = 0
for i in range(0, len(newtestlabels), 1):
    if prediction[i] != newtestlabels[i]:
        error += 1

f = open('result.txt', 'w')
f.write('Original data representation:')
f.write(str(round((error/len(newtestlabels))*100, 2)))
f.write(" %")
f.write('\n')



z_train = []
z_test = []
for abc in [10, 100, 1000, 10000]:
    z_train = []
    z_test = []
    for i in range(0, abc, 1):
        z_train.append(0.0)
        z_test.append(0.0)
    for k in range(0, abc, 1):
        w = []
        for j in range(0, cols, 1):
            w.append(random.uniform(-1, 1))
        wtx = []
        for i in range(0, len(newtrain), 1):
            wtx.append(dot(newtrain[i], w))
        w0 = random.uniform(min(wtx), max(wtx))
        tmp = []
        for i in range(0, len(newtrain), 1):
            if (dot(newtrain[i], w) + w0) <= 0:
                tmp.append(0)
            else:
                tmp.append(1)
        z_train[k] = tmp
        tmp = []
        for i in range(0, len(newtest), 1):
            if (dot(newtest[i], w) + w0) <= 0:
                tmp.append(0)
            else:
                tmp.append(1)
        z_test[k] = tmp

    z_train = list(map(list, zip(*z_train)))
    z_test = list(map(list, zip(*z_test)))

    '''
    z_train_ar = np.asarray(z_train)
    z_test_ar = np.asarray(z_test)
    trainlabel_ar = np.asarray(newtrainlabels)
    testlabel_ar = np.asarray(newtestlabels)
    '''
#print(len(z_train), len(newtrainlabels))
#print(len(z_test), len(newtestlabels))

    ## create classifier
    clf2 = LinearSVC(max_iter=10000)

## predict

    clf2.fit(z_train, newtrainlabels)
    prediction_2 = clf2.predict(z_test)

    error_2 = 0
    for i in range(0, len(newtestlabels), 1):
        if prediction_2[i] != newtestlabels[i]:
            error_2 += 1
    f.write("K =")
    f.write(str(abc))
    f.write("\n")
    f.write("New representation error:")
    f.write(str(round((error_2/len(newtestlabels))*100, 2)))
    f.write(" %\n")
    #print('K =', abc)
    #print('New representation error:', round((error_2/len(newtestlabels))*100, 2), '%')
    print("When K = ", abc, ", prediction:")
    for i in range(0, len(prediction_2), 1):
        print(prediction_2[i], i)
f.close()


