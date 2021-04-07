---
layout:     post
title:      "mybatisplus"
subtitle:   " \"mybatisplus\""
date:       2020-12-17 18:00:00
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 工具
---
* TOC
{:toc}

# 2.x转3.x

```
import com.baomidou.mybatisplus.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;

import com.baomidou.mybatisplus.service.IService;
import com.baomidou.mybatisplus.extension.service.IService;

import com.baomidou.mybatisplus.mapper.EntityWrapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.mapper.QueryWrapper;

import com.baomidou.mybatisplus.plugins.Page;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.baomidou.mybatisplus.service.impl.ServiceImpl;

import com.baomidou.mybatisplus.activerecord.Model;
import com.baomidou.mybatisplus.enums.IdType;
import com.baomidou.mybatisplus.annotations.TableField;
import com.baomidou.mybatisplus.annotations.TableId;
import com.baomidou.mybatisplus.annotations.TableName;

import com.baomidou.mybatisplus.extension.activerecord.Model;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

```

# 一些操作
mybatis设置创建时间和更新时间自动填入：
```
第一种：数据库中设置，设置为datetime，默认为CURRENT_TIMESTAMP,根据当前时间戳更新。
第二种：代码中操作，第一种不要操作，在mapper中相应字段添加注解@TableField(.. , update="now()") 使用数据库时间
```


批处理：
```

```

