from datetime import datetime
import numpy as np


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

	def trainNewModel(self):
		"""
		是否训练新模型
		:return: True or False, default False
		"""
		return False

class NoTrainSplit(TrainTestSplit):

	def __init__(self):
		super(NoTrainSplit, self).__init__()

	def split(self, dataset):
		super(NoTrainSplit, self).split(dataset)

		self.traindata = self.dataset[:0]
		self.testdata = self.dataset
		self.testid = 0

	def hasNextTest(self):
		return self.testid < len(self.dataset)

	def updateTrain(self):
		self.testid += 1
		self.traindata = self.dataset[:self.testid]


class TimeSplit(NoTrainSplit):
	"""
	从splittime开始，每个月更新一次
	"""
	def __init__(self, splittime):
		super(TimeSplit, self).__init__()
		self.splittime = splittime

	def split(self, dataset):
		self.dataset = dataset
		self.testid = np.searchsorted(dataset['datetime'], self.splittime, side='left')
		self.traindata = self.dataset[:self.testid]
		self.testdata = self.dataset[self.testid:]

	def trainNewModel(self):
		nextday = self.dataset[:self.testid+1].time
		if nextday.month != self.splittime.month:
			self.splittime = datetime(nextday.year, nextday.month, 1)
			return True
		return False
