# -*- coding:utf-8 -*-


class Analysis(object):
	"""
	绩效分析模块基类
	"""

	def analyse(self, trades):
		"""
		根据交易信息，分析收益率等指标
		:param trades:
		:return: 每一笔交易对应的收益率曲线。可能需要json格式
		"""