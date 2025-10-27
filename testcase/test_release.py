import time
from Base.Config.Authorization import *
from Base.Log.log import *
from Base.ReadExcel.placement import Placement
import requests


class Testcase_release:
    def __init__(self, excel_bytes):
        self.excel_bytes = excel_bytes  # 接收文件字节流
        self.logs = []  # 存储日志（用于网页展示）
        self.plac = Placement()
        self.host = Host
        # 初始化日志（同时写入文件和网页）
        self.log = Logger()

    def _log_to_web(self, message: str, level: str = "info"):
        """将日志同时记录到列表（用于网页展示）和原日志工具"""
        self.logs.append(f"[{time.strftime('%H:%M:%S')}] [{level.upper()}] {message}")
        if level == "info":
            self.log.info(message)
        elif level == "error":
            self.log.error(message)

    def test_release(self):
        try:
            # 从字节流读取 Excel 数据（需确保 Placement 类支持字节流输入）
            # 若原 Placement 只支持文件路径，需修改其方法（例如用 BytesIO 包装）
            authorization = self.plac.Authorization(self.excel_bytes)
            placementnum = self.plac.placement_num(self.excel_bytes)
            self._log_to_web(f"读取到 {placementnum} 条投放数据")

            # 循环调用接口
            for i in range(1, placementnum + 1):
                ind = i - 1
                self._log_to_web(f"开始处理第 {i} 条数据（索引：{ind}）")

                # 读取 Excel 中的参数（复用原逻辑）
                btime = self.plac.beginTime(self.excel_bytes)[ind]
                etime = self.plac.expireTime(self.excel_bytes)[ind]
                itemid = self.plac.itemId(self.excel_bytes)[ind]
                amount = self.plac.needAmount(self.excel_bytes)[ind]
                lock = self.plac.needUnlock(self.excel_bytes)[ind]
                sendtype = self.plac.sendType(self.excel_bytes)[ind]
                num = self.plac.totalCount(self.excel_bytes)[ind]
                locktype = self.plac.unlockType(self.excel_bytes)[ind]
                userid = self.plac.userIdList(self.excel_bytes)[ind]

                # 打印参数日志
                self._log_to_web(
                    f"参数 {i}：开始时间={btime}, 过期时间={etime}, 盒子ID={itemid}, "
                    f"解锁金额={amount}, 是否解锁={lock}, 时区类型={sendtype}, "
                    f"数量={num}, 解锁类型={locktype}, 用户ID={userid}"
                )

                # 调用接口
                url = self.host + "/adm-api/adm/user_item_drop/drop"
                headers = {
                    "content-type": "application/json;charset=UTF-8",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "authorization": authorization
                }
                data = {
                    "beginTime": btime,
                    "expireTime": etime,
                    "itemId": itemid,
                    "needAmount": amount,
                    "needUnlock": lock,
                    "sendType": sendtype,
                    "totalCount": num,
                    "unlockType": locktype,
                    "userIdList": userid
                }

                # 发送请求
                rep = requests.post(url=url, json=data, headers=headers)
                self._log_to_web(f"状态码 {i}：{rep.status_code}")
                result = rep.json()
                self._log_to_web(f"投放结果 {i}：{result}")

                # 延迟避免请求过于频繁
                time.sleep(3)

            self._log_to_web("所有数据处理完成", "info")

        except KeyError as e:
            self._log_to_web(f"列表不存在：{str(e)}", "error")
        except IndexError as e:
            self._log_to_web(f"数据索引超出范围：{str(e)}", "error")
        except ValueError as e:
            self._log_to_web(f"数据错误或为空：{str(e)}", "error")
        except Exception as e:
            self._log_to_web(f"接口调用出错：{str(e)}", "error")

