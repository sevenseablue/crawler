# coding: utf8

import re
import json
import ast

import utils


class ximalaya():
    def __init__(self, data_dir, download=False):
        self._data_dir = data_dir
        self._book_d = {}
        self._sound_d = {}
        self._soundDataDir = data_dir + "/sounds"
        utils.mkdir_p(self._soundDataDir)
        self._download = download

        self._booksFile = data_dir + "/books.txt"
        f_b = open(self._booksFile, 'r', encoding="utf-8")
        for line in f_b:
            line = line.strip()
            if line.startswith("["):
                list1 = ast.literal_eval(line)
                self._book_d[list1[0]] = list1
        f_b.close()

        self._soundsFile = data_dir + "/sounds.txt"
        f_s = open(self._soundsFile, 'r', encoding="utf-8")
        for line in f_s:
            line = line.strip()
            if line.startswith("["):
                list1 = ast.literal_eval(line)
                self._sound_d[list1[0]] = list1
        f_s.close()


        self._booksFileWriter = open(self._booksFile, 'wb')
        self._soundsFileWriter = open(self._soundsFile, 'wb')

    def getSoundInfo(self, url):
        status_code, html = utils.getHtml(url)
        # {"id":23787900,"play_path_64":"http://audio.xmcdn.com/group18/M00/A0/A0/wKgJKlgMtQ6DlIHKADIcioqs3bY923.m4a", \
        # "play_path_32":"http://audio.xmcdn.com/group20/M02/A1/EA/wKgJJ1gMtt-Bgw_tABMrJkgLTWU302.m4a",
        # "play_path":"http://audio.xmcdn.com/group18/M00/A0/A0/wKgJKlgMtQ6DlIHKADIcioqs3bY923.m4a",
        # "duration":405,"title":"\u5f15\u5b50","nickname":"\u60f3\u5f55\u975e\u975e\u9891\u9053",
        # "uid":44083167,"waveform":"group17/M02/A2/4E/wKgJKVgMtVOznUBjAAAKPZCIi5Y7922.js",
        # "upload_id":"u_23871683","cover_url":"http://fdfs.xmcdn.com/group19/M06/A1/DB/wKgJK1gMtOmTOF5RAAGJtVGwTuQ436.jpg",
        # "cover_url_142":"http://fdfs.xmcdn.com/group19/M06/A1/DB/wKgJK1gMtOmTOF5RAAGJtVGwTuQ436_web_large.jpg",
        # "formatted_created_at":"10\u670823\u65e5 21:03","is_favorited":false,
        # "play_count":114718,"comments_count":109,"shares_count":0,"favorites_count":335,
        # "album_id":5613404,"album_title":"\u65e0\u7f6a\u8fa9\u62a4\u2014\u5f20\u6d77\u751f","intro":null,
        # "have_more_intro":false,"time_until_now":"8\u6708\u524d","category_name":"book",
        # "category_title":"\u6709\u58f0\u4e66","played_secs":null,"is_paid":false,"is_free":null,
        # "price":null,"discounted_price":null}
        j = json.loads(html)
        results = []
        for k in ["id", "play_path_64", "duration", "title", "uid", "play_count", "comments_count", "favorites_count",
                  "album_id", "album_title"]:
            results.append(j.get(k, ""))
        results.append(html)
        return results

    def download_sound(self, url):
        utils.download_original_name((url, self._soundDataDir))



    def processOneBook(self, book):
        url1 = book[1]
        status_code, html = utils.getHtml(url1)

        pages = re.findall("data-page='(\d+)'", html)
        if pages == None or len(pages) == 0:
            pageMax = 1
        else:
            pagesInt = utils.str_list_to_int(pages)
            pagesMax = max(pagesInt)

        sound_ids_all = []
        # print(pages)
        for i in range(1, pagesMax + 1):
            url2 = url1 + "?page=%s" % i
            status_code, html = utils.getHtml(url2)

            sound_ids_strings = re.findall(
                r"(?ms)\<div class\=\"personal_body\" sound_ids=\"([0-9,]+)\">",
                html)
            if sound_ids_strings is not None and len(sound_ids_strings) == 1:
                sound_ids = sound_ids_strings[0].strip(",").split(",")
                sound_ids_int = utils.str_list_to_int(sound_ids)
                sound_ids_all.extend(sound_ids_int)

                for sound_id in sound_ids_int:
                    url3 = "http://www.ximalaya.com/tracks/%s.json" % sound_id
                    # print(url)
                    sound_info = self.getSoundInfo(url3)
                    soundUrl = sound_info[1]
                    if self._download and not (sound_id in self._sound_d) :
                        # print("downloading...")
                        self.download_sound(soundUrl)
                    self._sound_d[sound_id] = sound_info
                    self._soundsFileWriter.write((str(sound_info) + "\n").encode("utf8"))
                    self._soundsFileWriter.flush()

            else:
                print(book, " sound_ids_str is None")
        book.append(sound_ids_all)
        self._book_d[book[0]] = book
        self._booksFileWriter.write((str(book)+"\n").encode("utf8"))
        self._booksFileWriter.flush()

    def processOnePage(self, url):
        status_code, html = utils.getHtml(url)
        bookes = re.findall(
            r"(?ms)\<div class\=\"discoverAlbum_item\" album_id\=\"([0-9]+)\"\>.*?\<a href\=\"([^\"]+)\".*?\<img src\=\"([^\"]+)\".*?title\=\"([^\"]+)\"",
            html)
        for book in bookes:
            print(book)
            book = list(book)
            self.processOneBook(book)


    def processYouShengShu(self, url="http://www.ximalaya.com/dq/book/"):
        status_code, html = utils.getHtml(url)
        # pages = re.findall("unencode\>([0-9]+)\<\/a\>", html)
        pages = re.findall("data-page='(\d+)'", html)
        pagesInt = utils.str_list_to_int(pages)
        pagesMax = max(pagesInt)
        print(pages)
        for i in range(48, pagesMax + 1):
            url2 = url + str(i) + "/"
            self.processOnePage(url2)
            break

        self.closeFile()

    def closeFile(self):
        self._booksFileWriter.close()
        self._soundsFileWriter.close()


if __name__ == "__main__":
    ximalaya = ximalaya(r"E:\github\crawler\data", download=False)
    ximalaya.processYouShengShu()
