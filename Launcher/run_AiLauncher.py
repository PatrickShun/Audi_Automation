import uiautomator2 as u2
import subprocess


class AutoAiLauncher(object):
    def __init__(self):
        init_commend = 'python3 -m uiautomator2 init'
        subprocess.run(init_commend, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        self.device = u2.connect()
        # self.device = u2.connect(self.Bench_IP)
        # self.Bench_IP = "172.16.250.248:5555"
        # self.device.click_post_delay = 1.5  #方法已被弃用
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

    def get_widget_index(self):
        # 获取位置信息
        widget_class_dict = {'Reco':'com.elektrobit.aed.home.app:id/notification_text',
                             'Media_mid':'com.elektrobit.aed.home.app:id/album_click_area',
                             'Media_small':'com.elektrobit.aed.home.app:id/enter_play_page',
                             'Weather':'com.ticauto.weather:id/tv_real_tempnumber',
                             'Recently':'com.elektrobit.aed.home.app:id/tv_title',
                             'Clock':'com.ticauto.weather:id/tv_date',
                             'Navigation':'com.ticauto.generalcarserver:id/tv_top_address',
                             'Amap':'',
                             'BaiduMap':''}
        widget_indexList = ['one', 'two', 'three', 'four']
        for widClass in widget_class_dict:
            for index_class in widget_indexList:
                if self.device(resourceId='com.elektrobit.aed.home.app:id/%s' % index_class).child(
                               resourceId=widget_class_dict[widClass]).exists():
                    v_info = self.device.xpath('//*[@resource-id="com.elektrobit.aed.home.app:id/%s"]' % index_class).all()
                    v_index = str(int(v_info[0].attrib['index']) + 1)
                    print('%s in [%s] Widget, 在第%s位;' % (widClass, index_class, v_index))


    def main_run(self):
        self.test_reset_launcher()
        self.test_recoWidget_move()
        self.get_widget_index()


if __name__ == "__main__":
    irun = AutoAiLauncher()
    irun.main_run()
