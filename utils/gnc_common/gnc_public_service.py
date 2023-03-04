import yaml

from utils.config import get_path
from utils.gnc_common.common_list.gnc_LoginOrRegister import gnc_LoginOrRegister
from utils.gnc_common.gnc_initialize import gnc_initialize
from utils.gnc_common.common_list.gnc_questionnaire import gnc_questionnaire


class gnc_public_service(gnc_initialize):

    def __init__(self, setting):
        """获取问卷配置"""
        super().__init__(setting)
        self.file = open(get_path() + "/utils/gnc_common/gnc_common_data/gnc_questionnaire_common.yaml", "r", encoding="utf-8")
        self.data = yaml.load(self.file, Loader=yaml.FullLoader)
        # 初筛问卷配置
        self.QuickQuizData = self.data["QuickQuizData"]
        # 基础问卷配置
        self.HealthSurveyData = self.data["HealthSurveyData"]
        # 运动饮食问卷配置
        self.ProgramSurveyData = self.data["ProgramSurveyData"]
        self.Gnc_loginOrReg = gnc_LoginOrRegister(setting=self.CommonSetting, host=self.CommonHost, header=self.CommonHeaders)
        self.GncQues = gnc_questionnaire(setting=self.CommonSetting, host=self.CommonHost, header=self.CommonHeaders)


    """注册并输出用户基础信息"""
    def Register(self, email="", password=""):
        # 注册
        Registerres = self.Gnc_loginOrReg.RegisterUser(email, password)
        user_session = Registerres["session"]
        # 查询用户基础信息
        res = self.GncQues.GetUserInfo(user_session)
        res["session"] = user_session
        res.update(self.respones)
        return res

    """登录并输出用户基础信息"""
    def login(self, email, password):
        # 登录
        user_session = self.Gnc_loginOrReg.loginUser(email, password)
        # 查询用户基础信息
        res = self.GncQues.GetUserInfo(user_session["session"])
        res["session"] = user_session["session"]
        res.update(self.respones)
        return res

    """hcp登录并输出用户基础信息"""
    def loginHcp(self, email, password):
        # 登录
        resp = self.Gnc_loginOrReg.loginHcp(email, password)
        # 查询用户基础信息
        # res = self.GncQues.GetUserInfo(resp["session"])
        # res["session"] = resp["session"]
        resp.update(self.respones)
        return resp

    """
        登录账号进行初筛问卷
        email：用户邮箱
        password：用户密码
    """
    def LoginQuickQuiz(self, email, password):
        # 登录
        user_session = self.Gnc_loginOrReg.loginUser(email, password)
        # 开始问卷
        QuickRespone = self.GncQues.SaveQuiz(user_session["session"], self.QuickQuizData)
        print(QuickRespone)
        QuickRespone["session"] = user_session["session"]
        QuickRespone.update(self.respones)
        return QuickRespone

    """
        登录账号进行基础问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def LoginHealthSurvey(self, email, password, check_result="", Bloodtype=""):
        # 登录
        user_session = self.Gnc_loginOrReg.loginUser(email, password)
        # 开始问卷
        result_type = check_result
        respone = self.GncQues.SaveQuiz(user_session["session"], self.HealthSurveyData, result_type, Bloodtype)
        respone["session"] = user_session["session"]
        respone.update(self.respones)
        return respone

    """
        登录账号进行运动饮食问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def LoginProgramSurvey(self, email, password, check_result=""):
        # 登录
        user_session = self.Gnc_loginOrReg.loginUser(email, password)
        # 开始运动饮食问卷
        result_type = check_result
        respone = self.GncQues.SaveQuiz(user_session["session"], self.ProgramSurveyData, result_type)
        respone["session"] = user_session["session"]
        respone.update(self.respones)
        return respone

    """
        登录账号进行初筛+基础问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def LoginQuickHealthSurvey(self, email, password, check_result="", Bloodtype=""):
        # 登录
        user_session = self.Gnc_loginOrReg.loginUser(email, password)
        # 开始问卷
        # 初筛问卷参数
        QuickRespone = self.GncQues.SaveQuiz(user_session["session"], self.QuickQuizData)
        # 基础问卷参数
        result_type = check_result
        HealthRespone = self.GncQues.SaveQuiz(user_session, self.HealthSurveyData, result_type, Bloodtype)
        HealthRespone["session"] = user_session["session"]
        HealthRespone.update(self.respones)
        return HealthRespone

    """
        登录账号进行初筛+基础+运动问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def LoginQuickHealthProgramSurvey(self, email, password, check_result="", Bloodtype=""):
        # 登录
        user_session = self.Gnc_loginOrReg.loginUser(email, password)
        # 开始问卷
        # 初筛问卷
        QuickRespone = self.GncQues.SaveQuiz(user_session["session"], self.QuickQuizData)
        # 基础问卷
        result_type = 1
        HealthRespone = self.GncQues.SaveQuiz(user_session["session"], self.HealthSurveyData, result_type, Bloodtype)
        # 运动饮食问卷
        result_type = check_result
        ProgramRespone = self.GncQues.SaveQuiz(user_session["session"], self.ProgramSurveyData, result_type)
        ProgramRespone["session"] = user_session["session"]
        ProgramRespone.update(self.respones)
        return ProgramRespone

    """
        注册用户进行初筛问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def RegisterQuickQuiz(self, email="", password=""):
        # 注册
        Registerres = self.Gnc_loginOrReg.RegisterUser(email, password)
        user_session = Registerres["session"]
        # 开始问卷
        QuickRespone = self.GncQues.SaveQuiz(user_session, self.QuickQuizData)
        QuickRespone["session"] = user_session
        QuickRespone.update(self.respones)
        return QuickRespone

    """
        注册账号进行初筛+基础问卷
        email：用户邮箱，不填则自动创建
        password：用户密码 不填默认aa666666
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def RegisterQuickHealthSurvey(self, email="", password="", check_result="", Bloodtype=""):
        # 注册
        Registerres = self.Gnc_loginOrReg.RegisterUser(email, password)
        user_session = Registerres["session"]
        # 开始问卷
        # 初筛问卷参数
        QuickRespone = self.GncQues.SaveQuiz(user_session, self.QuickQuizData)
        # 基础问卷参数
        result_type = check_result
        HealthRespone = self.GncQues.SaveQuiz(user_session, self.HealthSurveyData, result_type, Bloodtype)
        HealthRespone["session"] = user_session
        HealthRespone.update(self.respones)
        return HealthRespone

    """
        注册账号进行初筛+基础+运动问卷
        email：用户邮箱，不填则自动创建
        password：用户密码 不填默认aa666666
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def RegisterQuickHealthProgramSurvey(self, email="", password="", check_result="", Bloodtype="", Medication=""):
        # 注册
        Registerres = self.Gnc_loginOrReg.RegisterUser(email, password)
        user_session = Registerres["session"]
        # 开始问卷
        # 初筛问卷
        QuickRespone = self.GncQues.SaveQuiz(user_session, self.QuickQuizData)
        # 基础问卷
        result_type = 1
        HealthRespone = self.GncQues.SaveQuiz(user_session, self.HealthSurveyData, result_type, Bloodtype, Medication)
        # 运动饮食问卷
        result_type = check_result
        ProgramRespone = self.GncQues.SaveQuiz(user_session, self.ProgramSurveyData, result_type)
        ProgramRespone["session"] = user_session
        ProgramRespone.update(self.respones)
        return ProgramRespone





if __name__ == "__main__":

    pass