---
layout:     post
title:      "tigergraph"
subtitle:   " \"知识图谱\""
date:       2020-08-07 15:30:00 
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 知识图谱
---
* TOC
{:toc}
# 安装以及基本操作

## 安装

[下载地址](https://www.tigergraph.com.cn/developer-download/)
安装：
```
tar xzf <your_tigergraph_package>.tar.gz 
cd tigergraph*/ 
sudo ./install.sh
```

## 基本操作

数据准备：
```
person.csv
name,gender,age,state
Tom,male,40,ca
Dan,male,34,ny
Jenny,female,25,tx
Kevin,male,28,az
Amily,female,22,ca
Nancy,female,20,ky
Jack,male,26,fl

friendship.csv
person1,person2,date
Tom,Dan,2017-06-03
Tom,Jenny,2015-01-01
Dan,Jenny,2016-08-03
Jenny,Amily,2015-06-08
Dan,Nancy,2016-01-03
Nancy,Jack,2017-03-02
Dan,Kevin,2015-12-30
```

在安装过程中创建的用户中进行登录：
```
例如账户test，密码test
输入gsql进入数据库shell界面
ls查看数据库中的库
drop all删除所有数据
Restarting TigerGraph services重启数据库服务
```

库的创建：
```
节点的创建：CREATE VERTEX person (PRIMARY_ID name STRING, name STRING, age INT, gender STRING, state STRING)
边的创建：CREATE UNDIRECTED EDGE friendship (FROM person, TO person, connect_day DATETIME)
图的创建：CREATE GRAPH social (person, friendship)
```

数据载入：
```
GSQL > USE GRAPH social
Using graph 'social'
GSQL > BEGIN
GSQL > CREATE LOADING JOB load_social FOR GRAPH social {
GSQL >    DEFINE FILENAME file1="/home/tigergraph/person.csv";
GSQL >    DEFINE FILENAME file2="/home/tigergraph/friendship.csv";
GSQL >
GSQL >    LOAD file1 TO VERTEX person VALUES ($"name", $"name", $"age", $"gender", $"state") USING header="true", separator=",";
GSQL >    LOAD file2 TO EDGE friendship VALUES ($0, $1, $2) USING header="true", separator=",";
GSQL > }
GSQL > END
The job load_social is created.

run loading job load_social
```

数据查询：
```
查询person顶点的个数
SELECT count(*) FROM person
查询指定定顶点的详细信息
SELECT * FROM person WHERE primary_id=="Tom"
```
