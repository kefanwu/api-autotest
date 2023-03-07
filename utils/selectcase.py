import os
import yaml
from utils.conect_sql import MysqlConnect



def get_path():
    BASE_PATH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    return BASE_PATH_DIR

def get_case_info(file_path):
    with open(get_path() + file_path, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


#选择测试数据时，未来需要知道，到底执行的是哪个app工程，此为demo，暂时不考虑，后续开发需要考虑进去
def selectcasedata(app_name, service_name, method_name, case_description):
    file_path = '/caseinfo/'+service_name+'/testdata/'+'TestData_'+method_name+'.yaml'
    TestData = get_case_info(file_path)
    for n in range(1, len(TestData)+1):
        mm = 'case' + str(n)
        if case_description == TestData.get(mm).get('summary'):
            return TestData.get(mm)
        else:
            print('循环查询该case的数据文件中是否有命中的case')


def findmethodname(app_name, service_name, method_name, case_description):
    file_path = '/caseinfo/'+service_name+'/testdata/'+'TestData_'+method_name+'.yaml'
    TestData = get_case_info(file_path)
    for n in range(1, len(TestData)+1):
        mm = 'case' + str(n)
        if case_description == TestData.get(mm).get('summary'):
            return TestData.get(mm).get('methodname')
        else:
            print('循环查询该case的数据文件中是否有命中的case')

def debugfindmethodname():
    file_path = '/caseinfo/GetDevices/testdata/TestData_get_userId.yaml'
    TestData = get_case_info(file_path)
    for n in range(1, len(TestData)+1):
        mm = 'case' + str(n)
        if '通过user_id查找设备case1' == TestData.get(mm).get('summary'):
            return TestData.get(mm).get('methodname')
        else:
            print('循环查询该case的数据文件中是否有命中的case')

def debugselectcasedata():
    file_path = '/caseinfo/GetDevices/testdata/TestData_get_userId.yaml'
    TestData = get_case_info(file_path)
    for n in range(1, len(TestData)+1):
        mm = 'case' + str(n)
        if '通过user_id查找设备case2' == TestData.get(mm).get('summary'):
            return TestData.get(mm)
        else:
            print('循环查询该case的数据文件中是否有命中的case')


def selectcaseinfo(caseid):
    sqliteserver = MysqlConnect('', 'root', '123456', 3306, 'autotestcase')
    selectsql = 'select a.id, a.case_description, b.app_name,b.service_name,b.method_name from autotestcase_autotestcases a,autotestcase_applictionname b where  b.Id = a.applictionnameid_id and  a.id = ' + caseid + ';'
    sqliteserver.select_one(selectsql)
