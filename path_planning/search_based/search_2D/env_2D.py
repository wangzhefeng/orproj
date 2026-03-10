# -*- coding: utf-8 -*-

# ***************************************************
# * File        : env.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2025-08-26
# * Version     : 1.0.082612
# * Description : Env 2D
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
import warnings
warnings.filterwarnings("ignore")

# global variable
LOGGING_LABEL = Path(__file__).name[:-3]


class Env:
    
    def __init__(self):
        self.x_range = 51  # size of background
        self.y_range = 31
        self.motions = [
            (-1, 0), (-1, 1), (0, 1),  (1, 1),
            (1, 0),  (1, -1), (0, -1), (-1, -1),
        ]
        self.obs = self.obs_map()

    def update_obs(self, obs):
        self.obs = obs

    def obs_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """
        x = self.x_range
        y = self.y_range
        
        obs = set()
        
        for i in range(x):
            obs.add((i, 0))
        for i in range(x):
            obs.add((i, y - 1))

        for i in range(y):
            obs.add((0, i))
        for i in range(y):
            obs.add((x - 1, i))

        for i in range(10, 21):
            obs.add((i, 15))
        for i in range(15):
            obs.add((20, i))

        for i in range(15, 30):
            obs.add((30, i))
        for i in range(16):
            obs.add((40, i))

        return obs




# 测试代码 main 函数
def main():
    env = Env()
    print(f"env.motions: \n{env.motions}")
    print(f"env.obs: \n{env.obs}")

if __name__ == "__main__":
    main()
