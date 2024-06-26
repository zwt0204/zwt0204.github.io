---
layout:     post
title:      "多机免密登录"
subtitle:   " \"多机免密登录\""
date:       2023-08-20 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - llms
---
* TOC
{:toc}

# 背景
多机之间多gpu的联合训练需要开启多机之间的免密登录。

# 步骤
1.查看本地是否存在秘钥文件
```
ls ~/.ssh/id_rsa.pub
注意：如果不存在的话需要进行第二步，存在的话就直接跳转第三步骤
```
2.使用 ssh-key-gen 在本地主机上创建公钥和密钥
```
ssh-keygen -t rsa
```
3.把公钥复制到需要打通的机器上
```
ssh-copy-id -i ~/.ssh/id_rsa.pub root@127.0.0.1
```
4.打通免密
```
需要打通的机器进行以上相同1.2.3的操作，否则只能单向免密。
打通后机器之间就可以随意ssh免密登录了
ssh 127.0.0.1
```

# 参考
1.[免密登录](https://www.cnblogs.com/atrox/p/13579548.html)