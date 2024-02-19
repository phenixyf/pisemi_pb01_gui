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
from pb01_bridge_driver import *

class Pb01MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.hidBdg = hid.device()
        self.hidStatus = False
        self.setupNotification()
        self.statusMessage = QLabel()
        self.statusMessage.setFont(QFont('Calibri', 10, QFont.Bold))  # 设置字体和加粗
        self.statusBar().addPermanentWidget(self.statusMessage)
        self.flagSingleAfe = False
        self.ledChainPageDev0 = []
        self.ledChainPageDev1 = []
        self.ledDevMgPageInitDev0 = []
        self.ledDevMgPageInitDev1 = []
        self.ledDevMgPageCurDev0 = []
        self.ledDevMgPageCurDev1 = []
        self.ledDevMgPageDcByte = []
        self.ledDevMgPageAlertPk = []
        self.initUI()  # 定义初始化函数

    def initUI(self):
        """
        GUI 初始化函数
        :return:
        """
        self.open_hid()
        self.init_tab_pages()
        """  配置信号和槽 """
        ''' chain configuration page (page1) '''
        self.radioButton_singleAfe.clicked.connect(self.slot_radio_single_dual_afe)
        self.radioButton_dualAfe.clicked.connect(self.slot_radio_single_dual_afe)
        self.pushButton_chainCfg_cfg.clicked.connect(self.slot_pushBtn_chainCfg_cfg)
        self.pushButton_chainCfg_reset.clicked.connect(self.slot_pushBtn_chainCfg_reset)
        ''' device management page (page2) '''
        self.pushButton_devMgPage_init.clicked.connect(self.slot_pushBtn_devMgPage_init)
        self.pushButton_devMgPage_reInit.clicked.connect(self.slot_pushBtn_devMgPage_reinit)
        self.pushButton_devMgPage_clear.clicked.connect(self.slot_pushBtn_devMgPage_clear)
        self.pushButton_devMgPage_readBack.clicked.connect(self.slot_pushBtn_devMgPage_readBack)

    def init_tab_pages(self):
        ''' inital chain configuration page (page1) '''
        # initial single AFE radio
        self.radioButton_dualAfe.setChecked(True)
        # self.radioButton_singleAfe.setChecked(True)
        self.radio_chainCfg_swCorEn.hide()

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

        set_table_item(self.table_chainCfg_pw, 30,
                       table_chainCfg_pwItems)

        set_table_item(self.table_chainCfg_rstReg, CHAIN_CFG_TABLE_ROWHG,
                       table_chainCfg_rstItems)

        # adjust chain configuration page table
        adjust_chainPage_ifid_tables(self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                                     self.table_chainCfg_addcfgReg)
        set_chainPage_ifid_color(2, self.table_chainCfg_devIdBlk, self.table_chainCfg_uifcfgReg,
                                 self.table_chainCfg_addcfgReg)

        self.ledChainPageDev0, self.ledChainPageDev1 = adjust_chainPage_pw_rst_tables(self.table_chainCfg_pw,
                                                                                      self.table_chainCfg_rstReg)

        # disable reset button
        current_style = self.pushButton_chainCfg_reset.styleSheet()
        new_style = current_style + " QPushButton {background-color: #d0d0d0;}"  # 原来颜色 #e84d00
        self.pushButton_chainCfg_reset.setStyleSheet(new_style)
        self.pushButton_chainCfg_reset.setDisabled(True)

        ''' initial device manage page (page2) '''
        set_table_item(self.table_devMgPage_init, CHAIN_CFG_TABLE_ROWHG,
                       table_devMg_iniItems)

        set_table_item(self.table_devMgPage_dc, CHAIN_CFG_TABLE_ROWHG,
                       table_devMg_dcItems)

        set_table_item(self.table_devMgPage_cur, CHAIN_CFG_TABLE_ROWHG,
                       table_devMg_curItems)

        self.ledDevMgPageInitDev0, self.ledDevMgPageInitDev1, \
        self.ledDevMgPageCurDev0, self.ledDevMgPageCurDev1, \
        self.ledDevMgPageDcByte, self.ledDevMgPageAlertPk = adjust_devMgPage_tables(self.table_devMgPage_init,
                                                                                    self.table_devMgPage_dc,
                                                                                    self.table_devMgPage_cur)

        # disable re-initial button
        current_style = self.pushButton_devMgPage_reInit.styleSheet()
        new_style = current_style + " QPushButton {background-color: #d0d0d0;}"  # 原来颜色 #ED7D31
        self.pushButton_devMgPage_reInit.setStyleSheet(new_style)
        self.pushButton_devMgPage_reInit.setDisabled(True)
        # disable clear comm button
        current_style = self.pushButton_devMgPage_clear.styleSheet()
        new_style = current_style + " QPushButton {background-color: #d0d0d0;}"  # 原来颜色 #FFC000
        self.pushButton_devMgPage_clear.setStyleSheet(new_style)
        self.pushButton_devMgPage_clear.setDisabled(True)

        ''' initial application configuration page (page3) '''
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

        ''' initial diagnostic configuration page (page4) '''
        set_table_head(self.table_diagCfgPage_testCurCfgReg, table_diagCfgPage_testCfg_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_diagCfgPage_testCurCfgReg, CHAIN_CFG_TABLE_ROWHG,
                       table_diagCfgPage_testCfg_items)
        set_table_head(self.table_diagCfgPage_diagThresReg, table_diagCfgPage_diagThre_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_diagCfgPage_diagThresReg, CHAIN_CFG_TABLE_ROWHG,
                       table_diagCfgPage_diagThre_items)
        set_table_head(self.table_diagCfgPage_aluTestDiagReg, table_diagCfgPage_aluTeDiag_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_diagCfgPage_aluTestDiagReg, CHAIN_CFG_TABLE_ROWHG,
                       table_diagCfgPage_aluTeDiag_items)

        adjust_diagCfgPage_tables(self.table_diagCfgPage_testCurCfgReg, self.table_diagCfgPage_diagThresReg,
                                  self.table_diagCfgPage_aluTestDiagReg)

        set_diagCfgPage_table_color(self.table_diagCfgPage_testCurCfgReg, self.table_diagCfgPage_diagThresReg,
                                    self.table_diagCfgPage_aluTestDiagReg)

        ''' initial acquisition request page (page5) '''
        self.radioButton_acqReqPage_acqiirbyp.setEnabled(False)
        self.radioButton_acqReqPage_acqiirproc.setEnabled(False)
        self.radioButton_acqReqPage_alutesten.setEnabled(False)
        self.radioButton_acqReqPage_dataUpdate.setEnabled(False)
        self.radioButton_acqReqPage_auxaDiagA.setEnabled(False)
        self.radioButton_acqReqPage_auxaDiagB.setEnabled(False)
        set_table_head(self.table_acqReqPage_acqReq, table_acqReqPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_acqReqPage_acqReq, CHAIN_CFG_TABLE_ROWHG,
                       table_acqReqPage_items)

        adjust_acqReqPage_tables(self.table_acqReqPage_osr, self.table_acqReqPage_acqReq)

        ''' initial measurement acquisition summary data page (page6) '''
        set_table_item(self.table_meaAcqSumPage_dc, CHAIN_CFG_TABLE_ROWHG,
                       table_devMg_dcItems)

        set_table_item(self.table_meaAcqSumPage_status, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqSumDataPage_statusTableItems)

        set_table_item(self.table_meaAcqSumPage_sumDataDev0, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqSumDataPage_sumDataItems)

        set_table_item(self.table_meaAcqSumPage_sumDataDev1, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqSumDataPage_sumDataItems)

        ledMeaAcqSumPageDc, ledMeaAcqSumPageAlert, \
        ledMeaAcqSumPageStaDev0, ledMeaAcqSumPageStaDev1 = adjust_meaAcqSumPage_tables(self.table_meaAcqSumPage_dc,
                                                                                       self.table_meaAcqSumPage_status,
                                                                                       self.table_meaAcqSumPage_sumDataDev0,
                                                                                       self.table_meaAcqSumPage_sumDataDev1)

        ''' initial measurement acquisition detailed data page (page7) '''
        set_table_item(self.table_meaAcqDetailData_alertRegDev0, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_alertRegItems)

        set_table_item(self.table_meaAcqDetailData_dataRegDev0, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_dataRegItems)

        set_table_item(self.table_meaAcqDetailData_alertRegDev1, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_alertRegItems)

        set_table_item(self.table_meaAcqDetailData_dataRegDev1, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_dataRegItems)

        adjust_meaAcqDetailPage_tables(self.table_meaAcqDetailData_alertRegDev0,
                                       self.table_meaAcqDetailData_dataRegDev0,
                                       self.table_meaAcqDetailData_alertRegDev1,
                                       self.table_meaAcqDetailData_dataRegDev1)

        set_meaAcqDetailPage_table_color(self.table_meaAcqDetailData_alertRegDev0,
                                         self.table_meaAcqDetailData_dataRegDev0,
                                         self.table_meaAcqDetailData_alertRegDev1,
                                         self.table_meaAcqDetailData_dataRegDev1)

        ledMeaAcqDetailPageDev0, \
        ledMeaAcqDetailPageDev1 = meaAcqDetailPage_insert_led(self.table_meaAcqDetailData_alertRegDev0,
                                                              self.table_meaAcqDetailData_alertRegDev1)

        ''' initial diagnostic acquisition data page (page8) '''
        set_table_item(self.table_diagAcqPage_dc, CHAIN_CFG_TABLE_ROWHG, table_devMg_dcItems)

        set_table_item(self.table_diagAcqPage_status, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_statusTableItems)

        set_table_item(self.table_diagAcqPage_alertReg_dev0, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_alertItems)

        set_table_item(self.table_diagAcqPage_dataReg_dev0, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_dev0DataItems)

        set_table_item(self.table_diagAcqPage_alertReg_dev1, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_alertItems)

        set_table_item(self.table_diagAcqPage_dataReg_dev1, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_dev1DataItems)

        ledDiagAcqDataPageDc, ledDiagAcqDataPageAlert, \
        ledDiagAcqDataPageStaDev0, ledDiagAcqDataPageStaDev1, \
        ledDiagAcqDataPageDev0, ledDiagAcqDataPageDev1 = adjust_diagAcqDataPage_tables(self.table_diagAcqPage_dc,
                                                                                       self.table_diagAcqPage_status,
                                                                                       self.table_diagAcqPage_alertReg_dev0,
                                                                                       self.table_diagAcqPage_dataReg_dev0,
                                                                                       self.table_diagAcqPage_alertReg_dev1,
                                                                                       self.table_diagAcqPage_dataReg_dev1)

        ''' initial cell balance page (page9) '''
        self.radioButton_cblPage_auto.setEnabled(False)
        self.radioButton_cblPage_discharge.setEnabled(False)
        self.radioButton_cblPage_autoMeaSnd.setEnabled(False)
        self.radioButton_cblPage_autoMeaMin.setEnabled(False)
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

        # dual afe initial ui as default
        self.slot_radio_single_dual_afe()

        # update led color
        self.ledChainPageDev0[0][13].setStyleSheet(led_blue_style)
        self.ledChainPageDev1[0][13].setStyleSheet(led_blue_style)
        self.ledDevMgPageInitDev0[0][13].setStyleSheet(led_blue_style)
        self.ledDevMgPageInitDev1[0][13].setStyleSheet(led_blue_style)
        self.ledDevMgPageCurDev0[0][13].setStyleSheet(led_blue_style)
        self.ledDevMgPageCurDev1[0][13].setStyleSheet(led_blue_style)

    def set_warning_message(self, pWarnLineEdit, pMes, pPrefix="WARNING:"):
        """
        在报错 lineEdit 中显示报错信息
        :param pWarnLineEdit: 报错 lineEdit 对象
        :param pMes: 报错信息
        :param pPrefix: 报错信息前缀，例如 "WARING: Write UIFCFG "
        :return:
        """
        pWarnLineEdit.setStyleSheet(lineEdit_warn_style)
        pWarnLineEdit.setText(pPrefix + pMes)

    def set_default_warn_bar(self, pWarnLineEdit):
        """
        将 warning bar 设置成默认无警告信息水蓝色背景
        :param pWarnLineEdit: 要设置的 warnning lineEdit 对象
        :return:
        """
        pWarnLineEdit.setStyleSheet(lineEdit_default_style)
        pWarnLineEdit.setText("WARNING:")

    def afe_write_read_all(self, pRegAddr, pRegDataLsb, pRegDataMsb):
        """
        向 daisy-chain 所有 AFE 某个寄存器写入数据，并再读取所有 AFE 该寄存器
        注意：本工程目前只支持 2 个 AFE，通过 AFE radio 选择，所以读取多少个 AFE 在函数实现中用 AFE radio 当前状态来判断
        :param pRegAddr: 要读写的寄存器地址
        :param pRegDataLsb: data lsb
        :param pRegDataMsb: data msb
        :return: 返回一个列表，
                 列表中包含从 daisy-chain 读取的所有 AFE 该寄存器的数据，如 [afe0DataLsb, afe0DataMsb, afe1DataLsb, afe1DataMsb]
        """
        # write register
        rtWr = pb01_write_all(self.hidBdg, pRegAddr, pRegDataLsb, pRegDataMsb, 0x00)  # write all, alseed=0x00
        if (rtWr == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_chainCfg_cfgWarn, rtWr, f"WARNING: Write reg{hex(pRegAddr)} ")
            return "error"

        # read register
        if self.flagSingleAfe:
            rtRd = pb01_read_all(self.hidBdg, pRegAddr, 1, 0x00)  # read all, alseed=0x00
            if (rtRd == ("message return RX error" or "pec check error")):
                self.set_warning_message(self.lineEdit_chainCfg_cfgWarn, rtRd, f"WARNING: Read reg{hex(pRegAddr)} ")
                return "error"
            else:
                return rtRd[2:4]
        else:
            rtRd = pb01_read_all(self.hidBdg, pRegAddr, 2, 0x00)  # read all, alseed=0x00
            if (rtRd == ("message return RX error" or "pec check error")):
                self.set_warning_message(self.lineEdit_chainCfg_cfgWarn, rtRd, f"WARNING: Read reg{hex(pRegAddr)} ")
                return "error"
            else:
                return rtRd[2:6]

    def update_table_item_data(self, pTable, pRow, pCol, pText):
        """
        保持单元格背景、对齐等原格式不变的前提下，更新单元格内容
        :param pTable: table object
        :param pRow: 单元格所在行
        :param pCol: 单元格所在列
        :param pText: 要更新的内容
        :return:
        """
        # 获取当前单元格的背景颜色和对齐格式
        current_bg_color = pTable.item(pRow, pCol).background()
        current_alignment = pTable.item(pRow, pCol).textAlignment()

        # 更新单元格数据
        pTable.setItem(pRow, pCol, QTableWidgetItem(pText))

        # 重新设置背景颜色和对齐格式
        pTable.item(pRow, pCol).setBackground(current_bg_color)
        pTable.item(pRow, pCol).setTextAlignment(current_alignment)

    def update_dc_led(self, pDc, pLedList):
        """
        根据 DC byte 各 bit 的值更新对应的 led
        此函数还有判断 DC byte 是否有 alert 功能，当返回 False (DC 不全为 0) 时说明有 alert
        :param pDc: DC byte 当前值
        :param pLedList: 各 tab 页对应的 DC byte led 串列表
        :return: True - DC byte 全为 0
                 False -  DC byte 不全为 0

        """
        flag = True
        for i in range(8):
            # status1
            if pDc & (0x80 >> i):  # biti = 1
                pLedList[i].setStyleSheet(led_red_style)
                flag = False
            else:  # biti = 0
                pLedList[i].setStyleSheet(led_green_style)
        return flag


    def update_alertPk_led(self, pAlertPk, pLedList):
        """
        根据 alert packet data 各 bit 的值更新对应的 led
        :param pAlertPk: alert packet data 当前值
        :param pLedList: 各 tab 页对应的 alert packet led 串列表
        :return: none
        """
        flag = True
        for i in range(48):
            # status1
            if pAlertPk & (0x800000 >> i):  # biti = 1
                pLedList[i].setStyleSheet(led_red_style)
                flag = False
            else:  # biti = 0
                pLedList[i].setStyleSheet(led_green_style)
        return flag


    def update_status_register_led(self, pSt1, pSt2, pFm1, pFm2, pLedList):
        """
        根据 status block 各寄存器的值，更新其对应的 led 颜色
        :param pSt1: status1 当前值
        :param pSt2: status2 当前值
        :param pFm1: fmea1 当前值
        :param pFm2: fmea2 当前值
        :param pLedList: 要更新的 led 串列表
                         在初始化时，包含 status block 的各 tab 页会生成不同的 led 列表
                         dev0, dev1 也会生成不同的 led 列表
                         所以该函数只有一个 pLedList 参数，更新 dev0 或 dev1 时要分别调用此函数
        :return:
        """
        for i in range(16):
            # status1
            if pSt1 & (0x8000 >> i):  # biti = 1
                if i == 13:
                    if pSt2 & 0x0060:
                        pLedList[0][i].setStyleSheet(led_green_style)
                    else:
                        pLedList[0][i].setStyleSheet(led_red_style)
                else:
                    pLedList[0][i].setStyleSheet(led_red_style)
            else:  # biti = 0
                pLedList[0][i].setStyleSheet(led_white_style)

            # status2
            if pSt2 & (0x8000 >> i):  # biti = 1
                if i == 9 or i == 10:
                    pLedList[1][i].setStyleSheet(led_green_style)
                else:
                    pLedList[1][i].setStyleSheet(led_red_style)
            else:  # biti = 0
                pLedList[1][i].setStyleSheet(led_white_style)

            # fmea1
            if 0 < i < 5:
                pLedList[2][i].setStyleSheet(led_gray_style)
            else:
                if pFm1 & (0x8000 >> i):  # biti = 1
                    pLedList[2][i].setStyleSheet(led_red_style)
                else:   # biti = 0
                    pLedList[2][i].setStyleSheet(led_white_style)

            # fmea2
            if 1 < i < 4:
                pLedList[3][i].setStyleSheet(led_gray_style)
            else:
                if pFm1 & (0x8000 >> i):  # biti = 1
                    pLedList[3][i].setStyleSheet(led_red_style)
                else:  # biti = 0
                    pLedList[3][i].setStyleSheet(led_white_style)


    def slot_pushBtn_chainCfg_cfg(self):
        # initial daisy chain
        daisyChainReturn = pb01_daisy_chain_initial(self.hidBdg, 0x00)
        if (daisyChainReturn == ("transaction5 time out" or
                                 "transaction5 time out" or
                                 "transaction5 time out" or
                                 "clear bridge rx buffer time out")):
            self.set_warning_message(self.lineEdit_chainCfg_cfgWarn, daisyChainReturn, "WARNING: Daisy chain initial error ")
            return
        else:
            if (daisyChainReturn[2] == '0x2') and self.flagSingleAfe:
                self.set_warning_message(self.lineEdit_chainCfg_cfgWarn,
                                         f"Daisy chain has 2 devices, please change AFE radio selection",
                                         "WARNING:")
                return
            elif (daisyChainReturn[2] == '0x1') and (self.flagSingleAfe == False):
                self.set_warning_message(self.lineEdit_chainCfg_cfgWarn,
                                         f"Daisy chain has 1 device, please change AFE radio selection",
                                         "WARNING:")
                return

        # write and read all UIFCFG register
        rtUifCfg = self.afe_write_read_all(0x10, 0x00, 0x26)  # write all A10=0x2600
        if rtUifCfg != "error":
            if self.flagSingleAfe:  # single afe
                rdDataDev0 = (rtUifCfg[1]<<8) | rtUifCfg[0]
                self.update_table_item_data(self.table_chainCfg_uifcfgReg, 0, 3, hex(rdDataDev0)[2:])

                bitsDev0 = (rdDataDev0>>7) & 0x1FF
                for i in range(9):
                    bitValue = (bitsDev0>>i) & 1
                    self.update_table_item_data(self.table_chainCfg_uifcfgReg, 0, 12-i, str(bitValue))
            else:   # dual afe
                rdDataDev0 = (rtUifCfg[3] << 8) | rtUifCfg[2]
                rdDataDev1 = (rtUifCfg[1] << 8) | rtUifCfg[0]
                self.update_table_item_data(self.table_chainCfg_uifcfgReg, 0, 3,
                                            hex(rdDataDev0)[2:])  # device 0
                self.update_table_item_data(self.table_chainCfg_uifcfgReg, 1, 3,
                                            hex(rdDataDev1)[2:])  # device 1

                bitsDev0 = (rdDataDev0 >> 7) & 0x1FF
                bitsDev1 = (rdDataDev1 >> 7) & 0x1FF
                for i in range(9):
                    bitValueDev0 = (bitsDev0 >> i) & 1
                    self.update_table_item_data(self.table_chainCfg_uifcfgReg, 0, 12-i, str(bitValueDev0)) # device 0
                    bitValueDev1 = (bitsDev1 >> i) & 1
                    self.update_table_item_data(self.table_chainCfg_uifcfgReg, 1, 12-i, str(bitValueDev1)) # device 1
        else:
            return

        # write and read all ADDRCFG register
        rtAddrCfg = self.afe_write_read_all(0x11, 0x20, 0x00)   # write all A11=0x0020
                                                                # (topDevAddr = 1, botDevAddr = 0)
                                                                # alseed=0x00
        if rtAddrCfg != "error":
            if self.flagSingleAfe:  # single afe
                rdDataDev0 = (rtAddrCfg[1] << 8) | rtAddrCfg[0]
                unlockBitDev0 = rdDataDev0 >> 15
                botAddrDev0 = (rdDataDev0 & 0x7C00) >> 10
                topAddrDev0 = (rdDataDev0 & 0x03E0) >> 5
                devAddrDev0 = rdDataDev0 & 0x001F
                listDataDev0 = [hex(rdDataDev0)[2:].zfill(4), hex(unlockBitDev0)[2:],
                                hex(botAddrDev0)[2:].zfill(2),
                                hex(topAddrDev0)[2:].zfill(2), hex(devAddrDev0)[2:].zfill(2)]
                for i in range(3, 8):
                    self.update_table_item_data(self.table_chainCfg_addcfgReg, 0, i,
                                                listDataDev0[i - 3])  # device 0
            else:  # dual afe
                rdDataDev0 = (rtAddrCfg[3] << 8) | rtAddrCfg[2]
                rdDataDev1 = (rtAddrCfg[1] << 8) | rtAddrCfg[0]
                unlockBitDev0 = rdDataDev0 >> 15
                unlockBitDev1 = rdDataDev1 >> 15
                botAddrDev0 = (rdDataDev0 & 0x7C00) >> 10
                botAddrDev1 = (rdDataDev1 & 0x7C00) >> 10
                topAddrDev0 = (rdDataDev0 & 0x03E0) >> 5
                topAddrDev1 = (rdDataDev1 & 0x03E0) >> 5
                devAddrDev0 = rdDataDev0 & 0x001F
                devAddrDev1 = rdDataDev1 & 0x001F
                listDataDev0 = [hex(rdDataDev0)[2:].zfill(4), hex(unlockBitDev0)[2:],
                                hex(botAddrDev0)[2:].zfill(2),
                                hex(topAddrDev0)[2:].zfill(2), hex(devAddrDev0)[2:].zfill(2)]
                listDataDev1 = [hex(rdDataDev1)[2:].zfill(4), hex(unlockBitDev1)[2:],
                                hex(botAddrDev1)[2:].zfill(2),
                                hex(topAddrDev1)[2:].zfill(2), hex(devAddrDev1)[2:].zfill(2)]
                for i in range(3, 8):
                    self.update_table_item_data(self.table_chainCfg_addcfgReg, 0, i,
                                                listDataDev0[i - 3])  # device 0
                    self.update_table_item_data(self.table_chainCfg_addcfgReg, 1, i,
                                                listDataDev1[i - 3])  # device 1
        else:
            return

        #wait 10ms to complete FEMA2 BIST
        time.sleep(0.01)

        # read device 0 id block
        rtIdBlkDev0 = pb01_read_block(self.hidBdg, 4, 0, 0x00, 0x00)  # read dev0 id block, alseed=0x00
        devid0 =  (rtIdBlkDev0[4] << 8) | rtIdBlkDev0[3]
        devid1 =  (rtIdBlkDev0[6] << 8) | rtIdBlkDev0[5]
        devid2 =  (rtIdBlkDev0[8] << 8) | rtIdBlkDev0[7]
        version = (rtIdBlkDev0[10] << 8) | rtIdBlkDev0[9]
        generation = (version & 0xE000) >> 13
        chCnt = (version & 0x1F00) >> 8
        swVer = (version & 0x00F0) >> 4
        hwVer = version & 0x000F
        listIdDev0 = [hex(devid0)[2:].zfill(4), hex(devid1)[2:].zfill(4),
                      hex(devid2)[2:].zfill(4), hex(version)[2:].zfill(4),
                      str(generation), str(chCnt),
                      hex(swVer)[2:], hex(hwVer)[2:]]
        for i in range(3, 11):
            self.update_table_item_data(self.table_chainCfg_devIdBlk, 0, i,
                                        listIdDev0[i - 3])  # device 0

        # read device 1 id block
        if self.flagSingleAfe == False:
            rtIdBlkDev1 = pb01_read_block(self.hidBdg, 4, 1, 0x00, 0x00)  # read dev1 id block, alseed=0x00
            devid0 = (rtIdBlkDev1[4] << 8) | rtIdBlkDev1[3]
            devid1 = (rtIdBlkDev1[6] << 8) | rtIdBlkDev1[5]
            devid2 = (rtIdBlkDev1[8] << 8) | rtIdBlkDev1[7]
            version = (rtIdBlkDev1[10] << 8) | rtIdBlkDev1[9]
            generation = (version & 0xE000) >> 13
            chCnt = (version & 0x1F00) >> 8
            swVer = (version & 0x00F0) >> 4
            hwVer = version & 0x000F
            listIdDev1 = [hex(devid0)[2:].zfill(4), hex(devid1)[2:].zfill(4),
                          hex(devid2)[2:].zfill(4), hex(version)[2:].zfill(4),
                          str(generation), str(chCnt),
                          hex(swVer)[2:], hex(hwVer)[2:]]
            for i in range(3, 11):
                self.update_table_item_data(self.table_chainCfg_devIdBlk, 1, i,
                                            listIdDev1[i - 3])  # device 0

        # read device 0 status block
        rtStaBlkDev0 = pb01_read_block(self.hidBdg, 4, 0, 0x04, 0x00)  # read dev0 id block, alseed=0x00
        status1Dev0 = (rtStaBlkDev0[4] << 8) | rtStaBlkDev0[3]
        status2Dev0 = (rtStaBlkDev0[6] << 8) | rtStaBlkDev0[5]
        fmea1Dev0 = (rtStaBlkDev0[8] << 8) | rtStaBlkDev0[7]
        fmea2Dev0 = (rtStaBlkDev0[10] << 8) | rtStaBlkDev0[9]
        listStaDev0 = [hex(status1Dev0)[2:].zfill(4), hex(status2Dev0)[2:].zfill(4),
                       hex(fmea1Dev0)[2:].zfill(4), hex(fmea2Dev0)[2:].zfill(4)]
        # fill chainCfgPage table
        for r in range(4):  # fill table
            self.update_table_item_data(self.table_chainCfg_pw, r+1, 3,
                                        listStaDev0[r])  # device 0
        # update led
        self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, self.ledChainPageDev0)

        if (status1Dev0 != 0x5000) or (status2Dev0 != 0x0080) or (fmea1Dev0 != 0x0000) or (fmea2Dev0 != 0x0000):
            self.set_warning_message(self.lineEdit_chainCfg_pwrUpWarn, "Dev0 STATUS block abnormal", "WARNING:")
            return
        # fill devMgPage table
        for r in range(4):  # fill table
            self.update_table_item_data(self.table_devMgPage_init, r+1, 2,
                                        listStaDev0[r])  # device 0
            self.update_table_item_data(self.table_devMgPage_cur, r + 1, 2,
                                        listStaDev0[r])  # device 0
        # update led
        self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, self.ledDevMgPageInitDev0)
        self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, self.ledDevMgPageCurDev0)


        # read device 1 status block
        if self.flagSingleAfe == False:
            rtStaBlkDev1 = pb01_read_block(self.hidBdg, 4, 1, 0x04, 0x00)  # read dev0 id block, alseed=0x00
            status1Dev1 = (rtStaBlkDev1[4] << 8) | rtStaBlkDev1[3]
            status2Dev1 = (rtStaBlkDev1[6] << 8) | rtStaBlkDev1[5]
            fmea1Dev1 = (rtStaBlkDev1[8] << 8) | rtStaBlkDev1[7]
            fmea2Dev1 = (rtStaBlkDev1[10] << 8) | rtStaBlkDev1[9]
            listStaDev1 = [hex(status1Dev1)[2:].zfill(4), hex(status2Dev1)[2:].zfill(4),
                           hex(fmea1Dev1)[2:].zfill(4), hex(fmea2Dev1)[2:].zfill(4)]
            # fill chainCfgPage table
            for r in range(4):
                self.update_table_item_data(self.table_chainCfg_pw, r + 1, 5,
                                            listStaDev1[r])  # device 1
            # update led
            self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1, self.ledChainPageDev1)

            if (status1Dev1 != 0x5000) or (status2Dev1 != 0x0080) or (fmea1Dev1 != 0x0000) or (fmea2Dev1 != 0x0000):
                self.set_warning_message(self.lineEdit_chainCfg_pwrUpWarn, "Dev1 STATUS block abnormal", "WARNING:")
                return
            # fill devMgPage table
            for r in range(4):  # fill table
                self.update_table_item_data(self.table_devMgPage_init, r + 1, 7,
                                            listStaDev1[r])  # device 1
                self.update_table_item_data(self.table_devMgPage_cur, r + 1, 7,
                                            listStaDev1[r])  # device 1
            # update led
            self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1, self.ledDevMgPageInitDev1)
            self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1, self.ledDevMgPageCurDev1)

        # re-setup chainCfgPage cfgWarn bar
        self.set_default_warn_bar(self.lineEdit_chainCfg_cfgWarn)
        self.set_default_warn_bar(self.lineEdit_chainCfg_pwrUpWarn)

        # disable configure button
        current_style = self.pushButton_chainCfg_cfg.styleSheet()
        new_style = current_style + " QPushButton {background-color: #d0d0d0;}"    # 原来颜色是 #3072B3
        self.pushButton_chainCfg_cfg.setStyleSheet(new_style)
        self.pushButton_chainCfg_cfg.setDisabled(True)
        # enable reset button
        current_style = self.pushButton_chainCfg_reset.styleSheet()
        new_style = current_style + " QPushButton {background-color: #e84d00;}"
        self.pushButton_chainCfg_reset.setStyleSheet(new_style)
        self.pushButton_chainCfg_reset.setDisabled(False)

    def slot_pushBtn_chainCfg_reset(self):
        # force por
        pb01_por(self.hidBdg)

        # re-initial ui
        self.init_tab_pages()

        # reset max17841
        max17841_init(self.hidBdg)

        # delay 1s before enable configure button
        time.sleep(1)

        # enable configure button
        current_style = self.pushButton_chainCfg_cfg.styleSheet()
        new_style = current_style + " QPushButton {background-color: #3072B3;}"
        self.pushButton_chainCfg_cfg.setStyleSheet(new_style)
        self.pushButton_chainCfg_cfg.setDisabled(False)
        # disable reset button
        current_style = self.pushButton_chainCfg_reset.styleSheet()
        new_style = current_style + " QPushButton {background-color: #d0d0d0;}"
        self.pushButton_chainCfg_reset.setStyleSheet(new_style)
        self.pushButton_chainCfg_reset.setDisabled(True)


    def slot_pushBtn_devMgPage_init(self):
        # clear status2 expected alerts
        wrAllReturn = pb01_write_all(self.hidBdg, 0x05, 0x80, 0x00, 0x00)   # write all Reg05 = 0x0080, alseed=0x00
        if (wrAllReturn == ("message return RX error" or "pec check error" )):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, wrAllReturn,
                                     "WARNING: clear status register ")
            return

        # clear status1 expected alerts
        wrAllReturn = pb01_write_all(self.hidBdg, 0x04, 0x00, 0x40, 0x00)  # write all Reg05 = 0x4000, alseed=0x00
        if (wrAllReturn == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, wrAllReturn,
                                     "WARNING: clear status register ")
            return

        # delay before read status block back
        time.sleep(0.01)

        # read device 0 status block
        rtStaBlkDev0 = pb01_read_block(self.hidBdg, 7, 0, 0x04, 0x00)  # read dev0 id block, alseed=0x00
        status1Dev0 = (rtStaBlkDev0[4] << 8) | rtStaBlkDev0[3]
        status2Dev0 = (rtStaBlkDev0[6] << 8) | rtStaBlkDev0[5]
        fmea1Dev0 = (rtStaBlkDev0[8] << 8) | rtStaBlkDev0[7]
        fmea2Dev0 = (rtStaBlkDev0[10] << 8) | rtStaBlkDev0[9]
        temp1Dev0 = (rtStaBlkDev0[12] << 8) | rtStaBlkDev0[11]
        temp2Dev0 = (rtStaBlkDev0[14] << 8) | rtStaBlkDev0[13]
        gpioDataDev0 = (rtStaBlkDev0[16] << 8) | rtStaBlkDev0[15]
        listStaDev0 = [hex(status1Dev0)[2:].zfill(4), hex(status2Dev0)[2:].zfill(4),
                       hex(fmea1Dev0)[2:].zfill(4), hex(fmea2Dev0)[2:].zfill(4)]
        listTemGpDev0 = [hex(temp1Dev0)[2:].zfill(4), hex(temp2Dev0)[2:].zfill(4),
                       hex(gpioDataDev0)[2:].zfill(4)]

        # fill devMgPage table
        for r in range(4):  # fill table
            self.update_table_item_data(self.table_devMgPage_init, r + 1, 2,
                                        listStaDev0[r])  # device 0
            self.update_table_item_data(self.table_devMgPage_cur, r + 1, 2,
                                        listStaDev0[r])  # device 0
        for r in range(5, 8):
            self.update_table_item_data(self.table_devMgPage_cur, r, 2,
                                        listTemGpDev0[r-5])  # device 0

        # update led
        self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, self.ledDevMgPageInitDev0)
        self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, self.ledDevMgPageCurDev0)

        if (status1Dev0 != 0x0000) or (status2Dev0 != 0x0000) or (fmea1Dev0 != 0x0000) or (fmea2Dev0 != 0x0000):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, "Dev0 STATUS block abnormal", "WARNING:")
            return

        # read device 1 status block
        if self.flagSingleAfe == False:
            rtStaBlkDev1 = pb01_read_block(self.hidBdg, 7, 1, 0x04, 0x00)  # read dev0 id block, alseed=0x00
            status1Dev1 = (rtStaBlkDev1[4] << 8) | rtStaBlkDev1[3]
            status2Dev1 = (rtStaBlkDev1[6] << 8) | rtStaBlkDev1[5]
            fmea1Dev1 = (rtStaBlkDev1[8] << 8) | rtStaBlkDev1[7]
            fmea2Dev1 = (rtStaBlkDev1[10] << 8) | rtStaBlkDev1[9]
            temp1Dev1 = (rtStaBlkDev0[12] << 8) | rtStaBlkDev0[11]
            temp2Dev1 = (rtStaBlkDev0[14] << 8) | rtStaBlkDev0[13]
            gpioDataDev1 = (rtStaBlkDev0[16] << 8) | rtStaBlkDev0[15]
            listStaDev1 = [hex(status1Dev1)[2:].zfill(4), hex(status2Dev1)[2:].zfill(4),
                           hex(fmea1Dev1)[2:].zfill(4), hex(fmea2Dev1)[2:].zfill(4)]
            listTemGpDev1 = [hex(temp1Dev1)[2:].zfill(4), hex(temp2Dev1)[2:].zfill(4),
                             hex(gpioDataDev1)[2:].zfill(4)]

            # fill devMgPage table
            for r in range(4):  # fill table
                self.update_table_item_data(self.table_devMgPage_init, r + 1, 7,
                                            listStaDev1[r])  # device 1
                self.update_table_item_data(self.table_devMgPage_cur, r + 1, 7,
                                            listStaDev1[r])  # device 1
            for r in range(5, 8):
                self.update_table_item_data(self.table_devMgPage_cur, r, 7,
                                            listTemGpDev1[r - 5])  # device 1

            # update led
            self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1, self.ledDevMgPageInitDev1)
            self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1, self.ledDevMgPageCurDev1)

            if (status1Dev1 != 0x0000) or (status2Dev1 != 0x0000) or (fmea1Dev1 != 0x0000) or (fmea2Dev1 != 0x0000):
                self.set_warning_message(self.lineEdit_devMgPage_initWarn, "Dev1 STATUS block abnormal", "WARNING:")
                return

        # re-setup chainCfgPage cfgWarn bar
        self.set_default_warn_bar(self.lineEdit_devMgPage_initWarn)

        # disable initial button
        current_style = self.pushButton_devMgPage_init.styleSheet()
        new_style = current_style + " QPushButton {background-color: #d0d0d0;}"  # 原来颜色是 #3072B3
        self.pushButton_devMgPage_init.setStyleSheet(new_style)
        self.pushButton_devMgPage_init.setDisabled(True)
        # enable re-initial button
        current_style = self.pushButton_devMgPage_reInit.styleSheet()
        new_style = current_style + " QPushButton {background-color: #ED7D31;}"
        self.pushButton_devMgPage_reInit.setStyleSheet(new_style)
        self.pushButton_devMgPage_reInit.setDisabled(False)
        # enable clear comm button
        current_style = self.pushButton_devMgPage_clear.styleSheet()
        new_style = current_style + " QPushButton {background-color: #FFC000;}"
        self.pushButton_devMgPage_clear.setStyleSheet(new_style)
        self.pushButton_devMgPage_clear.setDisabled(False)


    def slot_pushBtn_devMgPage_reinit(self):
        # clear fmea2 expected alerts
        wrAllReturn = pb01_write_all(self.hidBdg, 0x07, 0x04, 0x00, 0x00)  # write all Reg07 = 0x0004, alseed=0x00
        if (wrAllReturn == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, wrAllReturn,
                                     "WARNING: clear fmea2 ")
            return

        # clear fmea1 expected alerts
        wrAllReturn = pb01_write_all(self.hidBdg, 0x06, 0xFF, 0x87, 0x00)  # write all Reg06 = 0x87FF, alseed=0x00
        if (wrAllReturn == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, wrAllReturn,
                                     "WARNING: clear fmea1 ")
            return

        # clear status2 expected alerts
        wrAllReturn = pb01_write_all(self.hidBdg, 0x05, 0x8F, 0xFF, 0x00)  # write all Reg05 = 0xFF8F, alseed=0x00
        if (wrAllReturn == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, wrAllReturn,
                                     "WARNING: clear status2 ")
            return

        # clear status1 expected alerts
        wrAllReturn = pb01_write_all(self.hidBdg, 0x04, 0x00, 0x20, 0x00)  # write all Reg04 = 0x2000, alseed=0x00
        if (wrAllReturn == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, wrAllReturn,
                                     "WARNING: clear status1 ")
            return

        # clear status1 expected alerts
        wrAllReturn = pb01_write_all(self.hidBdg, 0x04, 0x00, 0x40, 0x00)  # write all Reg04 = 0x4000, alseed=0x00
        if (wrAllReturn == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, wrAllReturn,
                                     "WARNING: clear status1 ")
            return

        # delay before read status block back
        time.sleep(0.01)

        # read device 0 status block
        rtStaBlkDev0 = pb01_read_block(self.hidBdg, 7, 0, 0x04, 0x00)  # read dev0 id block, alseed=0x00
        status1Dev0 = (rtStaBlkDev0[4] << 8) | rtStaBlkDev0[3]
        status2Dev0 = (rtStaBlkDev0[6] << 8) | rtStaBlkDev0[5]
        fmea1Dev0 = (rtStaBlkDev0[8] << 8) | rtStaBlkDev0[7]
        fmea2Dev0 = (rtStaBlkDev0[10] << 8) | rtStaBlkDev0[9]
        temp1Dev0 = (rtStaBlkDev0[12] << 8) | rtStaBlkDev0[11]
        temp2Dev0 = (rtStaBlkDev0[14] << 8) | rtStaBlkDev0[13]
        gpioDataDev0 = (rtStaBlkDev0[16] << 8) | rtStaBlkDev0[15]
        listStaDev0 = [hex(status1Dev0)[2:].zfill(4), hex(status2Dev0)[2:].zfill(4),
                       hex(fmea1Dev0)[2:].zfill(4), hex(fmea2Dev0)[2:].zfill(4)]
        listTemGpDev0 = [hex(temp1Dev0)[2:].zfill(4), hex(temp2Dev0)[2:].zfill(4),
                         hex(gpioDataDev0)[2:].zfill(4)]

        # fill devMgPage table
        for r in range(4):  # fill table
            self.update_table_item_data(self.table_devMgPage_init, r + 1, 2,
                                        listStaDev0[r])  # device 0
            self.update_table_item_data(self.table_devMgPage_cur, r + 1, 2,
                                        listStaDev0[r])  # device 0
        for r in range(5, 8):
            self.update_table_item_data(self.table_devMgPage_cur, r, 2,
                                        listTemGpDev0[r - 5])  # device 0

        # update led
        self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, self.ledDevMgPageInitDev0)
        self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, self.ledDevMgPageCurDev0)

        if (status1Dev0 != 0x0000) or (status2Dev0 != 0x0000) or (fmea1Dev0 != 0x0000) or (fmea2Dev0 != 0x0000):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, "Dev0 STATUS block abnormal", "WARNING:")
            return

        # read device 1 status block
        if self.flagSingleAfe == False:
            rtStaBlkDev1 = pb01_read_block(self.hidBdg, 7, 1, 0x04, 0x00)  # read dev0 id block, alseed=0x00
            status1Dev1 = (rtStaBlkDev1[4] << 8) | rtStaBlkDev1[3]
            status2Dev1 = (rtStaBlkDev1[6] << 8) | rtStaBlkDev1[5]
            fmea1Dev1 = (rtStaBlkDev1[8] << 8) | rtStaBlkDev1[7]
            fmea2Dev1 = (rtStaBlkDev1[10] << 8) | rtStaBlkDev1[9]
            temp1Dev1 = (rtStaBlkDev0[12] << 8) | rtStaBlkDev0[11]
            temp2Dev1 = (rtStaBlkDev0[14] << 8) | rtStaBlkDev0[13]
            gpioDataDev1 = (rtStaBlkDev0[16] << 8) | rtStaBlkDev0[15]
            listStaDev1 = [hex(status1Dev1)[2:].zfill(4), hex(status2Dev1)[2:].zfill(4),
                           hex(fmea1Dev1)[2:].zfill(4), hex(fmea2Dev1)[2:].zfill(4)]
            listTemGpDev1 = [hex(temp1Dev1)[2:].zfill(4), hex(temp2Dev1)[2:].zfill(4),
                             hex(gpioDataDev1)[2:].zfill(4)]

            # fill devMgPage table
            for r in range(4):  # fill table
                self.update_table_item_data(self.table_devMgPage_init, r + 1, 7,
                                            listStaDev1[r])  # device 1
                self.update_table_item_data(self.table_devMgPage_cur, r + 1, 7,
                                            listStaDev1[r])  # device 1
            for r in range(5, 8):
                self.update_table_item_data(self.table_devMgPage_cur, r, 7,
                                            listTemGpDev1[r - 5])  # device 1

            # update led
            self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1,
                                            self.ledDevMgPageInitDev1)
            self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1,
                                            self.ledDevMgPageCurDev1)

            if (status1Dev1 != 0x0000) or (status2Dev1 != 0x0000) or (fmea1Dev1 != 0x0000) or (fmea2Dev1 != 0x0000):
                self.set_warning_message(self.lineEdit_devMgPage_initWarn, "Dev1 STATUS block abnormal", "WARNING:")
                return

        # re-setup chainCfgPage cfgWarn bar
        self.set_default_warn_bar(self.lineEdit_devMgPage_initWarn)


    def slot_pushBtn_devMgPage_clear(self):
        # clear status2 expected alerts
        wrAllReturn = pb01_write_all(self.hidBdg, 0x05, 0x8F, 0xFF, 0x00)  # write all Reg05 = 0xFF8F, alseed=0x00
        if (wrAllReturn == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, wrAllReturn,
                                     "WARNING: clear status2 ")
            return

        # clear status1 expected alerts
        wrAllReturn = pb01_write_all(self.hidBdg, 0x04, 0x00, 0x20, 0x00)  # write all Reg04 = 0x2000, alseed=0x00
        if (wrAllReturn == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, wrAllReturn,
                                     "WARNING: clear status1 ")
            return

        # delay before read status block back
        time.sleep(0.01)

        # read device 0 status block
        rtStaBlkDev0 = pb01_read_block(self.hidBdg, 7, 0, 0x04, 0x00)  # read dev0 id block, alseed=0x00
        status1Dev0 = (rtStaBlkDev0[4] << 8) | rtStaBlkDev0[3]
        status2Dev0 = (rtStaBlkDev0[6] << 8) | rtStaBlkDev0[5]
        fmea1Dev0 = (rtStaBlkDev0[8] << 8) | rtStaBlkDev0[7]
        fmea2Dev0 = (rtStaBlkDev0[10] << 8) | rtStaBlkDev0[9]
        temp1Dev0 = (rtStaBlkDev0[12] << 8) | rtStaBlkDev0[11]
        temp2Dev0 = (rtStaBlkDev0[14] << 8) | rtStaBlkDev0[13]
        gpioDataDev0 = (rtStaBlkDev0[16] << 8) | rtStaBlkDev0[15]
        listStaDev0 = [hex(status1Dev0)[2:].zfill(4), hex(status2Dev0)[2:].zfill(4),
                       hex(fmea1Dev0)[2:].zfill(4), hex(fmea2Dev0)[2:].zfill(4)]
        listTemGpDev0 = [hex(temp1Dev0)[2:].zfill(4), hex(temp2Dev0)[2:].zfill(4),
                         hex(gpioDataDev0)[2:].zfill(4)]

        # fill devMgPage table
        for r in range(4):  # fill table
            self.update_table_item_data(self.table_devMgPage_cur, r + 1, 2,
                                        listStaDev0[r])  # device 0
        for r in range(5, 8):
            self.update_table_item_data(self.table_devMgPage_cur, r, 2,
                                        listTemGpDev0[r - 5])  # device 0

        # update led
        self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, self.ledDevMgPageCurDev0)

        if (status1Dev0 != 0x0000) or (status2Dev0 != 0x0000) or (fmea1Dev0 != 0x0000) or (fmea2Dev0 != 0x0000):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, "Dev0 STATUS block abnormal", "WARNING:")
            return

        # read device 1 status block
        if self.flagSingleAfe == False:
            rtStaBlkDev1 = pb01_read_block(self.hidBdg, 7, 1, 0x04, 0x00)  # read dev0 id block, alseed=0x00
            status1Dev1 = (rtStaBlkDev1[4] << 8) | rtStaBlkDev1[3]
            status2Dev1 = (rtStaBlkDev1[6] << 8) | rtStaBlkDev1[5]
            fmea1Dev1 = (rtStaBlkDev1[8] << 8) | rtStaBlkDev1[7]
            fmea2Dev1 = (rtStaBlkDev1[10] << 8) | rtStaBlkDev1[9]
            temp1Dev1 = (rtStaBlkDev0[12] << 8) | rtStaBlkDev0[11]
            temp2Dev1 = (rtStaBlkDev0[14] << 8) | rtStaBlkDev0[13]
            gpioDataDev1 = (rtStaBlkDev0[16] << 8) | rtStaBlkDev0[15]
            listStaDev1 = [hex(status1Dev1)[2:].zfill(4), hex(status2Dev1)[2:].zfill(4),
                           hex(fmea1Dev1)[2:].zfill(4), hex(fmea2Dev1)[2:].zfill(4)]
            listTemGpDev1 = [hex(temp1Dev1)[2:].zfill(4), hex(temp2Dev1)[2:].zfill(4),
                             hex(gpioDataDev1)[2:].zfill(4)]

            # fill devMgPage table
            for r in range(4):  # fill table
                self.update_table_item_data(self.table_devMgPage_cur, r + 1, 7,
                                            listStaDev1[r])  # device 1
            for r in range(5, 8):
                self.update_table_item_data(self.table_devMgPage_cur, r, 7,
                                            listTemGpDev1[r - 5])  # device 1

            # update led
            self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1,
                                            self.ledDevMgPageCurDev1)

            if (status1Dev1 != 0x0000) or (status2Dev1 != 0x0000) or (fmea1Dev1 != 0x0000) or (fmea2Dev1 != 0x0000):
                self.set_warning_message(self.lineEdit_devMgPage_initWarn, "Dev1 STATUS block abnormal", "WARNING:")
                return

        # re-setup chainCfgPage cfgWarn bar
        self.set_default_warn_bar(self.lineEdit_devMgPage_initWarn)


    def slot_pushBtn_devMgPage_readBack(self):
        # read device 0 status block
        rtStaBlkDev0 = pb01_read_block(self.hidBdg, 7, 0, 0x04, 0x00)  # read dev0 id block, alseed=0x00
        status1Dev0 = (rtStaBlkDev0[4] << 8) | rtStaBlkDev0[3]
        status2Dev0 = (rtStaBlkDev0[6] << 8) | rtStaBlkDev0[5]
        fmea1Dev0 = (rtStaBlkDev0[8] << 8) | rtStaBlkDev0[7]
        fmea2Dev0 = (rtStaBlkDev0[10] << 8) | rtStaBlkDev0[9]
        temp1Dev0 = (rtStaBlkDev0[12] << 8) | rtStaBlkDev0[11]
        temp2Dev0 = (rtStaBlkDev0[14] << 8) | rtStaBlkDev0[13]
        gpioDataDev0 = (rtStaBlkDev0[16] << 8) | rtStaBlkDev0[15]
        dcDev0 = rtStaBlkDev0[17]
        listStaDev0 = [hex(status1Dev0)[2:].zfill(4), hex(status2Dev0)[2:].zfill(4),
                       hex(fmea1Dev0)[2:].zfill(4), hex(fmea2Dev0)[2:].zfill(4)]
        listTemGpDev0 = [hex(temp1Dev0)[2:].zfill(4), hex(temp2Dev0)[2:].zfill(4),
                         hex(gpioDataDev0)[2:].zfill(4)]

        # fill dc table
        self.update_table_item_data(self.table_devMgPage_dc, 0, 1,
                                    hex(dcDev0)[2:].zfill(2))  # dc byte
        # update dc byte led
        if self.update_dc_led(dcDev0, self.ledDevMgPageDcByte):
            pass
        else:
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, "DC byte has alert",
                                     "WARNING: ")
            # send alertpacket command
            alertPkReturn = pb01_alert_packet(self.hidBdg)
            if (alertPkReturn == ("message return RX error" or "pec check error")):
                self.set_warning_message(self.lineEdit_devMgPage_initWarn, alertPkReturn,
                                         "WARNING: ALERTPACKET ")
                return
            else:
                alertPkData = (alertPkReturn[6] << 40) | (alertPkReturn[5] << 32) | (alertPkReturn[4] << 24) \
                            | (alertPkReturn[3] << 16) | (alertPkReturn[2] << 8) | alertPkReturn[1]
                # fill alert packet data in dc table
                self.update_table_item_data(self.table_devMgPage_dc, 1, 1,
                                            hex(alertPkData)[2:].zfill(48))    # alert packet data
                # update alert packet led
                self.update_alertPk_led(alertPkData, self.ledDevMgPageAlertPk)

        # fill devMgPage current table
        for r in range(4):  # fill table
            self.update_table_item_data(self.table_devMgPage_cur, r + 1, 2,
                                        listStaDev0[r])  # device 0
        for r in range(5, 8):
            self.update_table_item_data(self.table_devMgPage_cur, r, 2,
                                        listTemGpDev0[r - 5])  # device 0

        # update led
        self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, self.ledDevMgPageCurDev0)

        if (status1Dev0 != 0x0000) or (status2Dev0 != 0x0000) or (fmea1Dev0 != 0x0000) or (fmea2Dev0 != 0x0000):
            self.set_warning_message(self.lineEdit_devMgPage_initWarn, "Dev0 STATUS block abnormal", "WARNING:")
            return

        # read device 1 status block
        if self.flagSingleAfe == False:
            rtStaBlkDev1 = pb01_read_block(self.hidBdg, 7, 1, 0x04, 0x00)  # read dev0 id block, alseed=0x00
            status1Dev1 = (rtStaBlkDev1[4] << 8) | rtStaBlkDev1[3]
            status2Dev1 = (rtStaBlkDev1[6] << 8) | rtStaBlkDev1[5]
            fmea1Dev1 = (rtStaBlkDev1[8] << 8) | rtStaBlkDev1[7]
            fmea2Dev1 = (rtStaBlkDev1[10] << 8) | rtStaBlkDev1[9]
            temp1Dev1 = (rtStaBlkDev0[12] << 8) | rtStaBlkDev0[11]
            temp2Dev1 = (rtStaBlkDev0[14] << 8) | rtStaBlkDev0[13]
            gpioDataDev1 = (rtStaBlkDev0[16] << 8) | rtStaBlkDev0[15]
            dcDev1 = rtStaBlkDev1[17]
            listStaDev1 = [hex(status1Dev1)[2:].zfill(4), hex(status2Dev1)[2:].zfill(4),
                           hex(fmea1Dev1)[2:].zfill(4), hex(fmea2Dev1)[2:].zfill(4)]
            listTemGpDev1 = [hex(temp1Dev1)[2:].zfill(4), hex(temp2Dev1)[2:].zfill(4),
                             hex(gpioDataDev1)[2:].zfill(4)]

            # fill dc table
            self.update_table_item_data(self.table_devMgPage_dc, 0, 1,
                                        hex(dcDev1)[2:].zfill(2))  # dc byte
            # update dc byte led
            if self.update_dc_led(dcDev1, self.ledDevMgPageDcByte):
                pass
            else:
                self.set_warning_message(self.lineEdit_devMgPage_initWarn, "DC byte has alert",
                                         "WARNING: ")
                # send alertpacket command
                alertPkReturn = pb01_alert_packet(self.hidBdg)
                if (alertPkReturn == ("message return RX error" or "pec check error")):
                    self.set_warning_message(self.lineEdit_devMgPage_initWarn, alertPkReturn,
                                             "WARNING: ALERTPACKET ")
                    return
                else:
                    alertPkData = (alertPkReturn[6] << 40) | (alertPkReturn[5] << 32) | (alertPkReturn[4] << 24) \
                                  | (alertPkReturn[3] << 16) | (alertPkReturn[2] << 8) | alertPkReturn[1]
                    # fill alert packet data in dc table
                    self.update_table_item_data(self.table_devMgPage_dc, 1, 1,
                                                hex(alertPkData)[2:].zfill(48))  # alert packet data
                    # update alert packet led
                    self.update_alertPk_led(alertPkData, self.ledDevMgPageAlertPk)

            # fill devMgPage current table
            for r in range(4):  # fill table
                self.update_table_item_data(self.table_devMgPage_cur, r + 1, 7,
                                            listStaDev1[r])  # device 1
            for r in range(5, 8):
                self.update_table_item_data(self.table_devMgPage_cur, r, 7,
                                            listTemGpDev1[r - 5])  # device 1

            # update led
            self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1,
                                            self.ledDevMgPageCurDev1)

            if (status1Dev1 != 0x0000) or (status2Dev1 != 0x0000) or (fmea1Dev1 != 0x0000) or (fmea2Dev1 != 0x0000):
                self.set_warning_message(self.lineEdit_devMgPage_initWarn, "Dev1 STATUS block abnormal", "WARNING:")
                return



        # re-setup chainCfgPage cfgWarn bar
        self.set_default_warn_bar(self.lineEdit_devMgPage_initWarn)



    def setupNotification(self):
        dbh = DEV_BROADCAST_DEVICEINTERFACE()
        dbh.dbcc_size = ctypes.sizeof(DEV_BROADCAST_DEVICEINTERFACE)
        dbh.dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE
        dbh.dbcc_classguid = GUID_DEVINTERFACE_USB_DEVICE
        self.hNofity = RegisterDeviceNotification(int(self.winId()),
                                                  ctypes.byref(dbh),
                                                  DEVICE_NOTIFY_WINDOW_HANDLE)

    def nativeEvent(self, eventType, msg):
        message = MSG.from_address(msg.__int__())
        if message.message == WM_DEVICECHANGE:
            self.onDeviceChanged(message.wParam, message.lParam)
        return False, 0

    def onDeviceChanged(self, wParam, lParam):
        if DBT_DEVICEARRIVAL == wParam:
            dev_info = ctypes.cast(lParam, ctypes.POINTER(DEV_BROADCAST_DEVICEINTERFACE)).contents
            device_path = ctypes.c_wchar_p(dev_info.dbcc_name).value
            cycCnt = 0
            if f"VID_{target_vid:04X}&PID_{target_pid:04X}" in device_path:
                while (self.open_hid() is not True) and (cycCnt < 5):
                    self.open_hid()
                    cycCnt += 1


        elif DBT_DEVICEREMOVECOMPLETE == wParam:
            dev_info = ctypes.cast(lParam, ctypes.POINTER(DEV_BROADCAST_DEVICEINTERFACE)).contents
            device_path = ctypes.c_wchar_p(dev_info.dbcc_name).value
            if f"VID_{target_vid:04X}&PID_{target_pid:04X}" in device_path:
                self.close_hid()

    def open_hid(self):
        try:
            if self.hidStatus == False:
                self.hidBdg.open(target_vid, target_pid)  # VendorID/ProductID
                self.hidBdg.set_nonblocking(1)
                self.hidStatus = True
                self.statusMessage.setStyleSheet("QLabel { color : blue; }")  # 设置字体颜色为蓝色
                self.statusMessage.setText("bridge board connect successfully")

                # reset max17841
                max17841_init(self.hidBdg)
                return self.hidStatus
            else:
                return self.hidStatus
        except:
            self.hidStatus = False
            self.statusMessage.setStyleSheet("QLabel { color : red; }")  # 设置字体颜色为蓝色
            self.statusMessage.setText("bridge board connect fail")
            return self.hidStatus

    def close_hid(self):
        try:
            if self.hidStatus == True:
                self.hidBdg.close()
                self.hidStatus = False
                self.statusMessage.setStyleSheet("QLabel { color : red; }")  # 设置字体颜色为红色
                self.statusMessage.setText("bridge board removed")
                return self.hidStatus
            else:
                return self.hidStatus
        except:
            self.statusMessage.setStyleSheet("QLabel { color : red; }")  # 设置字体颜色为红色
            self.statusMessage.setText("close hid failed")
            self.hidStatus = True

    def slot_radio_single_dual_afe(self):
        """
        根据 single afe 和 dual afe radio button 被选择的状态，
        设置 QTableWidget 显示不同的行数
        :return:
        """
        if self.radioButton_singleAfe.isChecked():
            self.flagSingleAfe = True
            # chain configuration page (page1)
            self.table_chainCfg_devIdBlk.hideRow(1)
            self.table_chainCfg_uifcfgReg.hideRow(1)
            self.table_chainCfg_addcfgReg.hideRow(1)
            self.table_chainCfg_pw.hideColumn(5)
            self.table_chainCfg_pw.hideColumn(6)
            self.table_chainCfg_rstReg.hideColumn(5)
            self.table_chainCfg_rstReg.hideColumn(6)
            # device manage page (page2)
            self.table_devMgPage_init.hideColumn(7)
            self.table_devMgPage_init.hideColumn(8)
            self.table_devMgPage_init.hideColumn(9)
            self.table_devMgPage_init.hideColumn(10)
            self.table_devMgPage_init.hideColumn(11)
            self.table_devMgPage_cur.hideColumn(7)
            self.table_devMgPage_cur.hideColumn(8)
            self.table_devMgPage_cur.hideColumn(9)
            self.table_devMgPage_cur.hideColumn(10)
            self.table_devMgPage_cur.hideColumn(11)
            # application configuration page (page3)
            self.table_appCfgPage_appCfg.hideColumn(8)
            self.table_appCfgPage_alertCfg.hideColumn(8)
            self.table_appCfgPage_thresholdReg.hideColumn(8)
            self.table_appCfgPage_acqReg.hideColumn(8)
            # diagnostic configuration page (page4)
            self.table_diagCfgPage_testCurCfgReg.hideColumn(12)
            self.table_diagCfgPage_diagThresReg.hideColumn(8)
            self.table_diagCfgPage_aluTestDiagReg.hideColumn(8)
            # acquisition request page (page5）
            self.table_acqReqPage_acqReq.hideRow(1)
            # measure acquisition summary data page (page6)
            self.table_meaAcqSumPage_status.hideColumn(7)
            self.table_meaAcqSumPage_status.hideColumn(8)
            self.table_meaAcqSumPage_status.hideColumn(9)
            self.table_meaAcqSumPage_status.hideColumn(10)
            self.table_meaAcqSumPage_status.hideColumn(11)
            self.frame_meaAcqSumPage_sumDataDev1.hide()
            self.table_meaAcqSumPage_sumDataDev1.hide()
            # measure acquisition detail data page (page7)
            self.frame_meaAcqDetailPage_alertDev1.hide()
            self.table_meaAcqDetailData_alertRegDev1.hide()
            self.frame_meaAcqDetailPage_dataDev1.hide()
            self.table_meaAcqDetailData_dataRegDev1.hide()
            # diagnostic acquisition data page (page8)
            self.table_diagAcqPage_status.hideColumn(7)
            self.table_diagAcqPage_status.hideColumn(8)
            self.table_diagAcqPage_status.hideColumn(9)
            self.table_diagAcqPage_status.hideColumn(10)
            self.table_diagAcqPage_status.hideColumn(11)
            self.frame_diagAcqDataPage_alertDev1.hide()
            self.table_diagAcqPage_alertReg_dev1.hide()
            self.frame_diagAcqDataPage_dataDev1.hide()
            self.table_diagAcqPage_dataReg_dev1.hide()
            # cell balance page (page9)
            self.table_cblPage_cblCfgReg.hideColumn(5)
            self.table_cblPage_cblCtrlSimDemo.hideColumn(5)
            self.table_cblPage_cblCtrlStaInf.hideColumn(9)
            self.table_cblPage_cblCtrlStaInf.hideColumn(10)
            self.table_cblPage_cblCtrlStaInf.hideColumn(11)
            self.table_cblPage_cblCtrlStaInf.hideColumn(12)
            self.table_cblPage_cblCtrlStaInf.hideColumn(13)
            self.table_cblPage_cblCtrlStaInf.hideColumn(14)
            self.table_cblPage_cblCtrlStaInf.hideColumn(15)
        elif self.radioButton_dualAfe.isChecked():
            self.flagSingleAfe = False
            # chain configuration page (page1)
            self.table_chainCfg_devIdBlk.showRow(1)
            self.table_chainCfg_uifcfgReg.showRow(1)
            self.table_chainCfg_addcfgReg.showRow(1)
            self.table_chainCfg_pw.showColumn(5)
            self.table_chainCfg_pw.showColumn(6)
            self.table_chainCfg_rstReg.showColumn(5)
            self.table_chainCfg_rstReg.showColumn(6)
            # device manage page (page2)
            self.table_devMgPage_init.showColumn(7)
            self.table_devMgPage_init.showColumn(8)
            self.table_devMgPage_init.showColumn(9)
            self.table_devMgPage_init.showColumn(10)
            self.table_devMgPage_init.showColumn(11)
            self.table_devMgPage_cur.showColumn(7)
            self.table_devMgPage_cur.showColumn(8)
            self.table_devMgPage_cur.showColumn(9)
            self.table_devMgPage_cur.showColumn(10)
            self.table_devMgPage_cur.showColumn(11)
            # application configuration page (page3)
            self.table_appCfgPage_appCfg.showColumn(8)
            self.table_appCfgPage_alertCfg.showColumn(8)
            self.table_appCfgPage_thresholdReg.showColumn(8)
            self.table_appCfgPage_acqReg.showColumn(8)
            # diagnostic configuration page (page4)
            self.table_diagCfgPage_testCurCfgReg.showColumn(12)
            self.table_diagCfgPage_diagThresReg.showColumn(8)
            self.table_diagCfgPage_aluTestDiagReg.showColumn(8)
            # acquisition request page (page5）
            self.table_acqReqPage_acqReq.showRow(1)
            # measure acquisition summary data page (page6)
            self.table_meaAcqSumPage_status.showColumn(7)
            self.table_meaAcqSumPage_status.showColumn(8)
            self.table_meaAcqSumPage_status.showColumn(9)
            self.table_meaAcqSumPage_status.showColumn(10)
            self.table_meaAcqSumPage_status.showColumn(11)
            self.frame_meaAcqSumPage_sumDataDev1.show()
            self.table_meaAcqSumPage_sumDataDev1.show()
            # measure acquisition detail data page (page7)
            self.frame_meaAcqDetailPage_alertDev1.show()
            self.table_meaAcqDetailData_alertRegDev1.show()
            self.frame_meaAcqDetailPage_dataDev1.show()
            self.table_meaAcqDetailData_dataRegDev1.show()
            # diagnostic acquisition data page (page8)
            self.table_diagAcqPage_status.showColumn(7)
            self.table_diagAcqPage_status.showColumn(8)
            self.table_diagAcqPage_status.showColumn(9)
            self.table_diagAcqPage_status.showColumn(10)
            self.table_diagAcqPage_status.showColumn(11)
            self.frame_diagAcqDataPage_alertDev1.show()
            self.table_diagAcqPage_alertReg_dev1.show()
            self.frame_diagAcqDataPage_dataDev1.show()
            self.table_diagAcqPage_dataReg_dev1.show()
            # cell balance page (page9)
            self.table_cblPage_cblCfgReg.showColumn(5)
            self.table_cblPage_cblCtrlSimDemo.showColumn(5)
            self.table_cblPage_cblCtrlStaInf.showColumn(9)
            self.table_cblPage_cblCtrlStaInf.showColumn(10)
            self.table_cblPage_cblCtrlStaInf.showColumn(11)
            self.table_cblPage_cblCtrlStaInf.showColumn(12)
            self.table_cblPage_cblCtrlStaInf.showColumn(13)
            self.table_cblPage_cblCtrlStaInf.showColumn(14)
            self.table_cblPage_cblCtrlStaInf.showColumn(15)



""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01MainWindow()
    win.show()

    sys.exit(app.exec_())

