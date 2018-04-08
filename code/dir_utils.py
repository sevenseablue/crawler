# -*- encoding: utf-8 -*-

import os
import errno
import re, requests
import time
import shutil

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

def get_files(path):
    files = os.listdir(path)
    for file_name in files:
        # print(file_name)

        if len(file_name.split("."))==4:
            fr = open("%s/%s" % (path, file_name), 'r')
            lines = [l for l in fr]
            rows_num = len(lines) - 1
            print("%s %s; \ngo" % ("select count(*) from", ".".join(file_name.split(".")[:3])))
            print("-- %s \n" % (rows_num))



def getHtml(request_url):
    page = requests.get(request_url, headers=headers)
    html_contents = page.text
    html = html_contents
    time.sleep(0.01)
    return html


def download(download_info):
    (url, path) = download_info
    for i in range(3):
        time.sleep(0.1)
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
        try:
            r = requests.get(url, timeout=1, stream=True)
            if r.status_code == 200:
                with open(file, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    return 1

        except:
            time.sleep(1)
            pass
    return 0




if __name__ == "__main__":
    path = r"E:\qunarproject\atploss\sample"
    get_files(path)
