#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.config import get_path
import yaml


def _init():
    global _global_dict
    _global_dict = {}

    # 默认环境
    _global_dict['env'] = 'pre'


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue


def get_yaml(key):
    file = open(get_path() + '/caseinfo/config_common.yaml', "r", encoding="utf-8")
    data = yaml.load(file, Loader=yaml.FullLoader)

    file.close()
    env = _global_dict['env']
    # print(data['config'])
    base_url = data['config'].get(key + "_" + env)
    return base_url


def get_db_yaml(key):
    print(key)
    file = open(get_path() + '/data/config_common.yaml', "r", encoding="utf-8")
    data = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    env = _global_dict['env']
    # print(data['config'])
    sql_content = data.get(key + "_" + env)
    print("连接sql环境", sql_content)
    return sql_content
