import numpy as np
import matplotlib.pyplot as plt
import os, json
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import StandardScaler


def stringlist_to_list(list_as_string):
    list_as_list = json.loads(list_as_string)
    return list_as_list


def ev_k(p,o):
    ev = o*p-1
    return p*ev**2/(1+ev-p)


def kelly(p, o):
    return (p*o-1)/(o-1)


capital = 100
list_capital = [capital]
outcomes = ['H', 'D', 'A']
f = open(os.path.realpath(rf'new.txt'), 'r').read()
splited = f.split('\n')
for game in splited:
    outcome = game[0]
    odds = game[1:]
    probabilities = #do prediction stuff here for odds
    list_ev = []
    for i in range(3):
        list_ev.append(ev_k(probabilities[i], odds[i][-1]))
    if max(list_ev) > 0:
        p = probabilities[list_ev.index(max(list_ev))]
        o = odds[list_ev.index(max(list_ev))][-1]
        bet = capital * kelly(p,o)
        capital -= bet
        if outcome == outcomes[list_ev.index(max(list_ev))]:
            capital += bet * o
        list_capital.append(capital)

print(capital)
print(len(list_capital))
fig = plt.figure()
ax = fig.add_subplot(111)
points = ax.scatter(np.array(len(list_capital)), np.array(list_capital))
plt.show()