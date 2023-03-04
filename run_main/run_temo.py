# import sys, stat  # sys模块用于判断是否传入了外部参数，从而引导环境区分走默认配置还是定制
import unittest  # unittest中的suite方法来加载测试用例
from utils import HTMLTestRunner
from utils.dingding import *
from test_cases.wukefan import demo  # 从业务层中导入编写case的模块
from bs4 import BeautifulSoup
from utils.config import get_path
from utils.log import logger


# 工具类中获取report中html文件的方法
def get_report(report_path):
    get_report_file(report_path)


# 构造测试集

suite = unittest.TestSuite()  # 声明一个测试套件用来添加用例

suite.addTest(demo.Record("test_clock_record"))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()  # 将unittest中的执行方法赋予新的对象runner
    runner.run(suite)  # 调试模式，不生成报告内容
    nowTime = time.strftime("%Y-%m-%d-%H.%M.%S")  # 获取当前时间作为报告的名称
    # filename = get_path() + "/report/" + nowTime + ".html"  # 文件路劲
    # with open(filename, "wb") as fr:
    #     report = HTMLTestRunner.HTMLTestRunner(title="系统回归case",
    #                                            description="测试用例参考",
    #                                            stream=fr
    #                                            )

        # report.run(suite)  # 发送报  告模式
    # time.sleep(2)
    # report_path = os.path.join(cur_path, "report/preview_ihospital_preview/")  # 测试报告路径
    # print(report_path)
    # file_name = get_report_file(report_path)
    # print(file_name)
    # new_report_file = report_path + "/" + file_name
    # url = "http://test-report-florence.intra.yiducloud.cn/report/preview_ihospital_preview/{}".format(file_name)
    # print(url)
    #
    # # response = requests.get(url)
    # # html = (response.content.decode("utf-8"))
    # # soup = BeautifulSoup(html, 'html.parser')
    # # for tag in soup.find_all('p', id='show_detail_line'):
    # #     fail = tag.find('a', class_='btn btn-danger').get_text()
    # #     success = tag.find('a', class_='btn btn-success').get_text()
    # #     all_case = tag.find('a', class_='btn btn-info').get_text()
    # #     print(fail, success, all_case)
    #
    # case_title = '系统回归case'
    # res = wechart_send_news(url, case_title)
    # logger.info("消息发送：%r", res)  # 打印请求结果
