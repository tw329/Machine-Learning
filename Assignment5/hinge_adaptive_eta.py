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
    if(trainlabels.get(int(a[1])) == 0):
        trainlabels[int(a[1])] = -1

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
eta = 0.0001
normw = 0
for j in range(0, cols-1, 1):
    normw += w[j]**2
obj = 0
for i in range(0, rows, 1):
    if trainlabels.get(i) != None:
        obj += max(0, 1 - trainlabels[i] * dot(w, data[i])) + (1/2) * normw

#print("start_obj = "+ str(obj))
pre_obj = obj + 1
#for k in range(100):
diff = 0.001
counter = 0
while(abs(pre_obj - obj) > diff):
# Compute Dellf
    dellf = []
    for j in range(0, cols, 1):
        dellf.append(0)
    for i in range(0, rows, 1):
        if trainlabels.get(i) != None:
            dp = dot(w, data[i])
            condition = dp * trainlabels[i]
            #print(condition)
            if condition < 1:
                for j in range(0, cols, 1):
                    dellf[j] += data[i][j] * trainlabels[i]
                #print(dellf)
            else:
                for j in range(0, cols, 1):
                    dellf[j] += 0
                #print(dellf)
    eta_list = [1, .1, .01, .001, .0001, .00001, .000001, .0000001, .00000001, .000000001, .0000000001, .00000000001]
    bestobj = 100000000000
    for k in range(0, len(eta_list), 1):
        eta = eta_list[k]
# Updata w
        for j in range(0, cols, 1):
            w[j] += (eta * (dellf[j]))
        pre_obj = obj
# Compute Obj
        normw = 0
        for j in range(0, cols-1, 1):
            normw += w[j]**2
        obj = 0
        for i in range(0, rows, 1):
            if trainlabels.get(i) != None:
                obj += max(0, 1 - trainlabels[i] * dot(w, data[i])) + (1/2) * normw
        if bestobj <= obj:
            bestobj = obj
            best_eta = eta_list[k]
        
        for j in range(0, cols, 1):
            w[j] -= (eta * dellf[j])
    #print("diff = "+ str(abs(pre_obj - obj)))
    #counter += 1


normw = 0
for j in range(0, cols-1, 1):
    normw += w[j]**2
obj = 0
for i in range(0, rows, 1):
    if trainlabels.get(i) != None:
        obj += max(0, 1 - trainlabels[i] * dot(w, data[i])) + (1/2) * normw

#print("start_obj = "+ str(obj))
pre_obj = obj + 1
#for k in range(100):
diff = 0.001
#counter = 0
while(abs(pre_obj - obj) > diff):
# Compute Dellf
    dellf = []
    for j in range(0, cols, 1):
        dellf.append(0)
    for i in range(0, rows, 1):
        if trainlabels.get(i) != None:
            dp = dot(w, data[i])
            condition = dp * trainlabels[i]
            #print(condition)
            if condition < 1:
                for j in range(0, cols, 1):
                    dellf[j] += data[i][j] * trainlabels[i]
                #print(dellf)
            else:
                for j in range(0, cols, 1):
                    dellf[j] += 0
                #print(dellf)
# Updata w
    for j in range(0, cols, 1):
        w[j] += (best_eta * (dellf[j]))
    pre_obj = obj
# Compute Obj
    normw = 0
    for j in range(0, cols-1, 1):
        normw += w[j]**2
    obj = 0
    for i in range(0, rows, 1):
        if trainlabels.get(i) != None:
            obj += max(0, 1 - trainlabels[i] * dot(w, data[i])) + (1/2) * normw


#print('final_obj = ' + str(obj))
#print("w = " + str(w))
normw = 0
for j in range(0, cols-1, 1):
    normw += w[j]**2
#print("\n")
normw = normw**(1/2)
#print("||w|| = "+ str(normw))
a = (w[len(w)-1]**2)**(1/2)
d_origin = a / normw
#print("distance to origin = " + str(d_origin))

# Prediction

for i in range(0, rows, 1):
    if (trainlabels.get(i) == None):
        dp = dot(w, data[i])
        if dp > 0:
            print("1 " + str(i))
        else:
            print("0 " + str(i))
#print('run_times = ' + str(counter))
