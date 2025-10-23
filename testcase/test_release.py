from Base.Config.Authorization import *
from Base.Config.upload_excel import *
from Base.Log.log import *
from Base.ReadExcel.placement import Placement
import requests


excel_path = simple_excel_upload()
if not excel_path:
    print("未选择文件，程序退出")
    exit()
log = Logger()
plac = Placement()
host = Host
authorization = plac.Authorization(excel_path)
placementnum = plac.placement_num(excel_path)

class Testcase_release:
    def test_release(self):
        try:
            btime = plac.beginTime(excel_path)
            etime = plac.expireTime(excel_path)
            itemid = plac.itemId(excel_path)
            amount = plac.needAmount(excel_path)
            lock = plac.needUnlock(excel_path)
            sendtype = plac.sendType(excel_path)
            num = plac.totalCount(excel_path)
            locktype = plac.unlockType(excel_path)
            userid = plac.userIdList(excel_path)
            for i in range(1,placementnum+1):
                ind = i-1
                log.info(f'{i},{ind}')
                url = host + '/adm-api/adm/user_item_drop/drop'
                header = {
                    'content-type': 'application/json;charset=UTF-8',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
                    'authorization': authorization
                }
                data = {
                    'beginTime':btime[ind],              # 开始时间
                    'expireTime':etime[ind],             # 过期时间
                    'itemId':itemid[ind],                 # 盒子ID
                    'needAmount':amount[ind],             # 解锁金额（有金额就输入，没有就有null）
                    'needUnlock':lock[ind],        # 是否需要解锁（是：true，否：false）
                    'sendType':sendtype[ind],               # 是否区分时区（2：否，1:是）
                    'totalCount':num[ind],             # 数量
                    'unlockType':locktype[ind],      # 解锁类型（充值：top_up，客服：service）
                    'userIdList':userid[ind]          # 用户ID
                }
                log.info(f'参数{i}:开始时间:{btime[ind]},过期时间:{etime[ind]},盒子ID:{itemid[ind]},解锁金额:{amount[ind]},是否需要解锁:{lock[ind]},是否区分时区:{sendtype[ind]},数量:{num[ind]},解锁类型:{locktype[ind]},用户ID:{userid[ind]}')
                rep = requests.post(url=url, json=data, headers=header)
                code = rep.status_code
                log.info(f'状态码{i}：{code}')
                result = rep.json()
                log.info(f'投放结果{i}：{result}')
        except KeyError as e:
            log.error(f'有列表不存在：{e}')
        except IndexError as e:
            log.error(f'读取数据超出索引：{e}')
        except ValueError as e:
            log.error(f'数据错误或数据为空：{e}')
        except Exception as e:
            log.error(f'调用投放接口出错：{e}')


if __name__ == '__main__':
    a = Testcase_release()
    a.test_release()


