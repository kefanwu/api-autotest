import json
import requests
import yaml
from utils.config import get_path
from utils.gnc_common.gnc_request import gnc_request
from utils.gnc_common.check_common import check_common


class gnc_LoginOrRegister():

    def __init__(self, setting, host, header):
        self.setting = setting
        self.host = host
        self.header = header
        """获取注册登录配置"""
        self.file = open(get_path() + "/utils/gnc_common/gnc_common_data/LoginOrRegisterData.yaml", "r", encoding="utf-8")
        self.data = yaml.load(self.file, Loader=yaml.FullLoader)
        self.request = gnc_request()
        self.CheckCommon = check_common()



    """注册"""
    def RegisterUser(self, email="", password=""):
        Url = self.data["register_url"]
        # 邮箱检查
        Email = self.CheckCommon.random_email(email, self.setting)
        Password = self.CheckCommon.random_password(password)
        # 构造传参
        params = {}
        params["firstName"] = Email
        params["lastName"] = self.setting
        params["email"] = Email
        params["password"] = Password
        params["timeZone"] = "Asia/Shanghai"
        session = requests.session()
        Respone = {}
        try:
            res = self.request.GncRequests("post", self.host + Url, session, params)
            res = json.loads(res.content)
            print(res)
            assert res["code"] == 0
            print('注册完成,注册邮箱：{0}，密码：{1}'.format(Email, Password))
            session.close()
            self.app_session = session
            Respone["session"] = session
            Respone["email"] = Email
            Respone["password"] = Password
            return Respone
        except Exception as e:
            print("用户注册失败,失败原因：{0}，注册返回结果:{1}".format(e, res))
            exit()
            return e

    """账号登录获取登录码"""

    def GetEncryptCode(self, type=""):
        if type == "hc":
            url = self.data["hc_getEncryptCode_url"]
        else:
            url = self.data["getEncryptCode_url"]
        response = self.request.GncRequests("get", self.host + url)
        res = json.loads(response.content)
        print("获取登录码结果:{0}".format(res))
        return res

    """账号登录"""
    def loginUser(self, email, password):
        Respone = {}
        url = self.data["login_url"]
        params = {}
        # 获取登录需要使用的登录码
        encryptCodes = self.GetEncryptCode()
        encryptCode = encryptCodes["data"]["encryptCode"]
        # 进行MD5 加密
        PasswordMd5 = self.CheckCommon.encryption_md5(encryptCode, password)
        # 组装入参
        params["email"] = email
        params["password"] = PasswordMd5
        print(params["password"])
        params["encryptCode"] = encryptCode
        session = requests.session()
        try:
            # 请求
            response = self.request.GncRequests("post", self.host + url, session, params)
            res = json.loads(response.content)
            session.close()
            print('账号：{0}---登录结果：{1}'.format(email, res))
            assert res["code"] == 0
            self.app_session = session
            Respone["session"] = session
            print("登录完成输出结果：{0}".format(Respone))
            # 返回session
            return Respone
        except Exception as e:
            print("登录失败", e)
            exit()
    """HCP账号登录"""
    def loginHcp(self, email, password):
        Respone = {}
        url = self.data["hc_login_email_url"]
        params = {}
        # 获取登录需要使用的登录码
        encryptCodes = self.GetEncryptCode()
        encryptCode = encryptCodes["data"]["encryptCode"]
        # 进行MD5 加密
        PasswordMd5 = self.CheckCommon.encryption_md5(encryptCode, password)
        # 组装入参
        params["email"] = email
        params["password"] = PasswordMd5
        print(params["password"])
        params["encryptCode"] = encryptCode
        session = requests.session()
        try:
            # 请求
            response = self.request.GncRequests("post", self.host + url, session, params)
            res = json.loads(response.content)
            print('hcp账号：{0}--登录结果：{1}'.format(email, res))
            assert res["code"] == 0
            session.close()
            self.app_session = session
            Respone["session"] = session
            print(Respone)
            # 返回session
            return Respone
        except Exception as e:
            print("登录失败", repr(e))
            exit()
if __name__ == "__main__":
    settings = "pre"
    host = ""
    headers = {'content-type': 'application/json;charset=UTF-8', 'Connection': 'close','Referer': "",}
    B = gnc_LoginOrRegister(settings, host, headers).GetEncryptCode()
    print(B)


