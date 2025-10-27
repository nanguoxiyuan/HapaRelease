import streamlit as st
from Base.Config.upload_excel import simple_excel_upload
from testcase.test_release import Testcase_release


def main():
    password = st.text_input("请输入操作密码", type="password")  # type="password" 是隐藏输入，固定写法
    correct_password = "asdfghjkl;'"
    if not password:
        st.warning("请输入密码以继续操作")
        st.stop()
    elif password != correct_password:
        st.error("密码错误！请重新输入")
        st.stop()
    # 设置页面配置
    st.set_page_config(
        page_title="投放测试工具",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("Excel 投放测试工具")
    st.divider()

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