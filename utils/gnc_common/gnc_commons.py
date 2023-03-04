from utils.gnc_common.common_list.gnc_Insulin import gnc_Insulin
from utils.gnc_common.common_list.gnc_diet import gnc_diet
from utils.gnc_common.gnc_public_service import gnc_public_service
from utils.gnc_common.common_list.gnc_recode import gnc_record


class gnc_commons():

    """注册并输出用户基础信息"""
    def Register(self, setting, email="", password=""):
        return gnc_public_service(setting).Register(email, password)

    """登录并输出用户基础信息"""
    def login(self, setting, email, password):
        return gnc_public_service(setting).login(email, password)

    """
    登录账号进行初筛问卷
    email：用户邮箱
    password：用户密码
    """
    def LoginQuickQuiz(self, setting, email, password):
        return gnc_public_service(setting).LoginQuickQuiz(email, password)

    """
        登录账号进行基础问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def LoginHealthSurvey(self, setting, email, password, check_result="", Bloodtype=""):
        return gnc_public_service(setting).LoginHealthSurvey(email, password, check_result, Bloodtype)
    """
        登录账号进行运动饮食问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def LoginProgramSurvey(self, setting, email, password, check_result=""):
        return gnc_public_service(setting).LoginProgramSurvey(email, password, check_result)

    """
        登录账号进行初筛+基础问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def LoginQuickHealthSurvey(self, setting, email, password, check_result="", Bloodtype=""):
        return gnc_public_service(setting).LoginQuickHealthSurvey(email, password, check_result, Bloodtype)

    """
        登录账号进行初筛+基础+运动问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def LoginQuickHealthProgramSurvey(self, setting, email, password, check_result="", Bloodtype=""):
        return gnc_public_service(setting).LoginQuickHealthProgramSurvey(email, password, check_result, Bloodtype)
    """
        注册用户进行初筛问卷
        email：用户邮箱
        password：用户密码
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def RegisterQuickQuiz(self, setting, email="", password=""):
        return gnc_public_service(setting).RegisterQuickQuiz(email, password)
    """
        注册账号进行初筛+基础问卷
        email：用户邮箱，不填则自动创建
        password：用户密码 不填默认aa666666
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def RegisterQuickHealthSurvey(self, setting, email="", password="", check_result="", Bloodtype=""):
        return gnc_public_service(setting).RegisterQuickHealthSurvey(email, password, check_result, Bloodtype)
    """
        注册账号进行初筛+基础+运动问卷
        email：用户邮箱，不填则自动创建
        password：用户密码 不填默认aa666666
        check_result: 是否需要查看问卷结果，填任意值为需要查看
    """
    def RegisterQuickHealthProgramSurvey(self, setting, email="", password="", check_result="", Bloodtype=""):
        return gnc_public_service(setting).RegisterQuickHealthProgramSurvey(email, password, check_result, Bloodtype)

    """
            注册并生成一个未选择服用胰岛素的账号
            注册账号进行初筛+基础+运动问卷
            email：用户邮箱，不填则自动创建
            password：用户密码 不填默认aa666666
            check_result: 是否需要查看问卷结果，填任意值为需要查看
        """

    def RegisterQuickHealthProgramSurveyNo(self, setting, email="", password="", check_result="", Bloodtype=""):
        return gnc_public_service(setting).RegisterQuickHealthProgramSurvey(email, password, check_result, Bloodtype, Medication="NO")

class Medical_Common():

    """用户单指标打卡
    medical：可打卡指标 FastingMedical->'空腹血糖',AfterBreakfast->'早餐后血糖',BeforeLunch->'午餐前血糖',AfterLunch->'午餐后血糖',BeforeDinner->'晚餐前血糖'
        AfterDinner->'晚餐后血糖',BeforeSleep->'睡前血糖',3AM->'3AM血糖',Weight->'体重',Waistline->'腰围',BloodPressure->'血压',HAIC->'HAIC'
        TG->'TG',TC->'TC',LDL_C->'LDL_C',HDL_C->'HDL_C',Sleep->'睡眠'
    measureValue： 打卡指标值 睡眠打卡填写小时数
    measureTimes: 可不填，不填时默认使用当前时间 填写规则：2022-02-22 10:12:12
    recordType: 默认可不填， 1-人工记录(默认) 2-设备记录，填其他数会强制转换成1"""
    def AddMedical(self, setting, user_session, medical, measureValue, measureTimes="", recordType=1):
        return gnc_record(setting).MedicalAddRecord(user_session, medical, measureValue, measureTimes, recordType)

    """用户多指标打卡
    medical_list：指标打卡列表，json格式，key为打卡指标，value为打卡值 例如：{'FastingMedical':122,'AfterBreakfast':150}"""
    def AddMedicalList(self, setting, user_session, medical_list, measureTimes="", recordType=1):
        return gnc_record(setting).MedicalAddRecordList(user_session, medical_list, measureTimes, recordType)
    """指标多天打卡
        Medical:需要打卡的指标值
        startData：打卡开始时间 "2022-06-15 08:00:05"
        endData： 打卡结束时间 "2022-06-15 08:00:05"
        measureValue：初始打卡值
        difference：每天打卡差值 填1则每天打卡值+1，填-1每天打卡值-1 默认为0
        recordType： 打卡类型：1 手动打卡 2 血糖仪打卡 默认为1
    """
    def AddMedicalDateList(self, setting, user_session, Medical, startData, endData, measureValue=None, difference=0, recordType=1):
        return gnc_record(setting).MedicalAddRecordDateList(user_session, Medical, startData, endData, measureValue, difference, recordType)
    """删除指定的指标打卡
        indicationType: 1-血糖 2-体重 3-腰围 4-血压 5-糖化血红蛋白 6-甘油三酯 7-总密度胆固醇 8-低密度胆固醇 9-高密度胆固醇 10-睡眠
    """
    def MedicalDeletelist(self, setting, user_session, indicationType):
        return  gnc_record(setting).MedicalDeletelist(user_session,indicationType)

