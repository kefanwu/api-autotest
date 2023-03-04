# coding: utf-8
import json
import requests
import os
from utils.config import get_path
from utils.log import logger
import time
from urllib import parse
import hashlib
import base64
import hmac
import sys
from utils.config import *

cur_path = get_path()


def get_report_file(report_path):
    """第三步：获取最新的测试报告
    :param report_path:
    """
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    logger.info("获取最新测试生成的报告：" + lists[-1])
    file_new = os.path.join(lists[-1])
    return file_new


def dingding_robot(data):
    # 自测机器人

    millis = int(round(time.time() * 1000))
    tester = "https://oapi.dingtalk.com/robot/send?" \
             "access_token=b2b0b1c323cab8c5c904a081587dc0066263bb7e6cc8157ee87caff2a55d98e7"
    # 业务测试组
    tester_group = "https://oapi.dingtalk.com/robot/send?" \
                   "access_token=d06aca9501837309c1e7533b044e0f81518790202beee7077c4917061033f0d7"
    # 测试伙伴群
    test_automated = "https://oapi.dingtalk.com/robot/send?" \
                     "access_token=dcb94400862d31f6e704924e023f0180918f92e5ae2a47051094440f2feef44e"
    # 自动化反馈群
    tester_fankui = "https://oapi.dingtalk.com/robot/send?access_token=363f6aef371338ab990a9ad2a1c962bf1dbf0b2042363d8fae65050f7e73e8f5"
    webhook = tester_fankui
    headers = {'content-type': 'application/json'
               }  # 请求头

    r = requests.post(webhook, headers=headers, data=json.dumps(data))
    r.encoding = 'utf-8'
    return r.text


def yach_robot(data):
    # 自测机器人
    timestamp = str(round(time.time() * 1000))
    secret = 'SECa9213a092cb0ce363f35358028328116'
    Webhook = "https://yach-oapi.zhiyinlou.com/robot/send?access_token=aFhCYWFHT01PL2gyZ0RQcXBnYi9BZEs3bFFnUFVDSEhienRHa2xzbmRsVEVRdlY4OTJxZ3ZKNjdSYmgvRjNCeQ&timestamp={}&sign={}"
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = parse.quote_plus(base64.b64encode(hmac_code))
    url = Webhook.format(timestamp, sign)
    headers = {
        # heard部分直接通过chrome部分request header部分
        'Content-Type': 'application/json'
    }
    # program = {"msgtype": "text", "text": {"content": "测试一下"}, "at": {"atYachIds": ["107930"]}, "isAtAll": False}
    # data = json.dumps(program)
    # print(data)
    r = requests.post(url, data=json.dumps(data), headers=headers)
    r.encoding = 'utf-8'
    print("11111", r.text)
    return r.text


def yach_robot_izklive(data):
    # 自测机器人
    timestamp = str(round(time.time() * 1000))
    secret = 'SEC08cff75588fc6635e0cf704346c62444'
    Webhook = "https://yach-oapi.zhiyinlou.com/robot/send?access_token=NFloUWlCT3ZhWnVhNkZEU3F0YmlvSzcyYnNtanVUMktoN1NTMk5veE5FV2dEZEhOekJUZFRsbHZ2bXpzL05lYQ&timestamp={}&sign={}"
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = parse.quote_plus(base64.b64encode(hmac_code))
    url = Webhook.format(timestamp, sign)
    headers = {
        # heard部分直接通过chrome部分request header部分
        'Content-Type': 'application/json'
    }
    # program = {"msgtype": "text", "text": {"content": "测试一下"}, "at": {"atYachIds": ["107930"]}, "isAtAll": False}
    # data = json.dumps(program)
    # print(data)
    r = requests.post(url, data=json.dumps(data), headers=headers)
    r.encoding = 'utf-8'
    print("11111", r.text)
    return r.text


def test_send_news():
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "AI话术",
                    "description": "测试一下",
                    "url": "https://www.baidu.com/",
                    "picurl": "https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=3548088877,2822060228&fm=11&gp=0.jpg"
                }
            ]
        }
    }
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6af065cc-3622-40dd-a34d-b6530e91139e"
    response = requests.post(url=url, json=payload, headers=headers)
    json_data = json.loads(response.content)
    print(json_data)


def wechart_send_markdown(title, result):
    proxies = get_proxies()
    headers = {
        "Content-Type": "application/json"
    }
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6af065cc-3622-40dd-a34d-b6530e91139e"
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": " # {title}  \
                                                         \n ### 数据构造结果:   <font color=\"comment\"> {result}</font>  \
                                                         \n\n # 【因数健康】".format(title=title, result=result)
        }
    }
    response = requests.post(url=url, json=data, headers=headers, verify=False, proxies=proxies)
    json_data = json.loads(response.content)
    return json_data


def wechart_send_news(report_url, title):
    """图文类型"""
    proxies = get_proxies()
    headers = {
        "Content-Type": "application/json"
    }
    group_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6af065cc-3622-40dd-a34d-b6530e91139e"
    data = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": title,
                    "description": "详细请点击链接查看报告",
                    "url": report_url,
                    "picurl": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbpic.588ku.com%2Felement_origin_min_pic%2F19%2F04%2F11%2Fa4d15b04e336cfdb7b6d2a6c70a1b695.jpg&refer=http%3A%2F%2Fbpic.588ku.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1631436688&t=aaa1fec31c09a20711e7d8c3d94ee4ea"
                }
            ]
        }
    }

    response = requests.post(url=group_url, json=data, headers=headers, proxies=proxies)
    json_data = json.loads(response.content)
    return json_data


if __name__ == "__main__":
    # 请求参数 可以写入配置文件中
    # report_path = os.path.join(cur_path, "report")
    # get_report_file(report_path)
    # # data = {
    # #     "msgtype": "link",
    # #     "link": {
    # #         "text": "测试一下 @吴可凡\n",
    # #         "title": "测试一下",
    # #         "picUrl": "http://img2.imgtn.bdimg.com/it/u=169994266,3317316142&fm=26&gp=0.jpg",
    # #         "messageUrl": "https://daohang.izhikang.com/test/2019-03-12-16.30.43.html"
    # #     },
    # #     "at": {
    # #         "atMobiles": [
    # #             "吴可凡"
    # #         ],
    # #         "isAtAll": False
    # #     }
    # # }
    # text_data = {
    #     "msgtype": "text",
    #     "text": {
    #         "content": "测试@人员"
    #     },
    #     "at": {
    #         "atMobiles": [
    #             "17610311376"
    #         ],
    #         "isAtAll": False
    #     }
    # }
    # new_data = {
    #     "msgtype": "markdown",
    #     "markdown": {
    #         "title": "测试一下",
    #         "text": "#### 测试一下 @17610311376\n" +
    #                 "> 执行结果：失败{} 成功：{}  用例总计：{}\n\n".format("0", "1", "1") +
    #                 "> ![screenshot](http://i.serengeseba.com/uploads/i_1_828568710x2456742079_26.jpg)\n" +
    #                 "> [详细内容点击此处查看报告]({}) \n".format("https://daohang.izhikang.com/test/2019-03-12-16.30.43.html")
    #     },
    #     "at": {
    #         "atMobiles": [
    #             "17610311376"
    #         ],
    #         "isAtAll": True
    #     }
    # }
    # res = yach_robot(text_data)
    # print(res)
    # logger.info("钉钉消息发送：%r", res)  # 打印请求结果
    res = wechart_send_news()
    print(res)
