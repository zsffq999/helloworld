# -*- coding:utf-8 -*-

# -------------------------------------------------------------
# 工作目录变更为当前目录
import os

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

# -------------------------------------------------------------
# 创建flask
from flask import Flask, render_template
from datetime import date, timedelta, datetime
import json

app = Flask("flask-demo")


# -------------------------------------------------------------
# 页面访问

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# -------------------------------------------------------------
# ajax访问

# 定义一个函数，输入日期x（格式yyyymmdd），输出一堆测试数据
@app.route("/getdata/<int:sid>")
def getdata(sid):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    try:
        d = date(sid // 10000, sid // 100 % 100, sid % 100)
        delta = d - date(1, 1, 1)
        return json.dumps([delta.days, d.isoweekday(), now_str])
    except:
        return json.dumps([None, -1, now_str])


if __name__ == "__main__":
    app.run(host="localhost", port=8818, debug=True)
