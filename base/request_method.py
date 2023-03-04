# conding:utf-8
import requests
import json


class RunMain:

    def __init__(self, url, params, data, headers, method):
        self.url = url
        self.params = params
        self.data = data
        self.headers = headers
        self.method = method

    def send_post(self):
        if 'json' in self.headers['Content-Type']:
            response = requests.post(url=self.url, json=self.data, headers=self.headers)
            return response
        else:
            response = requests.post(url=self.url, data=self.data, headers=self.headers)
            return response

    def send_get(self):
        response = requests.get(url=self.url, params=self.params, headers=self.headers)
        return response

    def parser_response(self, json_data):
        if isinstance(json_data, dict):
            return json.dumps(json_data, sort_keys=True, ensure_ascii=False, indent=4)
        else:
            return "参数类型错误，请输入json类型"

    def run_main(self):
        if self.method == 'GET':
            respose = self.send_get()
        else:
            respose = self.send_post()
        return respose


