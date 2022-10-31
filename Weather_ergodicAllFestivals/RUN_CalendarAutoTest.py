import requests
import json
import xlrd
from xlutils.copy import copy
from time import sleep
import configparser


"""
http://audi-pre.mobvoi.com/search/qa/?
query=附近的路况
appkey=CE435BCB81636B363DBDCB2F41090605
version=40000&address=中国,北京市,北京市,朝阳区,北京市朝阳区惠新东街,14号,39.979515,116.424273
output=lite
"""

# B70618D8E8132A32D4BCD6D68EFD08E2

class CalendarAutoTest():
    def __init__(self):

        self.CalendarResult = []
        self.CalendarQuery = []
        self.conf = configparser.ConfigParser()
        self.conf.read('config.ini')
        self.festivalsList = self.conf['festivals_list']
        self.testYear = self.conf['year']



    def postGetUrl(self,iquery):
        newQuery = '%s年的%s是什么时候' % (str(self.testYear['testYear']), iquery)
        self.CalendarQuery.append(newQuery)
        data = {
                "query": newQuery,
                # "appkey": "CE435BCB81636B363DBDCB2F41090605", # 保时捷普通话
                "appkey": "B70618D8E8132A32D4BCD6D68EFD08E2", # Audi普通话
                "version": "40000",
                "address": "中国,北京市,北京市,朝阳区,北京市朝阳区惠新东街,14号,39.979515,116.424273",
                "output": "lite",
                }
        baseURL = "http://audi-pre.mobvoi.com/search/qa/?"
        headers = {"User-Agent":"Mozilla/5.0"}
        res = requests.get(baseURL,params=data,headers=headers)
        res.encoding = "utf-8"
        html = res.text
        rDict = json.loads(html)
        # print(res.url)
        displayText = rDict["languageOutput"]["displayText"]
        if displayText:
            self.CalendarResult.append(str(displayText))
        else:
            self.CalendarResult.append("NULL")

        print("=" * 50)
        print("Query:",rDict["query"])
        print("Domain:",rDict["domain"])
        print("Display:",rDict["languageOutput"]["displayText"])
        print("MessageId:",rDict["messageId"])
        print("=" * 50, "\n")


    def writeExcel(self):
        try:
            rExcel = xlrd.open_workbook("CalendarList.xls",formatting_info=True)
            wExcel = copy(rExcel)
            wTable = wExcel.get_sheet(0)
            # row = 0 # 修改第一行
            # col = 3 # 修改第3列
            for i in range(len(self.CalendarResult)):
                wTable.write(i + 1, 1, self.CalendarQuery[i])
                wTable.write(i + 1, 3, self.CalendarResult[i]) # xlwt对象的写方法，参数分别是行、列、值
                wTable.write(i + 1, 4, '=IF(C2=D2,"PASS","FAIL")') #填写公式
        except Exception as e:
            raise e
        finally:
            wExcel.save("CalendarList.xls") # xlwt 对象的保存方法，这时便覆盖掉了原来的 Excel
            print("保存完成！")


    def runTest(self):
        print("====== Run to Asterix calendar automation test! =====")
        for i,j in zip(self.festivalsList,range(len(self.festivalsList))):
            self.postGetUrl(self.festivalsList[i])
            print("完成:%s/%s" %(j+1 ,len(self.festivalsList)))
            sleep(3)
        self.writeExcel()
        print("====================== Done! ========================")



if __name__ == "__main__":
    MyRun = CalendarAutoTest()
    MyRun.runTest()
