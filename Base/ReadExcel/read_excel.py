import os
from tkinter import messagebox

from openpyxl import load_workbook
import pathlib


# class Read_Excel:
#     # 读取excel
#     def read_excel(self,excel_path):
#         place = pathlib.Path(__file__).absolute()
#         place_path = place.parent / f'{excel_path}'
#         df = load_workbook(place_path)
#         dd = df.active
#         return dd


class Read_Excel:
    def read_excel(self, excel_path):
        df = load_workbook(excel_path)  # 读取用户选择的Excel
        dd = df.active  # 获取活跃工作表
        return dd