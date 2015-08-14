from strategy.system import System


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

		# 训练模型
		self.model.train(traintestsplit.traindata)
		while traintestsplit.hasNextTest():
			traintestsplit.updateTrain()
			_signal = self.model.predict(traintestsplit.traindata)
			_deal = self.trader.trade(_signal, traintestsplit.traindata) # _deal可能是None
			if _deal:
				self.receiveDeal(self.sendDeal(_deal))

		return self.analysis.analyse(self.trader.tradeinfo, traintestsplit.traindata)

class TrainTestSplit:
	"""
	训练集和测试集分割类
	"""

	def __init__(self):
		self.dataset = None
		self.traindata = None
		self.testdata = None

	def split(self, dataset):
		"""
		划分训练集和测试集
		:param dataset:
		:return:
		"""
		self.dataset = dataset

	def hasNextTest(self):
		"""
		根据训练集和测试集划分情况，迭代下一个测试集
		:return: bool
		"""
		pass

	def updateTrain(self):
		"""
		更新训练集
		:return:
		"""
		pass

class NoTrainSplit(TrainTestSplit):

	def __init__(self):
		super(NoTrainSplit, self).__init__()

	def split(self, dataset):
		super(NoTrainSplit, self).split(dataset[1000:])
		self.traindata = self.dataset[:0]
		self.testdata = self.dataset
		self.testid = 0

	def hasNextTest(self):
		return self.testid < len(self.dataset)

	def updateTrain(self):
		self.testid += 1
		self.traindata = self.dataset[:self.testid]