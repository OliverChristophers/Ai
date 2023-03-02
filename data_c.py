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
f = open(os.path.realpath(rf'structured_g_data.txt'), 'r').read()
splited = f.split('\n')
for i in splited:
    new1 = []
    new = i.split('; ')
    eye.append(stringlist_to_list(new[0]))
    for t in [2, 3, 4]:
        new1.append(stringlist_to_list(new[t]))
    
    bye.append(new1)


scaler = StandardScaler()
to = 900000
xtrain = bye[0:to]
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
model.fit(xtrain, ytrain, batch_size=32, epochs=4)


def ev_k(p,o):
    ev = o*p-1
    return p*ev**2/(1+ev-p)


def kelly(p, o):
    return (p*o-1)/(o-1)


capital = 100
list_capital = [capital]
outcomes = ['H', 'D', 'A']
f = open(os.path.realpath(rf'bet_ting.txt'), 'r').read()
splited = f.split('\n')
j = 0
for game in splited:
    game = game.split('; ')
    outcome = game[0]
    list_odds = game[1:]
    odds = []
    for i in list_odds:
        new = []
        for p in stringlist_to_list(i):
            new.append(p)
        odds.append(new)
    new = [odds]

    


    probabilities = (model.predict(np.array(new)))[0]


    print(odds)
    print(probabilities)
    j += 1
    if j == 10:
        quit()
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