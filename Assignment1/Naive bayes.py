import sys

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
n = []
n.append(0)
n.append(0)
l = f.readline()
while(l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    n[int(a[0])] += 1

# Training

# calculate the sum of 1 and 0

m1 = []
m0 = []
for i in range(0, rows, 1):
    if trainlabels.get(i) != None and trainlabels[i] == 1:
        m1.append(i)
    if trainlabels.get(i) != None and trainlabels[i] == 0:
        m0.append(i)

sum1 = []
sum_sq1 = []
for i in range(0, cols, 1):
    sum1.append(0)
    sum_sq1.append(0)

for i in m1:
    for j in range(0, cols, 1):
        sum1[j] = sum1[j] + data[i][j]
        sum_sq1[j] = sum_sq1[j] + (data[i][j])**2  #for standard deviation

sum0 = []
sum_sq0 = []
for i in range(0, cols, 1):
    sum0.append(0)
    sum_sq0.append(0)

for i in m0:
    for j in range(0, cols, 1):
        sum0[j] = sum0[j] + data[i][j]
        sum_sq0[j] = sum_sq0[j] + (data[i][j])**2  #for standard deviation

for i in range(0, len(sum0), 1):
    sum0[i] = sum0[i] + 0.01
    sum1[i] = sum1[i] + 0.01

for i in range(0, len(sum_sq0), 1):
    sum_sq0[i] = sum_sq0[i] + 0.0001
    sum_sq1[i] = sum_sq1[i] + 0.0001
# calculate the means of 1 and 0

mean1 = [i/(len(m1)+1) for i in sum1]
mean0 = [i/(len(m0)+1) for i in sum0]

# calculate the standard deviation
 
var1 = []
for j in range(0, cols, 1):
    var1.append(0)
for j in range(0, cols, 1):
    var1[j] = ((sum_sq1[j]-(len(m1)+1)*(mean1[j]**2))/(len(m1)))**(1/2)

var0 = []
for j in range(0, cols, 1):
    var0.append(0)
for j in range(0, cols, 1):
    var0[j] = ((sum_sq0[j]-(len(m0)+1)*(mean0[j]**2))/(len(m0)))**(1/2)

# Prediction
for i in range(0, rows, 1):
    if trainlabels.get(i) == None:
        d0 = 0
        d1 = 0
        for j in range(0, cols, 1):
            d0 = d0 + ((data[i][j] - mean0[j])/var0[j])**2
            d1 = d1 + ((data[i][j] - mean1[j])/var1[j])**2
        if d0 < d1 :
            print("0", i)
        else:
            print("1", i)

