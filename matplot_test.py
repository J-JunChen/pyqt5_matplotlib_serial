import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

# file_path = 'D://PythonCode//CAD//data.txt'
file_path = dir_path+'/data.txt'

fig = plt.figure()
ax = fig.add_subplot(111)


def open_file(i):
    with open(file_path) as file_object:
        for line in file_object:
            # print(line)
            data = line.split()
            if len(data) == 10:
                # print(data)
                if(data[0] == 'ma'):  # 表示基站0到基站x的距离
                    if(data[1] != '0e'):  # MASK=e(0000 1111)表示 RANGE0,RANGE1,RANGE2,RANGE3 都有效
                        print("ma's Range 只有 "+data[1]+" 工作。")
                        # break
                    else:
                        # 16进制转为10进制，距离单位：mm
                        # range_0 = int(data[2],16) range_0没有'ma'对应的操作说明
                        range_1 = int(data[3], 16)
                        range_2 = int(data[4], 16)
                        range_3 = int(data[5], 16)
                        print("基站0到基站1的距离：%d" % (range_1)+"，基站0到基站2的距离：%d" %
                              (range_2)+"，基站0到基站3的距离：%d" % (range_3))

                else:  # data[0] == 'mc' or 'mr' ：表示标签x到基站y的距离
                    if(data[1] != '0f'):  # MASK=7(0000 0111)表示 RANGE0,RANGE1,RANGE2 都有效
                        print("mc's Range 只有 "+data[1]+" 工作。")
                        # break
                    else:
                        # 16进制转为10进制，距离单位：mm
                        range_0 = int(data[2], 16)
                        range_1 = int(data[3], 16)
                        range_2 = int(data[4], 16)
                        range_3 = int(data[5], 16)
                        print("标签x到基站0的距离：%d" % (range_0)+"，标签x到基站1的距离：%d" % (range_1) +
                              "，标签x到基站2的距离：%d" % (range_2)+"，标签x到基站3的距离：%d" % (range_3))

                        # anchor_0 = (0,0)
                        # anchor_1 = (7500,0) # X轴
                        # anchor_2= (0,5000) # 第三条轴，不一定是Y轴
                        anchor_0 = np.array([0, 0])
                        anchor_1 = np.array([7500, 0])
                        anchor_2 = np.array([0, 5000])
                        tag_position = getLocation(
                            anchor_0, anchor_1, anchor_2, range_0, range_1, range_2)

                        print("标签坐标X:%d" %
                              tag_position[0]+"，Y:%d" % tag_position[1])
                        
                        ax.clear()
                        ax.scatter(tag_position[0],tag_position[1] , s=100, c='green',
                                   clip_on=False)  # clip_on = False：不裁剪原点


def getLocation(anchor_0, anchor_1, anchor_2, range_0, range_1, range_2):
    """ 根据trilateration 计算标签的坐标 """
    tag_position = np.array([0, 0])
    tag_position[0] = (range_0**2 - range_1**2 +
                       anchor_1[0]**2)/(2*anchor_1[0])
    distance = range_0**2 - tag_position[0]**2
    tag_position[1] = np.sqrt(distance)
    return tag_position


anchor_0 = np.array([0, 0], dtype=np.int64)
anchor_1 = np.array([7500, 0], dtype=np.int64)
anchor_2 = np.array([0, 5000], dtype=np.int64)


# plt.xticks(np.arange(0,7500,step = 1000))
# plt.yticks(np.arange(0,5000,step = 1000))
plt.xlabel("axis_X", fontsize=10)
plt.ylabel("axis_Y", fontsize=10)

plt.xlim(0, 7500)
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

""" # Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-')

# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2) 
"""
# plt.minorticks_on()
# plt.grid(b=True, which='minor', color='#666666',axis= 'x', linestyle='-')

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


""" 铺好砖就涂上颜色 """
""" for j in range(height_num):
    for i in range(width_num):
        brick_x = i*(brick_gap+brick_width)
        brick_y = j*(brick_gap+brick_height)
        
        rect = patches.Rectangle((brick_x,brick_y), brick_width, brick_height, linewidth=1,
                                edgecolor='r', facecolor='yellow')
        # Add the patch to the Axes
        currentAxis.add_patch(rect)  
 """

""" 动态 """
# x = np.arange(0, 2000*np.pi, 10)
# line, = ax.plot(x, np.sin(x))

# def init():  # only required for blitting to give a clean slate.
#     line.set_ydata([np.nan] * len(x))
#     return line,


def animate(i):
    graph_data = open(dir_path+'\example.txt','r').read()
    lines = graph_data.split('\n')
    xs=[]
    ys=[]
    for line in lines:
        if len(line)>1:
            x,y= line.split(',')
            xs.append(x)
            ys.append(y)
    # ax.clear()
    # ax.scatter(xs,ys,c='green',s=50,clip_on = False)
    ax.plot(xs,ys)




# ani = animation.FuncAnimation(
#     fig, animate, interval=200)  # interval=2：2ms时间间隔

plt.show()
