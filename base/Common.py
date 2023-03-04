"""
获取登陆cookie
"""
# 导入需要的依赖文件
import requests  # requests用于http协议请求
from api_auto_test.utils.config import *  # 调用工具类的中的config文件，里面有获取当前项目根目录路径
import yaml  # 用于读取data数据层中的yaml文件
from api_auto_test.utils import globalvar as gl  # 调用工具类中的globalvar，里面编写了环境区分的逻辑
# import nb_log


class Runn(object):
    def __init__(self):
        self.proxies = get_proxies()
        try:
            app_base_url = gl.get_yaml('ihospital')
            web_base_url = gl.get_yaml('florence')
        except:
            gl._init()
            app_base_url = gl.get_yaml('ihospital')
            web_base_url = gl.get_yaml('florence')

        self.file = open(get_path() + "/data/config_common.yaml", "r", encoding="utf-8")  # 打开文件
        self.data = yaml.load(self.file, Loader=yaml.FullLoader)  # 加载文件内容
        self.file.close()
        self.app_base_url = app_base_url
        self.web_base_url = web_base_url
        self.code = self.data["config"].get("code")

    def patient_login(self, user_name):
        """患者后台登录"""
        login_url = '/puh3-t2dm/api/yz-roma-biz/login.controller.web.v1/login/doLogin'
        headers = {'content-type': 'application/json;charset=UTF-8',
                   'TENANT': 'h1'
                   }
        post_data = {"userName":user_name, "password": "123456ABC"}
        session = requests.session()
        # 发起post请求
        try:
            r = session.post(self.app_base_url + login_url, json=post_data, headers=headers, verify=False, proxies=self.proxies)
            print('获取用户session', r.cookies['SESSION'])
            session.close()
            return session
        except Exception as e:
            print('获取患者后台session失败：\n{}'.format(e))

    def patient_h5_login(self, phone):
        """患者H5登录"""
        login_url = '/puh3-t2dm/api/yz-roma-biz/login.controller.web.v1/login/loginWithMobileAndCode'
        headers = {'content-type': 'application/json;charset=UTF-8',
                   'TENANT': 'h1'
                   }
        login_data = {"mobile":phone, "code": "555666"}
        session = requests.session()
        # 发起post请求
        try:
            login_res = session.post(self.app_base_url + login_url, json=login_data, headers=headers, verify=False, proxies=self.proxies)
            print('获取患者H5用户session', session)
            session.close()
            return session
        except Exception as e:
            print('获取患者H5session失败：\n{}'.format(e))

    def app_login(self, app_phone):
        """患者端app端登录"""
        # requests.adapters.DEFAULT_RETRIES = 5
        url = "/sanleixie/api/user/login/loginPatientWithMobile"
        headers = {
            'content-type': 'application/json;charset=UTF-8',
                   }
        post_data = {"code": '555666', "mobile": app_phone}
        session = requests.session()
        # session = self.web_session()

        # 发起post请求
        try:
            r = session.post(self.app_base_url + url, json=post_data, headers=headers, verify=False, proxies=self.proxies)
            print('获取患者端app端用户session', r.cookies['SESSION'])
            print('患者端app端登陆', r.text)
            return session
        except Exception as e:
            print('获取患者端app端session失败：\n{}'.format(e))

    def borgesAdm_login(self, app_phone):
        """宁波线下管理中心后台登陆"""
        # requests.adapters.DEFAULT_RETRIES = 5
        url = "/borgesAdm/usercenter/manage/login/mobile"
        headers = {
            'content-type': 'application/json;charset=UTF-8',
                   }
        post_data = {"code": '555666', "mobile": app_phone}
        session = requests.session()
        # session = self.web_session()

        # 发起post请求
        try:
            r = session.post(self.app_base_url + url, json=post_data, headers=headers, verify=False, proxies=self.proxies)
            print('宁波线下管理后台session', r.cookies['SESSION'])
            return session
        except Exception as e:
            print('获取app端session失败：\n{}'.format(e))

    def ihospital_login(self, phone):
        """运营后台登录"""
        # sso_url = 'http://proxy-auth.yiducloud.cn/sso/cookies'
        # session = requests.session()
        # session.get(sso_url)
        session = self.web_session()
        headers = {
            'content-type': 'application/json;charset=UTF-8'
        }
        post_data = {"code": self.code, "name": phone, "password": "654321"}
        login_url = '/flms/api/user/login/loginOperator'
        # 发起post请求
        try:
            r = session.post(self.web_base_url + login_url, json=post_data, headers=headers)
            print('获取用户session', r.cookies['SESSION'])
            session.close()
            return session
        except Exception as e:
            print('获取运营后台session失败：\n{}'.format(e))

    def web_session(self):
        """集团安全web网关安全校验"""
        try:
            session = requests.session()
            session.get("http://proxy-auth.yiducloud.cn/sso/cookies")
            session.close()
            print(session)
            return session
        except Exception as e:
            print('获取session失败：\n{}'.format(e))

    def app_doctor_login(self, app_phone):
        """医生端app端登录"""
        # requests.adapters.DEFAULT_RETRIES = 5
        url = "/doctor/api/user/login/loginDoctorWithMobile"
        headers = {
            'content-type': 'application/json;charset=UTF-8',
                   }
        post_data = {"code": '555666', "mobile": app_phone}
        session = requests.session()
        # session = self.web_session()

        # 发起post请求
        try:
            r = session.post(self.app_base_url + url, json=post_data, headers=headers, verify=False, proxies=self.proxies)
            print('获取医生app端用户session', r.cookies['SESSION'])
            # print('医生app端登陆', r.text)
            return session
        except Exception as e:
            print('获取医生端app端session失败：\n{}'.format(e))

    # GNC管理后台登录
    def gncadmin_management_login(self, app_phone):
        """医生端app端登录"""
        login_url = self.app_base_url + "/adm/usercenter/admin/login/email?_ts=1644475548264"
        headers = {
            'content-type': 'application/json;charset=UTF-8',
        }
        post_data = {"encryptCode": '1644475548249600447', "password": '78a5b539194d2d97b3ed6f81c6cf8c85',
                     "email": app_phone}
        # 发起post请求
        session = requests.session()
        r = session.post(url=login_url, json=post_data, headers=headers, proxies=self.proxies)
        # print('获取用户session', r.cookies['SESSION'])
        print(r.text)
        print(session)
        session.close()
        return session

        # GNC管理后台登录
    def routines_app_login(self):
        """gnc_routines_app login"""
        login_url = "https://hal-test.halhealthpilot.cf/routines/usercenter/user/mockLogin"
        headers = {
            'content-type': 'application/json;charset=UTF-8',
        }
        post_data = {"email": 'wukefan@163.com'}
        # 发起post请求
        session = requests.session()
        r = session.post(url=login_url, json=post_data, headers=headers, proxies=self.proxies)
        print('获取用户session', r.cookies['SESSION'])
        print(r.text)
        print(session)
        session.close()
        return session




if __name__ == "__main__":
    # Runn().borgesAdm_login('13377778888')
    # Runn().patient_h5_login('13023165861')
    # Runn().gncadmin_management_login('1104381972@qq.com')
    Runn().routines_app_login()

    # import time
    #
    # millis = int(round(time.time() * 1000))
    # print(millis)

