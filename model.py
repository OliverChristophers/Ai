import numpy as np
import numpy as np
import os, json
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def stringlist_to_list(list_as_string):
    list_as_list = json.loads(list_as_string)
    return list_as_list


eye = []
bye = []
f = open(os.path.realpath(rf'test_gang.txt'), 'r').read()
splited = f.split('\n')
for i in splited:
    new1 = []
    new = i.split('; ')
    eye.append(stringlist_to_list(new[0]))
    for t in [2, 3, 4]:
        new1.append(stringlist_to_list(new[t]))
    
    bye.append(new1)


scaler = StandardScaler()
to = 300000
xtrain = bye
xtest = bye[to:]
ytrain = eye[0:to]
ytest = eye[to:]

xtrain = np.array(xtrain)
xtest = np.array(xtest)
ytrain = np.array(ytrain)
ytest = np.array(ytest)
model = Sequential()
model.add(LSTM(64, input_shape=(3, 7)))
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='adam', loss='mse', metrics=['MAE'])
model.fit(xtrain, ytrain, batch_size=4, epochs=2)


def ev(p,o):
    return o*p-1
 


def kelly(p, o):
    return (p*o-1)/(o-1)




capital = 100
list_capital = [capital]
outcomes = ['H', 'D', 'A']
f = open(os.path.realpath(rf'bet_ting.txt'), 'r').read()
splited = f.split('\n')


bye = []
f = open(os.path.realpath(rf'bet_ting.txt'), 'r').read()
splited = f.split('\n')
for i in splited:
    new1 = []
    new = i.split('; ')
    for t in [1, 2, 3]:
        new1.append(stringlist_to_list(new[t]))
    
    bye.append(new1)


list_probabilities = (model.predict(np.array(bye)))

for g in range(len(list_probabilities)):
    game = splited[g]
    probabilities = list_probabilities[g]
    game = game.split('; ')
    list_outcome = game[0]
    list_odds = game[1:]
    odds = []
    for i in list_odds:
        new = []
        for p in stringlist_to_list(i):
            new.append(1/p)
        odds.append(new)
    
    list_ev = []
    for i in range(3):
        list_ev.append(ev(probabilities[i], odds[i][-1]))
    if max(list_ev) > 0:
        p = probabilities[list_ev.index(max(list_ev))]
        o = odds[list_ev.index(max(list_ev))][-1]
        outcome = stringlist_to_list(list_outcome)[list_ev.index(max(list_ev))]
        bet = capital * kelly(p,o)
        capital -= bet
        if outcome == 1:
            capital += bet * o
        list_capital.append(capital)
print(capital)
print(len(list_capital))
fig = plt.figure()
ax = fig.add_subplot(111)
points = ax.scatter(np.array(range(len(list_capital))), np.array(list_capital))
plt.show()


'''
model.fit(xtrain, ytrain, batch_size=32, epochs=10)

test_loss, test_acc = model.evaluate(xtest, ytest)
print('Test accuracy:', test_acc)

predictions = model.predict(xtest)


for i in range(len(predictions)):
    if i >= 30:
        break
    print('True Value:', ytest[i])
    print('Prediction:', predictions[i])
    print('----------------------------------------------')

'''