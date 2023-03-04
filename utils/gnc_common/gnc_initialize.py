import yaml
from utils.config import get_path
from utils.gnc_common.check_common import check_common
from utils.gnc_common.gnc_request import gnc_request

class gnc_initialize():
    def __init__(self, settings="pre"):
        """获取公共配置"""
        self.CommonFile = open(get_path() + "/utils/gnc_common/gnc_common_data/gnc_common.yaml", "r",
                               encoding="utf-8")
        self.CommonData = yaml.load(self.CommonFile, Loader=yaml.FullLoader)
        self.CheckSetting = check_common()
        self.CommonSetting = self.CheckSetting.check_host(settings)
        self.CommonHost = self.CommonData["host_url"][self.CommonSetting]
        self.CommonHeaders = self.CommonData["headers"]
        self.CommonHeaders["Referer"] = self.CommonHost
        self.respones = {"host": self.CommonHost, "headers": self.CommonHeaders, "setting": self.CommonSetting}
        self.request = gnc_request()