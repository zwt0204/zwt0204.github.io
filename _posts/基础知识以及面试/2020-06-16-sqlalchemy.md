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

base.py
from functools import wraps
from sqlalchemy.orm.query import Query
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr, as_declarative
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import AbstractConcreteBase
from contextlib import contextmanager
from sqlalchemy import inspect


class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}".format("user", "pwd", "url")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 1
    SQLALCHEMY_MAX_OVERFLOW = 0
    SQLALCHEMY_POOL_RECYCLE = 100


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, convert_unicode=True,
                       pool_size=Config.SQLALCHEMY_POOL_SIZE, max_overflow=Config.SQLALCHEMY_MAX_OVERFLOW,
                       pool_recycle=Config.SQLALCHEMY_POOL_RECYCLE)
Session = sessionmaker(bind=engine)


def close_session(fn):
    @wraps(fn)
    def close(obj, *args, **kwargs):
        obj.session = Session()
        res = fn(obj, *args, **kwargs)
        obj.session.close()
        return res
    return close


class DataQuery(Query):

    @close_session
    def get(self, *args, **kwargs):
        """增加关闭的功能"""
        return super(DataQuery, self).get(*args, **kwargs)

    @close_session
    def first(self):
        return super(DataQuery, self).first()

    @close_session
    def all(self):
        return super(DataQuery, self).all()


Base = declarative_base()


class DataModel(AbstractConcreteBase, Base):
    """table映射的基类"""

    @classmethod
    def query(cls):
        """"""
        return DataQuery(cls)

    def to_dict(self):
        return {k: getattr(self, k) for k in inspect(type(self)).c.keys()}


@contextmanager
def get_session(autocommit=False, **kwargs):
    """"""
    s = Session(autocommit=autocommit, **kwargs)
    try:
        if autocommit:
            s.begin()
        yield s
        s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


@contextmanager
def get_connect(**kwargs):

    connect = engine.connect(**kwargs)
    try:
        yield connect
    finally:
        connect.close()

op.py

from database.base import get_session
from database.db_model import BaseGoodsCorrect
import logging
import traceback
from datetime import datetime

_logger = logging.getLogger('database')


class BaseOP(object):

    def add(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        try:
            create_time = datetime.now()
            kwargs.update({"create_time": create_time})
            kwargs.update({"update_time": create_time})
            goods_persistence = BaseGoodsCorrect(**kwargs)
            with get_session(autocommit=True) as sess:
                sess.add(goods_persistence)
        except Exception as e:
            _logger.error('持久化失败，请检查数据格式： %s' % kwargs['pid'])
            traceback.print_exc()

    def add_all(self, data):
        """
        :param kwargs:
        :return:
        """
        try:
            create_time = datetime.now()
            temp = []
            for i in data:
                i.update({"create_time": create_time})
                i.update({"update_time": create_time})
                goods_persistence = BaseGoodsCorrect(**i)
                temp.append(goods_persistence)
            with get_session(autocommit=True) as sess:
                sess.add_all(temp)
        except Exception as e:
            _logger.error('持久化失败，请检查数据格式')
            traceback.print_exc()

    def delete_by_id(self, pid):
        """
        根据id删除会话
        :param pid: pid
        :return:
        """
        try:
            with get_session() as sess:
                sess.query(BaseGoodsCorrect).filter_by(pid=pid).delete()
        except Exception as e:
            traceback.print_exc()

    def get_by_id(self, pid):
        """
        根据id获取结果
        :param pid: pid
        :return:
        """
        try:
            with get_session(autocommit=True) as sess:
                res = sess.query(BaseGoodsCorrect).filter_by(pid=pid).first().to_dict()
            if res is None:
                return None
            else:
                return res
        except Exception as e:
            traceback.print_exc()
            return 'err'

    def get_all(self):
        """
        获取所有结果
        :return:
        """
        try:
            with get_session(autocommit=True) as sess:
                res = sess.query(BaseGoodsCorrect).all()
            if res is None:
                return None
            else:
                return res
        except Exception as e:
            traceback.print_exc()
            return 'err'

    def get_data_offset(self, start, end):
        """
        分页获取所有结果
        :return:
        """
        data = []
        try:
            with get_session(autocommit=True) as sess:
                res = sess.query(BaseGoodsCorrect).order_by(BaseGoodsCorrect.id.asc())[start: end]
                for r in res:
                    r = r.to_dict()
                    data.append(r)
            if res is None:
                return None
            else:
                return data
        except Exception as e:
            traceback.print_exc()
            return 'err'

    def get_count(self):
        """
        获取行数
        :return:
        """
        try:
            with get_session(autocommit=True) as sess:
                res = sess.query(BaseGoodsCorrect).count()
            if res is None:
                return None
            else:
                return res
        except Exception as e:
            traceback.print_exc()
            return 'err'

```

# 几种常见的查询

```
简单的查询：session.query(User.name, User.fullname).all()
带条件查询：session.query(User).filter(User.name == "user").all()
多条件查询：session.query(User).filter(and_(User.name.like("user%"), User.fullname.like("first%"))).all()；session.query(User).filter(or_(User.name.like("user%"), User.password != None)).all()
sql过滤：session.query(User).filter("id>:id").params(id=1).all()
关键查询：session.query(User, Address).filter(User.id == Address.user_id).all()；session.query(User).join(User.addresses).all()；session.query(User).outerjoin(User.addresses).all()
记录总数：session.query(func.count(User.id))
返回限制字段：session.query(Person.name, Person.created_at,Person.updated_at).filter_by(name="zhongwei").order_by(Person.created_at).first()
正则匹配
session.query(User).filter(User.district.op('regexp')(r'[\u4e00-\u9fa5]+').all()
```

# 批量增加

```
# 确实可以实现，但是需要和表中列都对应，除过自增字段
df = pd.read_csv('../pd.csv', sep='\t')
# df.to_sql("alg_saas_xd_base_goods_correct", con=engine, if_exists="append", index=False)

# temp为list，元素为所添加的对象
sess.add_all(temp)
```


# 参考
1. [几种查询总结](https://blog.csdn.net/shudaqi2010/article/details/51568219)
