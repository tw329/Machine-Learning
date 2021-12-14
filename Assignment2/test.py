
# changing start index to 2 from 0 
#print (list(enumerate(s1,2))) 

import pandas as pd
import numpy as np

frame = pd.DataFrame(np.random.randn(6))
#print(frame)
a = lambda x : format(x, '.2f')
print(frame.applymap(a))

obj = pd.Series([7, 7, 7, 7, 2, 3, 4])
print(obj.rank(method='max', ascending=False))

b = [1, 2, 3]
b.append(4)
print(b)

a = 'a b c'
l2 = a.split()