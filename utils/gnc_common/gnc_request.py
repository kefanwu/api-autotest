import warnings

import requests
from utils.config import get_proxies

class gnc_request():

    """
    设置用户请求header
    """
    def __init__(self):
        self.proxies = get_proxies()
        print("代理：{0}".format(self.proxies))
        self.headers = {
            'content-type': 'application/json;charset=UTF-8',
            'Connection': 'close',
            'Referer': "",
        }
        """解决报错"""
        warnings.simplefilter('ignore', ResourceWarning)

    """
        封装请求接口
    """
    def GncRequests(self, Type, Url, user_session="", Params=""):
        print("请求url：{0}".format(Url))
        self.headers["Referer"] = self.check_url(Url)
        if Type.lower() == "get":
            if user_session:
                if Params:
                    Respone = user_session.get(url=Url, params=Params, headers=self.headers, verify=False, proxies=self.proxies)
                else:
                    Respone = user_session.get(url=Url, headers=self.headers, verify=False, proxies=self.proxies)
            else:
                if Params:
                    Respone = requests.get(url=Url, params=Params, headers=self.headers, verify=False, proxies=self.proxies)
                else:
                    Respone = requests.get(url=Url, headers=self.headers, verify=False, proxies=self.proxies)
        elif Type.lower() == "post":
            if user_session:
                if Params:
                    Respone = user_session.post(url=Url, json=Params, headers=self.headers, verify=False, proxies=self.proxies)
                else:
                    Respone = user_session.post(url=Url, headers=self.headers, verify=False, proxies=self.proxies)
            else:
                if Params:
                    Respone = requests.post(url=Url, json=Params, headers=self.headers, verify=False, proxies=self.proxies)
                else:
                    Respone = requests.post(url=Url, headers=self.headers, verify=False, proxies=self.proxies)
        elif Type.lower() == "delete":
            if user_session:
                if Params:
                    Respone = user_session.delete(url=Url, params=Params, headers=self.headers, verify=False, proxies=self.proxies)
                else:
                    Respone = user_session.delete(url=Url, headers=self.headers, verify=False, proxies=self.proxies)
            else:
                if Params:
                    Respone = requests.delete(url=Url, params=Params, headers=self.headers, verify=False, proxies=self.proxies)
                else:
                    Respone = requests.delete(url=Url, headers=self.headers, verify=False, proxies=self.proxies)
        return Respone

    def check_url(self, url):
        try:
            new_url = url.split("/")[0] + "//" + url.split("/")[2]
        except Exception as e:
            print("获取url域名失败，原url：{0}，失败报错：{1}".format(url, repr(e)))
            exit()
        print("获取用户的域名：{0}".format(new_url))
        return new_url


if __name__ == "__main__":
    gnc_request().check_url()
