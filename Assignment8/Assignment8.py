import sys
import random

# Read file
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

# Read number of cluster K
K = int(sys.argv[2])

# Assgin data to random cluster
num = round(rows/K)
last = rows - (num*(K-1))

tmp_list = []
for k in range(0, K-1, 1):
    for n in range(0, num, 1):
        tmp_list.append(k)
for n in range(num*(K-1), rows, 1):
    tmp_list.append(K-1)

random.shuffle(tmp_list)

#print(tmp_list)
label = {}
for i in range(0, rows, 1):
    label[i] = tmp_list[i]


# Compute Mean for each cluster
mean = []
for k in range(0, K, 1):
    mean.append([])
    for j in range(0, cols, 1):
        mean[k].append(0.0)

#print(label)
for i in range(0, rows, 1):
    for k in range(0, K, 1):
        if label[i] == k:
            for j in range(0, cols, 1):
                mean[k][j] += data[i][j]

for k in range(0, K-1, 1):
    for j in range(0, cols, 1):
        mean[k][j] = mean[k][j]/num

for j in range(0, cols, 1):
    mean[K-1][j] = mean[K-1][j]/last

# Define distance
def distance(data, mean):
    d = 0
    for j in range(0, cols, 1):
        d += (data[j] - mean[j])**2
    return d


obj = 0
for k in range(0, K, 1):
    for i in range(0, rows, 1):
        if label[i] == k:
            obj += distance(data[i], mean[k])

pre_obj = obj + 1
while obj - pre_obj < 0:
    #print(label)
    #print(obj-pre_obj)
    # Reassign cluster
    dis = []
    for k in range(0, K, 1):
        dis.append(0.0)
    for i in range(0, rows, 1):
        for k in range(0, K, 1):
            dis[k] = distance(data[i], mean[k])
        label[i] = dis.index(min(dis))
        #print(dis)
    # Recompute mean
    mean = []
    for k in range(0, K, 1):
        mean.append([])
        for j in range(0, cols, 1):
            mean[k].append(0.0)
    for i in range(0, rows, 1):
        for k in range(0, K, 1):
            if label[i] == k:
                for j in range(0, cols, 1):
                    mean[k][j] += data[i][j]

    for k in range(0, K-1, 1):
        for j in range(0, cols, 1):
            mean[k][j] = mean[k][j]/num

    for j in range(0, cols, 1):
        mean[K-1][j] = mean[K-1][j]/last
    pre_obj = obj
    obj = 0
    for k in range(0, K, 1):
        for i in range(0, rows, 1):
            if label[i] == k:
                obj += distance(data[i], mean[k])
    #print(obj, pre_obj)
    #print(t)
for i in range(0, rows, 1):
    print(label[i], i)