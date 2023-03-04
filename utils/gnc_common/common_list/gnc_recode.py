import json
import yaml
from utils.config import get_path
from utils.gnc_common.check_common import check_common
from utils.gnc_common.gnc_initialize import gnc_initialize
from utils.gnc_common.gnc_request import gnc_request


class _record():

    def __init__(self, setting, host, header):
        self.setting = setting
        self.host = host
        self.header = header
        """获取注册登录配置"""
        self.file = open(get_path() + "/utils/gnc_common/gnc_common_data/gnc_record_common.yaml", "r", encoding="utf-8")
        self.data = yaml.load(self.file, Loader=yaml.FullLoader)
        self.request = gnc_request()

    """
       新增医学指标(手动增加) 指标打卡 血糖 血压 体重 腰围等
       recordType 记录方式 1-人工记录(默认) 2-设备记录 10-来自基线数据
    """
    def _medical_add(self, user_session, RecordData, measureTime, measureValue, recordType):
        # 获取本地的配置
        url = self.data["medical_add_url"]
        # 获取对应指标打卡基础参数
        if RecordData in self.data["medical_list"]:
            num = self.data["medical_list"][RecordData]
        else:
            print("输入的打卡指标--{0}不存在，请校验后输入".format(RecordData))
            exit()
        params = {}
        # 打卡时间
        params["measureTime"] = measureTime
        # 指标类型
        params["indicationType"] = num["indicationType"]
        # 记录方式 1-人工记录(默认) 2-设备记录
        params["recordType"] = recordType
        # 指标子类型（目前只有血糖指标有）
        if "subType" in num.keys():
            params["subType"] = num["subType"]
        # 指标测量值参数填充 睡眠,血压打卡单独处理
        if not measureValue and RecordData != "bloodpressure":
            measureValue = num["measureValue"]
        if RecordData == "sleep":
            params["measureValue"] = {"bedTime": measureTime-3600000*measureValue, "wakeTime": measureTime, "measureValue": measureValue, "measureValueUnit": num["measureValueUnit"]}
        elif RecordData == "bloodpressure":
            if not measureValue:
                sbp = num["sbp"]
                dbp = num["dbp"]
            else:
                sbp = measureValue.split("/")[0]
                dbp = measureValue.split("/")[1]
            params["measureValue"] = {"dbp": int(dbp), "sbp": int(sbp), "measureValueUnit": num["measureValueUnit"], "valueForShow":[{"value": str(sbp)+"/"+str(dbp), "unit":num["measureValueUnit"]}]}
        else:
            params["measureValue"] = {"measureValue": measureValue, "measureValueUnit": num["measureValueUnit"],"valueForShow": [{"value": measureValue,"unit": num["measureValueUnit"]}]}
        params["measureValue"] = json.dumps(params["measureValue"])
        print("{0}打卡入参：{1}".format(self.data["medical_list"][RecordData]["name"], params))

        try:
            response = self.request.GncRequests("post", self.host + url, user_session, params)
            res = json.loads(response.content)
            print("{0}打卡结果:{1}".format(self.data["medical_list"][RecordData]["name"], res))
            assert res["code"] == 0
            return res
        except Exception as e:
            print("打卡失败失败原因:{0}".format(repr(e)))
            exit()

    """按照指标type获取用户对应指标的所有打卡数据"""
    def _medical_list(self, user_session, indicationType):
        # 获取本地的配置
        url = self.data["medical_list_url"]
        params = self.data["medical_list_data"]
        params["indicationType"] = indicationType
        try:
            response = self.request.GncRequests("get", self.host + url, user_session, params)
            res = json.loads(response.content)
            print("指标打卡记录获取结果：{0}".format(res))
            assert res["code"] == 0
            id_list =[]
            if res["data"]["models"]:
                for i in res["data"]["models"]:
                    if i["recordType"] != 10:
                        id_list.append(i["id"])
            return id_list
        except Exception as e:
            print("指标打卡记录获取结果失败，失败原因:{0}".format(repr(e)))
            exit()

    """批量删除用户打卡数据"""
    def _delete_medical(self, user_session, id):
        # 获取本地的配置
        url = self.data["medical_delete_url"]
        params = {}
        params["id"] = id
        try:
            response = self.request.GncRequests("delete", self.host + url, user_session, params)
            res = json.loads(response.content)
            print("指标打卡删除结果：{0}".format(res))
            assert res["code"] == 0
            return res
        except Exception as e:
            print("指标打卡删除失败，失败原因:{0}".format(repr(e)))
            exit()




class gnc_record(gnc_initialize):

    """用户指标打卡"""
    def MedicalAddRecord(self, user_session, RecordDatas, measureValue, measureTimes, recordType):
        # 参数构造
        if recordType in (1, 2):
            recordType = recordType
        else:
            print("记录方式:recordtype输入值为：{0}，参数值非法，默认使用1-人工记录".format(recordType))
            recordType = 1
        # 处理参数
        RecordData = RecordDatas.lower()
        measureTime = check_common().input_timestrall(measureTimes)
        record = _record(setting=self.CommonSetting, host=self.CommonHost, header=self.CommonHeaders)
        respone = record._medical_add(user_session, RecordData, measureTime, measureValue, recordType)
        return respone

    """用户多指标打卡"""
    def MedicalAddRecordList(self, user_session, Record_list, measureTimes, recordType):
        # 参数构造
        if recordType in (1, 2):
            recordType = recordType
        else:
            print("记录方式:recordtype输入值为：{0}，参数值非法，默认使用1-人工记录".format(recordType))
            recordType = 1
        record = _record(setting=self.CommonSetting, host=self.CommonHost, header=self.CommonHeaders)
        # 处理参数
        measureTime = check_common().input_timestrall(measureTimes)
        for i in Record_list.keys():
            RecordData = i.lower()
            measureValue = Record_list[i]
            respone = record._medical_add(user_session, RecordData, measureTime, measureValue, recordType)
        return respone

    """指标多天打卡"""
    def MedicalAddRecordDateList(self, user_session, Medical, startData, endData, measureValue="", difference=0, recordType=1):
        # 参数构造
        if recordType in (1, 2):
            recordType = recordType
        else:
            print("记录方式:recordtype输入值为：{0}，参数值非法，默认使用1-人工记录".format(recordType))
            recordType = 1
        # 处理打卡时间
        time_list = check_common().input_time_list(startData, endData)
        record = _record(setting=self.CommonSetting, host=self.CommonHost, header=self.CommonHeaders)
        measureValuenew = measureValue
        for i in time_list:
            respone = record._medical_add(user_session, Medical.lower(), i, measureValuenew, recordType)
            measureValuenew = measureValuenew + difference

        return respone

    """删除用户指定的指标打卡下所有数据"""
    def MedicalDeletelist(self, user_session, indicationType):
        record = _record(setting=self.CommonSetting, host=self.CommonHost, header=self.CommonHeaders)
        id_list = record._medical_list(user_session, indicationType)
        for i in id_list:
            del_resp = record._delete_medical(user_session, i)
            print(del_resp)
        return del_resp






