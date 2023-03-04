import json
import requests

class gnc_login():

    """账号登录获取登录码"""
    def GetEncryptCode(self):
        url = self.data["getEncryptCode_url"]
        response = requests.get(url=self.host + url, headers=self.headers, verify=False)
        res = json.loads(response.content)
        print("获取登录码结果:{0}".format(res))
        return res

    """账号登录"""
    def loginUser(self, email, password):
        url = self.data["login_url"]
        params = {}
        # 获取登录需要使用的登录码
        encryptCodes = self.GetEncryptCode()
        encryptCode = encryptCodes["data"]["encryptCode"]
        # 进行MD5 加密
        PasswordMd5 = self.CheckSetting.encryption_md5(encryptCode, password)
        # 组装入参
        params["email"] = email
        params["password"] = PasswordMd5
        print(params["password"])
        params["encryptCode"] = encryptCode
        session = requests.session()
        try:
            # 请求
            aa = session.post(self.host + url, json=params, headers=self.headers, verify=False)
            print('登录完成，获取session', aa.text)
            session.close()
            self.app_session = session
            # 返回session
            return session
        except Exception as e:
            print("登录失败", e)
            return e


if __name__ == "__main__":
    # aa = gnc_login("aws_test")
    B = gnc_login("aws_test").loginUser("1360387508@aws.com", "aa666666")
    print(B)