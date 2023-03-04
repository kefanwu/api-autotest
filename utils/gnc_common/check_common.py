import datetime
import hashlib
import json
import time

import yaml
from utils.config import get_path


class check_common():

    def __init__(self):
        """获取基础配置"""
        self.file = open(get_path() + "/utils/gnc_common/gnc_common_data/gnc_common.yaml", "r", encoding="utf-8")
        self.data = yaml.load(self.file, Loader=yaml.FullLoader)
        self.host = self.data["host_list"]

    """校验用户输入环境在配置中是否存在，不存在则默认使用 pre"""
    def check_host(self, settings):
        if settings.lower() in self.host:
            print("环境校验完成，使用环境：{0}".format(settings))
            return settings.lower()
        else:
            print("环境校验完毕，传入环境变量：{0}不在列表中，默认使用pre环境".format(settings))
            return "pre"

    """md5加密"""
    def encryption_md5(self, *args):
        strs = "".join(str(x) for x in args)
        print("加密前字符串：{0}".format(strs))
        str1 = hashlib.md5(strs.encode("utf-8")).hexdigest()
        print("加密结果：{0}".format(str1))
        return str1

    """生成邮箱"""
    def random_email(self, email="", settings=""):
        if email:
            return email
        else:
            numb = str(int(time.time() * 1000))
            print(numb)
            email = numb + "@" + str(settings) + ".com"
            return email

    """生成密码"""
    def random_password(self, password=""):
        if password:
            return password
        else:
            return "aa666666"

    """时区转换"""
    def time_zone(self, zone):
        pass

    """获取日期，输出YYYY-MM-DD"""
    def input_YMD(self, days=0):
        today = datetime.date.today()
        print(today)
        print(type(today))
        oneday = datetime.timedelta(days=days)
        print(oneday)
        print(type(oneday))
        yesterday = today - oneday
        return str(yesterday)

    """输出当前时间戳"""
    def input_timestr(self, bit=13):
        if bit == 13:
            timeStamp = int(time.time() * 1000)
        else:
            timeStamp = int(time.time())
        return timeStamp
    """输出指定日期时间戳 data= 2022-06-15 19:00:00"""
    def input_timestrall(self, data):
        if data:
            timeArray = time.strptime(data, "%Y-%m-%d %H:%M:%S")
            # 转换为时间戳:
            timeStamp = int(time.mktime(timeArray) * 1000)
            print(timeStamp)
            return timeStamp
        else:
            return int(time.time() * 1000)

    """处理量表内容，获取量表的questionId"""

    def mach_ques(self, res):
        # 量表问卷题目列表
        questionIdList = []
        if res["data"]["sectionList"]:
            for i in res["data"]["sectionList"]:
                datas = {}
                datas["title"] = i["title"]
                datas["questionId"] = i["questionId"]
                questionIdList.append(datas)
            return questionIdList
        else:
            print("量表题目中无题目列表数据，请检查返回结果：{0}".format(res))
            return "error"

    """组装量表入参"""
    def check_crf_param(self, res, param, type, Medication):
        crf = self.mach_ques(res)
        params = param
        for i in params:
            for j in crf:
                if i["title"] == j["title"]:
                    i["questionId"] = j["questionId"]
                    if type == "Remission" and i["title"] == "What is your current weight?":
                        i["answerData"] = 200
                    if Medication == "NO" and i["title"] == "What diabetes medication(s) are you taking?":
                        i["answerData"] = "[\"\"]"
                    i.pop("title", None)
                    break
        return params

    """输出时间戳list"""
    def input_time_list(self, startDate, endDate):
        HMS = time.strftime("%H:%M:%S", time.strptime(startDate, '%Y-%m-%d %H:%M:%S'))
        print(type(HMS))
        startdate = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.strptime(startDate, '%Y-%m-%d %H:%M:%S')), "%Y-%m-%d")
        enddate = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.strptime(endDate, '%Y-%m-%d %H:%M:%S')), "%Y-%m-%d")
        time_list = []
        while (enddate - startdate).days >= 0:
            ls = datetime.datetime.strftime(startdate, "%Y-%m-%d") +" "+ HMS
            date = time.strptime(ls, '%Y-%m-%d %H:%M:%S')
            print("转换前时间：{0}".format(date))
            # 转换为时间戳:
            timeStamp = int(time.mktime(date) * 1000)
            time_list.append(timeStamp)
            startdate = startdate + datetime.timedelta(days=1)
        print(time_list)
        return time_list

    """饮食数据列表处理"""
    def processing_diet_data(self,dietData, timing):
        # 校验餐段是否正确
        foodlist =[]
        if timing:
            if dietData["data"][timing]:
                datalist = dietData["data"][timing]
                for i in datalist:
                    foods = {}
                    foods["dietRecipe"] = i
                    foods["eatenNoOfServing"] = 1
                    foodlist.append(foods)
        if not foodlist:
            foodlist = self.data["foodList"]
        return foodlist

    def check_respone(self, expets_data, data_respone):
        expets = expets_data
        data_respone = data_respone
        result = {}
        # if data_respone is list:
        #     for data_resp in data_respone:

        try:
            for k, v in expets.items():
                print(k, ">>>", v)
                if type(v) is dict:
                    result = self.check_respone(v, data_respone[k])
                    print("a1:::", result)
                    if result["success"] != True:
                        break
                elif type(v) is list:
                    for i in range(len(v)):
                        print("list-----i={0}".format(i))
                        print(type(v[i]))
                        if (type(v[i]) is dict) or (type(v[i]) is list):
                            result = self.check_respone(v[i], data_respone[k][i])
                            print("aa:::", result)
                            if result["success"] != True:
                                break
                        elif v[i] in data_respone[k]:
                            result['success'] = True
                        else:
                            result['success'] = False
                            result['fail_response'] = 'except_result=' + str({k: expets[k]}) + ' but really_reslut=' + str(
                                {k: data_respone[k]})
                            return result
                else:
                    if v == data_respone[k]:
                        result['success'] = True
                    else:
                        result['success'] = False
                        result['fail_response'] = 'except_result=' + str({k: expets[k]}) + ' but really_reslut=' + str({k: data_respone[k]})
                        break
        except Exception as e:
                    print("期望结果：{0}，实际返回值：{1}，错误信息：{2}".format(expets, data_respone, e))
                    result['success'] = False
                    return result
        return result

    def list_data(self, a, b):
        print("a={0},b={1}".format(a, b))
        if type(a) is list:
            for i in a:
                if (type(i) is dict) or (type(i) is list):
                    self.list_data(i, b)
                else:
                    if i in b:
                        print("true")
                    else:
                        print("false")
                        break
        elif type(a) is dict:
            for k, v in a.items():
                print(k, ">>>", v)
                if type(b) is list:
                    b2 =[]
                    b2.append(b)
                    for b1 in b:
                        if self.check_dict(b1, k):
                            b2.remove(b)
                            b2.append(b1[k])
                else:
                    b2 = b
                print("b2:{0}".format(b2))
                if type(v) is dict:
                    self.list_data(v, b2)
                elif type(v) is list:
                    self.list_data(v, b2)
                else:
                    # a和b判断
                    if v in b2:
                        print("true1")
                    else:
                        print("false1")

    def check_dict(self, data, num):
        if type(data) is dict:
            if num in data.keys():
                return True
            else:
                return False
        else:
            return False

    """参数替换 
        params： yaml文件读取的入参
        rep_param: 替换的参数
    """
    def param_replace(self, params, rep_param={}):
        param = json.dumps(params)
        if param.find('$visitSn') >= 0:
            if "visitSn" in rep_param.keys():
                param = param.replace('$visitSn', str(rep_param["visitSn"]))
        if param.find('$userId') >= 0:
            if "userId" in rep_param.keys():
                param = param.replace('$userId', str(rep_param["userId"]))
        if param.find('$patientSn') >= 0:
            if "patientSn" in rep_param.keys():
                param = param.replace('$patientSn', str(rep_param["patientSn"]))
        if param.find('$NowDate') >= 0:
            param = param.replace('$NowDate', self.input_YMD())
        res = json.loads(param)
        return res



if __name__ == "__main__":
    aa = check_common()
    # B = aa.encryption_md5("21", 2222, "wqeqw")
    # B = aa.input_YMD(4)
    expets = [{"data": {"data1": [{"data2": 1}, {"data3": 4}, "123"], "data4": 2}, "data5": 3}, 111]
    data_respone = {"data": {"data1": [{"data2": 1}, {"data3": "$visitSn"}, {"data6": "$visitSn"}, "123"], "data4": 2}, "data5": 3}
    # b = aa.list_data(expets, data_respone)
    b = aa.param_replace(data_respone, {"visitSn": 123})
    print(b)
    # B = aa.input_time_list("2022-06-01 12:22:22","2022-06-10 12:22:22")
    # Timing = {"BREAKFAST": "breakfasts", "DINNER": "lunches", "LUNCH": "dinners", "SNACKS": ""}
    # print(Timing.keys())
    # print(B)
    pass
