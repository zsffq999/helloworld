# -*- coding:utf-8 -*-

from strategy.model.macd import MacdModel, SimpleMacdModel
from strategy.model.kdj import KDJModel
from strategy.trade.simpletrade import SimpleTrade
from strategy.data.kline import KLine
from strategy.analysis.yields import YieldAnalysis
from strategy.test import TestSystem
from strategy.test.split import TimeSplit
from dateutil.relativedelta import relativedelta

from strategy.model.qualify import MACD, DIFF, DEA

import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np


def main():
	model = KDJModel(predict_range=1)
	#model = MacdModel()
	dataset = KLine('SH000001', 240, '../data')
	print(dataset.target)
	analysis = YieldAnalysis()
	trade = SimpleTrade()

	print("set up success")

	system = TestSystem(model, dataset, trade, analysis, relativedelta(months=1))

	print("set up success 2")

	dates, yields= system.run(TimeSplit(datetime(2004, 12, 31)))
	#dates, yields= system.run(TimeSplit(datetime(2004, 12, 31)))

	print(sum([y for y in yields if y < 0]))
	print(sum([y for y in yields if y > 0]))

	plt.plot(dates, np.cumsum(yields))
	plt.show()

if __name__ == "__main__":
	main()