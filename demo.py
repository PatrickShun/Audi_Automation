import uiautomator2 as u2
from time import sleep
import xlrd
from xlutils.copy import copy

d = u2.connect()

for elem in d.xpath('//android.widget.TextView').all():
    print(elem.text)

