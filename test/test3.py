import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

fig, ax = plt.subplots()  
ax.grid()  

data = np.cumsum(np.random.normal(size=100)) #some list of data
sc, = ax.plot(data[::2], data[1::2], marker="o", ls="") # set linestyle to none

def plot(a, data):
    data += np.cumsum(np.random.normal(size=100)+3e-2)
    sc.set_data(data[::2], data[1::2])
    ax.relim()
    ax.autoscale_view(True,True,True)

ani = matplotlib.animation.FuncAnimation(fig, plot, fargs=(data,),
            frames=4, interval=100, repeat=True) 
plt.show()