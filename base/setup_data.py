from utils import globalvar as gl  # 工具类中编写了环境区分的逻辑，里面可以配置当前执行环境
import warnings
from utils.config import *  # 导入工具类里面有生成手机号的方法和获取当前项目根目录路径的方法


def get_host(host_name):
    try:
        host_url = gl.get_yaml(host_name)  # 内网域名
        return host_url
    except:
        gl._init()
        host_url = gl.get_yaml(host_name)  # 内网域名
        return host_url


def get_data_info(file_path):
        case_info = get_case_info(file_path)
        return case_info
