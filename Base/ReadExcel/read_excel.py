from openpyxl import load_workbook


class Read_Excel:
    def read_excel(self, excel_path):
        df = load_workbook(excel_path)  # 读取用户选择的Excel
        dd = df.active  # 获取活跃工作表
        return dd