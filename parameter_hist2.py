import json, os
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import pandas as pd
import random
from fitter import Fitter, get_common_distributions, get_distributions
import scipy.stats
import shin

def shin_standardisation(list_odds):
    list_shin = list(shin.calculate_implied_probabilities(list_odds)['implied_probabilities'])
    return [float(x) for x in list_shin]


def stringlist_to_list(list_as_string):
    list_as_list = json.loads(list_as_string)
    return list_as_list


bye = []
f = open(os.path.realpath(rf'test_gang.txt'), 'r').read()
splited = f.split('\n')
list_lists_all = []
for item in splited:
    inner = item.split(', ')
    list_lists_all.append(inner)

random.shuffle(list_lists_all)
list_x = []
list_parameter = []
n = 1
for match in list_lists_all:
    print(n)
    n += 1
    if n > 50000000:
        break
    else:
        if int(match[2]) > 0:
            list_lists_odds = []
            for i in [-3, -2, -1]:
                list_lists_odds.append(stringlist_to_list(match[i]))
            arb_sum = -1
            for lo in list_lists_odds:
                arb_sum += min(lo)
            list_parameter.append(arb_sum)
            '''for i in range(len(list_lists_odds[0])):
                list_bookmaker_x_shin = shin_standardisation([list_lists_odds[0][i], list_lists_odds[1][i], list_lists_odds[2][i]])
                list_parameter.append(list_bookmaker_x_shin[1] / (1 - list_bookmaker_x_shin[0]))'''

                    
'''fig = plt.figure()
ax = fig.add_subplot(111)
points = ax.scatter(np.array(list_x), np.array(list_parameter))
plt.show()'''



f = Fitter(random.sample(list_parameter, round(len(list_parameter)/1)), distributions=["burr"], timeout=120)
f.fit()
print(f.summary())
print(f.fitted_param)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set(title = '', xlabel = "", ylabel = "")
points_1 = ax.hist(np.array(list_parameter), bins=100)#, range=())
plt.show()
