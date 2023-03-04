import json
import os
import random
import yaml
import sys


def get_path():
    BASE_PATH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    return BASE_PATH_DIR


def get_phone():
    phone = random.choice(['159', '188', '185', '136', '158', '151', '187', '139', "176"]) + "".join(
        random.choice("0123456789") for item in range(8))
    return phone


def get_proxies():
    file = open(get_path() + '/data/config_common.yaml', "r", encoding="utf-8")
    data = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    if 'proxies' in sys.argv:
        proxies = data['proxies']
        return proxies
    else:
        proxies = None
        return proxies


def get_case_info(file_path):
    with open(get_path() + file_path, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


def get_json_info(file_path):
    with open(get_path() + file_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data


def get_base_url(system):
    with open(get_path() + '/data/config_common.yaml', "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        env_list = ["aws_test", "dev"]
        if len(sys.argv) > 1:  # 如果list长度大于1说明有外部参数传入
            v_env = sys.argv[1]  # 根据下标获取外部传入的参数
            if v_env in env_list:  # 进行判断是否存在环境list中
                env = system + '_' + v_env
                base_url = data['host_url'][env]
                print('项目执行环境:', base_url)
                return base_url
            else:
                env = system + '_' + data['env']
                base_url = data['host_url'][env]
                print('项目执行环境:', base_url)
                return base_url
        else:
            env = system + '_' + data['env']
            base_url = data['host_url'][env]
            print('项目执行环境:', base_url)
            return base_url

print(get_base_url('routines'))
print(get_base_url('wenlai'))