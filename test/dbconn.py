__author__ = 'zsf'

# coding=utf-8

__author__ = 'zsf'

import pymysql
from sqlalchemy import *

engine = create_engine('mysql+pymysql://macd:macd@localhost:3306/test')
matadata = MetaData(engine)

user_table = Table('users', matadata, autoload=True)
i = user_table.insert()
print(i)
i.execute({'name': ['Tom','Mike']})
