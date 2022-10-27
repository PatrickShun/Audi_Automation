import uiautomator2 as u2
import subprocess
from time import sleep
import xlrd
from xlutils.copy import copy
import sys


class AutoAiLauncher(object):
    def __init__(self):
        # self.Bench_IP = "172.16.250.248:5555"
        # self.device = u2.connect(self.Bench_IP)
        init_commend = 'python3 uiautomator2 init'
        subprocess.run(init_commend, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        self.device = u2.connect()
        # self.device.click_post_delay = 1.5
        self.device.settings['operation_delay'] = (0.5, 1)
        self.device.wait_timeout = 20
        self.device.press('home')


    def test_reset_launcher(self):
        self.device.long_click(500, 500, 3)
        self.device.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/btn_left"]').click()
        self.device.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/btn_reset"]').click()
        self.device.xpath('//*[@resource-id="android:id/buttonPanel"]').click()
        self.device.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/btn_done"]').click()
        return "Ai Launcher mode reset succeeded!"

    def test_recoWidget_move(self):
        self.device.long_click(500, 500, 3)
        self.device.swipe(500, 400, 800, 400)
        self.device.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/btn_done"]').click()


    def main_run(self):
        self.test_reset_launcher()
        self.test_recoWidget_move()
        # htmls = self.device.dump_hierarchy()
        reco = self.device.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/one"]').all()
        media = self.device.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/two"]').all()
        weather = self.device.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/three"]').all()
        recently = self.device.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/four"]').all()
        reco_index = str(int(reco[0].attrib['index']) + 1)
        media_index = str(int(media[0].attrib['index']) + 1)
        weather_index = str(int(weather[0].attrib['index']) + 1)
        recently_index = str(int(recently[0].attrib['index']) + 1)
        print("推送流在第%s位" % reco_index)
        print("MediaWidget在第%s位" % media_index)
        print("天气小widget在第%s位" % weather_index)
        print("最近使用在第%s位" % recently_index)



if __name__ == "__main__":
    irun = AutoAiLauncher()
    irun.main_run()
