# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Float, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
import os
import numpy as np
from datetime import datetime


DB_CONNECT_STRING = "mysql+pymysql://macd:macd@localhost:3306/test"
engine = create_engine(DB_CONNECT_STRING, echo=True)

Base = declarative_base()

class StockDay(Base):

	__tablename__ = 'stockday'

	def __init__(self, name, *args):
		self.name = name
		self.date, self.before, self.open, self.low, self.high, self.close, self.volumn, self.amount = args

	id = Column(Integer, primary_key=True)
	name = Column(String(8))
	date = Column(DateTime)
	before = Column(Float)
	open = Column(Float)
	low = Column(Float)
	high = Column(Float)
	close = Column(Float)
	volumn = Column(BigInteger)
	amount = Column(BigInteger)

DB_session = sessionmaker(bind=engine)
session = DB_session()

StockDay.metadata.drop_all(engine)
StockDay.metadata.create_all(engine)

def insert(src, session, filter):
	listdir = os.listdir(src)
	listdir = sorted(listdir)
	for stk in listdir[:10]:
		data = np.load(os.path.join(src, stk))
		stk = stk[:-4]
		if not filter(stk):
			continue
		print('execute', stk, '...')
		for d in data:
			session.add(StockDay(stk, datetime(d[0]//10000, d[0]//100%100, d[0]%100, d[1]//10000, d[1]//100%100, d[1]%100), float(d[2]), float(d[3]), float(d[4]), float(d[5]), float(d[6]), int(d[7]), int(d[8])))
		session.commit()

if __name__ == "__main__":
	src = '../data/processing_day'
	insert(src, session, filter=lambda stk: stk[-1] == '1')