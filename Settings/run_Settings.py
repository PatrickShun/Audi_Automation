import unittest
import logging
import uiautomator2 as u2
import configparser
import HTMLTestRunner, time
from model.openAPP import openAPPs

# 初始化：python -m uiautomator2 init

class TestPorsche(unittest.TestCase):

    def setUp(self):
        self.conf = configparser.ConfigParser()
        self.conf.read('Settings/positioning_elements.ini')
        self.idevice = u2.connect()
        self.idevice.implicitly_wait(10)
        self.idevice.settings['operation_delay'] = (1, 2)
        self.logger = logging.getLogger()
        self.logger.setLevel('DEBUG')
        self.fmt = logging.Formatter('%(filename)s-%(lineno)d-%(asctime)s-%(levelname)s-%(message)s')
        self.file_handler = logging.FileHandler('mylog.log')
        self.file_handler.setLevel('DEBUG')
        self.file_handler.setFormatter(self.fmt)
        self.logger.addHandler(self.file_handler)
        self.openAPP = openAPPs()

    def tearDown(self):
        self.idevice.exists()

    def test01_Asterix_UC_Settings_Asterix_Settings_003_001(self):
        """进入AsterixSettings页面点击#3.1, 通过#3.1进入DefaultMap页面"""
        self.openAPP.openSettings()
        self.idevice.xpath(self.conf['settings']['default_map_button']).click()
        SystemMap_text = self.idevice.xpath(self.conf['settings']['system_map_text']).get_text()
        Amap_text = self.idevice.xpath(self.conf['settings']['Amap_text']).get_text()
        BaiduMap_text = self.idevice.xpath(self.conf['settings']['Baidumap_text']).get_text()
        SystemMap_nameList = ['MMI地图', 'MMI導航', 'MMI navigation',]
        AMap_Amap_nameList = ['高德地图',]
        BaiduMap_nameList = ['百度地图',]
        self.assertIn(SystemMap_text, SystemMap_nameList)
        self.assertIn(Amap_text, AMap_Amap_nameList)
        self.assertIn(BaiduMap_text, BaiduMap_nameList)


    def test02_Asterix_UC_Settings_Asterix_Settings_003_002(self):
        """进入AsterixSettings页面点击#3.2, 通过#3.2进入Recommendations页面"""
        self.idevice.app_start(package_name='com.ticauto.settings',
                               activity='com.ticauto.settings.SystemSettingsActivity')
        self.idevice.xpath(self.conf['settings']['RECO_button']).click()
        reco_service = self.idevice.xpath(self.conf['settings']['RECO_service']).get_text()
        reco_service_nameList = ['智能推荐服务', '智能推薦服務', 'AI recommendation service']
        print(reco_service)
        self.assertIn(reco_service, reco_service_nameList)

    def test03_Asterix_UC_Settings_Asterix_Settings_003_003(self):
        """进入AsterixSettings页面点击#3.3, 通过#3.3进入页面自定义编辑状态"""
        self.idevice.app_start(package_name='com.ticauto.settings',
                               activity='com.ticauto.settings.SystemSettingsActivity')
        self.idevice.swipe(900, 200, 900, 400, 0.2)

    def test04_Asterix_UC_Settings_Asterix_Settings_003_004(self):
        """进入AsterixSettings页面点击#3.4,通过#3.4进入LinkageAccounts页面"""
        self.idevice.app_start(package_name='com.ticauto.settings',
                               activity='com.ticauto.settings.SystemSettingsActivity')
        self.idevice.swipe(900, 200, 900, 400, 0.2)
        self.idevice.xpath(self.conf['settings']['accountLinkage']).click()
        kuwo = self.idevice.xpath(self.conf['settings']['kuwo']).get_text()
        ximalaya = self.idevice.xpath(self.conf['settings']['ximalaya']).get_text()
        mobvoi = self.idevice.xpath(self.conf['settings']['mobvoi']).get_text()
        kuwo_nameList = ['酷我音乐', '酷我音樂', 'Kuwo']
        Ximalaya_nameList = ['喜马拉雅', '喜馬拉雅', 'Himalaya']
        Mobvoi_nameList = ['出门问问', '出門問問', 'Mobvoi']
        self.assertIn(kuwo, kuwo_nameList)
        self.assertIn(ximalaya, Ximalaya_nameList)
        self.assertIn(mobvoi, Mobvoi_nameList)

    def test05_Asterix_UC_Settings_Asterix_Settings_003_005(self):
        """进入AsterixSettings页面点击#3.5, 通过#3.5进入Clearcache页面"""
        self.idevice.app_start(package_name='com.ticauto.settings',
                               activity='com.ticauto.settings.SystemSettingsActivity')
        self.idevice.swipe(900, 200, 900, 400, 0.2)
        self.idevice.xpath(self.conf['settings']['clear_cache']).click()
        clear_cache_title = self.idevice.xpath(self.conf['settings']['clear_cache_title']).get_text()
        clear_cache_titleList = ['清除缓存', '清除緩存', 'Clear cache']
        self.assertIn(clear_cache_title, clear_cache_titleList)


    def test06_Asterix_UC_Settings_Asterix_Settings_003_006(self):
        """进入AsterixSettings页面点击#3.5, 通过#3.6进入About页面"""
        self.idevice.app_start(package_name='com.ticauto.settings',
                               activity='com.ticauto.settings.SystemSettingsActivity')
        self.idevice.swipe(900, 400, 900, 200, 0.2)
        self.idevice.xpath(self.conf['settings']['about']).click()
        about_title = self.idevice.xpath(self.conf['settings']['about_title']).get_text()
        about_titleList = ['关于', '關於', 'About']
        self.assertIn(about_title, about_titleList)


    def test07_Asterix_UC_Settings_Asterix_Settings_001(self):
        """进入AsterixSettings页面, 通过#1返回MibSettings页面"""
        self.idevice.app_start(package_name='com.ticauto.settings',
                               activity='com.ticauto.settings.SystemSettingsActivity')
        # self.idevice.swipe(900, 200, 900, 400, 0.2)  # 向下滑动，显示完整的默认地图按钮。
        # self.idevice.xpath(self.conf['settings']['default_map_button']).click()
        self.idevice.xpath(self.conf['settings']['back_button']).click()
        # settings_title = self.idevice.xpath(self.conf['settings']['settings_title']).get_text()
        # settings_titleList = ['保时捷智慧互联设置', 'Porsche Connect 設定', 'Porsche Connect settings']
        # self.assertIn(settings_title, settings_titleList)



    def test08_Asterix_UC_Settings_Asterix_Settings_002(self):
        """进入AsterixSettings页面, Title的文案及展示"""
        self.idevice.app_start(package_name='com.ticauto.settings',
                               activity='com.ticauto.settings.SystemSettingsActivity')
        defaultMapList =    ['默认地图', '默認地圖', 'Default map']
        RECOList =          ['智能推荐', '智能推薦', 'Ai recommendation']
        accounLinkageList = ['账户关联', '帳戶關聯', 'Link accounts']
        clearCacheList =    ['清除缓存', '清除緩存', 'Clear cache']
        othersList =        ['其他', '其他', 'Others']
        aboutList =         ['关于', '關於', 'About']
        self.idevice.swipe(900, 200, 900, 400, 0.2)  # 向下滑动，显示完整的默认地图按钮。
        self.idevice.swipe(900, 400, 900, 330, 0.2)  # 向下滑动，显示完整的默认地图按钮。
        for i in range(1,7):
            value = self.idevice.xpath('//*[@resource-id="com.ticauto.settings:id/listview"]/android.widget.RelativeLayout[%s]/android.widget.TextView' % i).get_text()
            if i == 1:
                self.assertIn(value, defaultMapList)
            if i == 2:
                self.assertIn(value, RECOList)
            if i == 3:
                self.assertIn(value, accounLinkageList)
            if i == 4:
                self.assertIn(value, clearCacheList)
            if i == 5:
                self.assertIn(value, othersList)
            if i == 6:
                self.assertIn(value, aboutList)

    def Asterix_UC_Settings_Default_Map_List_003(self):
        """进入AsterixSettings_Defalut_map页面, 默认地图的列表区域"""
        # 车机初始状态下, 默认地图为系统地图&高德地图&百度地图为“未安装”状态(图片仅为示意)
        # 用户通过应用市场下载高德 or 百度地图后,对应地图状态变为“未选中”状态
        # 用户通过应用市场卸载高德 or 百度地图后, 对应地图状态变为“未安装”状态
        # 当地图状态为可被选中状态时, 用户可通过点击操作将地图设为默认地图, 点击后地图变为“选中”状态
        pass


    def Asterix_UC_Settings_Default_Map_List_001(self):
        """进入DefaultMap页面, 通过#1返回AsterixSettings页面"""
        pass


    def get_current_view_all_text(self):
        currentTextList = []
        for curText in self.idevice.xpath('//android.widget.TextView').all():
            currentTextList.append(curText.text)
        return currentTextList




if __name__ == '__main__':
    now = time.strftime("%y-%m_%d_%H_%M_%S_", time.localtime(time.time()))
    # unittest.main(verbosity=2)                                                            # unittest.main()与htmltestrunner不能同时存在
    testsuit = unittest.TestSuite()                                                         # 创建测试集
    testsuit.addTests([TestPorsche('test_001'), TestPorsche('test_002')])                   # 添加需要报告的用例列表
    # testsuit.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPorsche))           # 添加需要报告的整个类的用例

    # 创建报告
    go = open(str(now) + r'report.html', 'wb')                                              # 定义报告生成的路径
    runner = HTMLTestRunner.HTMLTestRunner(stream=go,
                                           title='Asterix_Settings_AutomationTeat_Report',  # 标题
                                           description='Settings_Stage')                    # 定义报告名，描述等
    runner.run(testsuit)                                                                    # 生成报告

    # debug：python3 -m unittest Settings.run_Settings.TestPorsche.test01_Asterix_UC_Settings_Asterix_Settings_003_001