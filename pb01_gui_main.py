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

        set_table_head(self.table_chainCfg_devIdBlk, table_chainCfg_devidHead,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_chainCfg_devIdBlk, CHAIN_CFG_TABLE_ROWHG,
                       table_chainCfg_devidItem)

        set_table_head(self.table_chainCfg_uifcfgReg, table_chainCfg_uartIfHead,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_chainCfg_uifcfgReg, CHAIN_CFG_TABLE_ROWHG,
                       table_chainCfg_uartIfItem)

        set_table_head(self.table_chainCfg_addcfgReg, table_chainCfg_uartAddrHead,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_chainCfg_addcfgReg, CHAIN_CFG_TABLE_ROWHG,
                       table_chainCfg_uartAddrItem)

        set_table_head(self.table_chainCfg_pw, table_chainCfg_pwHeaders,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_chainCfg_pw, 30,
                       table_chainCfg_pwItems)

        set_table_head(self.table_chainCfg_rstReg, table_chainCfg_rstHeaders,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_chainCfg_rstReg, CHAIN_CFG_TABLE_ROWHG,
                       table_chainCfg_rstItems)

        # adjust chain configuration page table
        adjust_chainPage_ifid_tables(self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                            self.table_chainCfg_addcfgReg)
        set_chainPage_ifid_color(2, self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                            self.table_chainCfg_addcfgReg)

        ledChainPageDev0, ledChainPageDev1 = adjust_chainPage_pw_rst_tables(self.table_chainCfg_pw,
                                                                            self.table_chainCfg_rstReg)

        ''' initial device manage page '''
        set_table_item(self.table_devMgPage_init, CHAIN_CFG_TABLE_ROWHG,
                       table_devMg_iniItems)

        set_table_item(self.table_devMgPage_dc, CHAIN_CFG_TABLE_ROWHG,
                       table_devMg_dcItems)

        set_table_item(self.table_devMgPage_cur, CHAIN_CFG_TABLE_ROWHG,
                       table_devMg_curItems)

        ledDevMgPageInitDev0, ledDevMgPageInitDev1, ledDevMgPageCurDev0, ledDevMgPageCurDev1, \
        ledDevMgPageDcByte, ledDevMgPageAlertPk = adjust_devMgPage_tables(self.table_devMgPage_init,
                                                                          self.table_devMgPage_dc,
                                                                          self.table_devMgPage_cur)



        ''' initial application configuration page '''
        set_table_head(self.table_appCfgPage_appCfg, table_appCfgPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_appCfgPage_appCfg, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_appCfgReg_items)
        set_table_head(self.table_appCfgPage_alertCfg, table_appCfgPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_appCfgPage_alertCfg, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_alertCfgReg_items)
        set_table_head(self.table_appCfgPage_thresholdReg, table_appCfgPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_appCfgPage_thresholdReg, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_theresholdReg_items)
        set_table_head(self.table_appCfgPage_acqReg, table_appCfgPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_appCfgPage_acqReg, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_acqReg_items)

        adjust_appCfgPage_tables(self.table_appCfgPage_appCfg, self.table_appCfgPage_alertCfg,
                                 self.table_appCfgPage_thresholdReg, self.table_appCfgPage_acqReg)
        set_appCfgPage_table_color(self.table_appCfgPage_appCfg, self.table_appCfgPage_alertCfg,
                                 self.table_appCfgPage_thresholdReg, self.table_appCfgPage_acqReg)

        ''' initial diagnostic configuration page '''
        set_table_head(self.table_diagCfgPage_testCurCfgReg, table_diagCfgPage_testCfg_headers,
                       CHAIN_CFG_TABLE_HEHG, 120)
        set_table_item(self.table_diagCfgPage_testCurCfgReg, CHAIN_CFG_TABLE_ROWHG,
                       table_diagCfgPage_testCfg_items)
        set_table_head(self.table_diagCfgPage_diagThresReg, table_diagCfgPage_diagThre_headers,
                       CHAIN_CFG_TABLE_HEHG, 360)
        set_table_item(self.table_diagCfgPage_diagThresReg, CHAIN_CFG_TABLE_ROWHG,
                       table_diagCfgPage_diagThre_items)
        set_table_head(self.table_diagCfgPage_aluTestDiagReg, table_diagCfgPage_aluTeDiag_headers,
                       CHAIN_CFG_TABLE_HEHG, 150)
        set_table_item(self.table_diagCfgPage_aluTestDiagReg, CHAIN_CFG_TABLE_ROWHG,
                       table_diagCfgPage_aluTeDiag_items)

        adjust_diagCfgPage_tables(self.table_diagCfgPage_testCurCfgReg, self.table_diagCfgPage_diagThresReg,
                                  self.table_diagCfgPage_aluTestDiagReg)

        set_diagCfgPage_table_color(self.table_diagCfgPage_testCurCfgReg, self.table_diagCfgPage_diagThresReg,
                                  self.table_diagCfgPage_aluTestDiagReg)

        ''' initial measurement acquisition detailed data page '''
        set_table_item(self.table_meaAcqDetailData_alertRegDev0, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_alertRegItems)
        # self.table_meaAcqDetailData_alertRegDev0.setFixedHeight(150)  # 设置 table 高度
        set_table_item(self.table_meaAcqDetailData_dataRegDev0, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_dataRegItems)
        # self.table_meaAcqDetailData_dataRegDev0.setFixedHeight(300)  # 设置 table 高度

        set_table_item(self.table_meaAcqDetailData_alertRegDev1,CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_alertRegItems)
        # self.table_meaAcqDetailData_alertRegDev1.setFixedHeight(150)  # 设置 table 高度
        set_table_item(self.table_meaAcqDetailData_dataRegDev1, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_dataRegItems)
        # self.table_meaAcqDetailData_dataRegDev1.setFixedHeight(300)  # 设置 table 高度

        adjust_meaAcqDetailPage_tables(self.table_meaAcqDetailData_alertRegDev0,self.table_meaAcqDetailData_dataRegDev0,
                                       self.table_meaAcqDetailData_alertRegDev1,self.table_meaAcqDetailData_dataRegDev1)

        set_meaAcqDetailPage_table_color(self.table_meaAcqDetailData_alertRegDev0,self.table_meaAcqDetailData_dataRegDev0,
                                       self.table_meaAcqDetailData_alertRegDev1,self.table_meaAcqDetailData_dataRegDev1)

        meaAcqDetailPage_insert_led(self.table_meaAcqDetailData_alertRegDev0,self.table_meaAcqDetailData_alertRegDev1)

        ''' initial measurement acquisition summary data page '''
        set_table_item(self.table_meaAcqSumPage_status, CHAIN_CFG_TABLE_ROWHG,
                       table_diagAcqDataPage_statusTableItems)

        set_table_item(self.table_meaAcqSumPage_sumDataDev0, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqSumDataPage_sumDataItems)

        set_table_item(self.table_meaAcqSumPage_sumDataDev1, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqSumDataPage_sumDataItems)

        led8_meaAcqSumPage = adjust_meaAcqSumPage_tables(self.table_meaAcqSumPage_status,
                                                         self.table_meaAcqSumPage_sumDataDev0,
                                                         self.table_meaAcqSumPage_sumDataDev1)

        ''' initial diagnostic acquisition data page '''
        set_table_item(self.table_diagAcqPage_status, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_statusTableItems)

        set_table_item(self.table_diagAcqPage_alertReg_dev0, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_alertItems)

        set_table_item(self.table_diagAcqPage_dataReg_dev0, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_dataItems)

        set_table_item(self.table_diagAcqPage_alertReg_dev1, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_alertItems)

        set_table_item(self.table_diagAcqPage_dataReg_dev1, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_dataItems)

        led8_diaAcqDataPage = adjust_diagAcqDataPage_tables(self.table_diagAcqPage_status,
                                                            self.table_diagAcqPage_alertReg_dev0,
                                                            self.table_diagAcqPage_dataReg_dev0,
                                                            self.table_diagAcqPage_alertReg_dev1,
                                                            self.table_diagAcqPage_dataReg_dev1)

        ''' initial cell balance page '''
        set_table_head(self.table_cblPage_cblExpTime, table_cblPage_cblExpTimHeaders,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_cblPage_cblExpTime, CHAIN_CFG_TABLE_ROWHG, table_cblPage_cblExpTimItems)

        set_table_head(self.table_cblPage_cblCfgReg, table_cblPage_cblCfgRegHeaders,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_cblPage_cblCfgReg, CHAIN_CFG_TABLE_ROWHG, table_cblPage_cblCfgRegItems)

        set_table_head(self.table_cblPage_cblCtrlSimDemo, table_cblPage_cblCtrlDemoHeaders,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_cblPage_cblCtrlSimDemo, CHAIN_CFG_TABLE_ROWHG, table_cblPage_cblCtrlDemoItems)

        set_table_item(self.table_cblPage_cblCtrlStaInf, CHAIN_CFG_TABLE_ROWHG, table_cblPage_cblCtrlInfItems)

        adjust_cblPage_tables(self.table_cblPage_cblExpTime, self.table_cblPage_cblCfgReg,
                                    self.table_cblPage_cblCtrlSimDemo, self.table_cblPage_cblCtrlStaInf)


        # single afe initial ui as default
        self.slot_radio_single_dual_afe()

        # update_led_color(ledList_pageChain_st1pu_dev0[3], "#aa0000")
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
            # chain configuration page
            self.table_chainCfg_devIdBlk.hideRow(1)
            self.table_chainCfg_uifcfgReg.hideRow(1)
            self.table_chainCfg_addcfgReg.hideRow(1)
            # application configuration page
            self.table_appCfgPage_appCfg.hideColumn(8)
            self.table_appCfgPage_alertCfg.hideColumn(8)
            self.table_appCfgPage_thresholdReg.hideColumn(8)
            self.table_appCfgPage_acqReg.hideColumn(8)
            # diagnostic configuration page
            self.table_diagCfgPage_testCurCfgReg.hideColumn(12)
            self.table_diagCfgPage_diagThresReg.hideColumn(8)
            self.table_diagCfgPage_aluTestDiagReg.hideColumn(8)
            # measure acquisition detail data page
            self.frame_meaAcqDetailPage_alertDev1.hide()
            self.frame_meaAcqDetailPage_dataDev1.hide()
            self.table_meaAcqDetailData_alertRegDev1.hide()
            self.table_meaAcqDetailData_dataRegDev0.hide()
        elif self.radioButton_dualAfe.isChecked():
            # chain configuration page
            self.table_chainCfg_devIdBlk.showRow(1)
            self.table_chainCfg_uifcfgReg.showRow(1)
            self.table_chainCfg_addcfgReg.showRow(1)
            # application configuration page
            self.table_appCfgPage_appCfg.showColumn(8)
            self.table_appCfgPage_alertCfg.showColumn(8)
            self.table_appCfgPage_thresholdReg.showColumn(8)
            self.table_appCfgPage_acqReg.showColumn(8)
            # diagnostic configuration page
            self.table_diagCfgPage_testCurCfgReg.showColumn(12)
            self.table_diagCfgPage_diagThresReg.showColumn(8)
            self.table_diagCfgPage_aluTestDiagReg.showColumn(8)
            # measure acquisition detail data page
            self.frame_meaAcqDetailPage_alertDev1.show()
            self.frame_meaAcqDetailPage_dataDev1.show()
            self.table_meaAcqDetailData_alertRegDev1.show()
            self.table_meaAcqDetailData_dataRegDev0.show()



""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01MainWindow()
    win.show()

    sys.exit(app.exec_())

