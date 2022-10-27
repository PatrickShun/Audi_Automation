import uiautomator2 as u2
from time import sleep
import xlrd
from xlutils.copy import copy
import sys


class AutoAiLauncher(object):
    def __init__(self):
        self.Bench_IP = "172.16.250.248:5555"
        self.device = u2.connect(self.Bench_IP)
        self.device.press('home')


    def func1(self):
        pass

    def run(self):
        print('123')


if __name__ == "__main__":
    irun = AutoAiLauncher()
    irun.run()
