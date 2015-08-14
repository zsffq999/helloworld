# -*- coding:utf-8 -*-

from strategy.model import Model
from strategy.model.qualify import MACD, DIFF, DEA


class MacdModel(Model):
	"""
	根据Macd金叉死叉预测股票涨跌，+1表示涨，-1表示跌
	"""

	# 股市状态
	NONE = 0 # 起始状态
	UPNODEAD = 1 # 0轴上方无死叉
	UPFIRSTDEAD = 2 # 0轴上方第一次死叉
	DOWNNOGOLD = -1 # 0轴下方无金叉
	DOWNFIRSTGOLD = -2 # 0轴下方第一次金叉

	# 金叉死叉
	GOLDCROSS = 1 # 金叉
	DEADCROSS = -1 # 死叉

	def __init__(self):
		super(MacdModel, self).__init__()
		self.DIFF = DIFF()
		self.DEA = DEA()
		self.MACD = MACD()
		self.state = self.NONE # 股市状态
		self.macd = 0

	def train(self, dataset):
		"""
		模型训练，在MACD模型中，没有训练过程
		:param dataset: DataSet基类, 行情数据，可能涉及多种行情每种行情以列表存储
		:return: void
		"""
		pass


	def predict(self, dataset):
		"""
		MACD模型
		（1）如果MACD>0，DIFF>0，则看涨
		（2）如果MACD>0，DIFF<0，但已经连续两次存在MACD>0（两次金叉），则看涨
		（3）如果MACD<0，DIFF<0，则看跌
		（4）如果MACD<0，DIFF>0，但出现第二次死叉，则看跌
		:param dataset: DataSet基类, 行情数据，每种行情以列表形式存储
		:return: int, 涨跌平，涨为+1，跌为-1，平为0
		"""
		if len(dataset) < self.MACD.DEA.b + self.MACD.DEA.c:
			return 0

		diff = self.DIFF(dataset['close'])
		macd = self.MACD(dataset['close'])

		# 判断股市走势
		_pred = 0
		if macd > 0:
			if diff > 0:
				_pred = 1
			else:
				_pred = 1 if self.state == self.UPNODEAD else -1
		else:
			if diff > 0:
				_pred = -1 if self.state == self.DOWNNOGOLD else 1
			else:
				_pred = -1

		# 判断当前金叉死叉
		_cross = self.__cross(macd)

		#更新金叉死叉状态
		if self.state == self.NONE:
			if macd > 0 and diff > 0:
				self.state = self.UPNODEAD
			elif macd < 0 and diff < 0:
				self.state = self.DOWNNOGOLD
		elif self.state == self.UPNODEAD:
			if diff < 0:
				self.state = self.DOWNNOGOLD
			elif _cross == self.DEADCROSS:
				self.state = self.UPFIRSTDEAD
		elif self.state == self.UPFIRSTDEAD:
			if diff < 0:
				self.state = self.DOWNNOGOLD
		elif self.state == self.DOWNNOGOLD:
			if diff > 0:
				self.state = self.UPNODEAD
			elif _cross == self.GOLDCROSS:
				self.state = self.DOWNFIRSTGOLD
		elif self.state == self.DOWNFIRSTGOLD:
			if diff > 0:
				self.state = self.UPNODEAD

		return _pred

	def __cross(self, _macd):
		_crs = self.NONE
		if self.macd <= 0 and _macd > 0:
			_crs = self.GOLDCROSS
		elif self.macd >= 0 and _macd < 0:
			_crs = self.DEADCROSS
		self.macd = _macd # 更新历史macd信息
		return _crs

class SimpleMacdModel(MacdModel):
	def __init__(self):
		super(SimpleMacdModel, self).__init__()

	def predict(self, dataset):
		if len(dataset) < self.MACD.DEA.b + self.MACD.DEA.c:
			return 0

		macd = self.MACD(dataset['close'])
		return 1 if macd > 0 else -1