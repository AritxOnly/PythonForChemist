from enum import Enum

import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class DisplayType(Enum):
    # 自定义枚举类型传入可视化类型参数
    Empty = 0
    LineChart = 1   # 折线图
    BarChart = 2    # 条形图
    Line3DChart = 3 # 3D折线图

class CircustanceData:
    def __init__(self, name: str, theta: list, intensity: list):
        self.name = name
        self.theta = theta
        self.intensity = intensity

    def display(self):
        plt.plot(self.theta, self.intensity)
        plt.xlabel('2θ (degree)')
        plt.ylabel('Intensity (a.u.)')
        plt.title('XRD Analysis ({})'.format(self.name))
        plt.show()
    
    def debugOutput(self):
        print(self.theta)
        print(self.intensity)

# 自定义判断一个数是否为数字的函数
def isNumber(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False

# 将不规范的txt转化为csv
def toCSV(filePath: str) -> str:
    # 预处理：判断后缀名
    if os.path.splitext(filePath)[-1] != '.txt':
        raise FileExistsError('the input file should be .txt')
    
    csvLines = []

    # 处理原始txt
    with open(filePath, 'r') as file:
        content = file.readlines()
        for line in content:
            keywords = line.split()
            csvLines.append(','.join(str(keyword) for keyword in keywords)) # 生成CSV标准形式
        file.close()
    
    csvPath = os.path.splitext(filePath)[0] + '.csv'    # 在工作目录下生成.csv
    print('{} is generated'.format(csvPath))
    with open(csvPath, 'w+') as file:
        for line in csvLines:
            file.write(line + '\n')
        file.close()
    
    return csvPath

'''
 XDRAnalysisPro api使用说明
 传入的filePath可以是列表，也可以是单个字符串
 filePath为单个字符串时，默认生成折线图
 filePath传入列表时可以开启compare功能，可以生成条形图
 其中条形图显示的为峰值
'''
def XRDAnalysisPro(filePath, 
                   displayType: DisplayType = DisplayType.Empty,
                   compare: bool = False,
                   compareIndex: list = []) -> None:
    # 使用多参数传递主要是为了提供丰富的接口和这个项目的PyQt UI对接

    # 函数预处理：检测数据类型、参数合法性
    if type(filePath).__name__ == 'list':
        isFiles = True
        path = filePath     # 其实可以直接用filePath，但是为了保证数据安全与后续操作的通用性，新开一个path
        if compare:
            # 检测compareIndex参数合法性
            tempIndex = compareIndex
            for index in tempIndex: # 防止更改列表数据导致的问题
                if index >= len(filePath):
                    compareIndex.remove(index)
    elif type(filePath).__name__ == 'str':
        isFiles = False
        path = [filePath]
        if displayType != DisplayType.LineChart:
            displayType = DisplayType.LineChart
            print('单文件模式下将默认生成折线图...')
        if compare:
            compare = False
            print('单文件模式下将默认关闭比较...')
    else:
        raise TypeError('the arg filePath should be a string or list')
        # 抛出异常
    
    # 文件操作：读入文件，写入数据库
    database = []

    for file in path:
        csv = toCSV(file) # 标准化为CSV
        data = pd.read_csv(csv)
        fileName = os.path.basename(csv)
        data.sort_values(by='2θ', inplace=True)
        # 新建一个基础数据对象存入database
        database.append(CircustanceData(fileName, data['2θ'], data['I']))
    # 生成图像
    match displayType:
        case DisplayType.LineChart:
            database[0].display()


if __name__ == '__main__':
    XRDAnalysisPro('E:\Codes\DataAnalysis\data\C Fe2.4.txt', DisplayType.LineChart, 
                   compare=True, compareIndex=[])