# -*- coding=utf8 -*-
"""
汉字的三个概率矩阵
    初始概率 （每个汉字的出现概率）
    转移概率 （汉字 向 汉字 的转移）
    发射概率 （汉字 向 拼音 的发射）
"""
import os

from sqlalchemy import Column, String, Integer, Float, create_engine, desc
from sqlalchemy.orm import sessionmaker

from model.common import current_dir, BaseModel

db_name = os.path.join(current_dir, 'hmm.sqlite')
engine = create_engine('sqlite:///{}'.format(db_name))
HMMSession = sessionmaker(bind=engine)


class Transition(BaseModel):

    __tablename__ = 'transition'

    id = Column(Integer, primary_key=True)
    previous = Column(String(1), nullable=False)
    behind = Column(String(1), nullable=False)
    probability = Column(Float, nullable=False)

    @classmethod
    def add(cls, previous, behind, probability):
        """添加转移记录

        Args:
            previous (string): 前面的汉字
            behind (string): 后面的汉字
            probability (float): 转移概率
        """
        session = HMMSession()
        record = cls(previous=previous, behind=behind, probability=probability)
        session.add(record)
        session.commit()
        return record

    @classmethod
    def join_emission(cls, pinyin, character):
        """join emission表查询

        Args:
            pinyin (string): 拼音
            characters (string): 上次的汉字
        """
        session = HMMSession()

        '''
        前一个汉字 -> 后一个汉字
        查询结果： 后一个汉字 + 概率
        概率 = 转移概率 * 发射概率
        
        转移表 和 发射表 做连接查询， 以 转移表的后一个汉字 和 发射表的汉字 做连接
        按照 前一个汉字 在转移表中 过滤
        按照 拼音 在发射表中 过滤
        '''
        query = session.query(cls.behind,
                              Emission.probability + cls.probability).\
            join(Emission, Emission.character == cls.behind).\
            filter(cls.previous == character).\
            filter(Emission.pinyin == pinyin).\
            order_by(desc(Emission.probability + cls.probability))
        result = query.first()
        session.commit()
        return result


class Emission(BaseModel):

    __tablename__ = 'emission'

    id = Column(Integer, primary_key=True)
    character = Column(String(1), nullable=False)
    pinyin = Column(String(7), nullable=False)
    probability = Column(Float, nullable=False)

    @classmethod
    def add(cls, character, pinyin, probability):
        """添加转移记录

        Args:
            character (string): 汉字
            pinyin (string): 拼音
            probability (float): 概率
        """
        session = HMMSession()
        record = cls(character=character, pinyin=pinyin, probability=probability)
        session.add(record)
        session.commit()
        return record

    @classmethod
    def join_starting(cls, pinyin, limit=10):
        """join starting表查询

        Args:
            pinyin (string): 拼音
            limit (int): 数据个数
        """
        session = HMMSession()

        # 查询目的，根据拼音，将所有汉字找到
        # 查询结果： 汉字 + 概率
        # 概率 = 汉字的概率 * 汉字向拼音发射的概率
        query = session.query(cls.character,
                              cls.probability + Starting.probability).\
            join(Starting, cls.character == Starting.character).\
            filter(cls.pinyin == pinyin).\
            order_by(desc(cls.probability + Starting.probability)).\
            limit(limit)
        result = query.all()
        session.commit()
        return result


class Starting(BaseModel):

    __tablename__ = 'starting'

    id = Column(Integer, primary_key=True)
    character = Column(String(1), nullable=False)
    probability = Column(Float, nullable=False)

    @classmethod
    def add(cls, character, probability):
        """添加转移记录

        Args:
            character (string): 汉字
            probability (float): 起始概率
        """
        session = HMMSession()
        record = cls(character=character, probability=probability)
        session.add(record)
        session.commit()
        return record


def init_hmm_tables():
    """
    创建表
    """
    if os.path.exists(db_name):
        os.remove(db_name)

    with open(db_name, 'w') as f:
        pass

    BaseModel.metadata.create_all(bind=engine, tables=[Transition.__table__,
                                                       Starting.__table__,
                                                       Emission.__table__])
