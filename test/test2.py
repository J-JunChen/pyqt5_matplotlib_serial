import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

fig, ax = plt.subplots()
x, y = (),() #元组数据结构，只能替换
sc = ax.scatter(x,y)
plt.xlim(0, 7500)
plt.ylim(0, 5000)
currentAxis = plt.gca()  # gca(): Get the current Axes
currentAxis.set_aspect('equal', adjustable='box')  # x,y 相同的分度尺

def animate(i):
    x = (np.random.rand(1)*5000)
    y = (np.random.rand(1)*5000)
    sc.set_offsets(np.c_[x,y])

ani = matplotlib.animation.FuncAnimation(fig, animate, 
                frames=2, interval=100, repeat=True) 
plt.show()