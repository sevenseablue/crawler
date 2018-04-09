
import sys
import datetime

def dt_dt_to_stri(dt1):
    return datetime.datetime.strftime(dt1, "%Y%m%d%H%M%S")

def now_str():
    return dt_dt_to_str(datetime.datetime.now())

def dt_str_to_dt(str1):
    return datetime.datetime.strptime(str1, "%Y-%m-%d %H:%M:%S")

def dt_dt_to_str(dt1):
    return datetime.datetime.strftime(dt1, "%Y-%m-%d %H:%M:%S")

def dt_str_to_date(str1):
    return datetime.datetime.strptime(str1, "%Y-%m-%d")

def dt_date_to_str(dt1):
    return datetime.datetime.strftime(dt1, "%Y-%m-%d")

def date_str_days(str1, num_days):
    dt1 = dt_str_to_date(str1)
    dt1 = dt1 + datetime.timedelta(days=num_days)
    return dt_date_to_str(dt1)

def dt_str_days(str1, num_days):
    dt1 = dt_str_to_dt(str1)
    dt1 = dt1 + datetime.timedelta(days=num_days)
    return dt_dt_to_str(dt1)

def dt_str_hours(str1, num_hours):
    dt1 = dt_str_to_dt(str1)
    dt1 = dt1 + datetime.timedelta(hours=num_hours)
    return dt_dt_to_str(dt1)

def dt_str_minutes(str1, num_minutes):
    dt1 = dt_str_to_dt(str1)
    dt1 = dt1 + datetime.timedelta(minutes=num_minutes)
    return dt_dt_to_str(dt1)

def dt_date_list(str1, str2):
    dt1 = dt_str_to_date(str1)
    dt2 = dt_str_to_date(str2)
    cur = dt1
    dt_list = []
    total_seconds = (dt2 - cur).total_seconds()

    while total_seconds>0:
        dt_list.append(dt_date_to_str(cur))
        cur = cur + datetime.timedelta(days=1)
        total_seconds = (dt2 - cur).total_seconds()

    return dt_list

def dt_dt_list(str1, str2):
    dt1 = dt_str_to_dt(str1)
    dt2 = dt_str_to_dt(str2)
    cur = dt1
    dt_list = []
    total_seconds = (dt2 - cur).total_seconds()

    while total_seconds>0:
        dt_list.append(cur)
        cur = cur + datetime.timedelta(days=1)
        total_seconds = (dt2 - cur).total_seconds()

    return dt_list

def dt_dt_minute_list(str1, str2):
    dt1 = dt_str_to_dt(str1)
    dt2 = dt_str_to_dt(str2)
    cur = dt1
    dt_list = []
    total_seconds = (dt2 - cur).total_seconds()

    while total_seconds>0:
        dt_list.append(cur)
        cur = cur + datetime.timedelta(minutes=1)
        total_seconds = (dt2 - cur).total_seconds()

    return dt_list


def dt_date_str_list(str1, str2):
    dt_list = dt_date_list(str1, str2)
    return [dt_date_to_str(e) for e in dt_list]

def dt_dt_str_list(str1, str2):
    dt_list = dt_dt_minute_list(str1, str2)
    return [dt_dt_to_str(e) for e in dt_list]



def get_operation_list(date1):
    operate_time_start = "%s 02:00:00" % date1
    operate_time_list = []
    for i in range(12):
        d1 = dt_str_hours(operate_time_start, 2 * i)
        operate_time_list.append(d1)
    return operate_time_list


def get_operation_list(date1, detect_hours):
    operate_time_start = "%s 00:00:00" % date1
    operate_time_list = []
    for i in range(1, int(24/detect_hours)+1):
        d1 = dt_str_hours(operate_time_start, detect_hours * i)
        operate_time_list.append(d1)
    return operate_time_list



def dt_str_delta_days(str1, str2):
    dt1 = dt_str_to_dt(str1)
    dt2 = dt_str_to_dt(str2)
    return (dt1-dt2).total_seconds()/(3600*24)

def dt_str_delta_minutes(str1, str2):
    dt1 = dt_str_to_dt(str1)
    dt2 = dt_str_to_dt(str2)
    return (dt1-dt2).total_seconds()/60

if __name__ == "__main__":
    # print(dt_dt_to_stri(datetime.datetime.now()))
    print(dt_dt_str_list("2017-01-01 00:00:00", "2017-01-01 01:00:00"))
    print(dt_str_minutes("2017-01-01 00:00:00", 1))