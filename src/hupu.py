# coding: utf8

import re
import json
import ast

import snownlp
from bs4 import BeautifulSoup
import datetime

import utils
import chat_utils
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

        quote_content = soup.find_all(attrs={"class": "quote-content"})
        quote_content_str = quote_content[0].get_text()



        sn = snownlp.SnowNLP(subheadstr)
        print(subheadstr)
        print(sn.summary()[0], sn.sentiments, sn.keywords())
        senti = ", 呵呵"
        if sn.sentiments>=0.8:
            senti = "happy， 哈哈"
        if sn.sentiments<=0.2:
            senti = "悲伤， 气愤"

        reponse_str = "%s, %s" % (chat_utils.deepThought.get_response(sn.summary()[0]), senti)
        self._post_writer.write("url\001%s\n" % url1)
        self._post_writer.write("subhead\001%s\n" % subheadstr)
        self._post_writer.write("quote_content\001%s\n" % quote_content_str)
        self._post_writer.write("sn.summary()[0]\001%s\n" % sn.summary()[0])
        self._post_writer.write("reponse_str\001%s\n" % reponse_str)


    def processOneList(self, url):
        status_code, html = utils.getHtml(url)
        bookes = re.findall(
            # r"(?ms)\<div class\=\"discoverAlbum_item\" album_id\=\"([0-9]+)\"\>.*?\<a href\=\"([^\"]+)\".*?\<img src\=\"([^\"]+)\".*?title\=\"([^\"]+)\"",
            r"""(?ms)\<div class\=\"titlelink box\".*?href\=\"\/(\d+)\.html\".*?\<span class\=\"ansour box\"\>(\d+)\&nbsp;\/\&nbsp;(\d+)\<\/span\>""",
            html)
        for book in bookes:
            print(book)
            if book[0] != "15806550":
                self.processOnePost(book)


    def processLists(self, url="https://bbs.hupu.com/bxj-postdate-%s"):
        for i in range(10, 11):
            urlstr = url % (i)
            print(urlstr)
            self.processOneList(urlstr)


        # self.closeFile()


    def closeFile(self):
        self._post_writer.close()


if __name__ == "__main__":
    hupu1 = hupu(r"E:\github\crawler\data", download=False)
    hupu1.processLists()
    # hupu1.processOnePost(["20188481", 28, 30])
