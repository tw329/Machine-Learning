import sys
import random

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
n = []
n.append(0)
n.append(0)
l = f.readline()
while(l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    n[int(a[0])] += 1
    #if(trainlabels.get(int(a[1])) == 0):
    #    trainlabels[int(a[1])] = -1

# Initialize, give random variable to w
w = [1, 0, -4]
#for j in range(0, cols, 1):
#    w.append(.02 * random.random() - .01)

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
error = 0
for i in range(0, rows, 1):
    if trainlabels.get(i) != None:
        error += (trainlabels[i] - dot(w, data[i]))**2
print("first_error = "+ str(error))
pre_err = error + 1
error
for k in range(2):
# Compute Dellf
    dellf = []
    for j in range(0, cols, 1):
        dellf.append(0)
    for i in range(0, rows, 1):
        if trainlabels.get(i) != None:
            dp = dot(w, data[i])
            for j in range(0, cols, 1):
                dellf[j] += (trainlabels[i] - dp) * data[i][j]
    print("dellf = "+ str(dellf))


# Updata w
    for j in range(0, cols, 1):
        w[j] += (eta * dellf[j])
    
    pre_err = error
# Compute Error
    error = 0
    for i in range(0, rows, 1):
        if trainlabels.get(i) != None:
            error += (trainlabels[i] - dot(w, data[i]))**2
    print("error = "+ str(error))

print("w = " + str(w))
normw = 0
for j in range(0, cols-1, 1):
    normw += w[j]**2
print("\n")
normw = normw**(1/2)
print("||w|| = "+ str(normw))
a = (w[len(w)-1]**2)**(1/2)
d_origin = a/ normw
print("distance to origin = " + str(d_origin))

# Prediction

for i in range(0, rows, 1):
    if (trainlabels.get(i) == None):
        dp = dot(w, data[i])
        if dp > 0:
            print("1 " + str(i))
        else:
            print("0 " + str(i))



