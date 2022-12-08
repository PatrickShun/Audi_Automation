import uiautomator2 as u2

class openAPPs():

    def __init__(self):
        self.idevice = u2.connect()
        self.idevice.implicitly_wait(10)
        self.idevice.settings['operation_delay'] = (1, 2)

    def openSettings(self):
        self.idevice.app_start(package_name='com.ticauto.settings', activity='com.ticauto.settings.SystemSettingsActivity')


    def openMedia(self):
        self.idevice.app_start(package_name='com.jidouauto.media', activity='com.jidouauto.media.ui.core.activity.MainActivity')



if __name__ == '__main__':
    irun = openAPPs()
    irun.openSettings()