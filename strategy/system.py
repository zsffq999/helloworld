# -*- coding:utf-8 -*-


class System(object):
	"""
	系统共分数据、模型、交易、评估四大模块
	和外界交互共4个接口：数据输入及更新（updateData），订单发送（__sendDeal），成交情况（receiveDeal），收益率评估（pinggu）
	"""

	def __init__(self, model, dataset, trader, analysis):
		self.model = model
		self.dataset = dataset
		self.trader = trader
		self.analysis = analysis

	def updateData(self, newdata):
		"""
		接收实时数据，更新系统数据库
		:param newdata: 从外界接收的新数据，限定为一个最新数据，不是序列
		:return: void
		"""
		# TODO 与外界交互模块
		self.dataset.update(newdata)
		_signal = self.model.predict(self.dataset)
		_deal = self.trader.trade(_signal, self.dataset) # _deal可能是None
		return self.sendDeal(_deal)

	def sendDeal(self, deal):
		"""
		向交易所发送交易订单
		:param trade: 交易信息
		:return: 发送交易结果
		"""
		# TODO 与外界交互模块
		return deal

	def receiveDeal(self, deal):
		"""
		:param deal: 接收的订单
		:return: void
		"""
		self.trader.rcvtrade(deal)

	def updateModel(self):
		"""
		根据最新的dataset数据，更新模型
		:return:
		"""
		self.model.train(self.dataset)

	def getTradeInfo(self):
		"""
		获取所有交易信息
		:return:
		"""
		return self.trader.tradeinfo

	def analysisModel(self):
		"""
		分析模拟交易结果
		:return:
		"""
		return self.analysis.analyse(self.getTradeInfo(), self.dataset)

