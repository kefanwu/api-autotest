import time
import datetime
from datetime import date
import calendar
from datetime import timedelta
from datetime import datetime


# 生成当前时间的时间戳，只有一个参数即时间戳的位数，默认为10位，输入位数即生成相应位数的时间戳，比如可以生成常用的13位时间戳
def now_to_timestamp(digits=10):
    time_stamp = time.time()
    digits = 10 ** (digits - 10)
    time_stamp = int(round(time_stamp * digits))
    return time_stamp


# 将时间戳规范为10位时间戳
def timestamp_to_timestamp10(time_stamp):
    time_stamp = int(time_stamp * (10 ** (10 - len(str(time_stamp)))))
    return time_stamp


# 将当前时间转换为时间字符串，默认为2017-10-01 13:37:04格式
def now_to_date_hour(format_string="%Y-%m-%d %H:%M:%S"):
    time_stamp = int(time.time())
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def now_to_date(format_string="%Y-%m-%d"):
    time_stamp = int(time.time())
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date

# 将10位时间戳转换为时间字符串，默认为2017-10-01 13:37:04格式
def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


# 将时间字符串转换为10位时间戳，时间字符串默认为2017-10-01 13:37:04格式
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


# 不同时间格式字符串的转换
def date_style_transfomation(date, format_string1="%Y-%m-%d %H:%M:%S", format_string2="%Y-%m-%d %H-%M-%S"):
    time_array = time.strptime(date, format_string1)
    str_date = time.strftime(format_string2, time_array)
    return str_date


def time_stamp_13():
    millis = int(round(time.time() * 1000))
    return millis


def time_stamp_13_data():
    now = int(round(time.time() * 1000))
    now02 = time.strftime("%Y-%m-%d", time.localtime(now / 1000))

    return now02


def last_data():
    # now_time_stamp = int(round(time.time() * 1000))
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    n_days = now + delta
    tom = n_days.strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(tom, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    time_stamp = (int(round(timeStamp * 1000)))
    return time_stamp


def get_month_range(start_date=None):
    if start_date is None:
        # print(date.today())  # 今天的日期
        start_date = date.today().replace(day=1)  # 修改当前时间。比如修改成当月1号
        # print(start_date)  # 当月的第一天日期
    days_in_month = calendar.monthrange(start_date.year, start_date.month) # 计算当月总天数
    # print(days_in_month[1])  # 31   当月总天数31天
    end_date = date.today().replace(day=days_in_month[1])
    return start_date, end_date


def get_week():
    # 当前
    now = datetime.datetime.now()
    # 上周五
    last_week_5 = now - timedelta(days=now.weekday()+3)
    str_last_5 = last_week_5.strftime("%Y-%m-%d")
    # 本周四
    this_week_4 = now + timedelta(days=3-now.weekday())
    str_this_4 = this_week_4.strftime("%Y-%m-%d")
    # 本周五
    this_week_5 = now + timedelta(days=4-now.weekday())
    str_this_5 = this_week_5.strftime("%Y-%m-%d")
    # 下周四
    next_week_4 = now - timedelta(days=now.weekday()-10)
    str_next_4 = next_week_4.strftime("%Y-%m-%d")
    data_info = [str_last_5, str_this_4, str_this_5, str_next_4]
    return data_info


def someMethod():
    currentSecond = datetime.now().second
    currentMinute = datetime.now().minute
    currentHour = datetime.now().hour

    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    return currentYear


def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime

# print(now_to_date())
# print(timestamp_to_date(1506816572))
# print(date_to_timestamp("2017-10-01 08:09:32"))
# print(timestamp_to_timestamp10(1506816572546))
# print(date_style_transfomation("2017-10-01 08:09:32"))
# print(time_stamp_13())
# print(time_stamp_13_data())
# print(last_data())

