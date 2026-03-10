# -*- coding: utf-8 -*-

# ***************************************************
# * File        : Dijkstra.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2025-08-26
# * Version     : 1.0.082615
# * Description : Dijkstra 2D
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

__all__ = []

# python libraries
import sys
from pathlib import Path
ROOT = str(Path.cwd())
if ROOT not in sys.path:
    sys.path.append(ROOT)
import math
import heapq
import warnings
warnings.filterwarnings("ignore")

from path_planning.search_based.search_2D import plotting_2D as plotting
from path_planning.search_based.search_2D.Astar import AStar

# global variable
LOGGING_LABEL = Path(__file__).name[:-3]


class Dijkstra(AStar):
    """
    Dijkstra set the cost as the priority 
    """
    def searching(self):
        """
        Breadth-first Searching.
        :return: path, visited order
        """
        self.PARENT[self.s_start] = self.s_start
        self.g[self.s_start] = 0
        self.g[self.s_goal] = math.inf
        heapq.heappush(self.OPEN, (0, self.s_start))

        while self.OPEN:
            _, s = heapq.heappop(self.OPEN)
            self.CLOSED.append(s)

            if s == self.s_goal:
                break

            for s_n in self.get_neighbor(s):
                new_cost = self.g[s] + self.cost(s, s_n)

                if s_n not in self.g:
                    self.g[s_n] = math.inf

                if new_cost < self.g[s_n]:  # conditions for updating Cost
                    self.g[s_n] = new_cost
                    self.PARENT[s_n] = s

                    # best first set the heuristics as the priority 
                    heapq.heappush(self.OPEN, (new_cost, s_n))

        return self.extract_path(self.PARENT), self.CLOSED




# 测试代码 main 函数
def main():
    s_start = (5, 5)
    s_goal = (45, 25)

    dijkstra = Dijkstra(s_start, s_goal, 'None')
    plot = plotting.Plotting(s_start, s_goal)

    path, visited = dijkstra.searching()
    plot.animation(path, visited, "Dijkstra's")  # animation generate

if __name__ == "__main__":
    main()
