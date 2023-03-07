"""
获取登陆cookie
"""
# 导入需要的依赖文件
import requests  # requests用于http协议请求
import yaml  # 用于读取data数据层中的yaml文件
from utils.config import *
import nb_log


class Login():
    def __init__(self):
        self.proxies = get_proxies()
        # try:
        #     app_base_url = gl.get_yaml('ihospital')
        #     web_base_url = gl.get_yaml('florence')
        # except:
        #     gl._init()
        #     app_base_url = gl.get_yaml('ihospital')
        #     web_base_url = gl.get_yaml('florence')
        self.gnc_base_url = get_base_url('routines')
        self.wenlai_base_url = get_base_url('wenlai')

    def patient_login(self, user_name):
        """患者后台登录"""
        login_url = ''
        headers = {'content-type': 'application/json;charset=UTF-8',
                   'TENANT': 'h1'
                   }
        post_data = {"userName": user_name, "password": "123456ABC"}
        session = requests.session()
        # 发起post请求
        try:
            session.post(self.app_base_url + login_url, json=post_data, headers=headers, verify=False,
                         proxies=self.proxies)
            print('获取患者后台用户session', session)
            session.close()
            return session
        except Exception as e:
            print('获取患者后台session失败：\n{}'.format(e))

    def patient_h5_login(self, phone):
        """患者H5登录"""
        Code_url = ''
        login_url = ''
        headers = {'content-type': 'application/json;charset=UTF-8',
                   'TENANT': 'h1'
                   }
        code_data = {"mobile": phone}
        login_data = {"mobile": phone, "code": "555666"}
        session = requests.session()
        # 发起post请求
        try:
            code_res = session.post(self.app_base_url + Code_url, json=code_data, headers=headers, verify=False,
                                    proxies=self.proxies)
            json_data = json.loads(code_res.content)
            assert json_data['code'] == 0
            login_res = session.post(self.app_base_url + login_url, json=login_data, headers=headers, verify=False,
                                     proxies=self.proxies)
            login_json = json.loads(login_res.content)
            assert login_json['code'] == 0
            print('获取患者H5用户session', session)
            session.close()
            return session
        except Exception as e:
            print('获取患者H5session失败：\n{}'.format(e))

    def app_login(self, app_phone):
        """app端登录"""
        # requests.adapters.DEFAULT_RETRIES = 5
        url = ""
        headers = {
            'content-type': 'application/json;charset=UTF-8',
        }
        post_data = {"code": '555666', "mobile": app_phone}
        session = requests.session()
        # session = self.web_session()

        # 发起post请求
        try:
            r = session.post(self.app_base_url + url, json=post_data, headers=headers, verify=False,
                             proxies=self.proxies)
            print('获取app端用户session', r.cookies['SESSION'])
            print('app端登陆', r.text)
            return session
        except Exception as e:
            print('获取app端session失败：\n{}'.format(e))

    def borgesAdm_login(self, app_phone):
        """宁波线下管理中心后台登陆"""
        # requests.adapters.DEFAULT_RETRIES = 5
        url = ""
        headers = {
            'content-type': 'application/json;charset=UTF-8',
        }
        post_data = {"code": '555666', "mobile": app_phone}
        session = requests.session()
        # session = self.web_session()

        # 发起post请求
        try:
            r = session.post(self.app_base_url + url, json=post_data, headers=headers, verify=False,
                             proxies=self.proxies)
            print('宁波线下管理后台session', r.cookies['SESSION'])
            return session
        except Exception as e:
            print('获取app端session失败：\n{}'.format(e))

    def ihospital_login(self, phone):
        """运营后台登录"""
        # sso_url = ''
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
            session.post(self.web_base_url + login_url, json=post_data, headers=headers)
            session.close()
            return session
        except Exception as e:
            print('获取运营后台session失败：\n{}'.format(e))

    def web_session(self):
        """集团安全web网关安全校验"""
        try:
            session = requests.session()
            session.get("")
            session.close()
            print(session)
            return session
        except Exception as e:
            print('获取session失败：\n{}'.format(e))

    def ihospitalnb_login(self, phone):
        """宁波项目运营后台登录"""
        session = self.web_session()
        headers = {
            'content-type': 'application/json;charset=UTF-8'
        }
        post_data = {"code": self.code, "name": phone}
        # login_url = '/borgesAdm/usercenter/manage/login/mobile'
        # web_url = self.data['config']['ihospital_beta']
        # print(web_url + login_url)
        # print(self.code)
        # 发起post请求
        url = ""
        try:
            session.post(url=url, json=post_data, headers=headers)
            session.close()
            return session
        except Exception as e:
            print('获取运营后台session失败：\n{}'.format(e))

    def patient_h5_login_new(self, phone):
        """患者H5登录"""
        login_url = ''
        headers = {'content-type': 'application/json;charset=UTF-8',
                   'TENANT': 'h1'
                   }
        login_data = {"mobile": phone, "code": "555666"}
        session = requests.session()
        # 发起post请求
        try:
            login_res = session.post(self.app_base_url + login_url, json=login_data, headers=headers,
                                     verify=False, proxies=self.proxies)
            print('获取患者H5用户session', session)
            session.close()
            return session
        except Exception as e:
            print('获取患者H5session失败：\n{}'.format(e))

    def routines_app_login(self, email):
        login_url = '/routines/usercenter/user/mockLogin'
        headers = {'content-type': 'application/json;charset=UTF-8'}
        login_data = {
            "email": email
        }
        session = requests.session()
        # 发起post请求
        try:
            login_res = session.post(self.gnc_base_url + login_url, json=login_data, headers=headers,
                                     verify=False, proxies=self.proxies)
            print('获取用户session', session)
            session.close()
            return session
        except Exception as e:
            print('获取患者H5session失败：\n{}'.format(e))


if __name__ == "__main__":
    Login().routines_app_login('userwukefan92201@163.com')
    # Runn().ihospital_login('13366668888')
