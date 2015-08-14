# -*- coding:utf-8 -*-


class Trade(object):
	"""
	交易模块基类，根据模型预测的涨跌信号和实时数据发出交易指令
	"""

	def __init__(self):
		self.tradeinfo = []

	def trade(self, signal, dataset):
		"""
		交易
		:param signal: 模型预测的涨跌信号（+-1,0）
		:param dataset: 实时行情，DataSet基类
		:return: 交易指令
		"""
		pass

	def rcvtrade(self, trade):
		print(*trade)
		if isinstance(trade, list):
			self.tradeinfo += trade
		else:
			self.tradeinfo.append(trade)

class Deal(object):
	"""
	每笔交易记录。如果涉及多笔交易记录，用list<Deal>存储
	"""

	__slots__ = ('time', 'target', 'amount', 'price')

	def __init__(self, time, target, amount, price):
		"""
		初始化函数
		:param time: 交易时间
		:param target: 交易标的
		:param amount: 成交量，以股为单位，<0为做空，>0为做多
		:param price: 成交金额
		:return:
		"""
		self.time = time
		self.target = target
		self.amount = amount
		self.price = price

	def __str__(self):
		return "Deal: <time: {0}, target: {1}, amount: {2}, price: {3}>".format(self.time, self.target, self.amount, self.price)

if __name__ == "__main__":
	print(*[Deal(1, 2, 3, 4), Deal(5,6,7,8)])