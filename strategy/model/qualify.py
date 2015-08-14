# -*- coding=utf-8 -*-

class MA:
	"""
	函数对象，若干段时间均线，输入：长度大于range的数值
	"""
	def __init__(self, range=1):
		self.range = range

	def __call__(self, ls):
		return sum(ls[-self.range:]) / self.range


class EMA:
	"""
	指数移动平均线
	"""
	def __init__(self, N):
		self.N = N
		self.num = 0
		self.pre = 0

	def __call__(self, ls):
		if self.num == 0:
			self.pre = ls[0]
			self.num = 1
		for d in ls[self.num:]:
			self.pre = self.pre * ((self.N-1)/(self.N+1)) + d * (2/(self.N+1))
		self.num = len(ls)
		return self.pre


class DIFF:
	"""
	DIFF指标
	"""
	def __init__(self, a=12, b=26):
		self.ema1 = EMA(a)
		self.ema2 = EMA(b)

	def __call__(self, ls):
		return self.ema1(ls) - self.ema2(ls)


class DEA:
	"""
	DEA指标
	"""
	def __init__(self, a=12, b=26, c=9):
		self.a, self.b, self.c = a, b, c
		self.num = 0
		self.pre = 0
		self.preema1 = 0
		self.preema2 = 0

	def __call__(self, ls):
		if self.num == 0:
			self.preema1 = self.preema2 = ls[0]
			self.pre = 0
			self.num = 1
		for d in ls[self.num:]:
			self.preema1 = self.preema1 * ((self.a-1)/(self.a+1)) + d * (2/(self.a+1))
			self.preema2 = self.preema2 * ((self.b-1)/(self.b+1)) + d * (2/(self.b+1))
			_diff = self.preema1 - self.preema2
			self.pre = self.pre * ((self.c-1)/(self.c+1)) + _diff * (2/(self.c+1))
		self.num = len(ls)
		return self.pre

class MACD:
	"""
	MACD指标
	"""
	def __init__(self, a=12, b=26, c=9):
		self.DEA = DEA(a,b,c)

	def __call__(self, ls):
		_dea = self.DEA(ls)
		_diff = self.DEA.preema1 - self.DEA.preema2
		return  (_diff - _dea) * 2

