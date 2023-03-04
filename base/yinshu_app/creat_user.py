class User:

    def __init__(self):
        pass

    def creat_user(self, name, cardNo, code, mobile):
        """用户实名认证"""
        headers = self.user_init_headers
        payload = self.user_init_payload
        payload["name"] = name
        payload["mobile"] = mobile
        payload["code"] = code
        payload["cardNo"] = cardNo
        response = requests.post(url=self.base_url + self.user_init_url, json=payload, headers=headers, cookies=self.cookie)
        self.assertEqual(response.status_code, self.user_init_expect['status_code'], "实名认证接口请求失败")
        data = json.loads(response.content)
        result = json.dumps(data, ensure_ascii=False, indent=4)
        try:
            code = data['code']
            # self.assertEqual(code, self.user_init_expect['code'], "断言失败")
            if code == self.user_init_expect['code']:
                return '手机号：{} 实名认证成功'.format(mobile)
            else:
                return '手机号：{} 实名认证失败, 错误信息：{}'.format(mobile, data)
        except Exception as e:
            print("错误信息：", e)
            print('url: ', response.url)
            print('headers: ', headers)
            print('参数信息: ', payload)