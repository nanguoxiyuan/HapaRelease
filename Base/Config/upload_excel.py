import os
import streamlit as st
from typing import Optional


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