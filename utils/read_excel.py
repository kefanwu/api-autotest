# coding:utf-8
import xlrd
from xlutils.copy import copy
from utils.config import get_path
# from utils.find_excel import *


class OperationExcel:
    def __init__(self, file_name=None, sheet_id=None):
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
        else:
            self.file_name = get_path() + '/企业导入模版.xlsx'
            self.sheet_id = 0
        self.data = self.get_data()

    # 获取sheets的内容
    def get_data(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        return tables

    def get_ncols(self):
        tables = self.data
        return tables.ncols

    # 获取总的行数
    def get_lines(self):
        tables = self.data
        return tables.nrows

    # 获取某一个单元格的内容
    def get_cell_value(self, row, col):
        return self.data.cell_value(row, col)

    def get_value(self, row, col):
        return self.data.cell_value(row, col)

    # 写入数据
    def write_value(self, row, col, value):
        """
        写入excel数据
        row,col,value
        :param value:
        :param row:
        :param col:
        """
        try:
            # 拿到Excel
            read_data = xlrd.open_workbook(self.file_name)
            # 复制一份
            write_data = copy(read_data)
            # 打开要操作的sheet
            sheet_data = write_data.get_sheet(self.sheet_id)
            # 写入表中，参数行、列、值
            sheet_data.write(row, col, value)
            # 保存
            write_data.save(self.file_name)
            print("写入行数:", row, "列:", col, "值:", value, "并保存成功")
        except Exception as e:
            print(e)

    # 根据对应的caseid 找到对应行的内容
    def get_rows_data(self, case_id):
        row_num = self.get_row_num(case_id)
        rows_data = self.get_row_values(row_num)
        return rows_data

    # 根据对应的caseid找到对应的行号
    def get_row_num(self, case_id):
        num = 0
        clols_data = self.get_cols_data()
        for col_data in clols_data:
            if case_id in col_data:
                return num
            num += 1

    # 根据行号，找到该行的内容
    def get_row_values(self, row):
        tables = self.data
        row_data = tables.row_values(row)
        return row_data

    # 获取某一列的内容
    def get_cols_data(self, col_id=None):
        if col_id is not None:
            cols = self.data.col_values(col_id)
        else:
            cols = self.data.col_values(0)
        return cols


if __name__ == '__main__':
    opers = OperationExcel()
    print(opers.get_cell_value(1, 4))
    # print(opers.get_value(1, 1))
    # print(opers.get_rows_data("Imooc-02"))
    # row_list = []
    # values = []
    # # 获取各行数据
    # sh = opers.get_data()
    # nrows = opers.get_lines()
    # for i in range(0, nrows):
    #     row_data = sh.row_values(i)
    #     # print(a)
    #     # print(type(a))
    #     row_list.append(row_data)
    # print(row_list)
    # b = [int(c[0]) for c in row_list]
    # for i in b:
    #     print(i)
    #     print(type(i))
    # for item in row_list:
    #     print(" ".join(list(item)))
    #     if "GET" in item:
    #         values.append(item)
    # print(values)
    # print(len(values))
    # 走链接数据库，获取数据库信息
    # 加入到列表中

    # print(values)
    # print(len(values))
    # 写入数据
    # opers.write_value(2, 9, "OK")
