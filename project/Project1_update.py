from sklearn import svm
import random
import sys

###read data

datafile = sys.argv[1]
f = open(datafile)
train = []
l = f.readline()

while(l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    train.append(l2)
    l = f.readline()
                                
rows = len(train)
cols = len(train[0])
f.close()
#print(rows)
#print(cols)
###read labels

labelfile = sys.argv[2]
f = open(labelfile)
labels = []
l = f.readline()
while(l != ''):
        a = l.split()
        labels.append(int(a[0]))
        l = f.readline()
f.close()
for i in labels:
        if i == 0:
                labels[i] = -1

##read test data

testfile = sys.argv[3]
f = open(testfile)
test = []
l = f.readline()

while(l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    test.append(l2)
    l = f.readline()

f.close()

def takeSecond(elem):
    return elem[1]

### feature selection pearson corr.
def pearson(data, label, final_features):
        new_data = data
        # mean of labels
        label_sum = 0
        for i in range(0, len(label), 1):
                label_sum += label[i]
        label_mean = label_sum/len(label)
        #corr of each cols
        corr = []
        for j in range(0, len(data[0]), 1):
                # mean of each cols
                col_sum = 0
                for i in range(len(data), 1):
                        col_sum += data[i][j]
                col_mean = col_sum/len(data[0])
                upp_sum = 0
                col_sum = 0
                lab_sum = 0
                for i in range(0, len(data), 1):
                        upp_sum += (data[i][j] - col_mean) * (label[i] - label_mean) 
                        col_sum += (data[i][j] - col_mean)**(2)
                        lab_sum += (label[i] - label_mean)**(2)
                r = upp_sum/((((col_sum)**(1/2))*((lab_sum)**(1/2)))+.000001)
                corr.append([j, abs(r)])
        corr.sort(key=takeSecond, reverse=True)
        stay_col = []
        for i in range(0, final_features, 1):
                stay_col.append(corr[i][0])
                #print(corr[i][1])
        remove_col = []
        for j in range(0, len(data[0]), 1):
                if j not in stay_col:
                        remove_col.append(j)
        return stay_col

                
random.seed()
 
rowIDs = []
for i in range(0, len(train), 1):
        rowIDs.append(i)
nsplits = 1 ##分成幾組
for x in range(0,nsplits,1):        
        #### Making a random train/validation split of ratio 90:10
        newtrain = []
        newlabels = []
        validation = []
        validationlabels = []
        #randomly reorder the row numbers      
                
        random.shuffle(rowIDs) 
        #print(rowIDs)
        for i in range(0, int(.9*len(rowIDs)), 1):
                newtrain.append(train[i])
                newlabels.append(labels[i])
        for i in range(int(.9*len(rowIDs)), len(rowIDs), 1):
                validation.append(train[i])
                validationlabels.append(labels[i])
        #### 特徵選擇
        stay_col = pearson(newtrain, newlabels, 20)
        newtrain_0 = []
        newtest_0 =[]
        for i in range(0, len(newtrain), 1):
                newtrain_0.append([])
                for j in stay_col:
                        newtrain_0[i].append(newtrain[i][j])
        for i in range(0, len(validation), 1):
                newtest_0.append([])
                for j in stay_col:
                        newtest_0[i].append(validation[i][j])

        #### Predict with SVM linear kernel for values of C={.001, .01, .1, 1, 10, 100} ###
        C = 0.01
        clf = svm.LinearSVC(C=C)
        clf.fit(newtrain_0, newlabels)
        prediction = clf.predict(newtest_0)
        pre_err = 100000000
        err = 0
        for i in range(0, len(prediction), 1):
                if(prediction[i] != validationlabels[i]):
                        err = err + 1
        if err < pre_err:
                best_feature = stay_col
                pre_err = err
        err = err/len(validationlabels)
        print(err)
        #error[C]+=err
        #print("err=",err,"C=",C,"split=",x)


bestC = 0.01
stay_col = best_feature
#print("Features:", stay_col)
newtrain = []
newtest =[]
for i in range(0, len(train), 1):
        newtrain.append([])
        for j in stay_col:
                newtrain[i].append(train[i][j])
for i in range(0, len(test), 1):
        newtest.append([])
        for j in stay_col:
                newtest[i].append(test[i][j])


clf = svm.LinearSVC(C=bestC)
clf.fit(train, labels)
prediction = clf.predict(test)
print('total feature number = 20')
f = open('feature.data', 'w')
for i in stay_col:
        f.write(str(i))
        f.write('\n')
f.close()
f = open('prediction.output', 'w')
for i in prediction:
        f.write(str(i))
        f.write('\n')
f.close()