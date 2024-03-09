---
layout:     post
title:      "springboot学习中的一些问题"
subtitle:   " \"springboot\""
date:       2020-12-17 18:00:00
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 工具
---
* TOC
{:toc}

# tomcat运行

前提已经在IDEA中配置了tomcat
配置tomcat运行：
第一步：
![01](https://zwt0204.github.io//img//tomcat.png)
第二步：
![01](https://zwt0204.github.io//img//tomcat1.png)
第三步：
![01](https://zwt0204.github.io//img//tomcat2.png)
在第三步中需要注意，如果只是dubbo接口则只加载相应的provider，如果还要封装dubbo接口为http则要安排好顺序，先provider再consumer。

第四步：
```
在运行起来之后，通常url中回加有相应war包的名称，默认起来会是provider的url，自行调换看consumer。
```
# Resource文件

读取resource下的文件
```
File file = ResourceUtils.getFile("classpath:excleTemplate/test.xlsx");
InputStream inputStream = new FileInputStream(file);
```