#! /usr/bin/env python
# -*- encoding:utf-8 -*-

import xlrd

ASR_DETAIL_KEYS = [u'测试集', u'Feature_ID', u'Asterix期望结果', u'录音文件', u'测试语料输入', u'测试语料输出',
                   u'ASR归一化结果', u'ASR错误代码']
WORD_SUMMARY_KEYS = ['Asterix', '1-WER']
SENTENCE_SUMMARY_KEYS = ['Asterix', 'PASS Rate']
NLU_DETAIL_KEYS = [u'测试集', u'Feature_ID', u'Asterix期望结果', u'录音文件', u'测试语料输入', u'Asterix结果',
                   u'Asterix实际结果', u'NLU结果', u'Domain预期', u'Domain实际', u'Intent预期', u'Intent实际',
                   u'Slot预期', u'Slot实际', u'Comments']
NLU_SUMMARY_KEYS = ['Asterix', 'PASS Rate']


class GetTResult(object):
    def __init__(self, dir_file):
        self.wb = xlrd.open_workbook(dir_file)

    def sum_word_data(self):
        return self.sum_data(WORD_SUMMARY_KEYS, 0)

    def sum_sentence_data(self):
        return self.sum_data(SENTENCE_SUMMARY_KEYS, 1)

    def sum_nlu_data(self):
        return self.sum_data(NLU_SUMMARY_KEYS, 0)

    def detail_asr_data(self):
        return self.detail_data(ASR_DETAIL_KEYS)

    def detail_nlu_data(self):
        return self.detail_data(NLU_DETAIL_KEYS)

    def detail_data(self, KEYS):
        # 该方法用于返回xls第0页的,KEYS列的所有数据.
        ws = self.wb.sheet_by_index(0)  # 创建对象，定位第0个sheet。
        nrows = ws.nrows  # 获取总行数如2971
        tags = [item.value for item in ws.row(0)]  # 获取第0行的所有标题。
        # print(tags)  # ['测试集', 'Feature_ID', 'Asterix期望结果', '录音文件',....
        # 获取符合要求的列表,定位KEYS在tags中的位置：
        cols = self.get_cols(tags, KEYS, 0)  # keys = NLU_DETAIL_KEYS = ['测试集', 'Feature_ID', 'Asterix期望结....
        # print(cols)  # [0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        datas = []
        datas.append(KEYS)
        for row in range(1, nrows):  # 遍历range从1开始到总行数的所有数据，从1开始为因为0行是标题。
            data = [ws.cell_value(row, col) for col in cols]  # 单行数据, 遍历cols的值col值(特定列数),保存每一行的特定列的数据.
            # print(data) # ['mandarin', 'AudiPayment-2', 'nlu_speech', '我要买144元的流量', '我要买144元的....
            datas.append(data)
        return datas

    def sum_data(self, KEYS, start):
        # 该方法用于返回xls中第二个sheet中第四行的KEYS列的数组。
        wd = self.wb.sheet_by_index(1)  # 创建sheet为第2页的对象wd
        nrows = wd.nrows  # 获取总列数"6"，就是总有7行
        tags = [item.value for item in wd.row(3)]  # 获取第四行的所有元素.
        # print(tags) "['Asterix', 'ERROR', 'FAIL', 'PASS', '总计', 'PASS Rate']"
        cols = self.get_cols(tags, KEYS, start)  # KEY=['Asterix', 'PASS Rate'] \\ start = 0 \\ clos是列表[0,5]
        sum_datas = []
        for row in range(4, nrows):  # 遍历数从4开头，因为结果合计数在第五行。nrows作为最后一行，也就是PASS Rate列。
            data = [wd.cell_value(row, col) for col in cols]  # 遍历cols,也就是[0，5]\\开始查找第4行第0列的作为data
            sum_datas.append(data)  # 把数组['nlu', '92.94%'],['nlu_speech', '94.66%'],['总计', '94.33%']添加到表sum_datas
        return sum_datas

    def get_cols(self, tags, keys, start):
        # 用于获取列表keys元素在xls(tags)的列位置，返回列数。【0，5】
        return [tags.index(key, start) for key in keys]


if __name__ == '__main__':
    dir_file = u'/home/xslan/Documents/Audi_Porsche_SDS_Report_Tools/Result/Audi_CW15_SDS自动化测试报告.xlsx'
    xr = GetTResult(dir_file)
    # print (xr.sum_word_data())
    # xr.count_difference('95.11%', '88.24')
