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
for i in range(len(data)):
    data[i].append(1.0)
                                
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

# Initialize, give random variable to w
#w = [1, 0, -4]
w = []
for j in range(0, cols, 1):
    w.append(.02 * random.random() - .01)
#print(w)
# Define inner product
def dot(u, v):
    rows_u = len(u)
    rows_v = len(v)

    if rows_u != rows_v:
        raise ArithmeticError('Error')
    
    sum_dot = 0.0
    for i in range(0, rows_u, 1):
        sum_dot += u[i]*v[i]
    return sum_dot

# Gradient Descent Iteration


eta = 0.001

obj = 0
for i in range(0, rows, 1):
    k = (1 + math.exp(-1 * dot(w, data[i])))**(-1)
    if trainlabels.get(i) != None:
        obj += (-1) * trainlabels[i] * math.log(k) - (1 - trainlabels[i])*math.log(1 - k)

print("start_obj = "+ str(obj))
pre_obj = obj + 1

diff = 0.001
counter = 0
#for k in range(100):
while abs(pre_obj - obj) > diff:
    # update w
    for i in range(0, rows, 1):
        if trainlabels.get(i) != None:

            dp = dot(w, data[i])

            k = (1 + math.exp(-1 * dp))**(-1)
            w[-1] += eta * (trainlabels[i] - k)
            
            for j in range(0, cols-1, 1):
                w[j] += eta * (trainlabels[i] - k) * data[i][j]
                
# Compute Obj
    
    pre_obj = obj
    obj = 0
    for i in range(0, rows, 1):
        dp = dot(w, data[i])
        k = (1 + math.exp(-1 * dp))**(-1)
        if trainlabels.get(i) != None:
            obj += (-1) * trainlabels[i] * math.log(k) - (1 - trainlabels[i]) * math.log(math.exp((-1)*dp)/(1+math.exp((-1)*dp)))

    counter += 1



print('final_obj = ' + str(obj))
print("w = " + str(w))
normw = 0
for j in range(0, cols-1, 1):
    normw += w[j]**2
print("\n")
normw = normw**(1/2)
print("||w|| = "+ str(normw))
a = (w[len(w)-1]**2)**(1/2)
d_origin = a / normw
print("distance to origin = " + str(d_origin))

# Prediction

for i in range(0, rows, 1):
    if (trainlabels.get(i) == None):
        dp = dot(w, data[i])
        if dp > 0:
            print("1 " + str(i))
        else:
            print("0 " + str(i))
print('run_times = ' + str(counter))
