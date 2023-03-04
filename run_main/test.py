# """
# app cases 汇总
# """
# import sys, stat  # sys模块用于判断是否传入了外部参数，从而引导环境区分走默认配置还是定制
# import nb_log  # 导入日志模块
# # sys.path.append('..')
# import unittest  # unittest中的suite方法来加载测试用例
# from utils import HTMLTestRunner  # 将结果生成html报告
# from utils.dingding import *
# from test_cases.sanleixie import demo  # 从业务层中导入编写case的模块
# from utils import globalvar as gl  # 导入环境区分编写逻辑
# from bs4 import BeautifulSoup
# from utils.config import get_path
#
# # 工具类中获取report中html文件的方法
# def get_report(report_path):
#     get_report_file(report_path)
#
#
# # 构造测试集
#
# suite = unittest.TestSuite()  # 声明一个测试套件用来添加用例
#
# """制卡激活流程"""
# suite.addTest(demo.Creat("test_run"))
#
# if __name__ == "__main__":
#     # 执行测试
#     print(sys.argv)  # 通过sys.argv可以进行外部的参数传递
#     gl._init()
#     env = gl.get_value('env')  # 读取初始环境
#     env_list = ['pre', 'beta', 'online']
#     if len(sys.argv) > 1:  # 如果list长度大于1说明有外部参数传入
#         v_env = sys.argv[1]  # 根据下标获取外部传入的参数
#         if v_env in env_list:  # 进行判断是否存在环境list中
#             env = v_env
#     gl.set_value('env', env)  # 修改环境区分中的执行环境字段
#     runner = unittest.TextTestRunner()  # 将unittest中的执行方法赋予新的对象runner
#     nowTime = time.strftime("%Y-%m-%d-%H.%M.%S")  # 获取当前时间作为报告的名称
#     filename = get_path() + "/report/" + nowTime + ".html"  # 文件路劲
#     fr = open(filename, "wb")  # 在访问非二进制文件的时候，访问模式通常加上‘b’
#     report = HTMLTestRunner.HTMLTestRunner(title="权益中心创建合同",
#                                            description="测试用例参考",
#                                            stream=fr,
#                                            # retry=1  # 失败重跑
#                                            )
#
#     report.run(suite)  # 发送报  告模式
#     # runner.run(suite)  # 调试模式，不生成报告内容
#     fr.close()  # 关闭文件
#     # report_path = os.path.join(cur_path, "report")  # 测试报告路径
#     # response = requests.request("GET", url)
#     # html = (response.content.decode("utf-8"))
#     # soup = BeautifulSoup(html, 'html.parser')
#     # for tag in soup.find_all('p', id='show_detail_line'):
#     #     # print(tag)
#     #     fail = tag.find('a', class_='btn btn-danger').get_text()
#     #     success = tag.find('a', class_='btn btn-success').get_text()
#     #     all_case = tag.find('a', class_='btn btn-info').get_text()
#     #     print(fail, success, all_case)
# print('1111111')

# import sys
#
# print(sys.argv)
import unittest


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_01(self):
            a = 1
            b = 2
            self.assertEqual(a, b)


    def test_02(self):
            a = 1
            b = 2
            self.assertEqual(a, b)


    def test_03(self):
            a = 1
            b = 1
            self.assertEqual(a, b)



def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    print('All case number')
    print(test_result.testsRun)
    print('Failed case number')
    print(len(test_result.failures))
    print('Failed case and reason')
    print(test_result.failures)
    for case, reason in test_result.failures:
        print(case.id())
        print(reason)


if __name__ == '__main__':
    main()
