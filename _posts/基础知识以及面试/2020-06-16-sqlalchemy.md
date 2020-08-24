---
layout:     post
title:      "sqlalchemy"
subtitle:   " \"ORM（Object-Relational Mapping）\""
date:       2020-06-16 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 编程
---
* TOC
{:toc}
# 简介
SQLAlchemy是Python编程语言下的一款开源软件。提供了SQL工具包及对象关系映射（ORM）工具。

# 使用
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# 连接数据库
engine = create_engine("mysql+pymysql://{}:{}@{}".format("user", "pwd", "url"), echo=True)  # echo=True表示打印出相关的sql语句
# 声明性基类
Base = declarative_base()
from sqlalchemy import Column, Integer, String
class User(Base):
	# 表名
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)
	nickname = Column(String)
	def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                                self.name, self.fullname, self.nickname)
if __name__ == '__main__':
    # 创建表
    # Base.metadata.create_all(engine)
    ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(ed_user)
    session.commit()
    our_user = session.query(User).filter_by(name='ed').first()
```

