import requests
import time

def sendreport(url,json,headers):
    print('============开始发送报告============')
    time.sleep(2)
    session = requests.session()
    res = session.get('http://proxy-auth.yiducloud.cn/sso/cookies')
    print('================res>:', res.text)
    response = session.post(url, json=json, headers=headers)
    print('发送报告的请求返回结果为：', response.text)
