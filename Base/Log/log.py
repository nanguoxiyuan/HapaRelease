import logging
import sys


class Logger:
    def __init__(self):
        # 初始化逻辑不变，但记录当前日志类的文件名（用于排除自身栈帧）
        self.logger_file = __file__
        frame = sys._getframe(1)
        module_name = frame.f_globals.get('__name__', '__main__')
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False  # 避免日志重复输出
        if not self.logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s - %(filename)s - line:%(lineno)d - %(levelname)s: %(message)s',
                datefmt='[%Y-%m-%d %H:%M:%S]'
            )
            self.file_log = logging.FileHandler('hapa.log', 'a', encoding='utf-8')
            self.file_log.setFormatter(formatter)
            self.file_log.setLevel(logging.DEBUG)
            self.logger.addHandler(self.file_log)

    def _log(self, level, msg, *args, exc_info=None):
        # 动态调整栈深度，找到业务代码的栈帧（排除日志类自身）
        global frame
        for stack_depth in range(2, 6):  # 尝试不同栈深度（2-5）
            try:
                frame = sys._getframe(stack_depth)
                # 排除日志类文件的栈帧，确保行号指向业务代码
                if self.logger_file not in frame.f_code.co_filename:
                    break
            except ValueError:
                frame = sys._getframe(2)  # 兜底
                break

        # 创建日志记录，传递异常堆栈（exc_info）
        record = self.logger.makeRecord(
            self.logger.name,
            level,
            frame.f_code.co_filename,
            frame.f_lineno,  # 正确的业务代码行号
            msg,
            args,
            exc_info=exc_info,  # 传递堆栈信息
            func=frame.f_code.co_name
        )
        self.logger.handle(record)

    # 重写日志方法，支持exc_info参数
    def debug(self, msg, *args, exc_info=None):
        self._log(logging.DEBUG, msg, *args, exc_info=exc_info)
    def info(self, msg, *args, exc_info=None):
        self._log(logging.INFO, msg, *args, exc_info=exc_info)
    def warning(self, msg, *args, exc_info=None):
        self._log(logging.WARNING, msg, *args, exc_info=exc_info)
    def error(self, msg, *args, exc_info=None):
        self._log(logging.ERROR, msg, *args, exc_info=exc_info)
    def exception(self, msg, *args):
        # 自动传递当前异常堆栈（sys.exc_info()）
        self._log(logging.ERROR, msg, *args, exc_info=sys.exc_info())
