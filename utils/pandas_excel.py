import json
from utils.config import get_path
secret = '230281SM3M1L'
with open(get_path()+'/data/preview_permission_preview/card_add.json','r',encoding='utf8')as fp:
    json_data = json.load(fp)
    # print('这是文件中的json数据：',json_data)
    # print('这是读取到文件数据的数据类型：', type(json_data))

    for i in json_data['data']:
        # print(i)
        if secret==i['secret']:
            continue
        print(i)
