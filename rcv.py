from interests import *
import os
import sys

def rcv_interests(price, rights, ration, ration_price, interests):
	res = (price - interests + ration*ration_price) / (1 + rights + ration)
	return (res*100+0.5).astype(np.int32) / 100.0

def rcv_interests_abv(stk_info, interests_info):
	for k, v in sorted(interests_info.items()):
		idx = np.searchsorted(stk_info['date'], k)
		rights, ration, ration_price, interests = v
		stk_info['before'][:idx] = rcv_interests(stk_info['before'][:idx], rights, ration, ration_price, interests)
		stk_info['open'][:idx] = rcv_interests(stk_info['open'][:idx], rights, ration, ration_price, interests)
		stk_info['high'][:idx] = rcv_interests(stk_info['high'][:idx], rights, ration, ration_price, interests)
		stk_info['low'][:idx] = rcv_interests(stk_info['low'][:idx], rights, ration, ration_price, interests)
		stk_info['close'][:idx] = rcv_interests(stk_info['close'][:idx], rights, ration, ration_price, interests)
	return stk_info

def rcv_batch(src, dst, interests_info, series=-1):
	listdir = os.listdir(src)
	listdir = sorted(listdir)
	for stk in listdir:
		if stk[-5] == str(series):
			print('executing', stk, '...')
			np.save(os.path.join(dst, stk), rcv_interests_abv(np.load(os.path.join(src, stk)), interests_info[stk[:-4]] if stk[:-4] in interests_info else {}))

if __name__ == "__main__":
	series = sys.argv[1]
	#load interests information
	interests_info = interestsinfo('data/wsSHSZ_SPLITs_' + series)
	#execute
	rcv_batch('data/processing_day', 'data/rehv_day', interests_info, 1)
	#rec_batch('processing_min', 'rehv_min', interests_info, 1)
