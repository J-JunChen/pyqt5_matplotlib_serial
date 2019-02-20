import sys
import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

# file_path = 'D://PythonCode//CAD//data.txt'
file_path = dir_path+'/data.txt'

def open_file():  
    with open(file_path) as file_object:
        for line in file_object:
            # print(line)
            data = line.split()
            if len(data) == 10:
                # print(data)
                if(data[0] == 'ma'): #表示基站0到基站x的距离
                    if(data[1] != '0e'): # MASK=e(0000 1111)表示 RANGE0,RANGE1,RANGE2,RANGE3 都有效
                        print("ma's Range 只有 "+data[1]+" 工作。")
                        # break
                    else:
                        #16进制转为10进制，距离单位：mm
                        # range_0 = int(data[2],16) range_0没有'ma'对应的操作说明
                        range_1 = int(data[3],16)
                        range_2 = int(data[4],16)
                        range_3 = int(data[5],16)
                        print("基站0到基站1的距离：%d"%(range_1)+"，基站0到基站2的距离：%d"%(range_2)+"，基站0到基站3的距离：%d"%(range_3))

                else: # data[0] == 'mc' or 'mr' ：表示标签x到基站y的距离
                    if(data[1] != '0f'): # MASK=7(0000 0111)表示 RANGE0,RANGE1,RANGE2 都有效
                        print("mc's Range 只有 "+data[1]+" 工作。")
                        # break
                    else:
                        #16进制转为10进制，距离单位：mm
                        range_0 = int(data[2],16) 
                        range_1 = int(data[3],16)
                        range_2 = int(data[4],16)
                        range_3 = int(data[5],16)
                        print("标签x到基站0的距离：%d"%(range_0)+"，标签x到基站1的距离：%d"%(range_1)+"，标签x到基站2的距离：%d"%(range_2)+"，标签x到基站3的距离：%d"%(range_3))

                        # anchor_0 = (0,0)
                        # anchor_1 = (7500,0) # X轴
                        # anchor_2= (0,5000) # 第三条轴，不一定是Y轴
                        anchor_0 = np.array([0,0])
                        anchor_1 = np.array([7500,0])
                        anchor_2 = np.array([0,5000])
                        tag_position = getLocation(anchor_0,anchor_1,anchor_2,range_0,range_1,range_2)
                        
                        print("标签坐标X:%d"%tag_position[0]+"，Y:%d"%tag_position[1])


def getLocation(anchor_0,anchor_1,anchor_2,range_0,range_1,range_2):
    """ 根据trilateration 计算标签的坐标 """
    tag_position = np.array([0,0])
    tag_position[0] = (range_0**2 - range_1**2 + anchor_1[0]**2)/(2*anchor_1[0])
    distance = range_0**2 - tag_position[0]**2
    tag_position[1] = np.sqrt(distance)
    return tag_position

if __name__ == "__main__":
    open_file()