import requests
import json
import xlrd
from xlutils.copy import copy
from time import sleep

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

        self.CalendarList = []
        self.CalendarResult = []


    def postGetUrl(self,iquery):
        data = {
                "query": iquery,
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
        print("MessageId",rDict["messageId"])
        print("=" * 50, "\n")



    def readExcel(self):
        try:
            data = xlrd.open_workbook("CalendarList.xls",formatting_info=True) #读取excel文件,参数为保留格式
            table = data.sheets()[0] # 定义变量，设置为第0个sheets。
            self.CalendarList = table.col_values(1)[1:] # 获取此表格的第1列。
            # return tableValueCol[1:] # 直接return列表，从第一个开始，不要标题。
        except Exception as e:
            print(e)


    def writeExcel(self):
        try:
            rExcel = xlrd.open_workbook("CalendarList.xls",formatting_info=True)
            wExcel = copy(rExcel)
            wTable = wExcel.get_sheet(0)
            # row = 0 # 修改第一行
            col = 3 # 修改第一列
            for i in range(len(self.CalendarResult)):
                wTable.write(i+1,col,self.CalendarResult[i]) # xlwt对象的写方法，参数分别是行、列、值
                # wTable.write(i+1,col,'=IF(C2=D2,"PASS","FAIL")') #填写公式
        except Exception as e:
            raise e
        finally:
            wExcel.save("CalendarList.xls") # xlwt 对象的保存方法，这时便覆盖掉了原来的 Excel
            print("保存完成！")


    def runTest(self):
        print("====== Run to porsche calendar autoTest! =====")
        # debug：
        # imp_query = input("请输入Query")
        # postGetUrl("2022年的元旦是什么时候")
        # ===================================

        # 1.读取列表中的query，保存变量列表。
        self.readExcel()

        # 2.使用获取到的列表，执行请求URL，保存结果到List
        for i in self.CalendarList:
            if i:
                # print(i)
                self.postGetUrl(i)
                sleep(3)

        # 3.获取结果列表后，存储到excel表格中。
        self.writeExcel()
        print("================== Done! ==================")



if __name__ == "__main__":
    MyRun = CalendarAutoTest()
    MyRun.runTest()
