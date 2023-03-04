import json
import time
import yaml
from utils.config import get_path
from utils.gnc_common.check_common import check_common
from utils.gnc_common.gnc_request import gnc_request


class gnc_questionnaire():

    def __init__(self, setting, host, header):
        self.setting = setting
        self.host = host
        self.header = header
        """获取注册登录配置"""
        self.file = open(get_path() + "/utils/gnc_common/gnc_common_data/gnc_questionnaire_common.yaml", "r", encoding="utf-8")
        self.data = yaml.load(self.file, Loader=yaml.FullLoader)
        self.request = gnc_request()
        self.CheckCommon = check_common()

    """获取量表id
        user_session：session
        type：问卷类型：screen--初筛 archive--基础 doHealth--运动饮食问卷
    """
    def GetCrfId(self, user_session, type):
        url = self.data["ques_list_url"]["get_crfid_url"]
        Respone = {}
        params = {}
        params["type"] = type
        try:
            response = self.request.GncRequests("get", self.host + url, user_session, params)
            res = json.loads(response.content)
            assert res["code"] == 0
            print("获取到{0}环境crfid：{1}".format(self.setting, res["data"]))
            print(response.text)
            Respone["res"] = res
            return Respone
        except Exception as e:
            print("{0}环境获取crfid失败：{1}".format(self.setting, e))
            return e

    """获取量表内容
        user_session：session
        crfId：问卷id
        visitSn：用户visitSn，初筛量表时未生成，传空
    """

    def GetCrfContent(self, user_session, crfId, visitSn=""):
        url = self.data["ques_list_url"]["get_crf_content"]
        Respone = {}
        params = {}
        params["crfId"] = crfId
        params["visitSn"] = visitSn
        try:
            response = self.request.GncRequests("get", self.host + url, user_session, params)
            res = json.loads(response.content)
            print(res)
            assert res["code"] == 0
            print("获取到{0}环境crf题目内容：{1}".format(self.setting, res["data"]))
            Respone["res"] = res
            return Respone
        except Exception as e:
            print("{0}环境获取crf题目内容失败：{1}".format(self.setting, e))
            return e

    """量表入参组装（由于不同环境的questionId不同，通过获取不同环境的题目questionId替换传参中的questionId）
        crf：问卷题目列表
        param： 问卷传参
    """
    def check_param(self, crf, param, type="", Medication=""):
        params = check_common().check_crf_param(crf, self.data[param], type, Medication)
        print("补全{0}环境questionId：{1}".format(self.setting, params))
        return params

    """提交量表
        user_session:session
        crfId: 问卷id
        patientSn：用户patientSn
        crfAnswerId：提交问卷id,第一次提交时不传
        visitSn：visitSn，用户未完成初筛问卷未生成v时不传
        status：问卷提交方式：save 保存不提交计算，submit 保存并提交计算
        answers: 问卷已选择项列表
        crfAnswerId: 保存问卷id，首次提交问卷时为空
    """
    def SaveQues(self, user_session, crfId, patientSn, status, answers, crfAnswerId="", visitSn=""):
        # 参数组装
        url = self.data["ques_list_url"]["save_ques_url"]
        Respone = {}
        params = {}
        if crfAnswerId:
            params["crfAnswerId"] = crfAnswerId
        params["crfId"] = crfId
        if visitSn:
            params["visitSn"] = visitSn
        params["status"] = status
        params["answers"] = answers
        params["patientSn"] = patientSn
        print("问卷信息提交入参：{0}---提交类型{1}".format(params, status))
        response = self.request.GncRequests("post", self.host + url, user_session, params)
        res = json.loads(response.content)
        print("问卷提交结果{0}".format(res))
        Respone["res"] = res
        return res

    """获取用户基础数据"""
    def GetUserInfo(self, user_session):
        url = self.data["user_status_url"]
        Respone = {}
        params = {}
        print("开始获取用户visitSn，patientSn等基本信息")
        response = self.request.GncRequests("get", self.host + url, user_session, params)
        print(response.status_code)
        print(response.content)
        print(response.url)
        res = json.loads(response.content)
        print("用户基本信息获取完成：{0}".format(res))
        assert res["code"] == 0
        Respone.update(res["data"])
        return Respone

    """查看用户问卷结果
        user_session: user_session
        visitSn: visitSn
        type:查询方案类型：target--基础量表 prescription--运动饮食量表
    """
    def ViewResult(self, user_session, visitSn, type):
        url = self.data["view_result_url"]
        params = {}
        params["type"] = type
        params["visitSn"] = visitSn
        response = self.request.GncRequests("post", self.host + url, user_session, params)
        res = json.loads(response.content)
        print("查看用户{0}方案.结果：{1}".format(type, res))
        return res

    """进行问卷填写
        user_session: user_session
        type:问卷类型：screen-初筛
        quizdata:问卷参数 QuickQuiz_data--初筛  HealthSurvey_data--基础
        status: 提交类型 save 保存 submit 保存并计算
        result_type: 查看问卷结果参数,不传 不查看结果
    """
    def SaveQuiz(self, user_session, quizdatas, result_type="", Bloodtype="", Medication=""):
        type = quizdatas["type"]
        quizdata = quizdatas["quizdata"]
        status = quizdatas["status"]
        quizname = quizdatas["name"]
        # 访问环境url和header地址
        Respone = {}
        # 获取用户基础信息
        user_data = self.GetUserInfo(user_session)
        visitSn = user_data["visitSn"]
        patientSn = user_data["patientSn"]
        # 获取问卷id
        crfres = self.GetCrfId(user_session, type)
        crfid = crfres["res"]["data"]
        # 获取问卷题目
        crf = self.GetCrfContent(user_session, crfid)
        # 问卷参数处理
        param = self.check_param(crf["res"], quizdata, Bloodtype, Medication)
        # 提交问卷
        print("开始{0}问卷填写".format(quizname))
        crfrespone = self.SaveQues(user_session, crfid, patientSn, status, param, "", visitSn)
        try:
            assert crfrespone["code"] == 0
            print("{0}环境提交{1}问卷成功，返回值：{2}".format(self.setting, quizname, crfrespone))
        except Exception as e:
            print("{0}环境提交{1}问卷失败：{1}".format(self.setting, quizname, repr(e)))
            return e
        # 查看问卷结果
        if result_type:
            time.sleep(5)
            result_type = self.data["quiz_result"][type]
            re = self.ViewResult(user_session, visitSn, result_type)
        # 查询用户基础信息
        res = self.GetUserInfo(user_session)
        Respone.update(res)
        return Respone

    """根据用户状态查看对应问卷结果
    
    """
    def ViewQuizResult(self):
        pass


if __name__ == "__main__":
    pass
    # B = gnc_questionnaire("aws_test").SaveQuiz("aws_test", "1360387508@aws.com", "aa666666")

    # print(B)