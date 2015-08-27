from strategy.model import Model
from strategy.model.labelconstructor import LabelConstructor
import numpy as np
from sklearn import preprocessing
from datetime import timedelta
from sklearn.svm import LinearSVC, SVC

class KDJ(object):

	def __init__(self, n=9):
		self.n = n
		self.datab4n = np.zeros((self.n, 2)) # 前n日的low, high, close值
		self.old_k, self.old_d, self.old_j = 0, 0, 0
		self.old_k_2, self.old_d_2, self.old_j_2 = 0, 0, 0

	def __call__(self, ls):
		"""
		默认ls每个数据代表一个时间区域
		:param ls: 数据格式：(datetime, before, open, low, high, close, amount, value)
		:return: n*3矩阵
		"""
		res = []
		k, d, j = 50.0, 50.0, 50.0
		# 先计算第0个值
		for i in range(len(ls)):
			if i >= self.n-1:
				dr = ls[i-8:i+1]
			else:
				dr = ls[:i+1]
			low = min(dr['low'])
			high = max(dr['high'])
			close = dr[-1]['close']
			rsv = (close-low) / (high-low) * 100.0 if high > low else 50.0
			k = (2/3)*k + (1/3)*rsv
			d = (2/3)*d + (1/3)*k
			j = 3*k - 2*d
			res.append([k,d,j])

		# 更新内存前若干日最大最小值及KDJ信息，假设len(ls)>9
		self.datab4n[max(self.n-len(ls), 0):,:] = [[d['low'], d['high']] for d in ls[-self.n:]]
		if self.n > len(ls):
			self.datab4n[:self.n-len(ls),:] = self.datab4n[self.n-len(ls),:]
		self.old_k, self.old_d, self.old_j = k, d, j
		self.old_k_2, self.old_d_2, self.old_j_2 = self.old_k, self.old_d, self.old_j
		return np.array(res)

	def current(self, data, update=False):
		"""
		计算当前data的KDJ值，如果data是新时刻的数据最大最小值
		:param data:
		:param update:
		:return:
		"""
		if update:
			self.datab4n[:self.n-1] = self.datab4n[1:]
			self.datab4n[-1] = [data['low'], data['high']]
			self.old_k, self.old_d, self.old_j = self.old_k_2, self.old_d_2, self.old_j_2
		else:
			self.datab4n[-1,0] = min(data['low'], self.datab4n[-1,0])
			self.datab4n[-1,1] = max(data['high'], self.datab4n[-1,1])
		low = min(self.datab4n[:,0])
		high = max(self.datab4n[:,1])
		close = data['close']
		rsv = (close-low) / (high-low) * 100 if high > low else 50.0
		k = (2/3)*self.old_k + (1/3)*rsv
		d = (2/3)*self.old_d + (1/3)*k
		j = 3*k - 2*d
		self.old_k_2, self.old_d_2, self.old_j_2 = k, d, j

		return k, d, j


class KDJModel(Model):

	def __init__(self, predict_range=1):
		"""
		初始化KDJ模型
		:param predict_range: K预测未来涨跌时间范围
		:return:
		"""
		super(KDJModel, self).__init__()
		self.predict_range = predict_range
		self.para_k, self.para_d, self.para_j = 0.0, 0.0, 0.0
		self.KDJ = KDJ()
		self.LC = LabelConstructor(predict_range)

	def train(self, dataset):
		print("Training SVM Model...")

		X_train = self.KDJ(dataset)
		# 数据缩放
		self.min_max_scaler = preprocessing.MinMaxScaler()
		X_train = self.min_max_scaler.fit_transform(X_train)
		print(self.min_max_scaler.scale_, self.min_max_scaler.min_)
		# 得到label Y
		Y_train = self.LC.construct(dataset)

		#for (i,d) in enumerate(dataset):
		#	print(d, X_train_minmax[i], Y_train[i])

		# 用SVM拟合数据
		self.svm = SVC()
		self.svm.fit(X_train, Y_train)

		print("Linear SVM Model:", self.svm)



	def predict(self, dataset):
		k, d, j = self.KDJ.current(dataset[-1], True)
		y = self.svm.predict(self.min_max_scaler.transform([k,d,j]))[0]
		print(dataset[-1], [k,d,j], y)
		return y
