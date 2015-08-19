# -*- coding=utf-8 -*-


from strategy.data import DataSet
import numpy as np
import os
from datetime import datetime


class KLine(DataSet):
	"""
	K线图数据，一个类只存储一个标的的一种K线图
	"""

	def __init__(self, target, range, dir=None):
		super(KLine, self).__init__(target)
		self.range = range # 按分钟，5为5分钟，240为一天，7200为一个月
		if dir == None:
			self.list = []
			return

		if range == 5:
			self.list = np.load(os.path.join(dir, 'processing_min/'+self.target+'.npy'))
		else:
			self.list = np.load(os.path.join(dir, 'processing_day/'+self.target+'.npy'))

	def __getitem__(self, item):
		if isinstance(item, slice):
			res = KLine(self.target, self.range)
			res.list = self.list[item]
			return res
		return self.list[item]

	@property
	def time(self):
		return self.list[-1][0]

	@property
	def price(self):
		return self.list[-1][5]

	def closeprice(self, date):
		_date = datetime(date.year, date.month, date.day, 23, 59, 59)
		_id = np.searchsorted(self.list['datetime'], _date, side='right')-1
		return self.list[_id]['close']

