# import time
#
# from Base.Config.Authorization import *
# from Base.Config.upload_excel import *
# from Base.Log.log import *
# from Base.ReadExcel.placement import Placement
# import requests
#
#
# excel_path = simple_excel_upload()
# if not excel_path:
#     print("未选择文件，程序退出")
#     exit()
# log = Logger()
# plac = Placement()
# host = Host
# authorization = plac.Authorization(excel_path)
# placementnum = plac.placement_num(excel_path)
#
# class Testcase_release:
#     def test_release(self):
#         try:
#             btime = plac.beginTime(excel_path)
#             etime = plac.expireTime(excel_path)
#             itemid = plac.itemId(excel_path)
#             amount = plac.needAmount(excel_path)
#             lock = plac.needUnlock(excel_path)
#             sendtype = plac.sendType(excel_path)
#             num = plac.totalCount(excel_path)
#             locktype = plac.unlockType(excel_path)
#             userid = plac.userIdList(excel_path)
#             for i in range(1,placementnum+1):
#                 ind = i-1
#                 log.info(f'{i},{ind}')
#                 url = host + '/adm-api/adm/user_item_drop/drop'
#                 header = {
#                     'content-type': 'application/json;charset=UTF-8',
#                     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
#                     'authorization': authorization
#                 }
#                 data = {
#                     'beginTime':btime[ind],              # 开始时间
#                     'expireTime':etime[ind],             # 过期时间
#                     'itemId':itemid[ind],                 # 盒子ID
#                     'needAmount':amount[ind],             # 解锁金额（有金额就输入，没有就有null）
#                     'needUnlock':lock[ind],        # 是否需要解锁（是：true，否：false）
#                     'sendType':sendtype[ind],               # 是否区分时区（2：否，1:是）
#                     'totalCount':num[ind],             # 数量
#                     'unlockType':locktype[ind],      # 解锁类型（充值：top_up，客服：service）
#                     'userIdList':userid[ind]          # 用户ID
#                 }
#                 log.info(f'参数{i}:开始时间:{btime[ind]},过期时间:{etime[ind]},盒子ID:{itemid[ind]},解锁金额:{amount[ind]},是否需要解锁:{lock[ind]},是否区分时区:{sendtype[ind]},数量:{num[ind]},解锁类型:{locktype[ind]},用户ID:{userid[ind]}')
#                 rep = requests.post(url=url, json=data, headers=header)
#                 code = rep.status_code
#                 log.info(f'状态码{i}：{code}')
#                 result = rep.json()
#                 log.info(f'投放结果{i}：{result}')
#                 time.sleep(3)
#         except KeyError as e:
#             log.error(f'有列表不存在：{e}')
#         except IndexError as e:
#             log.error(f'读取数据超出索引：{e}')
#         except ValueError as e:
#             log.error(f'数据错误或数据为空：{e}')
#         except Exception as e:
#             log.error(f'调用投放接口出错：{e}')
#
#
# if __name__ == '__main__':
#     a = Testcase_release()
#     a.test_release()



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

