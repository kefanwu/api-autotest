import unittest  # 单元测试框架
import warnings

#单用例调试时，可以这么干，确保每次只执行一条用例
from utils.conect_sql import MysqlConnect


class Unittest(unittest.TestCase):
    warnings.simplefilter('ignore', ResourceWarning)
    def tearDown(self):
        print('=======++>this is demo', self.result)
        result = self.result.get('success')
        caseid = self.caseid
        sqliteserver = MysqlConnect('172.31.6.23', 'root', '123456', 3306, 'autotestcase')
        print('==========>当前执行的case状态是：', result)
        if result == True:
            #更新数据库状态成功
            updatesql = 'UPDATE autotestcase_autotestcases SET case_status = 1 where id = '+caseid+';'
            sqliteserver.execute_update_insert(updatesql)
            print()
        else:
            #更新数据库状态为失败，并且将错误原因写入到数据库表case_excute_record的reslut_response字段中
            # 更新数据库状态成功
            updatesql = 'UPDATE autotestcase_autotestcases SET case_status = 2 where id = '+caseid+';'
            sqliteserver.execute_update_insert(updatesql)



