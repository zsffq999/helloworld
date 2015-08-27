# -*- coding:utf-8 -*-

from strategy.model.macd import MacdModel, SimpleMacdModel
from strategy.model.kdj import KDJModel
from strategy.trade.simpletrade import SimpleTrade
from strategy.data.kline import KLine
from strategy.analysis.yields import YieldAnalysis
from strategy.test import TestSystem
from strategy.test.split import TimeSplit

import csv

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

	system = TestSystem(model, dataset, trade, analysis)

	print("set up success 2")

	dates, yields= system.run(TimeSplit(datetime(2005, 1, 1)))

	print(sum([y for y in yields if y < 0]))
	print(sum([y for y in yields if y > 0]))

	plt.plot(dates, np.cumsum(yields))
	plt.show()

if __name__ == "__main__":
	#main()
	test1 = [row for row in csv.reader(open("money.csv", "r", encoding="utf-8"))]
	test2 = [row for row in csv.reader(open("kdj_test/output.csv", "r", encoding="utf-8"))][1:]
	for t in test1:
		dt = datetime.strptime(t[0][:10], "%Y-%m-%d").strftime("%Y-%m-%d")
		for i, t2 in enumerate(test2):
			if dt == t2[0]:
				if abs(float(t[5]) - float(t2[9])) > 1e-4:
					print("{}, t1:{}, t2:{}".format(dt, float(t[5])*100, float(t2[9])*100))