import json
import yaml
from utils.config import get_path
from utils.gnc_common.gnc_initialize import gnc_initialize
from utils.gnc_common.gnc_request import gnc_request


class _Insulin():

    def __init__(self, setting, host, header):
        self.setting = setting
        self.host = host
        self.header = header
        """获取basal 胰岛素相关配置"""
        self.file = open(get_path() + "/utils/gnc_common/gnc_common_data/gnc_Insulin_common.yaml", "r", encoding="utf-8")
        self.data = yaml.load(self.file, Loader=yaml.FullLoader)
        self.request = gnc_request()

    def _add_basal_insulin(self, hcp_session, email):
        """创建basal胰岛素用户"""
        url = self.data["add_basal_insulin_url"]
        params = self.data["add_basal_insulin_data"]["params_data1"]
        params["patientProfile"]["firstName"] = email
        params["patientProfile"]["lastName"] = self.setting
        params["patientProfile"]["email"] = email
        try:
            response = self.request.GncRequests("post", self.host + url, hcp_session, params)
            res = json.loads(response.content)
            print("创建邮箱为：{0}的basal胰岛素账号结果：{1}".format(email, res))
            assert res["code"] == 0
            return res
        except Exception as e:
            print("basal胰岛素创建失败，失败返回：{0}".format(repr(e)))
            exit()

    """HCP开启bolus胰岛素计算器"""
    def _saveBolusInsulin(self, hcp_session, user_id):
        url = self.data["saveBolusInsulinCalculatorCfg_url"]
        params = self.data["saveBolusInsulinCalculatorCfg_data"]["params_data1"]
        params["userId"] = user_id
        try:
            response = self.request.GncRequests("post", self.host + url, hcp_session, params)
            res = json.loads(response.content)
            print("开启user_id={0}的bolus胰岛素计算器权限结果：{1}".format(user_id, res))
            assert res["code"] == 0
            return res
        except Exception as e:
            print("bolus胰岛素计算器权限开启失败，失败返回：{0}".format(repr(e)))
            exit()

class gnc_Insulin(gnc_initialize):

    """basal胰岛素用户创建"""
    def add_basal_insulin(self, hcp_session, email):
        insulin = _Insulin(setting=self.CommonSetting, host=self.CommonHost, header=self.CommonHeaders)
        respone = insulin._add_basal_insulin(hcp_session, email)
        return respone
    """bolus胰岛素计算器开启"""
    def saveBolusInsulin(self, hcp_session, userid):
        insulin = _Insulin(setting=self.CommonSetting, host=self.CommonHost, header=self.CommonHeaders)
        respone = insulin._saveBolusInsulin(hcp_session, userid)
        return respone
