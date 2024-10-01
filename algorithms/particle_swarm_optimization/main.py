# -*- coding: utf-8 -*-

# ***************************************************
# * File        : main.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2024-10-01
# * Version     : 1.0.100114
# * Description : 粒子群算法 DEMO
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

import numpy as np
import matplotlib.pyplot as plt

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


"""
问题：
min f(x1,x2) = x1**2 + x2**2
s.t. 
x1,x2 belongs to [-10,10]
"""


class PSO:
    
    def __init__(self, population_size, max_steps):
        self.w = 0.6  # 惯性权重
        self.c1 = self.c2 = 2
        self.population_size = population_size  # 粒子群数量
        self.dim = 2  # 搜索空间的维度(决策变量数量)
        self.max_steps = max_steps  # 最大迭代次数
        self.x_bound = [-10, 10]  # 解空间范围
        self.x = np.random.uniform(self.x_bound[0], self.x_bound[1], (self.population_size, self.dim))  # 初始化粒子群位置
        self.v = np.random.rand(self.population_size, self.dim)  # 初始化粒子群速度
        
        fitness = self.calculate_fitness(self.x)  # 计算适应度
        self.p = self.x  # 个体的最佳位置
        self.pg = self.x[np.argmin(fitness)]  # 全局最佳位置
        self.individual_best_fitness = fitness  # 个体的最优适应度
        self.global_best_fitness = np.max(fitness)  # 全局最佳适应度
 
    def calculate_fitness(self, x):
        """
        适应度函数，即目标函数
        """
        return np.sum(np.square(x), axis = 1)
 
    def evolve(self):
        fig = plt.figure()
        for step in range(self.max_steps):
            # TODO
            r1 = np.random.rand(self.population_size, self.dim)
            r2 = np.random.rand(self.population_size, self.dim)
            
            # 更新速度和权重
            self.v = self.w*self.v+self.c1*r1*(self.p-self.x)+self.c2*r2*(self.pg-self.x)
            self.x = self.v + self.x
            
            # 数据可视化
            plt.clf()
            plt.scatter(self.x[:, 0], self.x[:, 1], s = 30, color = 'k')
            plt.xlim(self.x_bound[0], self.x_bound[1])
            plt.ylim(self.x_bound[0], self.x_bound[1])
            plt.pause(0.01)
            plt.ion()
            plt.show()
            
            # 计算适应度
            fitness = self.calculate_fitness(self.x)
            
            # 需要更新的个体
            update_id = np.greater(self.individual_best_fitness, fitness)
            self.p[update_id] = self.x[update_id]
            self.individual_best_fitness[update_id] = fitness[update_id]
            
            # 新一代出现了更小的 fitness，所以更新全局最优 fitness 和位置
            if np.min(fitness) < self.global_best_fitness:
                self.pg = self.x[np.argmin(fitness)]
                self.global_best_fitness = np.min(fitness)
            
            print(f"best fitness: {self.global_best_fitness:.5f}, mean fitness: {np.mean(fitness):.5f}")




# 测试代码 main 函数
def main():
    pso = PSO(population_size = 10, max_steps = 100)
    pso.evolve()

if __name__ == "__main__":
    main()
