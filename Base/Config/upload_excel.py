# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk
# import os
# from typing import List, Optional
#
# def simple_excel_upload():
#     # 存储选择的文件路径
#     selected_path: List[Optional[str]] = [None]  # 用列表存储，方便在内部函数中修改
#
#     root = tk.Tk()
#     root.title("Excel上传")
#     root.geometry("400x200")
#
#     def select_and_upload():
#         file_path = filedialog.askopenfilename(
#             title="选择Excel文件",
#             filetypes=[("Excel文件", "*.xlsx *.xls")]
#         )
#         if file_path:
#             selected_path[0] = file_path  # 保存选择的路径
#             messagebox.showinfo(
#                 "上传成功",
#                 f"文件: {os.path.basename(file_path)}\n"
#             )
#             root.quit()  # 关闭GUI窗口，继续执行后续代码
#         else:
#             messagebox.showwarning("提示", "请选择一个Excel文件")
#
#     # 界面组件
#     label = ttk.Label(root, text="Excel文件上传", font=('微软雅黑', 14))
#     label.pack(pady=20)
#     upload_btn = ttk.Button(root, text="选择Excel文件并上传", command=select_and_upload)
#     upload_btn.pack(pady=10)
#     close_btn = ttk.Button(root, text="关闭", command=root.quit)
#     close_btn.pack(pady=10)
#
#     root.mainloop()  # 启动GUI循环，用户操作后退出
#     root.destroy()  # 彻底销毁窗口
#     return selected_path[0]



import os
import streamlit as st
from typing import List, Optional


def simple_excel_upload() -> Optional[bytes]:
    """
    网页版文件上传：返回上传文件的字节流（替代本地文件路径）
    """
    st.subheader("Excel 文件上传")
    uploaded_file = st.file_uploader(
        label="选择 Excel 文件（.xlsx 或 .xls）",
        type=["xlsx", "xls"],
        accept_multiple_files=False
    )

    if uploaded_file:
        st.success(f"上传成功：{os.path.basename(uploaded_file.name)}")
        return uploaded_file.getvalue()  # 返回文件字节流（供后续读取）
    elif st.button("取消上传", type="secondary"):
        st.info("已取消文件选择")
        return None
    return None