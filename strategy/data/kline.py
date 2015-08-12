# -*- coding=utf-8 -*-


from strategy.data import DataSet, datetime
import numpy as np


class KLine(DataSet):
	"""
	K线图数据，一个类只存储一个标的的一种K线图
	"""

	def __init__(self, target, range):
		super(KLine, self).__init__(target)
		self.range = range # 按分钟，5为5分钟，240为一天，7200为一个月

		if range == 5:
			self.list = np.load('../../data/processing_min/' + self.target + '.npy')
		else:
			self.list = np.load('../../data/processing_day/' + self.target + '.npy')

	@property
	def time(self):
		return self.list[0]

	@property
	def price(self):
		return self.list[5]
