# -*- coding:utf-8 -*-


class Model(object):
	"""
	Model模块基类，用于存储，训练和预测模型
	"""

	def __init__(self):
		pass

	def train(self, dataset):
		"""
		模型训练
		:param dataset: DataSet基类, 行情数据，可能涉及多种行情，此时以列表等形式存储
		:return: void
		"""
		pass

	def predict(self, dataset):
		"""
		模型预测，根据实时行情给出预测结果：涨、跌、平
		:param dataset: Market基类, 行情数据，可能涉及多种行情，此时以列表等形式存储
		:return: int, 涨跌平，涨为+1，跌为-1，平为0
		"""
		pass

