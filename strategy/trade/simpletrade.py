# -*- coding:utf-8 -*-


from strategy.trade import Trade, Deal


class SimpleTrade(Trade):
	"""
	最简单的交易模块，如果预期上涨买1手，如果预期下跌卖1手，如果预期平则平仓
	"""

	def __init__(self):
		super(SimpleTrade, self).__init__()
		self.status = 0

	def trade(self, signal, dataset):
		if signal != self.status:
			amount = signal - self.status
			self.status = signal
			return [Deal(dataset.time, dataset.target, amount, dataset.price)]
