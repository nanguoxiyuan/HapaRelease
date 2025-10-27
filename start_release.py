# import os
# import sys
# import logging
#
# # 设置工作目录到脚本所在目录
# if getattr(sys, 'frozen', False):
#     base_dir = os.path.dirname(sys.executable)
# else:
#     base_dir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(base_dir)
#
#
# # 导入并执行主程序
# from testcase.test_release import Testcase_release
#
# if __name__ == "__main__":
#     try:
#         test_case = Testcase_release()
#         test_case.test_release()
#     except Exception as e:
#         # 确保即使出错也能记录日志
#         logging.basicConfig(
#             level=logging.INFO,
#             format='%(asctime)s - %(levelname)s: %(message)s',
#             handlers=[
#                 logging.FileHandler('hapa.log', encoding='utf-8'),
#                 logging.StreamHandler()
#             ]
#         )
#         logging.error(f"程序执行出错: {e}", exc_info=True)




import streamlit as st
from Base.Config.upload_excel import simple_excel_upload
from testcase.test_release import Testcase_release


def main():
    # 设置页面配置
    st.set_page_config(
        page_title="投放测试工具",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("Excel 投放测试工具")
    st.divider()  # 分隔线

    # 步骤1：上传文件
    excel_bytes = simple_excel_upload()

    # 步骤2：处理文件（上传后显示"开始测试"按钮）
    if excel_bytes:
        if st.button("开始投放测试", type="primary"):
            with st.spinner("正在执行测试..."):
                # 初始化测试类并执行
                test_case = Testcase_release(excel_bytes)
                test_case.test_release()

                # 步骤3：展示日志结果
                st.subheader("执行日志")
                log_container = st.container(height=400)  # 固定高度的日志容器
                with log_container:
                    for log in test_case.logs:
                        # 错误日志标红，其他正常显示
                        if "[ERROR]" in log:
                            st.error(log)
                        else:
                            st.info(log)


if __name__ == "__main__":
    main()