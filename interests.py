import numpy as np
import cPickle as cp

def date2int(date):
	return date[0] * 10000 + date[1] * 100 + date[2]

def interestsinfo(filename):
	info = {}
	with open(filename, 'r') as f:
		flag = True
		for line in f:
			if flag:
				flag = False
				continue
			context = line.strip().split(',')
			if context[0] in info:
				info[context[0]][int(context[1])] = [float(context[2]), float(context[3]), float(context[4]), float(context[5])]
			else:
				info[context[0]] = {int(context[1]): [float(context[2]), float(context[3]), float(context[4]), float(context[5])]}
	return info

def rminterests(price, rights, ration, ration_price, interests):
	res = (price - interests + ration*ration_price) / (1 + rights + ration)
	return float(int(res*100+0.5)) / 100

