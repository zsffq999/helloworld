# -*- coding:utf-8 -*-

from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import random
from itertools import accumulate

if __name__ == "__main__":
    day_cnt = 365
    d = date(2001, 1, 1)
    dates = [d + timedelta(days=i) for i in range(day_cnt)]
    pchg = [random.uniform(-1, 1) for i in range(day_cnt)]
    nav = list(accumulate(pchg))
    plt.plot(dates, nav)
    plt.show()
