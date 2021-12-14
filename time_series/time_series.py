import numpy as np
import pandas as pd
import sys
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
import csv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
 
## read file
with open("time_series\Sales_Transactions_Dataset_Weekly.csv", 'r') as f:
  reader = csv.reader(f)
  data_list = list(reader)
# remove title
del data_list[0]
# remove product name
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


## read windows
for window in range(2, 51, 1):
## cut data by window
# do to every product
    predict = []
    for i in range(0, len(data_list), 1):
        train_data = []
        train_label = []
        test_data = []
        test_label = []
        tmp = []
        for j in range(window, 0, -1):
            tmp.append(data_list[i][-1-window])
        test_data.append(tmp)
        test_label.append(data_list[i][-1])
        for j in range(0, len(data_list[i])-window-1, 1):
            tmp = []
            for k in range(0, window, 1):
                tmp.append(data_list[i][j+k])
            train_data.append(tmp)
            train_label.append(data_list[i][j+window])
        ## predict
        
        clf = Ridge(alpha=1, normalize=False)
        clf.fit(train_data, train_label)
        predict.append(clf.predict(test_data))
        
        '''
        clf = SVR(kernel='linear', C=1e3)
        clf.fit(train_data, train_label)
        predict.append(clf.predict(test_data))
        '''
        '''
        clf = LinearRegression()
        clf.fit(train_data, train_label)
        predict.append(clf.predict(test_data))
        '''
        '''
        clf = Lasso(alpha=0.1)
        clf.fit(train_data, train_label)
        predict.append(clf.predict(test_data))
        '''
    ## count error
    err_sum = 0
    for i in range(0, len(data_list), 1):
        err_sum += (predict[i] - data_list[i][-1])**2

    error = err_sum/len(data_list)

    #print(predict)
    print('Window =', window)
    print('Mean Square Error=', error)

