import os
import sys

from interests import *

def exedate(fmtdate):
	year = int(fmtdate[:4])
	month = int(fmtdate[5:7])
	day = int(fmtdate[8:10])
	hr = int(fmtdate[11:13])
	mi = int(fmtdate[14:16])
	se = int(fmtdate[17:19])
	return year*10000+month*100+day, hr*10000+mi*100+se

def loadcsv(filename, interests_info):
	res_day = []
	res_min = []
	with open(filename, 'r') as f:
		flag = True
		for line in f:
			if flag:
				flag = False
				continue
			context = line.strip().split(',')
			_date, _time = exedate(context[0])
			_before = float(context[1]) if len(res_day) == 0 else res_day[-1][6]
			if _time == 0 or _time == 935:
				if _date in interests_info:
					_info = interests_info[_date]
					_before = rminterests(_before, _info[0], _info[1], _info[2], _info[3])
			data = (_date, _time, _before, float(context[1]), float(context[2]), float(context[3]), float(context[4]), int(context[5])*100, int(float(context[6])))
			if _time == 0:
				res_day.append(data)
			else:
				res_min.append(data)
	dtype = np.dtype([('date',np.int32), ('time',np.int32), ('before',np.float32), ('open',np.float32), ('low', np.float32), ('high',np.float32), ('close',np.float32), ('vol',np.int64), ('amt', np.int64)])
	return np.array(res_day, dtype=dtype), np.array(res_min, dtype=dtype)

def csv2npy(src, dst_day, dst_min, interests_info, series=-1):
	listdir = os.listdir(src)
	listdir = sorted(listdir)
	print(listdir)
	for stk in listdir:
		if stk[-5] == str(series) and stk == 'SH600031.csv':
			print('executing', stk, '...')
			stk_day, stk_min = loadcsv(os.path.join(src, stk), interests_info[stk[:-4]] if stk[:-4] in interests_info else {})
			np.save(os.path.join(os.path.join(dst_day, stk[:-4]+'.npy')), stk_day)
			np.save(os.path.join(os.path.join(dst_min, stk[:-4]+'.npy')), stk_min)

if __name__ == '__main__':
	series = '1'#sys.argv[1]
	#load interests information
	interests_info = interestsinfo('data/rights/wsSHSZ_SPLITs_' + series)
	#execute
	csv2npy('data/wstock/SH', 'data/processing_day', 'data/processing_min', interests_info, series)
	csv2npy('data/wstock/SZ', 'data/processing_day', 'data/processing_min', interests_info, series)