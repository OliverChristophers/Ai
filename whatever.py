import numpy as np
import matplotlib.pyplot as plt
import random
import scipy.stats

'''par = []
for i in range(30):
    par.append(scipy.stats.burr.rvs(1000, 1.317, -88, 88.41))'''

fig = plt.figure()
ax = fig.add_subplot(111)
#points_1 = ax.hist(np.array(par), bins=10)#, range=())
x = np.linspace(0, 1, 100)
points_6 = ax.plot(x, scipy.stats.burr.pdf(x, 5393116.767453392, 4.697790235849236, -109856.80302585084, 109856.7995706124)) #0.02037
points_6 = ax.plot(x, scipy.stats.burr.pdf(x, 1000, 4.7, -20.365, 20.36))
plt.show()
