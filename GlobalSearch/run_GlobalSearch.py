import uiautomator2 as u2
from time import sleep
import xlrd
from xlutils.copy import copy
import sys


def read_excel():
    try:
        data = xlrd.open_workbook("QueryList.xls")
        table = data.sheets()[0]
        tableValueCol = table.col_values(0)
        print('Query总数：%s' % len(tableValueCol))
        return tableValueCol
    except Exception as e:
        print(e)


class AutoGlobalSearch(object):

    def __init__(self):
        print("====== Run to Porsche GlobalSearch AutoTest! =====")
        print("!请确认高德、智慧加油、停车、娱乐应用的用户协议已同意！")
        input("!按任意键继续！")
        self.Bench_IP = "172.16.250.248:5555"
        try:
            # self.d = u2.connect(self.Bench_IP)
            self.d = u2.connect()
            self.d.implicitly_wait(30)
            self.d.settings['operation_delay'] = (2, 6)
            print("Bench connect Success...")
            self.d.press('home')
            sleep(5)
            self.d.swipe(300, 350, 1400, 350, 0.1)                                                      # 滑动到GS页面
        except Exception as er:
            print("初始化报错：%s" % er)

    def AutoRun(self):
        global wExcel
        queryList = read_excel()                                                                   # 读取Excel内容
        try:
            rExcel = xlrd.open_workbook('QueryList.xls', formatting_info=True)
            wExcel = copy(rExcel)
            wTable = wExcel.get_sheet(0)
            # row = 0   # 修改第一行
            col = 1     # 修改第二列
            for qn in range(len(queryList)):
                print("%s/%s 正在搜索【%s】..." % (qn+1, len(queryList), queryList[qn]))
                self.d.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/search_text"]').set_text(queryList[qn])
                self.d.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/icon_search"]').click()  # 点击搜索
                for i in range(10):
                    if self.d.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/loading_tv"]').exists is True:
                        print('loading %ss ...' % str(i*5))
                    else:
                        break
                resultData = []
                widgetTextView = self.d.xpath('//android.widget.TextView').all()
                for elem in range(len(widgetTextView)):
                    if elem + 1 == len(widgetTextView):
                        resultData.append(widgetTextView[elem].text)
                    else:
                        resultData.append(widgetTextView[elem].text + '\n')
                print(resultData)
                wTable.write(qn, col, resultData)
                self.d.screenshot('./Screenshot/%s.png' % queryList[qn])
                self.d.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/iv_back"]').click()      # 返回上一层
                
        except Exception as e:
            raise e
        finally:
            wExcel.save('QueryList.xls')
            print("Save done...")
            sys.exit()


if __name__ == '__main__':
    RunAuto = AutoGlobalSearch()
    RunAuto.AutoRun()
