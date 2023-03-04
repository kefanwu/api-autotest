import pymysql
import time


class MysqlConnect(object):
    # 初始化, 构造函数
    def __init__(self, host, user, password, port, database):
        """
        :param host: IP
        :param user: 用户名
        :param password: 密码
        :param port: 端口号
        :param database: 数据库名
        """
        try:
            self.db = pymysql.connect(host=host, user=user, password=password, port=port, database=database,
                                      charset='utf8')
            self.cursor = self.db.cursor()
            # logger.info("链接数据库成功,库名：%r", database)
            print("链接数据库成功,库名：", database)
        except Exception as e:
            # logger.error("链接数据库失败：%r", e)
            print("链接数据库失败：", e)

    # 将要插入的数据写成元组传入
    def exec_data(self, sql, data=None):
        # 执行SQL语句
        self.cursor.execute(sql, data)
        # 提交到数据库执行
        self.db.commit()

    # sql拼接时使用repr()，将字符串原样输出
    def exec(self, sql):
        self.cursor.execute(sql)
        # 提交到数据库执行
        self.db.commit()

    # 查询所有数据
    def select_all(self, sql):
        """
        查询多条数据
        :param sql:
        """
        try:
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                return row
        except Exception as e:
            # logger.info("查询语句失败：%r", e)
            print("查询失败：%r", e)

    def select_all_data(self, sql):
        """
        查询多条数据，全部返回
        :param sql:
        """
        try:
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            # logger.info("查询语句失败：%r", e)
            print("查询失败：%r", e)

    def select_many_data(self, sql):
        """
        查询多条数据，全部返回
        :param sql:
        """
        try:
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchmany(1000)
            return results
        except Exception as e:
            # logger.info("查询语句失败：%r", e)
            print("查询失败：%r", e)

    def select_one(self, sql):
        """
        查询单条数据
        :param sql:
        """
        try:
            self.cursor.execute(sql)
            # 获取单条记录列表
            results = self.cursor.fetchone()
            return results
        except Exception as e:
            # logger.info("查询失败：%r", e)
            print("查询失败：%r", e)

    def execute_update_insert(self, sql):
        """
        插入或更新记录 成功返回最后的id
        :param sql:
        """
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.lastrowid

    def execute_delete(self, sql):
        """
        删除数据
        :param sql:
        """
        try:
            self.cursor.execute(sql)
            # 提交
            self.db.commit()
        except Exception as e:
            # logger.info("删除失败：%r", e)
            self.db.rollback()

    def close(self):
        self.cursor.close()
        self.db.close()
        # logger.info("关闭数据库链接")
        print("关闭数据库链接")


if __name__ == '__main__':
    mc = MysqlConnect(host='localhost', user='root', password='123456', port=3306, database='test')
    res = mc.select_one(
        'select * from test_case')
    print("查询返回结果：%r", res)
    # mc = MysqlConnect('192.144.166.161', 'edu_auth_rw', 'V7rh2yEbPrPU', 3606, 'bi_warehouse')
    # mc.exec('insert into test(id, text) values(%s, %s)' % (1, repr('哈送到附近')))
    # mc.exec_data('insert into test(id, text) values(%s, %s)' % (1, repr('哈送到附近')))
    # mc.exec_data('insert into test(id, text) values(%s, %s)',(13, '哈送到附近'))
    # res = mc.select_one("select * from dw_continuous_enroll_detail where student_id = '%s'" % 'ff80808168e63e440169428f92b87d9a')
    # logger.info("查询返回结果：%r", res)
    # logger.info(res[1])
    # logger.info(res[2])
    # data = time.strftime("%Y-%m-%d")
    # print(data)
    # if data in str(res[-2]):
    #     logger.info(res[-2])
    #     print("od")
    mc.close()
