from utils import globalvar as gl


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
