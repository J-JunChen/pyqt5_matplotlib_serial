"""
==================
Animated line plot
==================

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib import style
import sys
import os
import serial
import serial.tools.list_ports
# from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QTimer

# style.use('fivethirtyeight')

dir_path = os.path.dirname(os.path.realpath(__file__))

file_path = dir_path+'/example.txt'

anchor_0 = np.array([0, 0], dtype=np.int64)
anchor_1 = np.array([7500, 0], dtype=np.int64)
anchor_2 = np.array([0, 5000], dtype=np.int64)

fig, ax = plt.subplots()

plt.xlabel("axis_X", fontsize=10)
plt.ylabel("axis_Y", fontsize=10)

plt.xlim(0,7500)
plt.ylim(0, 5000)

currentAxis = plt.gca()  # gca(): Get the current Axes
currentAxis.set_aspect('equal', adjustable='box')  # x,y 相同的分度尺


axis_x_point = [anchor_0[0], anchor_1[0], anchor_2[0]]
axis_y_point = [anchor_0[1], anchor_1[1], anchor_2[1]]
ax.scatter(axis_x_point, axis_y_point, s=100, c='blue',
           clip_on=False)  # clip_on = False：不裁剪原点

# plt.plot(anchor_0[0],anchor_0[1],anchor_1[0],anchor_1[1],c = "red",linewidth = 3)
ax.plot([anchor_0[0], anchor_1[0]],
        [anchor_0[1], anchor_1[1]], c="purple", linewidth=4)  # 在两点做出之间
ax.plot([anchor_0[0], anchor_2[0]], [
    anchor_0[1], anchor_2[1]], c="purple", linewidth=4)


brick_width = 1000  # 砖长：300mm
brick_height = 1000
brick_gap = 50  # 砖间隙：5mm

height_num = np.int(anchor_2[1]/brick_height)
width_num = np.int(anchor_1[0]/brick_width)


brick = np.zeros((width_num*height_num, 4), dtype=int)  # 可利用json数据类型


""" 砖摆放，从x,y轴出发 """
for j in range(height_num):
    for i in range(width_num):

        brick_x = i*(brick_gap+brick_width)
        brick_y = j*(brick_gap+brick_height)

        brick[i+j] = [i, j, brick_x, brick_y]  # 填写每一块砖的信息
        print(brick[i+j])

        rect = patches.Rectangle((brick_x, brick_y), brick_width, brick_height, linewidth=1,
                                 edgecolor='r', facecolor='none')
        # Add the patch to the Axes
        currentAxis.add_patch(rect)


# x, y = (0), (0)  # 元组数据结构，只能替换
# sc = ax.scatter(x, y)
dot, = ax.plot([],[],'ro')


def gen_dot():
    # graph_data = open(file_path, 'r').read()
    # lines = graph_data.split('\n')
    # for line in lines:
    #     if len(line) > 1:
    #         x,y = line.split(',')
    #         newdot = [x,y]
    #         yield newdot

    x = np.random.rand(1) *5000
    y = np.random.rand(1)*5000
    newDot = [x,y]
    yield newDot

def animate(newDot):
    dot.set_data(newDot[0],newDot[1])
    return dot,

ani = animation.FuncAnimation(
    fig, animate, frames=gen_dot,repeat=True)

plt.show() 
