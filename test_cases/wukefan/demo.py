"""
Author: 吴可凡
detail: 新增用药记录
"""

import unittest  # 单元测试框架
# from api_auto_test.utils.gnc_common.check_settings import CheckSettings  # 导入来平的环境判断方法

import warnings
# from api_auto_test.utils.gnc_common.gnc_login import GncLogin  # 导入来平的登陆方法获取session
import json
from utils.config import *
from utils.Common import Login


class Record(unittest.TestCase):  # 声明一个类，这个类继承类unittest.TestCase属性

    def setUp(self):  # unit test框架自带的初始化方法，在执行方法前都会先执行初始化方法
        warnings.simplefilter('ignore', ResourceWarning)
        self.proxies = get_proxies()
        # 第一步读取gnc_common.yaml中的内容，里面存放了各环境下的域名
        # 将登陆方法赋予给self.user_info
        self.session = Login().routines_app_login('userwukefan92201@163.com')
        self.gnc_base_url = get_base_url('routines')

        # 下面是获取接口用例的步骤，第一步读取用例文件
        self.data_info = get_case_info('/data/wukefan/test_demo.yaml')

        self.clock_record_payload = self.data_info["clock_record"].get("payload")
        self.clock_record_url = self.data_info["clock_record"].get("url")
        self.clock_record_headers = self.data_info["clock_record"].get("headers")
        self.clock_record_expect = self.data_info["clock_record"].get("expect_value")
        print(type(self.clock_record_expect))

    def tearDown(self):
        """此方法在所有方法执行后执行，做一些关闭操作"""
        pass

    def test_clock_record(self):
        payload = self.clock_record_payload
        # 注意post请求一定要注意headers中的content-type，如果是application/json，那么下面就写json=payload，如果不是，则改为data=payload
        response = self.session.post(url=self.gnc_base_url + self.clock_record_url, json=payload, headers=self.clock_record_headers,
                                     proxies=self.proxies, verify=False)
        try:
            self.assertEqual(response.status_code, 200)
            res_data = json.loads(response.content)
            print(res_data)
            code = res_data['code']
            self.assertEqual(code, 0)
            self.assertEqual(res_data['data']['taskCode'], self.clock_record_expect['data']['taskCode'])
        except Exception as e:
            print("错误信息：", e)
            print('url: ', response.url)
            print('参数信息: ', payload)
            raise e


if __name__ == "__main__":
    unittest.main()
