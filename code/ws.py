# coding: utf8

import re
import json
import ast

import utils

class ws():
    def __init__(self):
        self.calendar_url = "https://api-prod.wallstreetcn.com/apiv1/finfo/calendars?start=%s&end=%s"

    def getCarlendarOneDay(self, dtstr):
        dt = utils.dt_str_to_dt(dtstr)
        dts = int(dt.timestamp())
        dte = int((dt + datetime.timedelta(seconds=86399)).timestamp())
        url = "https://api-prod.wallstreetcn.com/apiv1/finfo/calendars?start=%s&end=%s&stars" % (dts, dte)
        status_code, car = utils.getHtml(url)
        print(car)
        # j = json.loads(car)
        with open(r"E:\github\crawler\data\ws\carlendar\%s.txt" % dtstr[:10], 'w', encoding="utf8") as fw:
            fw.write(car)

    def getCarlendar(self, date1, date2):
        # d1 = utils.dt_str_to_dt(date1)
        # d2 = utils.dt_str_to_dt(date2)
        date1 = date1 + " 00:00:00"
        date2 = date2 + " 00:00:00"
        for dt in utils.dt_dt_list(date1, date2):
            dtstr = utils.dt_dt_to_str(dt)
            self.getCarlendarOneDay(dtstr)



import time

import sys

import datetime
day1 = datetime.datetime.strptime("2014-12-01 00:00:00", "%Y-%m-%d %H:%M:%S")
day2 = datetime.datetime.strptime("2014-12-07 23:59:59", "%Y-%m-%d %H:%M:%S")
print(day1.timestamp())
print(day2.timestamp())
# print(time.time())
# sys.exit(-1)
if __name__ == "__main__":
    ws = ws()
    ws.getCarlendar("2017-01-01", "2017-01-02")