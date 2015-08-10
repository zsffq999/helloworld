import os
import sys

from dbinit.interests import *

def rcv_interests(price, rights, ration, ration_price, interests):
	res = (price - interests + ration*ration_price) / (1 + rights + ration)
	return res

def rcv_interests_abv(stk_info, interests_info):
	for k, v in sorted(interests_info.items()):
		idx = np.searchsorted(stk_info['date'], k)
		rights, ration, ration_price, interests = v
		stk_info['before'][:idx] = rcv_interests(stk_info['before'][:idx], rights, ration, ration_price, interests)
		stk_info['open'][:idx] = rcv_interests(stk_info['open'][:idx], rights, ration, ration_price, interests)
		stk_info['high'][:idx] = rcv_interests(stk_info['high'][:idx], rights, ration, ration_price, interests)
		stk_info['low'][:idx] = rcv_interests(stk_info['low'][:idx], rights, ration, ration_price, interests)
		stk_info['close'][:idx] = rcv_interests(stk_info['close'][:idx], rights, ration, ration_price, interests)
	#save 2 float numbers
	for idx in ['before', 'open', 'high', 'low', 'close']:
		stk_info[idx] = np.round(stk_info[idx]*100)/100.0
	return stk_info

def rcv_batch(src, dst, interests_info, filter):
	listdir = os.listdir(src)
	listdir = sorted(listdir)
	for stk in listdir:
		data = np.load(os.path.join(src, stk))
		stk = stk[:-4]
		if filter(stk):
			print('executing', stk, '...')
			np.save(os.path.join(dst, stk), rcv_interests_abv(data, interests_info[stk] if stk in interests_info else {}))

if __name__ == "__main__":
	series = sys.argv[1]
	#load interests information
	interests_info = interestsinfo('data/wsSHSZ_SPLITs_' + series)
	#execute
	rcv_batch('data/processing_day', 'data/rehv_day', interests_info, filter=lambda x:x[-1] == '1')
	#rec_batch('processing_min', 'rehv_min', interests_info, 1)
