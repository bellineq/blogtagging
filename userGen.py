import pandas as pd
import numpy as np
import random
import string

userDf = pd.DataFrame()
columns = ['username', 'password']


result = [['user'+str(i), ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) 
for _ in range(4)) ] for i in range (100)]

result.append(['admin', ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) 
for _ in range(4))])

result.append(['guest',''])

userDf = pd.DataFrame(result, columns = ['username', 'password'])
userDf.to_csv('./data/user.csv', index=False)
