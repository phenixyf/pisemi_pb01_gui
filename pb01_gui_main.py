# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 10:44
# @Author  : yifei.su
# @File    : pb01_gui_main.py


""" step1: 导入必须的库和 layout 文件 """
import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import QColor

from main_window import Ui_MainWindow
from ui_configure import *

class Pb01MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()  # 定义初始化函数

    def initUI(self):
        """
        GUI 初始化函数
        :return:
        """
        ''' inital CHAIN CONFIGURATION page '''
        # uart interface configuration tables
        initial_tablewidget(self.tableWidget_uartIf_conf, uartIf_table1_headers, HEADERHEIGHT, 130)
        initial_tablewidget(self.tableWidget_uartIf_addr, uartIf_table2_headers, HEADERHEIGHT, 130)
        self.radioButton_singleAfe.setChecked(True)
        self.slot_radio_single_dual_afe()
        # status register tables
        initial_tablewidget(self.tableWidget_statusReg_pwrUpDev0, statusReg_table_headers1, HEADERHEIGHT, 160)
        set_table_item_data_and_background_color(self.tableWidget_statusReg_pwrUpDev0, 4, ROWHEIGHT,
                                                 statusReg_table_items1, [3], [],[])
        initial_tablewidget(self.tableWidget_statusReg_initDev0, statusReg_table_headers1, HEADERHEIGHT, 160)
        set_table_item_data_and_background_color(self.tableWidget_statusReg_initDev0, 4, ROWHEIGHT,
                                                 statusReg_table_items1, [3], [],[])

        initial_tablewidget(self.tableWidget_statusReg_pwrUpDev1, statusReg_table_headers2, HEADERHEIGHT, 160)
        set_table_item_data_and_background_color(self.tableWidget_statusReg_pwrUpDev1, 4, ROWHEIGHT,
                                                 statusReg_table_items2, [0], [],[])
        initial_tablewidget(self.tableWidget_statusReg_initDev1, statusReg_table_headers2, HEADERHEIGHT, 160)
        set_table_item_data_and_background_color(self.tableWidget_statusReg_initDev1, 4, ROWHEIGHT,
                                                 statusReg_table_items2, [0], [],[])

        ''' initial application configuration page '''
        initial_tablewidget(self.tableWidget_appCfgRegBlock, appCfgReg_table_headers, HEADERHEIGHT, 190)
        set_table_item_data_and_background_color(self.tableWidget_appCfgRegBlock, 5, ROWHEIGHT,
                                                 appCfgReg_table_items, [3, 4], [], [2])

        initial_tablewidget(self.tableWidget_alertCfgRegBlock, alertCfgReg_table_headers, HEADERHEIGHT, 160)
        set_table_item_data_and_background_color(self.tableWidget_alertCfgRegBlock, 4, ROWHEIGHT,
                                                 alertCfgReg_table_items, [3, 4], [], [2])

        initial_tablewidget(self.tableWidget_acquisitionRegBlock, acquistionReg_table_headers, HEADERHEIGHT, 160)
        set_table_item_data_and_background_color(self.tableWidget_acquisitionRegBlock, 4, ROWHEIGHT,
                                                 acquistionReg_table_items, [9, 10], [], [2])

        initial_tablewidget(self.tableWidget_thresholdRegBlock, theresholdReg_table_headers, HEADERHEIGHT, 460)
        set_table_item_data_and_background_color(self.tableWidget_thresholdRegBlock, 14, ROWHEIGHT,
                                                 theresholdReg_table_items, [5, 6], [], [2])

        # update_led_color(self.label_186, "#aa0000")

        ''' 配置信号和槽 '''
        self.radioButton_singleAfe.clicked.connect(self.slot_radio_single_dual_afe)
        self.radioButton_dualAfe.clicked.connect(self.slot_radio_single_dual_afe)
        self.pushButton_uartIfConf.clicked.connect(self.cfg_uart_if)

    def cfg_uart_if(self):
        self.tableWidget_uartIf_conf.item(1, 6).setText("try")

    def slot_radio_single_dual_afe(self):
        """
        根据 single afe 和 dual afe radio button 被选择的状态，
        设置 QTableWidget 显示不同的行数
        :return:
        """
        if self.radioButton_singleAfe.isChecked():
            set_table_item_data_and_background_color(self.tableWidget_uartIf_conf, 2, ROWHEIGHT,
                                                     uartIf_table1_items, [3], range(4, 14),[])
            set_table_item_data_and_background_color(self.tableWidget_uartIf_addr, 2, ROWHEIGHT,
                                                     uartIf_table2_items, [3], range(4, 8),[])
            self.tableWidget_statusReg_pwrUpDev1.hide()
            self.tableWidget_statusReg_initDev1.hide()
            self.frame_statusReg_pwrUp_ledArray.hide()
            self.frame_statusReg_init_ledArray.hide()
        elif self.radioButton_dualAfe.isChecked():
            set_table_item_data_and_background_color(self.tableWidget_uartIf_conf, 3, ROWHEIGHT,
                                                     uartIf_table1_items, [3], range(4, 14),[])
            set_table_item_data_and_background_color(self.tableWidget_uartIf_addr, 3, ROWHEIGHT,
                                                     uartIf_table2_items, [3], range(4, 8),[])
            self.tableWidget_statusReg_pwrUpDev1.show()
            self.tableWidget_statusReg_initDev1.show()
            self.frame_statusReg_pwrUp_ledArray.show()
            self.frame_statusReg_init_ledArray.show()


""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01MainWindow()
    win.show()

    sys.exit(app.exec_())