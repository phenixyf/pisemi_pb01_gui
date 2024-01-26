# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 21:33
# @Author  : yifei.su
# @File    : dan_application_page_try_main.py

""" step1: 导入必须的库和 layout 文件 """
import sys

from dan_application_config_page import Ui_MainWindow

from ui_configure import *

class DanApplicationCfgPageWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()  # 定义初始化函数

    def initUI(self):
        initial_tablewidget(self.tableWidget_appCfgRegBlock, appCfgReg_table_headers, HEADERHEIGHT, 160)
        set_table_item_data_and_background_color(self.tableWidget_appCfgRegBlock, 5, ROWHEIGHT,
                                                 appCfgReg_table_items, [3, 4], [])

        initial_tablewidget(self.tableWidget_alertCfgRegBlock, alertCfgReg_table_headers, HEADERHEIGHT, 140)
        set_table_item_data_and_background_color(self.tableWidget_alertCfgRegBlock, 4, ROWHEIGHT,
                                                 alertCfgReg_table_items, [3, 4], [])

        initial_tablewidget(self.tableWidget_acquisitionRegBlock, acquistionReg_table_headers, HEADERHEIGHT, 140)
        set_table_item_data_and_background_color(self.tableWidget_acquisitionRegBlock, 4, ROWHEIGHT,
                                                 acquistionReg_table_items, [9, 10], [])

        initial_tablewidget(self.tableWidget_thresholdRegBlock, theresholdReg_table_headers, HEADERHEIGHT, 600)
        set_table_item_data_and_background_color(self.tableWidget_thresholdRegBlock, 14, ROWHEIGHT,
                                                 theresholdReg_table_items, [5, 6], [])

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = DanApplicationCfgPageWindow()
    win.show()

    sys.exit(app.exec_())