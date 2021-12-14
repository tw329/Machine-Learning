import sys
import random


def gini_split(data, trainlabels):
    pre_gini = 100000000
    rows = len(data)
    cols = len(data[0])
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
            else:
                break
            gini = (Lsize/rows)*(Lp/Lsize)*(1 - Lp) + (Rsize/rows)*(Rp/Rsize)*(1 - Rp)
                #print("gini =", gini)
            if gini < pre_gini:
                best_cols = j
                best_split = split[k]
                best_gini = gini
                pre_gini = gini
            
    return {'column': best_cols, 'value': best_split}


# Read Data

datafile = sys.argv[1]
f = open(datafile)
dataset = []
l = f.readline()

while(l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    dataset.append(l2)
    l = f.readline()
                                
rows = len(dataset)
cols = len(dataset[0])
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

vote = []
for i in range(0, rows, 1):
    vote.append(0)

for k in range(0, 100):
    #runs 100 times
    bootstrapping = [random.randint(0, rows) for everything in range(rows)]
    b_data = []
    for i in bootstrapping:
        if trainlabels.get(i) != None:
            b_data.append(dataset[i])
        
    b_label = []
    for i in bootstrapping:
        if trainlabels.get(i) != None:
            b_label.append(trainlabels[i])

    #create new dataset b_data by bootstrap
    stump = gini_split(b_data, b_label)

    c = stump['column']
    t = stump['value']
    #print(c)
    
    majority = [0, 0]
    for i in range(len(b_data)):
        if b_data[i][int(c)] < t:
            if b_label[i] == -1:
                majority[0] += 1
            else:
                majority[1] += 1
    if majority[0] > majority[1]:
        pre = -1
    else:
        pre = 1


    for i in range(0, rows, 1):
        if trainlabels.get(i) == None:
            if dataset[i][c] < t:
                vote[i] += pre
            else:
                vote[i] -= pre

for i in range(0, rows, 1):
    if trainlabels.get(i) == None:
        if vote[i] > 0:
            print('1', str(i))
        else:
            print('0', str(i))