# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 21:33
# @Author  : yifei.su
# @File    : dan_application_page_try_main.py

""" step1: 导入必须的库和 layout 文件 """
import sys

from dan_app_cfg_page import Ui_MainWindow

from ui_configure import *

class DanApplicationCfgPageWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()  # 定义初始化函数

    def initUI(self):
        set_table_head(self.tableWidget_appCfgRegBlock, appCfgReg_table_headers, HEADERHEIGHT, 160)
        set_table_item(self.tableWidget_appCfgRegBlock,  ROWHEIGHT,
                                                 appCfgReg_table_items )

        set_table_head(self.tableWidget_alertCfgRegBlock, alertCfgReg_table_headers, HEADERHEIGHT, 140)
        set_table_item(self.tableWidget_alertCfgRegBlock, ROWHEIGHT,
                                                 alertCfgReg_table_items )

        set_table_head(self.tableWidget_acquisitionRegBlock, acquistionReg_table_headers, HEADERHEIGHT, 140)
        set_table_item(self.tableWidget_acquisitionRegBlock, ROWHEIGHT,
                                                 acquistionReg_table_items)

        set_table_head(self.tableWidget_thresholdRegBlock, theresholdReg_table_headers, HEADERHEIGHT, 600)
        set_table_item(self.tableWidget_thresholdRegBlock, ROWHEIGHT,
                                                 theresholdReg_table_items)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = DanApplicationCfgPageWindow()
    win.show()

    sys.exit(app.exec_())