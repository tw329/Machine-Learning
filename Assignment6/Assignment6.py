import sys
import random
import math

# Read Data

datafile = sys.argv[1]
f = open(datafile)
data = []
l = f.readline()

while(l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()
                                
rows = len(data)
cols = len(data[0])
f.close()

# Read Labels
labelfile = sys.argv[2]
f = open(labelfile)
trainlabels = {}
l = f.readline()
while(l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    if(trainlabels.get(int(a[1])) == 0):
        trainlabels[int(a[1])] = -1

pre_gini = 100000000

for j in range(0, cols, 1):
    #print("cols =", j)
    split = []
    sort_tmp = []
    for i in range(0, rows, 1):
        sort_tmp.append(data[i][j])
        sort_tmp.sort()
    for i in range(0, rows-1, 1):
        split.append((sort_tmp[i] + sort_tmp[i+1])/2)
    #print(split)
    for k in range(0, len(split), 1):
        L_tmp = []
        R_tmp = []
        for i in range(0, rows, 1):
            #print("Split =", k)
            if data[i][j] <= split[k]:
                L_tmp.append(trainlabels[i])
            else:
                R_tmp.append(trainlabels[i])
        #print(L_tmp, R_tmp)
        if len(L_tmp) != 0 and len(R_tmp) != 0:
            Lp = L_tmp.count(-1)/len(L_tmp)
            Lsize = len(L_tmp)
            Rp = R_tmp.count(-1)/len(R_tmp)
            Rsize = len(R_tmp)
            #print(Lp, Rp)
        else:
            break
        gini = (Lsize/rows)*(Lp)*(1 - Lp) + (Rsize/rows)*(Rp)*(1 - Rp)
        #print("gini =", gini)
        if gini < pre_gini:
            best_cols = j
            best_split = split[k]
            best_gini = gini
            pre_gini = gini


print('cols:', best_cols, '\nsplit:', best_split, '\ngini:', best_gini)
    