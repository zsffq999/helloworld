# -*- coding:utf-8 -*-

from datetime import datetime


class DataSet(object):
	"""
	行情数据基类，存储不同类型和不同数据结构的行情数据
	注意：一个DataSet类只存储一种标的的一种类型的数据
	"""

	def __init__(self, target):
		self.target = target
		self.list = []

	def __getitem__(self, item):
		"""
		提供列表操作的接口
		:param item:
		:return:
		"""
		return self.list[item]

	def __setitem__(self, key, value):
		"""
		提供列表操作的接口
		:param key:
		:param value:
		:return:
		"""
		self.list[key] = value

	def append(self, value):
		"""
		提供列表操作的接口
		"""
		if isinstance(value, list):
			self.list += value
		else:
			self.list.append(value)

	@property
	def time(self):
		"""
		数据最新时间
		"""
		return datetime.now()

	@property
	def price(self):
		"""
		最新价格
		"""
		pass


# TODO 如果涉及多种行情，可能需要定义MultiData类，为单个行情的集合
class MultiData(DataSet):
	"""
	多种行情的集合
	"""
	def __init__(self):
		self.list = [[]]

	def append(self, value):
		if isinstance(value, MultiData):
			self.list += value
		else:
			self.list.append(value)