# coding: utf8

import re
import json
import ast
import random

import snownlp
from bs4 import BeautifulSoup
import datetime

import utils
import date_utils

class hupu():
    def __init__(self, data_dir, download=False):
        self._data_dir = data_dir + "/hupu"
        dti = date_utils.dt_dt_to_stri(datetime.datetime.now())
        self._post_log = self._data_dir + "/post_%s.txt" % (dti)
        self._post_writer = open(self._post_log, 'w', encoding="utf8")

    def processOnePost(self, book):
        url1 = "https://bbs.hupu.com/%s.html" % (book[0])
        status_code, html = utils.getHtml(url1)
        print("status_code, ", status_code)
        if status_code != 200:
            return

        soup = BeautifulSoup(html, "lxml")
        chucuole=soup.find("h4")
        if chucuole!= None:
            print(chucuole.get_text())
            if chucuole.get_text().startswith("\n嗯，出错了..."):
                print("嗯，出错了...")
                return

        subhead = soup.find_all(attrs={"class": "subhead"})
        subheadstr = subhead[0].get_text()

        floor_box = soup.find_all(attrs={"class": "floor_box"})
        liangle = list(map(lambda x: '' if x.find(attrs={"class": "ilike_icon_list"}) is None else x.find(
            attrs={"class": "ilike_icon_list"}).get_text(), floor_box))
        lianglei = [ int(e[3:-1]) if e.startswith("亮了") else -1 for e in liangle ]
        responses = list(map(lambda x: '' if x.find(attrs={"class": "quote-content"}) is None else x.find(
            attrs={"class": "quote-content"}).get_text(), floor_box))

        # responses_2 = [e[:e.rfind("发自虎扑")].replace("\n","") if e.rfind("发自虎扑")>=0 else e.replace("\n","") for e in responses]
        responses_2 = [e[:e.rfind("发自虎扑")].replace("\n", "") if e.rfind("发自虎扑") >= 0 else e.replace("发自手机虎扑 m.hupu.com", "").replace("\n", "") for e in
                       responses]

        result_list = [(e1, e2) for e1, e2 in zip(lianglei, responses_2) if len(e2) >= 6 and e1 >= 0]
        if result_list is None or len(result_list) < 10:
            return

        result_list.sort(key=lambda x: x[0], reverse=True)
        result_list = result_list[4:]
        result_list_v2 = [ e for e in result_list if 0<e[0]<=37]
        if result_list_v2 is not None and len(result_list_v2)>0:
            result = result_list_v2[random.randint(0, len(result_list_v2)-1)]
            response_str = result[1]
        else:
            response_str = result_list[3][1]

        self._post_writer.write("%s\001%s\001\n" % (url1, response_str))
        self._post_writer.flush()


    def processOneList(self, url):
        status_code, html = utils.getHupuHtml(url)
        books = re.findall(
            # r"(?ms)\<div class\=\"discoverAlbum_item\" album_id\=\"([0-9]+)\"\>.*?\<a href\=\"([^\"]+)\".*?\<img src\=\"([^\"]+)\".*?title\=\"([^\"]+)\"",
            r"""(?ms)\<div class\=\"titlelink box\".*?href\=\"\/(\d+)\.html\".*?\<span class\=\"ansour box\"\>(\d+)\&nbsp;\/\&nbsp;(\d+)\<\/span\>""",
            html)
        soup = BeautifulSoup(html, 'lxml')
        soup.find_all(attrs={"class": "titlelink"})
        print(books)
        for book in books:
            print(book)
            if book[0] != "15806550" and random.randint(0, 9)>=7:
                self.processOnePost(book)


    def processLists(self, url="https://bbs.hupu.com/bxj-postdate-%s"):
        for i in range(7, 27):
            urlstr = url % (i)
            print(urlstr)
            self.processOneList(urlstr)


        self.closeFile()

    def closeFile(self):
        self._post_writer.close()

if __name__ == "__main__":
    hupu1 = hupu(r"E:\github\crawler\data", download=False)
    hupu1.processLists()
    # hupu1.processOnePost(["20188481", 28, 30])
