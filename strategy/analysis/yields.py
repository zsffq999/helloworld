# -*- coding=utf-8 -*-

from strategy.analysis import Analysis
import operator
from datetime import datetime, timedelta
import numpy as np


class YieldAnalysis(Analysis):
	"""
	按天计算收益率
	"""

	def analyse(self, trades, dataset):
		trades = sorted(trades, key=lambda x: x.time)

		dates = []
		yields = []

		# 在交易的节点算账户余额
		# 开仓资金
		_money = -trades[0].amount * trades[0].price
		_begin = abs(_money)
		_own = trades[0].amount
		_date = trades[0].time.date()
		_date = datetime(_date.year, _date.month, _date.day, 23, 59, 59)
		f = open('deal.csv', 'w')
		f2 = open('money.csv', 'w')
		print(trades[0].time, trades[0].amount, trades[0].price, sep=',', file=f)
		for trade in trades[1:]:
			# 如果收盘，结算当天收益（假设按照收盘价结算，而不是收盘最后若干分钟平均价结算）
			while _date < trade.time:
				_close = dataset.closeprice(_date)
				_end = _money + _own * _close
				dates.append(_date)
				_yield = _end / _begin
				yields.append(_yield)
				print(_date, _own, _begin, _close, _end, _yield)
				print(_date, _own, _begin, _close, _end, _yield, sep=',', file=f2)
				_money = -_own * _close
				_begin = abs(_money)
				_date = _date + timedelta(1)
			_money -= trade.amount * trade.price
			_own += trade.amount
			print(trade.time, trade.amount, trade.price, sep=',', file=f)

		while _date < dataset.time +timedelta(1):
			_close = dataset.closeprice(_date)
			_end = _money + _own * _close
			dates.append(_date)
			_yield = _end / _begin
			yields.append(_yield)
			print(_date, _own, _begin, _close, _end, _yield)
			print(_date, _own, _begin, _close, _end, _yield, sep=',', file=f2)
			_money = -_own * _close
			_begin = abs(_money)
			_date = _date + timedelta(1)
		f.close()
		f2.close()

		'''
		for d in dataset[id:]:
			_from = d[0]
			#_to = d[0] + timedelta(360)
			fid = np.searchsorted(dataset['datetime'], _from)
			#tid = np.searchsorted(dataset['datetime'], _to, side='right')
			#if tid >= len(dataset):
			#	break

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
		'''

		return dates, yields
