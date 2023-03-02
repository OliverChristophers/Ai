import json, os
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from functions.structure_functions import correct_data    


f = open(os.path.realpath(rf'data\train_data.txt'), 'r').read()
list_first = f.split('\n')
list_correct_data = []
for incorrect_data in list_first:
    list_correct_data.append(correct_data(incorrect_data))

list_parameter = []
for match in list_correct_data:
    list_parameter.append(match[2])
    '''for venue_i in [2,3,4]:
        o, p, pd, u, ev, e = match[venue_i]
        k = (o * p - 1)**3 / ((o - 1) * ((o * p - 1)**2 + o**2 * 1 * e))
        e_p = k / (p - (1 - p) / (o - 1))
        list_parameter.append(e_p)'''

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set(title = 'n Bookmakers', xlabel = "", ylabel = "Frequency")
points_1 = ax.bar(np.array(range(3,10)), np.array(list_parameter))#, bins=100, range=(1, 1.1))
plt.show()