class Diet_Common():
    """用户饮食打卡
        dateTime:打卡日期 2022-06-22
        visitSn： 用户visitSn
        meal： 打卡餐段 BREAKFAST 早餐 "DINNER" 晚餐 "LUNCH" 午餐 "SNACKS" 加餐
        scene: 用餐场景 可不填 默认self  EAT_OUT,FAMILY,SELF,SOCIAL,TAKEOUT
    """
    def AddDiet(self, setting, user_session, dateTime, visitSn, meal, scene=""):
        return  gnc_diet(setting).AddDiet(user_session, dateTime, visitSn, meal, scene)



class HCP_Common():
    """hcp登录"""
    def loginHcp(self, setting, email, password):
        return gnc_public_service(setting).loginHcp(email, password)

    """hcp 创建basal胰岛素用户
        hcp_email：hcp账号
        hcp_password：hcp密码
        user_email： 用户邮箱
        user_password： 用户密码
        Bloodtype: 服务类型 Remission 缓解组 BG BG组
    """
    def add_basal_insulin(self, setting, hcp_email, hcp_password, user_email, user_password="", Bloodtype=""):
        hcp_resp = gnc_public_service(setting).loginHcp(hcp_email, hcp_password)
        basal_resp = gnc_Insulin(setting).add_basal_insulin(hcp_resp["session"], user_email)
        return gnc_public_service(setting).RegisterQuickHealthProgramSurvey(user_email, user_password, "1", Bloodtype)

    """创建bolus胰岛素用户"""
    def add_bolus_insulin(self, setting, hcp_email, hcp_password, user_email, user_password="", Bloodtype=""):
        hcp_resp = gnc_public_service(setting).loginHcp(hcp_email, hcp_password)
        basal_resp = gnc_Insulin(setting).add_basal_insulin(hcp_resp["session"], user_email)
        user_resp = gnc_public_service(setting).RegisterQuickHealthProgramSurvey(user_email, user_password, "1", Bloodtype)
        bolus_resp = gnc_Insulin(setting).saveBolusInsulin(hcp_resp["session"], user_resp["userId"])
        return user_resp

if __name__ == "__main__":
    setting = "pre"
    # hcpemail = "testqipre1006@qq.com"
    # hcppaw = "Aa123456"
    hcpemail ="LaiPing00001@163.com"
    hcppaw = "Aa123456"
    medical_list = {"FastingMedical":122,"AfterBreakfast":150, "BeforeLunch":"", "AfterLunch":"", "BeforeDinner":"",
                    "AfterDinner": "", "BeforeSleep":"", "3AM":"", "Weight":"", "Waistline":"", "BloodPressure":"",
                    "HAIC": "", "TG":"", "TC":"", "LDL_C":"", "HDL_C":"", "Sleep":"",
                    }
    # # hcp登录
    # hcpinfo = HCP_Common().loginHcp(setting, hcpemail, hcppaw)
    # hcpinfo = HCP_Common().add_bolus_insulin(setting, hcpemail, hcppaw, "testqiaws7020@qq.com", Bloodtype="Remission")
    # userinfo = gnc_commons().RegisterQuickHealthProgramSurveyNo(setting, "testqipre9042@qq.com", "aa666666", "2", "Remission")
    # 用户登录
    userinfo = gnc_commons().login(setting, "testqipre9030@qq.com", "aa666666")
    # 批量指标打卡

    aa = Diet_Common().AddDiet(setting, userinfo["session"], "2022-06-28 18:00:05", userinfo["visitSn"], "DINNER")
    # aa1 = Medical_Common().AddMedicalDateList(setting, userinfo["session"], "AfterLunch", "2022-06-01 12:00:05", "2022-06-28 12:00:05", 150, 0)
    # aa2 = Medical_Common().AddMedicalDateList(setting, userinfo["session"], "Sleep", "2022-06-01 22:00:05", "2022-06-28 22:00:05", 140, 0)

    # 批量删除指标打卡
    # aa = Medical_Common().MedicalDeletelist(setting, userinfo["session"], 1)
    # 饮食打卡
    # aa = Diet_Common().AddDiet(setting, userinfo["session"], "2022-06-24", userinfo["visitSn"], "DINNER")
    print(aa)
    # print(aa1)