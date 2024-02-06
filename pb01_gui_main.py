# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 10:44
# @Author  : yifei.su
# @File    : pb01_gui_main.py


""" step1: 导入必须的库和 layout 文件 """
import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import QColor
import time

from pb01_gui_main_window import Ui_MainWindow
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
        # initial single AFE radio
        self.radioButton_dualAfe.setChecked(True)
        # self.radioButton_singleAfe.setChecked(True)

        # device id tables initial
        set_table_head(self.table_chainCfg_devIdBlk, table_chainCfg_devidHead,
                       CHAIN_CFG_TABLE_HEHG, 85)

        # uifcfg register tables initial
        set_table_head(self.table_chainCfg_uifcfgReg, table_chainCfg_uartIfHead,
                       CHAIN_CFG_TABLE_HEHG, 85)


        # address register tables initial
        set_table_head(self.table_chainCfg_addcfgReg, table_chainCfg_uartAddrHead,
                       CHAIN_CFG_TABLE_HEHG, 85)

        # status power up dev0 table initial
        ledList_pageChain_st1pu_dev0, ledList_pageChain_st2pu_dev0, ledList_pageChain_fm1pu_dev0, \
        ledList_pageChain_fm2pu_dev0 = init_status_led_table_dev0(self.table_chainCfg_statusBlk_pwrUpDev0, 150)

        # status power up dev1 table initial
        ledList_pageChain_st1pu_dev1, ledList_pageChain_st2pu_dev1, ledList_pageChain_fm1pu_dev1, \
        ledList_pageChain_fm2pu_dev1 = init_status_led_table_dev1(self.table_chainCfg_statusBlk_pwrUpDev1, 150)

        # status initial dev0 table initial
        ledList_pageChain_st1in_dev0, ledList_pageChain_st2in_dev0, ledList_pageChain_fm1in_dev0, \
        ledList_pageChain_fm2in_dev0 = init_status_led_table_dev0(self.table_chainCfg_statusBlk_initDev0, 110)

        # status initial dev1 table initial
        ledList_pageChain_st1in_dev1, ledList_pageChain_st2in_dev1, ledList_pageChain_fm1in_dev1, \
        ledList_pageChain_fm2in_dev1 = init_status_led_table_dev1(self.table_chainCfg_statusBlk_initDev1, 110)

        # status current dev0 table initial
        ledList_pageChain_st1cu_dev0, ledList_pageChain_st2cu_dev0, ledList_pageChain_fm1cu_dev0, \
        ledList_pageChain_fm2cu_dev0 = init_status_led_table_dev0(self.table_chainCfg_statusBlk_curDev0, 110)

        # status current dev1 table initial
        ledList_pageChain_st1cu_dev1, ledList_pageChain_st2cu_dev1, ledList_pageChain_fm1cu_dev1, \
        ledList_pageChain_fm2cu_dev1 = init_status_led_table_dev1(self.table_chainCfg_statusBlk_curDev1, 110)

        # reset dev0 table initial
        set_table_head(self.table_chainCfg_rstBlk_Dev0, table_chainCfg_rstHead_dev0,
                       CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_RSTHG)
        set_table_item(self.table_chainCfg_rstBlk_Dev0, 1, CHAIN_CFG_TABLE_ROWHG,
                       table_chainCfg_rstItem_dev0)
        self.table_chainCfg_rstBlk_Dev0.item(0, 3).setBackground(QColor("#E2F0D9"))
        # reset dev1 table initial
        set_table_head(self.table_chainCfg_rstBlk_Dev1, table_chainCfg_rstHead_dev1,
                       CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_RSTHG)
        set_table_item(self.table_chainCfg_rstBlk_Dev1, 1, CHAIN_CFG_TABLE_ROWHG,
                       table_chainCfg_rstItem_dev1)
        self.table_chainCfg_rstBlk_Dev1.item(0, 0).setBackground(QColor("#E2F0D9"))

        # single afe initial ui as default
        self.slot_radio_single_dual_afe()

        # adjust chain configuration page interface & ID register table size and background color
        time.sleep(0.5)
        adjust_if_id_tables(self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                            self.table_chainCfg_addcfgReg)
        set_if_id_tables_color(2, self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                            self.table_chainCfg_addcfgReg)

        self.table_chainCfg_statusBlk_pwrUpDev0.setColumnWidth(2, self.table_chainCfg_rstBlk_Dev0.columnWidth(2))
        self.table_chainCfg_statusBlk_initDev0.setColumnWidth(2, self.table_chainCfg_rstBlk_Dev0.columnWidth(2))
        self.table_chainCfg_statusBlk_curDev0.setColumnWidth(2, self.table_chainCfg_rstBlk_Dev0.columnWidth(2))

        ''' initial application configuration page '''
        set_table_head(self.table_appCfgPage_appCfg, table_appCfgPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 160)
        set_table_item(self.table_appCfgPage_appCfg, 5, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_appCfgReg_items)
        set_table_head(self.table_appCfgPage_alertCfg, table_appCfgPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 130)
        set_table_item(self.table_appCfgPage_alertCfg, 4, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_alertCfgReg_items)
        set_table_head(self.table_appCfgPage_thresholdReg, table_appCfgPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 380)
        set_table_item(self.table_appCfgPage_thresholdReg, 14, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_theresholdReg_items)
        set_table_head(self.table_appCfgPage_acqReg, table_appCfgPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 130)
        set_table_item(self.table_appCfgPage_acqReg, 4, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_acqReg_items)


        update_led_color(ledList_pageChain_st1pu_dev0[3], "#aa0000")
        # update_led_color(self.label_186, "#aa0000")

        ''' 配置信号和槽 '''
        self.radioButton_singleAfe.clicked.connect(self.slot_radio_single_dual_afe)
        self.radioButton_dualAfe.clicked.connect(self.slot_radio_single_dual_afe)


    def slot_radio_single_dual_afe(self):
        """
        根据 single afe 和 dual afe radio button 被选择的状态，
        设置 QTableWidget 显示不同的行数
        :return:
        """
        if self.radioButton_singleAfe.isChecked():
            set_table_item(self.table_chainCfg_devIdBlk, 1, CHAIN_CFG_TABLE_ROWHG,
                           table_chainCfg_devidItem)
            set_table_item(self.table_chainCfg_uifcfgReg, 1, CHAIN_CFG_TABLE_ROWHG,
                           table_chainCfg_uartIfItem)
            set_table_item(self.table_chainCfg_addcfgReg, 1, CHAIN_CFG_TABLE_ROWHG,
                           table_chainCfg_uartAddrItem)
            self.table_chainCfg_devIdBlk.setRowCount(1)
            self.table_chainCfg_statusBlk_pwrUpDev1.hide()
            self.table_chainCfg_statusBlk_initDev1.hide()
            self.table_chainCfg_statusBlk_curDev1.hide()
            self.table_chainCfg_rstBlk_Dev1.hide()
            adjust_if_id_tables(self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                                self.table_chainCfg_addcfgReg)
            set_if_id_tables_color(1, self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                                   self.table_chainCfg_addcfgReg)
        elif self.radioButton_dualAfe.isChecked():
            set_table_item(self.table_chainCfg_devIdBlk, 2, CHAIN_CFG_TABLE_ROWHG,
                           table_chainCfg_devidItem)
            set_table_item(self.table_chainCfg_uifcfgReg, 2, CHAIN_CFG_TABLE_ROWHG,
                           table_chainCfg_uartIfItem)
            set_table_item(self.table_chainCfg_addcfgReg, 2, CHAIN_CFG_TABLE_ROWHG,
                           table_chainCfg_uartAddrItem)
            self.table_chainCfg_devIdBlk.setRowCount(2)
            self.table_chainCfg_statusBlk_pwrUpDev1.show()
            self.table_chainCfg_statusBlk_initDev1.show()
            self.table_chainCfg_statusBlk_curDev1.show()
            self.table_chainCfg_rstBlk_Dev1.show()
            adjust_if_id_tables(self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                                self.table_chainCfg_addcfgReg)
            set_if_id_tables_color(2, self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                                   self.table_chainCfg_addcfgReg)


""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01MainWindow()
    win.show()

    sys.exit(app.exec_())

