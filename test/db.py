# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    def __init__(self, name):
        self.name = name

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(50))
    password = Column(String(50))


engine = create_engine('mysql+pymysql://macd:macd@localhost/test')

User.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

for i in range(10):
    user = User("user%d" % i)
    session.add(user)
session.commit()
