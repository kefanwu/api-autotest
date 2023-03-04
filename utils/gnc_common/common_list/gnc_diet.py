import json
import yaml
from utils.config import get_path
from utils.gnc_common.check_common import check_common
from utils.gnc_common.gnc_initialize import gnc_initialize
from utils.gnc_common.gnc_request import gnc_request


class _diet():

    def __init__(self, setting, host, header):
        self.setting = setting
        self.host = host
        self.header = header
        """获取饮食配置"""
        self.file = open(get_path() + "/utils/gnc_common/gnc_common_data/gnc_diet_common.yaml", "r", encoding="utf-8")
        self.data = yaml.load(self.file, Loader=yaml.FullLoader)
        self.request = gnc_request()

    """获取饮食打卡推荐食谱"""
    def _record_recommend(self, user_session, dateTime, visitSn):
        # 获取本地的配置
        url = self.data["record_recommend_url"]
        # 组装参数
        params = {}
        params["visitSn"] = visitSn
        params["dateTime"] = dateTime
        # 开始请求
        try:
            response = self.request.GncRequests("get", self.host + url, user_session, params)
            res = json.loads(response.content)
            print("饮食打卡推荐食谱列表结果：{0}".format(res))
            assert res["code"] == 0
            return res
        except Exception as e:
            print("获取饮食打卡推荐食谱列表结果异常：{0}".format(repr(e)))
            return ""

    """饮食打卡"""
    def _diet_record(self, user_session, date, foodlist, timing, visitSn, scene, id=""):
        # 获取本地的配置
        url = self.data["diet_record_url"]
        # 组装参数
        params = {}
        params["date"] = date
        params["foodList"] = foodlist
        if not scene:
            params["scene"] = "SELF"
        else:
            params["scene"] = scene
        params["timing"] = timing
        params["visitSn"] = visitSn
        params["hasDietPrescription"] = "true"
        if id:
            params["id"] = id
        # 开始请求
        print("饮食打卡入参：{0}".format(params))
        try:
            response = self.request.GncRequests("post", self.host + url, user_session, params)
            res = json.loads(response.content)
            print("饮食打卡结果：{0}".format(res))
            assert res["code"] == 0
            return res
        except Exception as e:
            print("获取饮食打卡结果异常：{0}".format(repr(e)))
            exit()

class gnc_diet(gnc_initialize):

    """用户饮食打卡"""
    def AddDiet(self, user_session, date, visitSn, meal, scene=""):
        # 对打卡餐段进行判断，不在可打卡餐段内报错退出
        meal = meal.upper()
        if meal not in self.CommonData["Timing"].keys():
            print("打卡餐段：{0}不正确，请确认".format(meal))
            exit()
        else:
            timing = self.CommonData["Timing"][meal]
        diet = _diet(setting=self.CommonSetting, host=self.CommonHost, header=self.CommonHeaders)
        diet_list = diet._record_recommend(user_session, date, visitSn)
        # 对推荐食谱做处理，有数据则使用推荐食谱打卡，无数据则使用默认菜品打卡
        food_list = check_common().processing_diet_data(diet_list, timing)
        record_diet = diet._diet_record(user_session, date, food_list, meal, visitSn, scene)
        return record_diet

    pass