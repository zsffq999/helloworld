# -*- coding:utf-8 -*-

from strategy.model.macd import MacdModel, SimpleMacdModel
from strategy.trade.simpletrade import SimpleTrade
from strategy.data.kline import KLine
from strategy.analysis.yields import YieldAnalysis
from strategy.test import TestSystem, NoTrainSplit

from strategy.model.qualify import MACD, DIFF, DEA

import matplotlib.pyplot as plt


def main():
	model = SimpleMacdModel()
	dataset = KLine('SH000300', 5, '../data')
	print(dataset.target)
	analysis = YieldAnalysis()
	trade = SimpleTrade()

	print("set up success")

	system = TestSystem(model, dataset, trade, analysis)

	print("set up success 2")

	dates, yields= system.run(NoTrainSplit())

	print(sum([y for y in yields if y < 0]))
	print(sum([y for y in yields if y > 0]))

	plt.plot(dates, yields)
	plt.show()


if __name__ == "__main__":
	main()