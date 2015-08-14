# -*- coding=utf-8 -*-

from strategy.analysis import Analysis
import operator
from datetime import datetime, timedelta
import numpy as np


class YieldAnalysis(Analysis):
	"""
	按天计算以3个月为单位的年化收益率
	"""

	def analyse(self, trades, dataset):
		trades = sorted(trades, key=lambda x: x.time)
		id = np.searchsorted(dataset['datetime'], trades[0].time)
		own = 0
		trid = 0

		dates = []
		yields = []

		for d in dataset[id:]:
			_from = d[0]
			_to = d[0] + timedelta(360)
			fid = np.searchsorted(dataset['datetime'], _from)
			tid = np.searchsorted(dataset['datetime'], _to, side='right')
			if tid >= len(dataset):
				break

			#计算初始拥有量
			if trades[trid].time <= _from:
				own += trades[trid].amount
				trid += 1

			#计算初始资金（包括市值）
			_begin = -dataset[fid]['close'] * own
			_money = _begin
			_own = own

			#根据交易记录计算盈亏状况
			for trade in trades[trid:]:
				if trade.time > _to:
					break
				_money -= trade.amount * trade.price
				_own += trade.amount

			#计算结束时资金
			_end = _money + _own * dataset[tid]['close']

			#计算收益率
			_yield = _end / abs(_begin) * (365.0/360.0)
			print(_from, own, dataset[fid]['close'], _begin, _own, dataset[tid]['close'], _end)

			dates.append(_from)
			yields.append(_yield)

		return dates, yields
