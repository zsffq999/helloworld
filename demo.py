import numpy as np

class DemoList(list):
	def __init__(self, args=None):
		super(self.__class__, self).__init__(args)

l1 = DemoList([1,2,3,4,5])

l2 = DemoList([3,4])

print([1,2].__contains__(1))

print(l1.__class__)

print(l1[1:3].__class__)

print(np.array([]).__class__)