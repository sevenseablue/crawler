# coding: utf8

import os
import errno
import urllib.request, re, requests, urllib.parse
import time
import shutil
from PIL import Image

headers={ 'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
                "QProxy-Token": "5eXfF1"}




def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def getHtml(request_url):
#     request=urllib.request.Request(request_url,None,headers=urlopenheader)
#     response=urllib.request.urlopen(request)
    page = requests.get(request_url, headers=headers)
    page.encoding='utf-8'
    html_contents = page.text
    status_code=page.status_code
    html = html_contents
    time.sleep(0.01)
#     print(type(html))
#     html = response.read().decode('utf8')
    return status_code, html





# import geetest_hupu

# def getHupuHtml(request_url):
#     return 200, geetest_hupu.getHtml(request_url)


def download(download_info):
    (url, path) = download_info
    for i in range(3):
        time.sleep(0.1)
        #         print("trying %d times." % i)
        try:
            r = requests.get(url, timeout=1, stream=True)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    return 1

        except:
            time.sleep(1)
            pass
    return 0

def download_original_name(download_info):
    (url, path) = download_info
    name = url.split("/")[-1]
    file = path+"/"+name
    for i in range(3):
        time.sleep(0.1)

        #         print("trying %d times." % i)
        try:
            r = requests.get(url, timeout=1, stream=True)
            if r.status_code == 200:
                with open(file, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    return file

        except:
            time.sleep(1)
            pass
    return file



def str_list_to_int(list1):
    list2 = []
    for str in list1:
        list2.append(int(str))
    return list2


import datetime
def dt_str_to_dt(str1):
    return datetime.datetime.strptime(str1, "%Y-%m-%d %H:%M:%S")

def dt_dt_to_str(dt1):
    return datetime.datetime.strftime(dt1, "%Y-%m-%d %H:%M:%S")

def dt_dt_list(str1, str2):
    dt1 = dt_str_to_dt(str1)
    dt2 = dt_str_to_dt(str2)
    cur = dt1
    dt_list = []
    total_seconds = (dt2 - cur).total_seconds()

    while total_seconds>=0:
        dt_list.append(cur)
        cur = cur + datetime.timedelta(days=1)
        total_seconds = (dt2 - cur).total_seconds()

    return dt_list

# print(dt_dt_list("2017-07-09 23:59:59", "2017-07-13 23:59:59"))

def main():
    download_original_name(("https://castatic.fengkongcloud.com/cr/v1.0.1/set-000008-1.0.1-r1/9a0bf0b6ea89c0d6f48629a8fbfb2b11_fg.png", "E:\github\crawler\data"))
    # for i in range(1, 17):
    #     url = "http://cs231n.stanford.edu/slides/2017/cs231n_2017_lecture%s.pdf" % i
    #     path = "e:/tech/courses/cs231n/2017"
    #     download_original_name((url, path))

if __name__ == "__main__":
    main()