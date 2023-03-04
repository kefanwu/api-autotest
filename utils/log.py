import sys

# sys.path.append('..')
import time
from utils.config import get_path
from nb_log import LogManager, get_logger

# 第一种方式
t = time.strftime("%Y-%m-%d")
logger = get_logger('wkf', log_filename=get_path() + '/log/{}.log'.format(t))
logger.error('测试一下不封装')

# 第二种方式
# def logger():
#     t = time.strftime("%Y-%m-%d")
#
#     log = LogManager('tester').get_logger_and_add_handlers(log_filename=t + '.log',
#                                                            log_path=get_path() + '/log/')
#     return log
#
#
# logger = logger()


# logger = get_logger('preview_permission_preview')
# logger.debug('debug是绿色')
# logger.info('info是天蓝色')
# logger.warning('黄色有警告')
# logger.error('代码发生了错误')
#
# print(112123123123123)
