# -*- coding: utf-8 -*-

# ***************************************************
# * File        : main.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2024-10-01
# * Version     : 1.0.100115
# * Description : 模拟退火算法 DEOM
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# * TODO        : 1.
# ***************************************************

__all__ = []

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
import random
from typing import List

import numpy as np
import matplotlib.pyplot as plt

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]

"""
问题：

max f(x) = (x**2 - 5x) * sin(x**2)
s.t.
"""


class SA:

    def __init__(self, 
                 interval: List, 
                 tab: str = 'min', 
                 T_max: int = 10000, 
                 T_min: int = 1, 
                 iterMax = 1000, 
                 rate = 0.95):
        self.interval = interval  # 给定状态空间, 即待求解空间
        self.T_max = T_max  # 初始退火温度, 温度上限
        self.T_min = T_min  # 截止退火温度, 温度下限
        self.iterMax = iterMax  # 定温内部迭代次数
        self.rate = rate  # 退火降温速度
        self.x_seed = random.uniform(interval[0], interval[1])  # 解空间内的种子
        self.tab = tab.strip()  # 求解最大值还是最小值的标签('min': 最小值, 'max': 最大值)
        
        self.solve() # 完成主体的求解过程
        self.display() # 数据可视化展示
    
    def solve(self):
        # 采用反射方法提取对应的处理函数
        temp = 'deal_' + self.tab
        if hasattr(self, temp):
            deal = getattr(self, temp)
        else:
            exit('>>>tab标签传参有误："min"|"max"<<<')
        # 模拟退火算法
        x1 = self.x_seed
        T = self.T_max
        while T >= self.T_min:
            for i in range(self.iterMax):
                # 计算状态
                f1 = self._func(x1)
                # 将随机解束缚在给定状态空间内
                delta_x = random.random() * 2 - 1  # [-1,1) 之间的随机值
                if x1 + delta_x >= self.interval[0] and x1 + delta_x <= self.interval[1]:
                    x2 = x1 + delta_x
                else:
                    x2 = x1 - delta_x
                # 重新计算状态
                f2 = self._func(x2)
                # 计算 TODO
                delta_f = f2 - f1
                # 求解最优解
                x1 = deal(x1, x2, delta_f, T)
            # 更新退火温度最大值
            T *= self.rate
        # 提取最终退火解
        self.x_solu = x1      
    
    def _func(self, x):
        """
        状态产生函数，即待求解函数
        """
        value = (x**2 - 5*x) * np.sin(x**2)

        return value
    
    def _p_min(self, delta, T):
        """
        计算最小值时，容忍解的状态迁移概率
        """
        probability = np.exp(-delta/T)
        return probability
        
    def _p_max(self, delta, T):
        """
        计算最大值时，容忍解的状态迁移概率
        """
        probability = np.exp(delta/T)
        return probability
    
    def deal_min(self, x1, x2, delta, T):
        if delta < 0: # 更优解
            return x2
        else: # 容忍解
            # 容忍解的状态迁移概率
            P = self._p_min(delta, T)
            if P > random.random(): 
                return x2
            else: 
                return x1
    
    def deal_max(self, x1, x2, delta, T):
        if delta > 0: # 更优解
            return x2
        else: # 容忍解
            # 容忍解的状态迁移概率
            P = self._p_max(delta, T)
            if P > random.random():
                return x2
            else:
                return x1
    
    def display(self):
        print(f"seed: {self.x_seed}\nsolution: {self.x_solu}")
        x = np.linspace(self.interval[0], self.interval[1], 300)
        y = self._func(x)
        
        # 结果可视化
        plt.figure(figsize=(6, 4))
        plt.plot(x, y, 'g-', label='function')
        plt.plot(self.x_seed, self._func(self.x_seed), 'bo', label='seed')
        plt.plot(self.x_solu, self._func(self.x_solu), 'r*', label='solution')
        plt.title('solution = {}'.format(self.x_solu))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.savefig('./algorithms/simulated_annealing_algorithm/SA.png', dpi=500)
        plt.show()
        plt.close()




# 测试代码 main 函数
def main():
    SA(interval = [-5, 5], tab = 'min')

if __name__ == "__main__":
    main()
