import time
import requests
import json
import xlrd
from xlutils.copy import copy
import configparser

"""
http://audi-pre.mobvoi.com/search/qa/?
query=附近的路况
appkey=CE435BCB81636B363DBDCB2F41090605
version=40000&address=中国,北京市,北京市,朝阳区,北京市朝阳区惠新东街,14号,39.979515,116.424273
output=lite
"""


class CalendarAutoTest:
    def __init__(self):

        self.CalendarExpectedResult = []
        self.CalendarActualResult = []
        self.CalendarQuery = []
        self.CalendarName = []
        self.conf = configparser.ConfigParser()
        self.conf.read('config.ini')
        self.festivalsList = self.conf['festivals_list']
        self.testYear = self.conf['year']['testYear']
        self.testProject = self.conf['project']['projectName']
        self.testLanguage = self.conf['language']['testLanguage']
        self.timestamp = time.strftime('%Y%m%d.%H%M%S', time.localtime(time.time()))
        if self.testProject == 'Audi' and self.testLanguage == 'mandarin':
            self.appkey = 'B70618D8E8132A32D4BCD6D68EFD08E2'                # Audi - sop2 - 普通话
        elif self.testProject == 'Audi' and self.testLanguage == 'cantonese':
            self.appkey = '5DDD2B9CCD6977BDFF3E109FBFBD0E15'                # Audi - sop2 - 粤语
        elif self.testProject == 'Porsche':
            self.appkey = 'CE435BCB81636B363DBDCB2F41090605'                # Porsche - 普通话
        self.test_parameters = "Project is %s. \nTest language is %s. \nAppkey is %s. \nTest keywords is %s." % (
            self.testProject,
            self.testLanguage,
            self.appkey,
            self.testYear)


    def postGetUrl(self, iquery):
        if self.testYear == 'null':
            newQuery = '%s是什么时候' % (iquery)
        else:
            newQuery = '%s的%s是什么时候' % (str(self.testYear), iquery)
        self.CalendarQuery.append(newQuery)
        data = {
            "query": newQuery,
            "appkey": self.appkey,
            "version": "40000",
            "address": "中国,北京市,北京市,朝阳区,北京市朝阳区惠新东街,14号,39.979515,116.424273",
            "output": "lite",
        }

        baseURL = "http://audi-pre.mobvoi.com/search/qa/?"                  # Stage 环境
        # baseURL = "http://audi.mobvoi.com/search/qa/?"                    # Live 环境
        # baseURL = "http://audi-dev.mobvoi.com/search/qa/?"                # dev 环境
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(baseURL, params=data, headers=headers)
        res.encoding = "utf-8"
        html = res.text
        rDict = json.loads(html)
        # print(res.url)
        self.CalendarName.append(iquery)
        displayText = rDict["languageOutput"]["displayText"]
        if displayText:
            self.CalendarActualResult.append(str(displayText))
        else:
            self.CalendarActualResult.append("NULL")

        print("=" * 50)
        print("Query:", rDict["query"])
        print("Domain:", rDict["domain"])
        print("Display:", rDict["languageOutput"]["displayText"])
        print("MessageId:", rDict["messageId"])
        print("=" * 50, "\n")

    def writeExcel(self):
        rExcel = xlrd.open_workbook("./template/CalendarList_%s_%s.xls"%(self.testProject,self.testLanguage),formatting_info=True)
        rTable = rExcel.sheet_by_name(u'All_FestivalsList')
        if self.testYear == '今年' or self.testYear == '2022年':
            self.CalendarExpectedResult = rTable.col_values(1)[1::]                 # 除了标题行的所有第2列内容。
        elif self.testYear == '明年' or self.testYear == '2023年':
            self.CalendarExpectedResult = rTable.col_values(2)[1::]
        elif self.testYear == '后年' or self.testYear == '2024年':
            self.CalendarExpectedResult = rTable.col_values(3)[1::]

        wExcel = copy(rExcel)
        try:
            wTable = wExcel.get_sheet(1)

            for i in range(len(self.CalendarActualResult)):
                wTable.write(i + 1, 0, self.CalendarName[i])
                wTable.write(i + 1, 1, self.CalendarQuery[i])
                wTable.write(i + 1, 2, self.CalendarExpectedResult[i])
                wTable.write(i + 1, 3, self.CalendarActualResult[i])            # xlwt对象的写方法，参数分别是行、列、值
                value1 = self.CalendarActualResult[i].replace('，',',').replace('。','.').replace(' ','')
                value2 = self.CalendarExpectedResult[i].replace('，',',').replace('。','.').replace(' ','')
                if value1 == value2:
                    wTable.write(i + 1, 4, 'PASS')
                else:
                    wTable.write(i + 1, 4, 'FAIL')
        except Exception as e:
            raise e
        finally:
            fileName = "CalendarList_Result_%s_%s_%s.xls" % (self.testProject, self.testLanguage, self.timestamp)
            wExcel.save(fileName)         # xlwt对象的保存方法;
            print(self.test_parameters)
            print('保存完成！---> %s' % fileName)

    def runTest(self):
        print("====== Run to Asterix calendar automation test! =====")
        print(self.test_parameters)
        for i, j in zip(self.festivalsList, range(len(self.festivalsList))):
            self.postGetUrl(self.festivalsList[i])
            print("完成:%s/%s..." % (j + 1, len(self.festivalsList)))
            time.sleep(1)
        self.writeExcel()
        print("====================== Done! ========================")


if __name__ == "__main__":
    MyRun = CalendarAutoTest()
    MyRun.runTest()
