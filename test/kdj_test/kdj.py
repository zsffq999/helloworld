# -*- coding:utf-8 -*-

"""
读入csv格式的日线行情，计算kdj指标，用svm按月滚动训练和预测，Y是下一个交易日收盘价的涨跌，然后汇总累加收益率
"""

import csv, itertools, math
from datetime import datetime, timedelta, date
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot


class Record:
    def __init__(self, row):
        # 预先配置好要用到字段
        self.tdate = datetime.strptime(row[0], "%Y/%m/%d").date()
        self.open = float(row[1])
        self.high = float(row[2])
        self.low = float(row[3])
        self.close = float(row[4])
        self.vol = float(row[5])
        self.turnover = float(row[6])
        self.predict = 0
        self.ret = 0.0
        self.total_ret = 0.0

    def __repr__(self):
        return "Record:date={},close={}".format(self.tdate, self.close)


def first_index_of(lst, func):
    for i in range(len(lst)):
        if func(lst[i]):
            return i
    return -1


def last_index_of(lst, func):
    for i in range(len(lst) - 1, -1, -1):
        if func(lst[i]):
            return i
    return -1


def train_and_predict(train_data, predict_data):
    # 注意，训练数据的最后一条没有下一日涨跌幅
    x_array = [(r.k, r.d, r.j) for r in train_data[:-1]]
    y_array = [math.copysign(1, d2.close - d1.close) for (d1, d2) in zip(train_data[:-1], train_data[1:])]
    # 默认svm参数，默认归一化，训练和预测
    scaler = MinMaxScaler()
    x_array_scaled = scaler.fit_transform(x_array)
    model = SVC()
    model.fit(x_array_scaled, y_array)
    x_array_predict_scaled = scaler.transform([(r.k, r.d, r.j) for r in predict_data])
    y_array_predict = model.predict(x_array_predict_scaled)
    return y_array_predict


if __name__ == "__main__":

    # 读入csv
    rows = [row for row in csv.reader(open("data.csv", "r", encoding="utf-8"))]
    data = [Record(row) for row in rows[1:]]

    # 计算kdj，默认周期为9，平滑因子1/3
    for i in range(len(data)):
        idx0 = max(0, i - 9 + 1)
        h = max([d.high for d in data[idx0:i + 1]])
        l = min([d.low for d in data[idx0:i + 1]])
        if h == l:
            data[i].rsv = 50.0
        else:
            data[i].rsv = (data[i].close - l) / (h - l) * 100.0

        if i == 0:
            data[i].k = 100.0
            data[i].d = 0.0
        else:
            data[i].k = data[i - 1].k * 2.0 / 3.0 + data[i].rsv / 3.0
            data[i].d = data[i - 1].d * 2.0 / 3.0 + data[i].k / 3.0
        data[i].j = data[i].k * 3.0 - data[i].d * 2.0

    # 从2000-01-01开始滚动预测，每次滚动一个月
    # 即用[1990-12-19,1999-12-31]的数据作为训练，从2000-01-01的收盘时刻开始交易
    sdate = date(2005, 1, 1)
    group_by_month = [list(g) for k, g in itertools.groupby(data, key=lambda d: d.tdate.strftime("%Y%m"))]
    idx = first_index_of(group_by_month, lambda grp: grp[0].tdate >= sdate)
    for i in range(idx, len(group_by_month)):
        train_data = list(itertools.chain.from_iterable(group_by_month[:i]))
        predict_data = group_by_month[i]
        print("train data from {} to {}, predict data from {} to {}".format(train_data[0].tdate, train_data[-1].tdate,
                                                                            predict_data[0].tdate,
                                                                            predict_data[-1].tdate))
        for j, predict in enumerate(train_and_predict(train_data, predict_data)):
            predict_data[j].predict = predict

    # 开始计算收益
    for d1, d2 in zip(data[:-1], data[1:]):
        d2.ret = (d2.close / d1.close - 1) * d1.predict
        d2.total_ret = d1.total_ret + d2.ret

    # 输出到csv，画图
    writer = csv.writer(open("output.csv", "w", newline=''))
    writer.writerow(["tdate", "open", "high", "low", "close", "k", "d", "j", "predict", "ret", "total_ret"])
    for d in data:
        writer.writerow([d.tdate, d.open, d.high, d.low, d.close, d.k, d.d, d.j, d.predict, d.ret, d.total_ret])

    idx = first_index_of(data, lambda d: d.tdate >= sdate)
    pyplot.plot(*zip(*[(d.tdate, d.total_ret) for d in data[idx:]]))
    pyplot.show()
