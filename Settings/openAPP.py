import uiautomator2 as u2
import os

class openAPPs():

    def __init__(self):
        self.idevice = u2.connect()
        self.idevice.implicitly_wait(10)
        self.idevice.settings['operation_delay'] = (1, 2)

    def openSettings(self):
        self.idevice.app_start(package_name='com.ticauto.settings', activity='com.ticauto.settings.SystemSettingsActivity')


    def openMedia(self):
        self.idevice.app_start(package_name='com.jidouauto.media', activity='com.jidouauto.media.ui.core.activity.MainActivity')


    def install_Amap(self):
        amap_path = os.path.normpath('./App/Auto_4.6.7.609561_signed.apk')
        self.idevice.app_install(amap_path)

    def uninstall_Amap(self):
        self.idevice.app_uninstall('com.autonavi.amapauto')

    def install_BaiduMap(self):
        baidumap_path = os.path.normpath('./App/BaiduMapAuto_v15.7.5.917_release_202112161621.apk')
        self.idevice.app_install(baidumap_path)

    def uninstall_BaiduMap(self):
        self.idevice.app_uninstall('com.baidu.BaiduMap.auto')



if __name__ == '__main__':
    irun = openAPPs()
    irun.openSettings()