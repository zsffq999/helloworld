from strategy.system import System
from datetime import timedelta


class TestSystem(System):
	"""
	模拟测试系统。
	几个假设：
	（1）数据（Market）被分为训练集和测试集
	（2）交易总能成功，不存在撤单交易
	split: 划分训练集及测试集函数
	"""

	def __init__(self, model, dataset, trader, analysis):
		super(TestSystem, self).__init__(model, dataset, trader, analysis)

	def run(self, traintestsplit):
		"""
		运行system
		:param traintestsplit: 测试集和训练集分割类
		:return:
		"""
		# 划分训练集及测试集
		traintestsplit.split(self.dataset)
		recent_update_time = traintestsplit.traindata.time

		# 训练模型
		self.model.train(traintestsplit.traindata)
		while traintestsplit.hasNextTest():
			traintestsplit.updateTrain()
			_signal = self.model.predict(traintestsplit.traindata)
			_deal = self.trader.trade(_signal, traintestsplit.traindata) # _deal可能是None
			if _deal:
				self.receiveDeal(self.sendDeal(_deal))
			# 更新模型
			if traintestsplit.trainNewModel():
				print(traintestsplit.traindata.time, ": Updating model")
				self.model.train(traintestsplit.traindata)

		return self.analysis.analyse(self.trader.tradeinfo, traintestsplit.traindata)
