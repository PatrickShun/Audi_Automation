#! /usr/bin/env python

import os
import configparser

PWD = os.path.split(os.path.abspath(__file__))[0]
PPWD = r'/home/xslan/Documents/02_Audi_Porsche_SDS_Report_Tools'
CONFIG_FILE = os.path.join(PPWD, 'config.ini')
# print (CONFIG_FILE)

class Config(object):
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read(CONFIG_FILE, encoding='utf-8')
        self.project = self.conf['config']['project']
        self.dir_asr = os.path.join(PPWD, self.conf['path']['dir_asr'])
        self.dir_his_asr = os.path.join(PPWD, self.conf['path']['dir_his_asr'])
        self.dir_nlu = os.path.join(PPWD, self.conf['path']['dir_nlu'])
        self.dir_his_nlu = os.path.join(PPWD, self.conf['path']['dir_his_nlu'])
        self.dir_result = os.path.join(PPWD, self.conf['path']['dir_result'])
        self.template = os.path.join(PPWD, 'templates')
        if self.project.lower().strip() in ['audi', 'audiclu37']:
            self.dir_template = os.path.join(self.template, 'Audi_CW15_SDS自动化测试报告.xlsx')
        elif self.project.lower().strip() in ['porsche']:
            self.dir_template = os.path.join(self.template, 'Porsche_CW15_SDS自动化测试报告.xlsx')



if __name__ == '__main__':
    config = Config()



