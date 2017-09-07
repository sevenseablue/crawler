
import sys
import datetime

def dt_str_to_dt(str1):
    return datetime.datetime.strptime(str1, "%Y-%m-%d %H:%M:%S")

def dt_dt_to_str(dt1):
    return datetime.datetime.strftime(dt1, "%Y-%m-%d %H:%M:%S")

def dt_dt_to_stri(dt1):
    return datetime.datetime.strftime(dt1, "%Y%m%d%H%M%S")

def dt_str_to_date(str1):
    return datetime.datetime.strptime(str1, "%Y-%m-%d")

def dt_date_to_str(dt1):
    return datetime.datetime.strftime(dt1, "%Y-%m-%d")

if __name__ == "__main__":
    print(dt_dt_to_stri(datetime.datetime.now()))