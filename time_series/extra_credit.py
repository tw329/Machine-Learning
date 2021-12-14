import numpy as np
import pandas as pd
import sys
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
import csv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
## read file
with open("Sales_Transactions_Dataset_Weekly.csv", 'r') as f:
  reader = csv.reader(f)
  data_list = list(reader)
# remove title
del data_list[0]
# save product name then del
product_name = []
for i in range(0, len(data_list), 1):
    product_name.append(data_list[i][0])
for i in range(0, len(data_list), 1):
    del data_list[i][0]

data_size = len(data_list[0])
# remove useless data
for i in range(0, len(data_list), 1):
    for j in range(52, data_size, 1):
        del data_list[i][len(data_list[i])-1]
# transfer str to int
for i in range(0, len(data_list), 1):
    for j in range(0, len(data_list[0]), 1):
        data_list[i][j] = float(data_list[i][j])

#print(len(data_list))
## read windows

for window in [26]:
## cut data by window
# do to every product
    predict = []
    train_data = []
    train_label = []
    test_data = []
    test_label = []
    for i in range(0, len(data_list), 1):
        tmp = []
        for j in range(window, 0, -1):
            tmp.append(data_list[i][-1-window])
        test_data.append(tmp)
        test_label.append(data_list[i][-1])
        for j in range(0, len(data_list[i])-window-1, 1): #condider only train data, doesn't include week 51.
            tmp = []
            for k in range(0, window, 1):
                tmp.append(data_list[i][j+k])
            train_data.append(tmp)
            train_label.append(data_list[i][j+window])
    ## predict
    clf = Ridge(alpha=.1)
    clf.fit(train_data, train_label)
    predict=(clf.predict(test_data))
    '''
    clf = SVR(kernel='linear', C=1e3)
    clf.fit(train_data, train_label)
    predict.append(clf.predict(test_data))
    '''
## count error
    err_sum = 0
    for i in range(0, len(data_list), 1):
        err_sum += (predict[i] - data_list[i][-1])**2

    error = err_sum/len(data_list)

    for i in range(0, len(predict), 1):
        print(product_name[i], 'W51 sells:', round(predict[i]))
    print('Window =', window)
    print('Mean Square Error=', error)

