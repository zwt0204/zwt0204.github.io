---
layout:     post
title:      "matplotlib"
subtitle:   " \"matplotlib\""
date:       2024-03-14 18:00:00
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 工具
---
* TOC
{:toc}

# 中文乱码问题
1. 删除缓存
```
import matplotlib as mpl
print(mpl.get_cachedir())
# /Users/xiewenwen/.matplotlib
```
2. 下载字体[SimHei](http://129.204.205.246/downloads/SimHei.ttf)
3. fc-cache -fv 刷新字体缓存
测试：
```python
import matplotlib as mpl
import matplotlib.pyplot as plt

def plot_demo():
    #print(mpl.get_cachedir())
    # 绘制折线图
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
    year = [2017, 2018, 2019, 2020]
    people = [20, 40, 60, 70]
    # 生成图表
    plt.plot(year, people)
    plt.xlabel('年份')
    plt.ylabel('人口')
    plt.title('人口增长')
    # 设置纵坐标刻度
    plt.yticks([0, 20, 40, 60, 80])
    # 设置填充选项：参数分别对应横坐标，纵坐标，纵坐标填充起始值，填充颜色
    plt.fill_between(year, people, 20, color='green')
    # 显示图表
    # plt.savefig("./plt.png")
    plt.show()

plot_demo()
```