import os
import sys
import logging

# 设置工作目录到脚本所在目录
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)


# 导入并执行主程序
from testcase.test_release import Testcase_release

if __name__ == "__main__":
    try:
        test_case = Testcase_release()
        test_case.test_release()
    except Exception as e:
        # 确保即使出错也能记录日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('hapa.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        logging.error(f"程序执行出错: {e}", exc_info=True)