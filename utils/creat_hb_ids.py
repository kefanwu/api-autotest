import requests
import json
from utils.conect_sql import MysqlConnect
"""查询用户中心姓名"""


#
# with open('test1.txt', "w") as f:
#     for i in range(0, 1000):
#         telephone1 = random.choice(['139', '188', '185', '136', '158', '151', '187', '139']) + "".join(random.choice("0123456789") for item in range(8))
#         now_time = (int(round(time.time()*1000)))
#         hb_code = telephone1+str(now_time)
#         telephone2 = random.choice(['010', '020', '021', '024', '0577', '029', '027', '028']) + "".join(random.choice("abcdefghijk") for item in range(8))
#         now_time = (int(round(time.time()*1000)))
#         sender = telephone2+str(now_time)
#         print(sender+",", hb_code)
#         # f = open('test1.txt', 'w')
#         f.write('{:},{:}\n'.format(str(sender), str(hb_code)))
#     f.close()
#
# with open('/Users/kefan/project/py3_unittest/tester/test_03/test.txt', 'r+') as f:
#     content = f.read()
#     print(content)

def class_8():

    # f2 = open('test.txt',"r")
    # lines = f2.readlines()
    # for line in lines:
    #     stu_id = line.strip('\n')
    select = MysqlConnect("192.144.166.161", "edu_auth_rw", "V7rh2yEbPrPU", 5606, "edu")

    sql_select = "SELECT  DISTINCT student_id,city_code FROM tb_pre_enroll_course WHERE deleted = 0 AND STATUS = 3 AND category_id not in ('20191227164113155096000001466500') AND `year` = 2021 AND term IN (4, 1)"  # 查询sql，主要是查询客户姓名和电话
    data_info = select.select_all_data(sql_select)  # 执行查询语句
    print(data_info)
    res_list = []
    for item in data_info:
        student_id = item[0]
        res_list.append(student_id)
    print(res_list)
    print(len(res_list))

    for stu_id in res_list:
        url = "http://pre-usercenter.izhikang.com/usercenter/v2/user/getUserByUserId?"

        payload = {
            "userId": stu_id
        }
        headers = {
            'time': '1583133767664',
            'sign': '94846BA1F481DF40AC4DD1F7C6207931',
            'operatorId': '123',
            'operatorName': '63369726346456d65bbe7aaf5eda7c6f',
            'Content-Type': 'application/json',
            'code': '10002'
        }

        response = requests.get(url=url, params=payload, headers=headers)
        response_data = json.loads(response.content)
        result = json.dumps(response_data, ensure_ascii=False, indent=4)
        stu_name = response_data["data"]["realName"]
        print(stu_name)
        with open('test.txt', "a") as f:
            f.write(stu_name + "\n")
#
#
# def one_to_one():
#     select = MysqlConnect("192.144.166.161", "edu_auth_rw", "V7rh2yEbPrPU", 4706, "zkteacher")
#
#     sql_select = "select student_id from tb_pressure_test"  # 查询sql，主要是查询客户姓名和电话
#     data_info = select.select_many_data(sql_select)  # 执行查询语句
#     res_list = []
#     for item in data_info:
#         student_id = item[0]
#         res_list.append(student_id)
#     print(res_list)
#     print(len(res_list))
#
#     for stu_id in res_list:
#         url = "http://pre-usercenter.izhikang.com/usercenter/v2/user/getUserByUserId?"
#
#         payload = {
#             "userId": stu_id
#         }
#         headers = {
#             'time': '1583133767664',
#             'sign': '94846BA1F481DF40AC4DD1F7C6207931',
#             'operatorId': '123',
#             'operatorName': '63369726346456d65bbe7aaf5eda7c6f',
#             'Content-Type': 'application/json',
#             'code': '10002'
#         }
#
#         response = requests.get(url=url, params=payload, headers=headers)
#         response_data = json.loads(response.content)
#         result = json.dumps(response_data, ensure_ascii=False, indent=4)
#         print(result)
#         stu_name = response_data["data"]["realName"]
#         print(stu_id+","+stu_name)
#         # update_sql = 'UPDATE tb_pressure_test SET student_name = "{}" WHERE student_id = "{}"'.format(stu_name,stu_id)
#         # res = select.execute_update_insert(update_sql)
#         # print(res)
#     # f2.close()
#
class_8()


