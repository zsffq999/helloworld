from datetime import timedelta
import numpy as np


class LabelConstructor(object):

	def __init__(self, time_delta):
		self.time_delta = time_delta

	def construct(self, dataset):
		Y = []
		for (i,d) in enumerate(dataset):
			j = min(len(dataset)-1, i + self.time_delta)
			_begin = d['close']
			_end = dataset[j]['close']
			if _begin > _end:
				_label = -1
			else:
				_label = 1
			Y.append(_label)
		return np.array(Y)

