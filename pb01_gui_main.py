# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 10:44
# @Author  : yifei.su
# @File    : pb01_gui_main.py

""" step1: 导入必须的库和 layout 文件 """
import sys
import os
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import QColor
import time
from PyQt5.QtWidgets import QFileDialog
import json
import numpy as np

from pb01_gui_main_window import Ui_MainWindow
from pb01_bridge_driver import *
from ui_configure import *
from assist import *


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
        """ self variables """
        self.hidBdg = hid.device()
        self.hidStatus = False
        self.setupNotification()
        """ software correction """
        self.dev0ParList = []
        self.dev1ParList = []
        """ status bar """
        self.statusMessage = QLabel()
        self.statusMessage.setFont(QFont('Calibri', 10, QFont.Bold))  # 设置字体和加粗
        self.statusBar().addPermanentWidget(self.statusMessage)
        ''' chainCfgPage (page1) '''
        self.flagSingleAfe = False  # chainCfgPage single afe radio button flag
        self.flag_radio_acqReqPage_acqcbalint = False  # acqReqPage acqcbalint radio button flag
        self.flag_radio_acqReqPage_acqiirinit = False  # acqReqPage acqiirinit radio button flag
        self.ledChainPageDev0 = []
        self.ledChainPageDev1 = []
        self.ledDevMgPageInitDev0 = []
        self.ledDevMgPageInitDev1 = []
        self.ledDevMgPageCurDev0 = []
        self.ledDevMgPageCurDev1 = []
        self.ledDevMgPageDcByte = []
        self.ledDevMgPageAlertPk = []
        ''' appCfgPage (page3) '''
        self.polCfgValue = 0x0000       # register POLARITYCFG(0x14) value
        self.auxRefCfgVal = 0x0000      # register AUXREFCFG(0x16) value
        ''' acqReqPage (page5) '''
        self.acqCtrlVal = 0x0B41      # acqReqPage ACQCTRL (0x44) register value
        self.acqMode = 0x01           # acqReqPage acquisition mode value (由 radio button 选择设置）
        self.radioGroup_acqReqPage_acqMode = QButtonGroup(self)    # 将 acqReqPage radio 归为一组
        self.acqMode_radio_list = [self.radioButton_acqReqPage_dataUpdate,
                             self.radioButton_acqReqPage_normalMeas, self.radioButton_acqReqPage_redundantMeas,
                             self.radioButton_acqReqPage_pathDiag, self.radioButton_acqReqPage_balswShortDiag,
                             self.radioButton_acqReqPage_balswOpenDiag, self.radioButton_acqReqPage_cellOpenDiag,
                             self.radioButton_acqReqPage_busOpenDiag, self.radioButton_acqReqPage_cellHvmuxDiag,
                             self.radioButton_acqReqPage_busHvmuxDiag, self.radioButton_acqReqPage_auxrDiag,
                             self.radioButton_acqReqPage_auxaDiagA, self.radioButton_acqReqPage_auxaDiagB,
                             self.radioButton_acqReqPage_diagDataClear]
        for i in range(0, 14):
            if i==13:
                self.radioGroup_acqReqPage_acqMode.addButton(self.acqMode_radio_list[i], id = i+1)
            else:
                self.radioGroup_acqReqPage_acqMode.addButton(self.acqMode_radio_list[i], id = i)
        ''' cblPage '''
        self.cblTime = 0x0002       # cblPage CBALTIMECFG (0x46) register value
        self.cblCfgVal = 0x01F0     # cblPage CBALCFG (0x49) register value
        self.cblMode = 0x0          # cblPage cell balance mode value (由 radio button 选择设置）
        self.radioGroup_cblPage_cblMode = QButtonGroup(self)        # 将 cblPage radio 归为一组
        self.cblMode_radio_list = [self.radioButton_cblPage_disable, self.radioButton_cblPage_manEven,
                                   self.radioButton_cblPage_manOdd, self.radioButton_cblPage_semiAuto,
                                   self.radioButton_cblPage_auto, self.radioButton_cblPage_discharge,
                                   self.radioButton_cblPage_autoMeaSnd, self.radioButton_cblPage_autoMeaMin]        
        for i in range(0, 8):
                self.radioGroup_cblPage_cblMode.addButton(self.cblMode_radio_list[i], id=i)

        """ self functions """
        self.open_hid()
        self.init_tab_pages()
        """  配置信号和槽 """
        ''' menu bar '''
        self.actionLoad.triggered.connect(self.slot_menu_load)
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
        ''' application configuration page (page3) '''
        self.pushButton_appCfgPage_appCfgWR.clicked.connect(self.slot_pushBtn_appCfgPage_appCfgWR)
        self.pushButton_appCfgPage_appCfgRd.clicked.connect(self.slot_pushBtn_appCfgPage_appCfgRd)
        self.pushButton_appCfgPage_alertCfgWR.clicked.connect(self.slot_pushBtn_appCfgPage_alertCfgWR)
        self.pushButton_appCfgPage_alertCfgRd.clicked.connect(self.slot_pushBtn_appCfgPage_alertCfgRd)
        self.pushButton_appCfgPage_thresholdRegWR.clicked.connect(self.slot_pushBtn_appCfgPage_thresholdRegWR)
        self.pushButton_appCfgPage_thresholdRegRd.clicked.connect(self.slot_pushBtn_appCfgPage_thresholdRegRd)
        self.pushButton_appCfgPage_acqRegWr.clicked.connect(self.slot_pushBtn_appCfgPage_acqRegWr)
        self.pushButton_appCfgPage_acqRegRd.clicked.connect(self.slot_pushBtn_appCfgPage_acqRegRd)
        self.table_appCfgPage_appCfg.cellChanged.connect(self.slot_table_appCfgPage_appCfg_cellChange)
        self.table_appCfgPage_thresholdReg.cellChanged.connect(self.slot_table_appCfgPage_thReg_cellChange)
        ''' diagnostic configuration page (page4) '''
        self.pushButton_diagCfgPage_curCfgWR.clicked.connect(self.slot_pushBtn_diagCfgPage_curCfgWR)
        self.pushButton_diagCfgPage_curCfgRd.clicked.connect(self.slot_pushBtn_diagCfgPage_curCfgRd)
        self.pushButton_diagCfgPage_diagThWR.clicked.connect(self.slot_pushBtn_diagCfgPage_diagThWR)
        self.pushButton_diagCfgPage_diagThRd.clicked.connect(self.slot_pushBtn_diagCfgPage_diagThRd)
        self.pushButton_diagCfgPage_aluTeWR.clicked.connect(self.slot_pushBtn_diagCfgPage_aluTeWR)
        self.pushButton_diagCfgPage_aluTeRd.clicked.connect(self.slot_pushBtn_diagCfgPage_aluTeRd)
        ''' acquisition request page (page5) '''
        self.radioButton_acqReqPage_acqcbalint.clicked.connect(self.solt_radioBtn_acqReqPage_acqcbalint)
        self.radioButton_acqReqPage_acqiirinit.clicked.connect(self.solt_radioBtn_acqReqPage_acqiirinit)
        self.radioGroup_acqReqPage_acqMode.buttonClicked.connect(self.solt_radioGroup_acqReqPage_acqMode)
        self.pushButton_acqReqPage_request.clicked.connect(self.solt_pushBtn_acqReqPage_request)
        ''' cell balance page (page9) '''
        self.radioGroup_cblPage_cblMode.buttonClicked.connect(self.solt_radioGroup_cblPage_cblMode)
        self.pushButton_cblPage_cblCfgWr.clicked.connect(self.solt_pushBtn_cblPage_cblCfgWr)
        self.pushButton_cblPage_cblCfgRd.clicked.connect(self.solt_pushBtn_cblPage_cblCfgRd)
        self.pushButton_cblPage_cblCtrlStop.clicked.connect(self.solt_pushBtn_cblPage_cblCtrlStop)
        self.pushButton_cblPage_cblCtrlStart.clicked.connect(self.solt_pushBtn_cblPage_cblCtrlStart)
        self.pushButton_cblPage_cblCtrlRd.clicked.connect(self.solt_pushBtn_cblPage_cblCtrlRd)
        self.table_cblPage_cblExpTime.cellChanged.connect(self.solt_table_cblPage_cblExpTime_cellChange)


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

        ''' initial application configuration page (page3) '''
        set_table_head(self.table_appCfgPage_appCfg, table_appCfgPage_appAndAlert_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_appCfgPage_appCfg, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_appCfgReg_items)
        set_table_head(self.table_appCfgPage_alertCfg, table_appCfgPage_appAndAlert_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_appCfgPage_alertCfg, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_alertCfgReg_items)
        set_table_head(self.table_appCfgPage_thresholdReg, table_appCfgPage_thAndAcq_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_appCfgPage_thresholdReg, CHAIN_CFG_TABLE_ROWHG,
                       table_appCfgPage_theresholdReg_items)
        set_table_head(self.table_appCfgPage_acqReg, table_appCfgPage_thAndAcq_headers,
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
        # set default checked status
        self.radioButton_acqReqPage_acqcbalint.setChecked(True)
        self.radioButton_acqReqPage_acqiirinit.setChecked(True)
        self.radioButton_acqReqPage_normalMeas.setChecked(True) 
        # disable some radio buttons
        self.radioButton_acqReqPage_acqiirbyp.setEnabled(False)
        self.radioButton_acqReqPage_acqiirproc.setEnabled(False)
        self.radioButton_acqReqPage_alutesten.setEnabled(False)
        self.radioButton_acqReqPage_dataUpdate.setEnabled(False)
        self.radioButton_acqReqPage_auxaDiagA.setEnabled(False)
        self.radioButton_acqReqPage_auxaDiagB.setEnabled(False)
        set_table_item(self.table_acqReqPage_auxPar, CHAIN_CFG_TABLE_ROWHG,
                       table_acqReqPage_auxPar_items)
        set_table_head(self.table_acqReqPage_acqReq, table_acqReqPage_headers,
                       CHAIN_CFG_TABLE_HEHG, 0)
        set_table_item(self.table_acqReqPage_acqReq, CHAIN_CFG_TABLE_ROWHG,
                       table_acqReqPage_items)

        adjust_acqReqPage_tables(self.table_acqReqPage_osr, self.table_acqReqPage_auxPar, self.table_acqReqPage_acqReq)

        ''' initial measurement acquisition summary data page (page6) '''
        set_table_item(self.table_meaAcqSumPage_dc, CHAIN_CFG_TABLE_ROWHG,
                       table_devMg_dcItems)

        set_table_item(self.table_meaAcqSumPage_status, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqSumDataPage_statusTableItems)

        set_table_item(self.table_meaAcqSumPage_sumDataDev0, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqSumDataPage_sumDataItems)

        set_table_item(self.table_meaAcqSumPage_sumDataDev1, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqSumDataPage_sumDataItems)

        self.ledMeaAcqSumPageDc, self.ledMeaAcqSumPageAlert, \
        self.ledMeaAcqSumPageStaDev0, self.ledMeaAcqSumPageStaDev1 = adjust_meaAcqSumPage_tables(
                                                                        self.table_meaAcqSumPage_dc,
                                                                        self.table_meaAcqSumPage_status,
                                                                        self.table_meaAcqSumPage_sumDataDev0,
                                                                        self.table_meaAcqSumPage_sumDataDev1)

        ''' initial measurement acquisition detailed data page (page7) '''
        set_table_item(self.table_meaAcqDetailData_alertRegDev0, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_alertRegItems)

        set_table_item(self.table_meaAcqDetailData_dataRegDev0, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_dev0_dataRegItems)

        set_table_item(self.table_meaAcqDetailData_alertRegDev1, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_alertRegItems)

        set_table_item(self.table_meaAcqDetailData_dataRegDev1, CHAIN_CFG_TABLE_ROWHG,
                       table_meaAcqDetailPage_dev1_dataRegItems)

        adjust_meaAcqDetailPage_tables(self.table_meaAcqDetailData_alertRegDev0,
                                       self.table_meaAcqDetailData_dataRegDev0,
                                       self.table_meaAcqDetailData_alertRegDev1,
                                       self.table_meaAcqDetailData_dataRegDev1)

        set_meaAcqDetailPage_table_color(self.table_meaAcqDetailData_alertRegDev0,
                                         self.table_meaAcqDetailData_dataRegDev0,
                                         self.table_meaAcqDetailData_alertRegDev1,
                                         self.table_meaAcqDetailData_dataRegDev1)

        self.ledMeaAcqDetailPageDev0, \
        self.ledMeaAcqDetailPageDev1 = meaAcqDetailPage_insert_led(self.table_meaAcqDetailData_alertRegDev0,
                                                              self.table_meaAcqDetailData_alertRegDev1)

        ''' initial diagnostic acquisition data page (page8) '''
        set_table_item(self.table_diagAcqPage_dc, CHAIN_CFG_TABLE_ROWHG, table_devMg_dcItems)

        set_table_item(self.table_diagAcqPage_status, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_statusTableItems)

        set_table_item(self.table_diagAcqPage_alertReg_dev0, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_alertItems)

        set_table_item(self.table_diagAcqPage_dataReg_dev0, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_dev0DataItems)

        set_table_item(self.table_diagAcqPage_alertReg_dev1, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_alertItems)

        set_table_item(self.table_diagAcqPage_dataReg_dev1, CHAIN_CFG_TABLE_ROWHG, table_diagAcqDataPage_dev1DataItems)

        self.ledDiagAcqDataPageDc, self.ledDiagAcqDataPageAlert, \
        self.ledDiagAcqDataPageStaDev0, self.ledDiagAcqDataPageStaDev1, \
        self.ledDiagAcqDataPageDev0, self.ledDiagAcqDataPageDev1 = adjust_diagAcqDataPage_tables(
                                                                    self.table_diagAcqPage_dc,
                                                                    self.table_diagAcqPage_status,
                                                                    self.table_diagAcqPage_alertReg_dev0,
                                                                    self.table_diagAcqPage_dataReg_dev0,
                                                                    self.table_diagAcqPage_alertReg_dev1,
                                                                    self.table_diagAcqPage_dataReg_dev1)

        ''' initial cell balance page (page9) '''
        # set default checked status
        self.radioButton_cblPage_disable.setChecked(True)
        # set disable radio buttons
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

        self.ledCblPageStatusDev0, self.ledCblPageStatusDev1,\
        self.ledCblPageUvStaDev0, self.ledCblPageUvStaDev1 = adjust_cblPage_tables(self.table_cblPage_cblExpTime,
                                                                                   self.table_cblPage_cblCfgReg,
                                                                                   self.table_cblPage_cblCtrlSimDemo,
                                                                                   self.table_cblPage_cblCtrlStaInf)

        ''' dual afe initial ui as default '''
        self.slot_radio_single_dual_afe()

        ''' disable push button '''
        # chainCfg page
        self.pushBtn_disable(self.pushButton_chainCfg_reset)    # reset
        # devMg page
        self.pushBtn_disable(self.pushButton_devMgPage_init)        # initialize
        self.pushBtn_disable(self.pushButton_devMgPage_reInit)      # reinitialize
        self.pushBtn_disable(self.pushButton_devMgPage_clear)       # clear comm
        self.pushBtn_disable(self.pushButton_devMgPage_readBack)    # read back


    def message_box(self, pMessage):
        """
        弹出消息框
        :param pWarning: 消息框要显示的信息
        :return:
        """
        self.hidBdg.close()
        self.hidBdg = None
        time.sleep(0.05)
        self.hidBdg = hid.device()
        self.hidBdg.open(0x1a86, 0xfe07)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)  # 设置消息框图标
        msg.setWindowTitle('Message')  # 设置消息框标题
        msg.setText(pMessage)  # 设置消息框显示信息
        msg.setStandardButtons(QMessageBox.Ok)  # 设置一个标准按钮OK
        msg.exec_()  # 显示消息框


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

    def afe_write_read_all(self, pRegAddr, pData):
        """
        向 daisy-chain 所有 AFE 某个寄存器写入数据，并再读取所有 AFE 该寄存器
        注意：本工程目前只支持 2 个 AFE，通过 AFE radio 选择，所以读取多少个 AFE 在函数实现中用 AFE radio 当前状态来判断
        :param pRegAddr: 要读写的寄存器地址
        :param pData: data
        :return: 返回一个列表，
                 列表中包含从 daisy-chain 读取的所有 AFE 该寄存器的数据，
                 如 [afe0DataLsb, afe0DataMsb, afe1DataLsb, afe1DataMsb]
                 注意 byte0 就是 data, 不是 daisy-chain uart 协议的 command
        """
        # write register
        rtWr = pb01_write_all(self.hidBdg, pRegAddr, pData, 0x00)  # write all, alseed=0x00
        if rtWr == "message return RX error" or rtWr == "pec check error":
            self.message_box(rtWr)
            return False

        # read register
        if self.flagSingleAfe:
            rtRd = pb01_read_all(self.hidBdg, pRegAddr, 1, 0x00)  # read all, alseed=0x00
            if rtRd == "message return RX error" or rtRd == "pec check error":
                self.message_box(rtRd)
                return False
            else:
                return rtRd[2:4]
        else:
            rtRd = pb01_read_all(self.hidBdg, pRegAddr, 2, 0x00)  # read all, alseed=0x00
            if rtRd == "message return RX error" or rtRd == "pec check error":
                self.message_box(rtRd)
                return False
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
            if pDc & (0x80 >> i):  # biti = 1
                pLedList[i].setStyleSheet(led_red_style)
                flag = False
            else:  # biti = 0
                pLedList[i].setStyleSheet(led_white_style)
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
            if pAlertPk & (0x800000000000 >> i):  # biti = 1
                if i == 0:
                    pLedList[i].setStyleSheet(led_green_style)
                else:
                    pLedList[i].setStyleSheet(led_red_style)
                flag = False
            else:  # biti = 0
                pLedList[i].setStyleSheet(led_white_style)
        return flag


    def update_dc_aleter_table(self, pDcTable, pDcByte, pDcLed, pAlertLed):
        """
        完成更新 DC byte table 的动作:
            1. 填写 DC byte 并更新对应的 led
            2. 如果 DC byte 不为 0 则自动发送 ALERTPACKET command
            3. 如果发送 ALERTPACKET command 填写返回的 alert data 并更新对应的 led
        :param pDcTable: 各 tab 页对应的 dc table object
        :param pDcByte: 调用此函数前获得的 DC byte 值
        :param pDcLed: 此 dc table 对应的 dc led (init_tab_pages 函数中有各 tab 页对应的 dc led)
        :param pAlertLed: 此 dc table 对应的 alert led (init_tab_pages 函数中有各 tab 页对应的 alert led)
        :return:
        """
        # fill dc byte into table
        self.update_table_item_data(pDcTable, 0, 1, hex(pDcByte)[2:].upper().zfill(2))

        # fill dc byte led into table
        self.update_dc_led(pDcByte, pDcLed)

        # send alertpacket command
        alertPkReturn = pb01_17841_alert_packet(self.hidBdg)
        if alertPkReturn == "message return RX error" or alertPkReturn == "pec check error":
            self.message_box(alertPkReturn)
            return
        else:
            alertPkData = (alertPkReturn[6] << 40) | (alertPkReturn[5] << 32) | (alertPkReturn[4] << 24) \
                          | (alertPkReturn[3] << 16) | (alertPkReturn[2] << 8) | alertPkReturn[1]
            # fill alert packet data in table
            self.update_table_item_data(pDcTable, 1, 1,
                                        hex(alertPkData)[2:].upper().zfill(12))  # alert packet data
            # update alert packet led
            self.update_alertPk_led(alertPkData, pAlertLed)


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
                if i == 0:
                    pLedList[0][i].setStyleSheet(led_green_style)
                elif i == 13: # CBAL bit
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
                if pFm2 & (0x8000 >> i):  # biti = 1
                    pLedList[3][i].setStyleSheet(led_red_style)
                else:  # biti = 0
                    pLedList[3][i].setStyleSheet(led_white_style)


    def update_acquistion_alert_regiser_led(self, pListAlertBlkData, pListAlertLed):
        """
        更新 meaAcqDetailDataPage alert register table 中 led 状态
        :param pListAlertBlkData: alert register block 各寄存器数据组成的列表
        :param pListAlertLed: alert register block 各寄存器对应的 led 串组成的列表
        :return:
        """
        for regCnt in range(6):
            for bitCnt in range(16):
                if pListAlertBlkData[regCnt] & (0x8000 >> bitCnt):
                    pListAlertLed[regCnt][bitCnt].setStyleSheet(led_red_style)
                else:
                    pListAlertLed[regCnt][bitCnt].setStyleSheet(led_green_style)


    def update_diagnostic_alert_regiser_led(self, pListAlertBlkData, pListAlertLed):
        """
        更新 meaAcqDetailDataPage alert register table 中 led 状态
        :param pListAlertBlkData: alert register block 各寄存器数据组成的列表
        :param pListAlertLed: alert register block 各寄存器对应的 led 串组成的列表
        :return:
        """
        for regCnt in range(2):
            for bitCnt in range(17):
                if pListAlertBlkData[regCnt] & (0x10000 >> bitCnt):
                    pListAlertLed[regCnt][bitCnt].setStyleSheet(led_red_style)
                else:
                    pListAlertLed[regCnt][bitCnt].setStyleSheet(led_green_style)


    def update_status_block_table(self, pTable, pDev0Col, pDev1Col, pDev0LedList, pDev1LedList, pFlagTem):
        """
        这个函数执行 read block command 去读取 PB01 STATUS Block 中 7 个寄存器的值
        因多个 tab 页面有 status table 要去更新，所以用此函数方便代码维护
        是否读取 dev1 的 status block, 在函数内根据 self.flagSingleAfe 自动判读，不需要额外输入参数
        :param pTable: 指定具体哪个页面下的哪个 status table 要被更新
        :param pDev0Col: dev0 读取到的值填入到哪一列
        :param pDev1Col: dev1 读取到的值填入到哪一列
        :param pDev0LedList: 该 table 对应的 dev0 led 列表
        :param pDev1LedList: 该 table 对应的 dev1 led 列表
        :param pFlagTem: 有的 table 没有 temp1, temp2 和 GPIO，通过此值判断是否要填写这 3 行
                         True - 要填写这三行
                         False - 不要填写这三行
        :return: DC byte - DC byte has alert
                 True - all operation run well
                 False - read block fail
        """
        dcDev0 = 0
        dcDev1 = 0
        """ device 0 process """
        ''' read device 0 status block '''
        rtStaBlkDev0 = pb01_read_block(self.hidBdg, 7, 0, 0x04, 0x00)  # read dev0 id block, alseed=0x00
        if (rtStaBlkDev0 == "message return RX error" or rtStaBlkDev0 == "pec check error"):
            self.message_box(rtStaBlkDev0)
            return False
        else:
            status1Dev0 = (rtStaBlkDev0[4] << 8) | rtStaBlkDev0[3]
            status2Dev0 = (rtStaBlkDev0[6] << 8) | rtStaBlkDev0[5]
            fmea1Dev0 = (rtStaBlkDev0[8] << 8) | rtStaBlkDev0[7]
            fmea2Dev0 = (rtStaBlkDev0[10] << 8) | rtStaBlkDev0[9]
            temp1Dev0 = (rtStaBlkDev0[12] << 8) | rtStaBlkDev0[11]
            temp2Dev0 = (rtStaBlkDev0[14] << 8) | rtStaBlkDev0[13]
            gpioDataDev0 = (rtStaBlkDev0[16] << 8) | rtStaBlkDev0[15]
            dcDev0 = rtStaBlkDev0[17]
            listStaDev0 = [hex(status1Dev0)[2:].upper().zfill(4), hex(status2Dev0)[2:].upper().zfill(4),
                           hex(fmea1Dev0)[2:].upper().zfill(4), hex(fmea2Dev0)[2:].upper().zfill(4)]
            listTemGpDev0 = [hex(temp1Dev0)[2:].upper().zfill(4), hex(temp2Dev0)[2:].upper().zfill(4),
                             hex(gpioDataDev0)[2:].upper().zfill(4)]

            temp1CelDev0 = str(round(temp1Dev0 / 8 - 273.15, 2)) + "°C"
            temp2CelDev0 = str(round(temp2Dev0 / 8 - 273.15, 2)) + "°C"
            temp1FhDev0 = str(round((temp1Dev0 /8 - 273.15) * 9 / 5 + 32, 2)) + "°F"
            temp2FhDev0 = str(round((temp2Dev0 /8 - 273.15) * 9 / 5 + 32, 2)) + "°F"

            listTemValDev0 = [[temp1CelDev0, temp1FhDev0], [temp2CelDev0, temp2FhDev0],
                              [hex(rtStaBlkDev0[16])[2:].upper().zfill(2), hex(rtStaBlkDev0[15])[2:].upper().zfill(2)]]

            ''' fill data into dev0 status table '''
            for r in range(4):  # fill table
                self.update_table_item_data(pTable, r + 1, pDev0Col,
                                            listStaDev0[r])  # device 0
            if pFlagTem:
                for r in range(5, 8):
                    self.update_table_item_data(pTable, r, pDev0Col,
                                                listTemGpDev0[r - 5])  # device 0
                    self.update_table_item_data(pTable, r, 3,
                                                listTemValDev0[r - 5][0])  # device 0
                    self.update_table_item_data(pTable, r, 5,
                                                listTemValDev0[r - 5][1])  # device 0

            ''' update dev0 status table led '''
            self.update_status_register_led(status1Dev0, status2Dev0, fmea1Dev0, fmea2Dev0, pDev0LedList)

        """ device 1 process """
        ''' read device 1 status block '''
        if self.flagSingleAfe == False:
            rtStaBlkDev1 = pb01_read_block(self.hidBdg, 7, 1, 0x04, 0x00)  # read dev1 id block, alseed=0x00
            if (rtStaBlkDev1 == "message return RX error" or rtStaBlkDev1 == "pec check error"):
                self.message_box(rtStaBlkDev1)
                return False
            else:
                status1Dev1 = (rtStaBlkDev1[4] << 8) | rtStaBlkDev1[3]
                status2Dev1 = (rtStaBlkDev1[6] << 8) | rtStaBlkDev1[5]
                fmea1Dev1 = (rtStaBlkDev1[8] << 8) | rtStaBlkDev1[7]
                fmea2Dev1 = (rtStaBlkDev1[10] << 8) | rtStaBlkDev1[9]
                temp1Dev1 = (rtStaBlkDev1[12] << 8) | rtStaBlkDev1[11]
                temp2Dev1 = (rtStaBlkDev1[14] << 8) | rtStaBlkDev1[13]
                gpioDataDev1 = (rtStaBlkDev1[16] << 8) | rtStaBlkDev1[15]
                dcDev1 = rtStaBlkDev1[17]
                listStaDev1 = [hex(status1Dev1)[2:].upper().zfill(4), hex(status2Dev1)[2:].upper().zfill(4),
                               hex(fmea1Dev1)[2:].upper().zfill(4), hex(fmea2Dev1)[2:].upper().zfill(4)]
                listTemGpDev1 = [hex(temp1Dev1)[2:].upper().zfill(4), hex(temp2Dev1)[2:].upper().zfill(4),
                                 hex(gpioDataDev1)[2:].upper().zfill(4)]

                temp1CelDev1 = str(round(temp1Dev1 / 8 - 273.15, 2)) + "°C"
                temp2CelDev1 = str(round(temp2Dev1 / 8 - 273.15, 2)) + "°C"
                temp1FhDev1 = str(round((temp1Dev1 / 8 - 273.15) * 9 / 5 + 32, 2)) + "°F"
                temp2FhDev1 = str(round((temp2Dev1 / 8 - 273.15) * 9 / 5 + 32, 2)) + "°F"

                listTemValDev1 = [[temp1CelDev1, temp1FhDev1], [temp2CelDev1, temp2FhDev1],
                                  [hex(rtStaBlkDev1[16])[2:].upper().zfill(2), hex(rtStaBlkDev1[15])[2:].upper().zfill(2)]]

                ''' fill data into dev1 status table '''
                for r in range(4):  # fill table
                    self.update_table_item_data(pTable, r + 1, pDev1Col,
                                                listStaDev1[r])  # device 1
                if pFlagTem:
                    for r in range(5, 8):
                        self.update_table_item_data(pTable, r, pDev1Col,
                                                    listTemGpDev1[r - 5])  # device 1
                        self.update_table_item_data(pTable, r, 8,
                                                    listTemValDev1[r - 5][0])  # device 1
                        self.update_table_item_data(pTable, r, 10,
                                                    listTemValDev1[r - 5][1])  # device 1

                ''' update dev1 status table led '''
                self.update_status_register_led(status1Dev1, status2Dev1, fmea1Dev1, fmea2Dev1, pDev1LedList)

        if dcDev0 != 0x00:
            return dcDev0
        elif dcDev1 != 0x00:
            return dcDev1
        else:
            return True


    def read_dc_and_status(self, pDcTable, pLedDcByt, pLedAlertPk,
                                 pStatusTable, pLedStatusDev0, pLedStatusDev1):
        """
        用 readall command 读取 status block 中某个寄存器，并获得此次操作的 DC-Byte
        用返回的 DC byte 更新指定页面的 DC table
        用返回的 status block 各寄存器数据更新指定页面的 status table
        :param pDcTable: 指定页面的 dc table
        :param pLedDcByt: 指定页面 dc table 对应的 dc led 串列表
        :param pLedAlertPk: 指定页面 dc table 对应的 alertpacket led 串列表
        :param pStatusTable: 指定页面的 status table
        :param pLedStatusDev0: 指定页面 status table 对应的 dev0 led 串列表
        :param pLedStatusDev1: 指定页面 status table 对应的 dev1 led 串列表
        :return:
        """
        """ use READ ALL read one status registers to get DC byte """
        # read status1
        if self.flagSingleAfe:
            rtData = pb01_read_all(self.hidBdg, 0x04, 1, 0x00)
            if rtData == "message return RX error" or rtData == "pec check error":
                self.message_box(rtData)
                return
            else:
                dcByte = rtData[4]
        else:
            rtData = pb01_read_all(self.hidBdg, 0x04, 2, 0x00)
            if rtData == "message return RX error" or rtData == "pec check error":
                self.message_box(rtData)
                return
            else:
                dcByte = rtData[6]
        # update dc table
        self.update_dc_aleter_table(pDcTable, dcByte, pLedDcByt, pLedAlertPk)

        # # read status2
        # if self.flagSingleAfe:
        #     rtData = pb01_read_all(self.hidBdg, 0x05, 1, 0x00)
        #     if rtData == "message return RX error" or rtData == "pec check error":
        #         self.message_box(rtData)
        #         return
        #     else:
        #         dcByte = rtData[4]
        # else:
        #     rtData = pb01_read_all(self.hidBdg, 0x05, 2, 0x00)
        #     if rtData == "message return RX error" or rtData == "pec check error":
        #         self.message_box(rtData)
        #         return
        #     else:
        #         dcByte = rtData[6]
        # # update dc table
        # self.update_dc_aleter_table(pDcTable, dcByte, pLedDcByt, pLedAlertPk)
        #
        # # read fmea1
        # if self.flagSingleAfe:
        #     rtData = pb01_read_all(self.hidBdg, 0x06, 1, 0x00)
        #     if rtData == "message return RX error" or rtData == "pec check error":
        #         self.message_box(rtData)
        #         return
        #     else:
        #         dcByte = rtData[4]
        # else:
        #     rtData = pb01_read_all(self.hidBdg, 0x06, 2, 0x00)
        #     if rtData == "message return RX error" or rtData == "pec check error":
        #         self.message_box(rtData)
        #         return
        #     else:
        #         dcByte = rtData[6]
        # # update dc table
        # self.update_dc_aleter_table(pDcTable, dcByte, pLedDcByt, pLedAlertPk)
        #
        # # read fmea2
        # if self.flagSingleAfe:
        #     rtData = pb01_read_all(self.hidBdg, 0x07, 1, 0x00)
        #     if rtData == "message return RX error" or rtData == "pec check error":
        #         self.message_box(rtData)
        #         return
        #     else:
        #         dcByte = rtData[4]
        # else:
        #     rtData = pb01_read_all(self.hidBdg, 0x07, 2, 0x00)
        #     if rtData == "message return RX error" or rtData == "pec check error":
        #         self.message_box(rtData)
        #         return
        #     else:
        #         dcByte = rtData[6]
        # # update dc table
        # self.update_dc_aleter_table(pDcTable, dcByte, pLedDcByt, pLedAlertPk)

        """ update status block table """
        if not self.update_status_block_table(pStatusTable, 2, 7,
                                              pLedStatusDev0, pLedStatusDev1, True):
            return


    def update_write_read_op(self, pReg, pData, pTable, pRow, pCol):
        """
        appCfgPage, diagCfgPage, cblPage write+read button 点击后更新某个寄存信息
        一次只更新一个寄存器
        1个还是 2 个 afe， 函数内部自动判断，不用外部参数
        :param pReg: register address
        :param pData: register data
        :param pTable: table object
        :param pRow: returned data fill row num
        :param pCol: returned data fill col num
        :return: None
        """
        rtData = self.afe_write_read_all(pReg, pData)  # configure A13 = 0x2000
        if rtData != False:
            if self.flagSingleAfe:  # single afe
                rdDataDev0 = (rtData[1] << 8) | rtData[0]
                self.update_table_item_data(pTable, pRow, pCol, hex(rdDataDev0)[2:].upper().zfill(4))   # dev0
            else:  # dual afe
                rdDataDev0 = (rtData[3] << 8) | rtData[2]
                rdDataDev1 = (rtData[1] << 8) | rtData[0]
                self.update_table_item_data(pTable, pRow, pCol, hex(rdDataDev0)[2:].upper().zfill(4))   # dev0
                self.update_table_item_data(pTable, pRow, pCol+1, hex(rdDataDev1)[2:].upper().zfill(4)) # dev1
        else:
            return


    def update_config_readback_op(self, pReg, pTable, pRow, pCol):
        """
        appCfgPage, diagCfgPage, cblPage read back button 点击后更新某个寄存信息
        一次只更新一个寄存器
        1个还是 2 个 afe， 函数内部自动判断，不用外部参数
        :param pReg: register address
        :param pTable: table object
        :param pRow: returned data fill row num
        :param pCol: returned data fill col num
        :return: None
        """
        # read register
        if self.flagSingleAfe:  # single afe
            rtRd = pb01_read_all(self.hidBdg, pReg, 1, 0x00)  # read all, alseed=0x00
            if rtRd == "message return RX error" or rtRd == "pec check error":
                self.message_box(rtRd)
                return False
            else:
                rdDataDev0 = (rtRd[3] << 8) | rtRd[2]
                self.update_table_item_data(pTable, pRow, pCol, hex(rdDataDev0)[2:].upper().zfill(4))  # dev0
        else:   # dual afe
            rtRd = pb01_read_all(self.hidBdg, pReg, 2, 0x00)  # read all, alseed=0x00
            if rtRd == "message return RX error" or rtRd == "pec check error":
                self.message_box(rtRd)
                return False
            else:
                rdDataDev0 = (rtRd[5] << 8) | rtRd[4]
                rdDataDev1 = (rtRd[3] << 8) | rtRd[2]
                self.update_table_item_data(pTable, pRow, pCol, hex(rdDataDev0)[2:].upper().zfill(4))  # dev0
                self.update_table_item_data(pTable, pRow, pCol + 1, hex(rdDataDev1)[2:].upper().zfill(4))  # dev1


    def update_meaAcqSumPage_sumDataTable(self):
        """
        读取 SUMMARY DATA Register block
        并将读取值更新到 meaAcqSumPage summary data table
        :return:
        """
        ''' read device 0 summary data block '''
        rtData = pb01_read_block(self.hidBdg, 10, 0, 0x86, 0x00)
        if rtData == "message return RX error" or rtData == "pec check error":
            self.message_box(rtData)
            return
        else:
            minMaxLocDev0 = (rtData[4] << 8) | rtData[3]
            maxCellRegDev0 = (rtData[6] << 8) | rtData[5]
            minCellRegDev0 = (rtData[8] << 8) | rtData[7]
            maxAuxRegDev0 = (rtData[10] << 8) | rtData[9]
            minAuxRegDev0 = (rtData[12] << 8) | rtData[11]
            totalRegDev0 = (rtData[14] << 8) | rtData[13]
            altTotRegDev0 = (rtData[16] << 8) | rtData[15]
            pmmLocDev0 = (rtData[18] << 8) | rtData[17]
            pmmCellRegDev0 = (rtData[20] << 8) | rtData[19]
            pmmAuxRegDev0 = (rtData[22] << 8) | rtData[21]

            # fill value column
            listSumDataDev0 = [hex(minMaxLocDev0)[2:].upper().zfill(4), hex(maxCellRegDev0)[2:].upper().zfill(4),
                               hex(minCellRegDev0)[2:].upper().zfill(4), hex(maxAuxRegDev0)[2:].upper().zfill(4),
                               hex(minAuxRegDev0)[2:].upper().zfill(4), hex(totalRegDev0)[2:].upper().zfill(4),
                               hex(altTotRegDev0)[2:].upper().zfill(4), hex(pmmLocDev0)[2:].upper().zfill(4),
                               hex(pmmCellRegDev0)[2:].upper().zfill(4), hex(pmmAuxRegDev0)[2:].upper().zfill(4)]

            for i in range(10):
                self.table_meaAcqSumPage_sumDataDev0.item(i, 2).setText(listSumDataDev0[i])

            # fill MINMAXLOC row
            listMinMaxLocBitsDev0 = [str((minMaxLocDev0 & 0xF000) >> 12),
                                     str((minMaxLocDev0 & 0x0F00) >> 8),
                                     str((minMaxLocDev0 & 0x00F0) >> 4),
                                     str(minMaxLocDev0 & 0x000F)]
            for i in range(4):
                self.table_meaAcqSumPage_sumDataDev0.item(0, 3 + 2 * i).setText(listMinMaxLocBitsDev0[i])

            # fill PMMLOC row
            listPmmLocBitsDev0 = [str((pmmLocDev0 & 0x0F00) >> 8),
                                  str(pmmLocDev0 & 0x000F)]
            self.table_meaAcqSumPage_sumDataDev0.item(7, 5).setText(listPmmLocBitsDev0[0])
            self.table_meaAcqSumPage_sumDataDev0.item(7, 9).setText(listPmmLocBitsDev0[1])

            # fill other rows
            listOtherSumBitsDev0 = [str(round((maxCellRegDev0 / ADC_FULL_DATA * CELL_SCALE), 5)) + 'V',
                                    str(round((minCellRegDev0 / ADC_FULL_DATA * CELL_SCALE), 5)) + 'V',
                                    str(round((maxAuxRegDev0  / ADC_FULL_DATA * 100),        2)) + '%',
                                    str(round((minAuxRegDev0  / ADC_FULL_DATA * 100),        2)) + '%',
                                    str(round((totalRegDev0   / ADC_FULL_DATA * HV_SCALE),   5)) + 'V',
                                    str(round((altTotRegDev0  / ADC_FULL_DATA * HV_SCALE),   5)) + 'V',
                                    str(round((pmmCellRegDev0 / ADC_FULL_DATA * CELL_SCALE), 5)) + 'V',
                                    str(round((pmmAuxRegDev0  / ADC_FULL_DATA * 100),        2)) + '%'
                                    ]
            for i in range(6):
                self.table_meaAcqSumPage_sumDataDev0.item(i + 1, 3).setText(listOtherSumBitsDev0[i])

            self.table_meaAcqSumPage_sumDataDev0.item(8, 3).setText(listOtherSumBitsDev0[6])
            self.table_meaAcqSumPage_sumDataDev0.item(9, 3).setText(listOtherSumBitsDev0[7])

        ''' read device 1 summary data block '''
        if not self.flagSingleAfe:
            rtData = pb01_read_block(self.hidBdg, 10, 1, 0x86, 0x00)
            if rtData == "message return RX error" or rtData == "pec check error":
                self.message_box(rtData)
                return
            else:
                minMaxLocDev1 = (rtData[4] << 8) | rtData[3]
                maxCellRegDev1 = (rtData[6] << 8) | rtData[5]
                minCellRegDev1 = (rtData[8] << 8) | rtData[7]
                maxAuxRegDev1 = (rtData[10] << 8) | rtData[9]
                minAuxRegDev1 = (rtData[12] << 8) | rtData[11]
                totalRegDev1 = (rtData[14] << 8) | rtData[13]
                altTotRegDev1 = (rtData[16] << 8) | rtData[15]
                pmmLocDev1 = (rtData[18] << 8) | rtData[17]
                pmmCellRegDev1 = (rtData[20] << 8) | rtData[19]
                pmmAuxRegDev1 = (rtData[22] << 8) | rtData[21]

                # fill value column
                listSumDataDev1 = [hex(minMaxLocDev1)[2:].upper().zfill(4),  hex(maxCellRegDev1)[2:].upper().zfill(4),
                                   hex(minCellRegDev1)[2:].upper().zfill(4), hex(maxAuxRegDev1)[2:].upper().zfill(4),
                                   hex(minAuxRegDev1)[2:].upper().zfill(4),  hex(totalRegDev1)[2:].upper().zfill(4),
                                   hex(altTotRegDev1)[2:].upper().zfill(4),  hex(pmmLocDev1)[2:].upper().zfill(4),
                                   hex(pmmCellRegDev1)[2:].upper().zfill(4), hex(pmmAuxRegDev1)[2:].upper().zfill(4)]

                for i in range(10):
                    self.table_meaAcqSumPage_sumDataDev1.item(i, 2).setText(listSumDataDev1[i])

                # fill MINMAXLOC row
                listMinMaxLocBitsDev1 = [str((minMaxLocDev1 & 0xF000) >> 12),
                                         str((minMaxLocDev1 & 0x0F00) >> 8),
                                         str((minMaxLocDev1 & 0x00F0) >> 4),
                                         str(minMaxLocDev1 & 0x000F)]
                for i in range(4):
                    self.table_meaAcqSumPage_sumDataDev1.item(0, 3 + 2 * i).setText(listMinMaxLocBitsDev1[i])

                # fill PMMLOC row
                listPmmLocBitsDev1 = [str((pmmLocDev1 & 0x0F00) >> 8),
                                      str(pmmLocDev1 & 0x000F)]
                self.table_meaAcqSumPage_sumDataDev1.item(7, 5).setText(listPmmLocBitsDev1[0])
                self.table_meaAcqSumPage_sumDataDev1.item(7, 9).setText(listPmmLocBitsDev1[1])

                # fill other rows
                listOtherSumBitsDev1 = [str(round((maxCellRegDev1 / ADC_FULL_DATA * CELL_SCALE), 5)) + 'V',
                                        str(round((minCellRegDev1 / ADC_FULL_DATA * CELL_SCALE), 5)) + 'V',
                                        str(round((maxAuxRegDev1  / ADC_FULL_DATA * 100),        2)) + '%',
                                        str(round((minAuxRegDev1  / ADC_FULL_DATA * 100),        2)) + '%',
                                        str(round((totalRegDev1   / ADC_FULL_DATA * HV_SCALE),   5)) + 'V',
                                        str(round((altTotRegDev1  / ADC_FULL_DATA * HV_SCALE),   5)) + 'V',
                                        str(round((pmmCellRegDev1 / ADC_FULL_DATA * CELL_SCALE), 5)) + 'V',
                                        str(round((pmmAuxRegDev1  / ADC_FULL_DATA * 100),        2)) + '%']
                for i in range(6):
                    self.table_meaAcqSumPage_sumDataDev1.item(i + 1, 3).setText(listOtherSumBitsDev1[i])

                self.table_meaAcqSumPage_sumDataDev1.item(8, 3).setText(listOtherSumBitsDev1[6])
                self.table_meaAcqSumPage_sumDataDev1.item(9, 3).setText(listOtherSumBitsDev1[7])


    def update_meaAcqDetailPage_alertTable(self):
        """
        读取 ALERT Register block
        并将读取值更新到 meaAcqDetailDataPage Alert Register Block table
        :return:
        """
        ''' read device 0 alert register block '''
        rtData = pb01_read_block(self.hidBdg, 6, 0, 0x80, 0x00)
        if rtData == "message return RX error" or rtData == "pec check error":
            self.message_box(rtData)
            return
        else:
            alertOvDev0 = (rtData[4] << 8) | rtData[3]
            alertUvDev0 = (rtData[6] << 8) | rtData[5]
            alertAltOvDev0 = (rtData[8] << 8) | rtData[7]
            alertAltUvDev0 = (rtData[10] << 8) | rtData[9]
            alertAuxOvDev0 = (rtData[12] << 8) | rtData[11]
            alertAuxUvDev0 = (rtData[14] << 8) | rtData[13]

            # fill value column
            listAlertRegDev0 = [hex(alertOvDev0)[2:].upper().zfill(4),
                                hex(alertUvDev0)[2:].upper().zfill(4),
                                hex(alertAltOvDev0)[2:].upper().zfill(4),
                                hex(alertAltUvDev0)[2:].upper().zfill(4),
                                hex(alertAuxOvDev0)[2:].upper().zfill(4),
                                hex(alertAuxUvDev0)[2:].upper().zfill(4)]
            for r in range(1, 7):
                self.table_meaAcqDetailData_alertRegDev0.item(r, 2).setText(listAlertRegDev0[r - 1])

            # update led
            self.update_acquistion_alert_regiser_led([alertOvDev0,
                                                      alertUvDev0,
                                                      alertAltOvDev0,
                                                      alertAltUvDev0,
                                                      alertAuxOvDev0,
                                                      alertAuxUvDev0], self.ledMeaAcqDetailPageDev0)

            ''' read device 1 alert register block  '''
            if not self.flagSingleAfe:
                rtData = pb01_read_block(self.hidBdg, 6, 1, 0x80, 0x00)
                if rtData == "message return RX error" or rtData == "pec check error":
                    self.message_box(rtData)
                    return
                else:
                    alertOvDev1 = (rtData[4] << 8) | rtData[3]
                    alertUvDev1 = (rtData[6] << 8) | rtData[5]
                    alertAltOvDev1 = (rtData[8] << 8) | rtData[7]
                    alertAltUvDev1 = (rtData[10] << 8) | rtData[9]
                    alertAuxOvDev1 = (rtData[12] << 8) | rtData[11]
                    alertAuxUvDev1 = (rtData[14] << 8) | rtData[13]

                    # fill value column
                    listAlertRegDev1 = [hex(alertOvDev1)[2:].upper().zfill(4),
                                        hex(alertUvDev1)[2:].upper().zfill(4),
                                        hex(alertAltOvDev1)[2:].upper().zfill(4),
                                        hex(alertAltUvDev1)[2:].upper().zfill(4),
                                        hex(alertAuxOvDev1)[2:].upper().zfill(4),
                                        hex(alertAuxUvDev1)[2:].upper().zfill(4)]
                    for r in range(1, 7):
                        self.table_meaAcqDetailData_alertRegDev1.item(r, 2).setText(listAlertRegDev1[r - 1])

                    # update led
                    self.update_acquistion_alert_regiser_led([alertOvDev1,
                                                              alertUvDev1,
                                                              alertAltOvDev1,
                                                              alertAltUvDev1,
                                                              alertAuxOvDev1,
                                                              alertAuxUvDev1], self.ledMeaAcqDetailPageDev1)


    def update_meaAcqDetailPage_dataTable(self, pHexRow, pValRow, pRegAddr, pPolAuxCfg, pAuxFlag):
        """
        更新 acquistion detail data table
        一次调用只更新 table 中的一个 block
        acquistion detail data table 中有 4 个 block，需调用该函数 4 次才能完整更新整个 table
        :param pHexRow: 当前调用要更新的 hex data 所在行的行号
        :param pValRow: 当前调用要更新的 value data 所在行的行号
        :param pRegAddr: 当前调用要读取的 block 首寄存器地址
        :param pPolAuxCfg: 此参数根据读取的 block 不同有两种含义
                           场景1：当前读取的是 cell data
                           cell data 根据传入的 pPolAuxCfg 判断是否做 bipolar 处理
                           pPolAuxCfg bit = 0 - unipolar
                                      bit = 1 - bipolar
                           场景2：当前读取的是 aux data
                           aux data 根据传入的 pPolAuxCfg 判断转换成摄氏度还是百分比
                           pPolAuxCfg bit = 0 - 摄氏度
                                      bit = 1 - 百分比
        :param pAuxFlag: 因 aux block 计算公式和其它 block 不同，所以用此 flag 来区分
                         True - 当前处理 aux block
                         False - 当前处理非 aux block
        :return:
        """
        """ read device 0 CELL IIR DATA block """
        rtData = pb01_read_block(self.hidBdg, 16, 0, pRegAddr, 0x00)
        if rtData == "message return RX error" or rtData == "pec check error":
            self.message_box(rtData)
            return
        else:
            regData0Dev0  =  (rtData[4] << 8)  | rtData[3]
            regData1Dev0  =  (rtData[6] << 8)  | rtData[5]
            regData2Dev0  =  (rtData[8] << 8)  | rtData[7]
            regData3Dev0  =  (rtData[10] << 8) | rtData[9]
            regData4Dev0  =  (rtData[12] << 8) | rtData[11]
            regData5Dev0  =  (rtData[14] << 8) | rtData[13]
            regData6Dev0  =  (rtData[16] << 8) | rtData[15]
            regData7Dev0  =  (rtData[18] << 8) | rtData[17]
            regData8Dev0  =  (rtData[20] << 8) | rtData[19]
            regData9Dev0  =  (rtData[22] << 8) | rtData[21]
            regData10Dev0 = (rtData[24] << 8) | rtData[23]
            regData11Dev0 = (rtData[26] << 8) | rtData[25]
            regData12Dev0 = (rtData[28] << 8) | rtData[27]
            regData13Dev0 = (rtData[30] << 8) | rtData[29]
            regData14Dev0 = (rtData[32] << 8) | rtData[31]
            regData15Dev0 = (rtData[34] << 8) | rtData[33]

            ''' int & actual data list '''
            listRegDataIntDev0 = [regData0Dev0,
                                  regData1Dev0,
                                  regData2Dev0,
                                  regData3Dev0,
                                  regData4Dev0,
                                  regData5Dev0,
                                  regData6Dev0,
                                  regData7Dev0,
                                  regData8Dev0,
                                  regData9Dev0,
                                  regData10Dev0,
                                  regData11Dev0,
                                  regData12Dev0,
                                  regData13Dev0,
                                  regData14Dev0,
                                  regData15Dev0]

            listRegDataActualDev0 = ['0', '0', '0', '0', '0', '0', '0', '0',
                                     '0', '0', '0', '0', '0', '0', '0', '0']

            if not pAuxFlag:    # cell data
                ''' hex data '''
                listRegDataHexDev0 = [hex(regData0Dev0)[2:].upper().zfill(4),
                                      hex(regData1Dev0)[2:].upper().zfill(4),
                                      hex(regData2Dev0)[2:].upper().zfill(4),
                                      hex(regData3Dev0)[2:].upper().zfill(4),
                                      hex(regData4Dev0)[2:].upper().zfill(4),
                                      hex(regData5Dev0)[2:].upper().zfill(4),
                                      hex(regData6Dev0)[2:].upper().zfill(4),
                                      hex(regData7Dev0)[2:].upper().zfill(4),
                                      hex(regData8Dev0)[2:].upper().zfill(4),
                                      hex(regData9Dev0)[2:].upper().zfill(4),
                                      hex(regData10Dev0)[2:].upper().zfill(4),
                                      hex(regData11Dev0)[2:].upper().zfill(4),
                                      hex(regData12Dev0)[2:].upper().zfill(4),
                                      hex(regData13Dev0)[2:].upper().zfill(4),
                                      hex(regData14Dev0)[2:].upper().zfill(4),
                                      hex(regData15Dev0)[2:].upper().zfill(4)]
                ''' calculate actual data '''
                for i in range(16):
                    if (0x0001 << i) & pPolAuxCfg:     # convert into bipolar
                        listRegDataActualDev0[i] = str(round(
                            convert_complement_data(listRegDataIntDev0[i], 16) / ADC_FULL_DATA * CELL_SCALE, 5))
                    else:   # use unipolar
                        listRegDataActualDev0[i] = str(round(
                            listRegDataIntDev0[i] / ADC_FULL_DATA * CELL_SCALE, 5))
                    # listRegDataActualDev0.append(listRegDataIntDev0[i])
            else:   # AUX data
                ''' hex data '''
                listRegDataHexDev0 = [hex(regData8Dev0)[2:].upper().zfill(4),       # ALTAUX 0
                                      hex(regData9Dev0)[2:].upper().zfill(4),
                                      hex(regData10Dev0)[2:].upper().zfill(4),
                                      hex(regData11Dev0)[2:].upper().zfill(4),
                                      hex(regData12Dev0)[2:].upper().zfill(4),
                                      hex(regData13Dev0)[2:].upper().zfill(4),
                                      hex(regData14Dev0)[2:].upper().zfill(4),
                                      hex(regData15Dev0)[2:].upper().zfill(4),      # ALTAUX 7
                                      hex(regData0Dev0)[2:].upper().zfill(4),       # AUX 0
                                      hex(regData1Dev0)[2:].upper().zfill(4),
                                      hex(regData2Dev0)[2:].upper().zfill(4),
                                      hex(regData3Dev0)[2:].upper().zfill(4),
                                      hex(regData4Dev0)[2:].upper().zfill(4),
                                      hex(regData5Dev0)[2:].upper().zfill(4),
                                      hex(regData6Dev0)[2:].upper().zfill(4),
                                      hex(regData7Dev0)[2:].upper().zfill(4)]       # AUX 7
                ''' calculate actual data '''
                for i in range(8):
                    if (0x01 << i) & pPolAuxCfg:     # convert into percent
                        listRegDataActualDev0[i] = str(round(listRegDataIntDev0[i + 8] /
                                                             ADC_FULL_DATA * CELL_SCALE, 5)) + 'V'        # ALTAUX
                        listRegDataActualDev0[i + 8] = str(round(listRegDataIntDev0[i] /
                                                                 ADC_FULL_DATA * CELL_SCALE, 5)) + 'V'    # AUX
                    else:   # convert into celsius
                        listRegDataActualDev0[i] = str(round(self.cal_ntc_temp_value(listRegDataIntDev0[i + 8]), 2)) \
                                                   + '°C'        # ALTAUX
                        listRegDataActualDev0[i + 8] = str(round(self.cal_ntc_temp_value(listRegDataIntDev0[i]), 2)) \
                                                       + '°C'    # AUX

        # fill table
        for c in range(18, 2, -1):
            self.table_meaAcqDetailData_dataRegDev0.item(pHexRow, c).setText(listRegDataHexDev0[18 - c])
            self.table_meaAcqDetailData_dataRegDev0.item(pValRow, c).setText(listRegDataActualDev0[18 - c])

        """ read device 1 alert register block """
        if not self.flagSingleAfe:
            rtData = pb01_read_block(self.hidBdg, 16, 1, pRegAddr, 0x00)
            if rtData == "message return RX error" or rtData == "pec check error":
                self.message_box(rtData)
                return
            else:
                regData0Dev1  = (rtData[4] << 8)  | rtData[3]
                regData1Dev1  = (rtData[6] << 8)  | rtData[5]
                regData2Dev1  = (rtData[8] << 8)  | rtData[7]
                regData3Dev1  = (rtData[10] << 8) | rtData[9]
                regData4Dev1  = (rtData[12] << 8) | rtData[11]
                regData5Dev1  = (rtData[14] << 8) | rtData[13]
                regData6Dev1  = (rtData[16] << 8) | rtData[15]
                regData7Dev1  = (rtData[18] << 8) | rtData[17]
                regData8Dev1  = (rtData[20] << 8) | rtData[19]
                regData9Dev1  = (rtData[22] << 8) | rtData[21]
                regData10Dev1 = (rtData[24] << 8) | rtData[23]
                regData11Dev1 = (rtData[26] << 8) | rtData[25]
                regData12Dev1 = (rtData[28] << 8) | rtData[27]
                regData13Dev1 = (rtData[30] << 8) | rtData[29]
                regData14Dev1 = (rtData[32] << 8) | rtData[31]
                regData15Dev1 = (rtData[34] << 8) | rtData[33]

                ''' int & actual data list '''
                listRegDataIntDev1 = [regData0Dev1,
                                      regData1Dev1,
                                      regData2Dev1,
                                      regData3Dev1,
                                      regData4Dev1,
                                      regData5Dev1,
                                      regData6Dev1,
                                      regData7Dev1,
                                      regData8Dev1,
                                      regData9Dev1,
                                      regData10Dev1,
                                      regData11Dev1,
                                      regData12Dev1,
                                      regData13Dev1,
                                      regData14Dev1,
                                      regData15Dev1]

                listRegDataActualDev1 = ['0', '0', '0', '0', '0', '0', '0', '0',
                                         '0', '0', '0', '0', '0', '0', '0', '0']

                if not pAuxFlag:    # cell data
                    ''' hex data '''
                    listRegDataHexDev1 = [hex(regData0Dev1)[2:].upper().zfill(4),
                                          hex(regData1Dev1)[2:].upper().zfill(4),
                                          hex(regData2Dev1)[2:].upper().zfill(4),
                                          hex(regData3Dev1)[2:].upper().zfill(4),
                                          hex(regData4Dev1)[2:].upper().zfill(4),
                                          hex(regData5Dev1)[2:].upper().zfill(4),
                                          hex(regData6Dev1)[2:].upper().zfill(4),
                                          hex(regData7Dev1)[2:].upper().zfill(4),
                                          hex(regData8Dev1)[2:].upper().zfill(4),
                                          hex(regData9Dev1)[2:].upper().zfill(4),
                                          hex(regData10Dev1)[2:].upper().zfill(4),
                                          hex(regData11Dev1)[2:].upper().zfill(4),
                                          hex(regData12Dev1)[2:].upper().zfill(4),
                                          hex(regData13Dev1)[2:].upper().zfill(4),
                                          hex(regData14Dev1)[2:].upper().zfill(4),
                                          hex(regData15Dev1)[2:].upper().zfill(4)]
                    ''' calculate actual data '''
                    for i in range(16):
                        if (0x0001 << i) & pPolAuxCfg:  # convert into bipolar
                            listRegDataActualDev1[i] = str(round(
                                convert_complement_data(listRegDataIntDev1[i], 16) / ADC_FULL_DATA * CELL_SCALE, 5))
                        else:  # use unipolar
                            listRegDataActualDev1[i] = str(round(
                                listRegDataIntDev1[i] / ADC_FULL_DATA * CELL_SCALE, 5))
                else:   # AUX data
                    ''' hex data '''
                    listRegDataHexDev1 = [hex(regData8Dev1)[2:].upper().zfill(4),           # ALTAUX0
                                          hex(regData9Dev1)[2:].upper().zfill(4),
                                          hex(regData10Dev1)[2:].upper().zfill(4),
                                          hex(regData11Dev1)[2:].upper().zfill(4),
                                          hex(regData12Dev1)[2:].upper().zfill(4),
                                          hex(regData13Dev1)[2:].upper().zfill(4),
                                          hex(regData14Dev1)[2:].upper().zfill(4),
                                          hex(regData15Dev1)[2:].upper().zfill(4),          # ALTAUX0
                                          hex(regData0Dev1)[2:].upper().zfill(4),           # AUX0
                                          hex(regData1Dev1)[2:].upper().zfill(4),
                                          hex(regData2Dev1)[2:].upper().zfill(4),
                                          hex(regData3Dev1)[2:].upper().zfill(4),
                                          hex(regData4Dev1)[2:].upper().zfill(4),
                                          hex(regData5Dev1)[2:].upper().zfill(4),
                                          hex(regData6Dev1)[2:].upper().zfill(4),
                                          hex(regData7Dev1)[2:].upper().zfill(4)]           # AUX7
                    ''' calculate actual data '''
                    for i in range(8):
                        if (0x01 << i) & pPolAuxCfg:     # convert into percent
                            listRegDataActualDev1[i] = str(round(listRegDataIntDev1[i + 8] /
                                                                 ADC_FULL_DATA * CELL_SCALE, 5)) + 'V'        # ALTAUX
                            listRegDataActualDev1[i + 8] = str(round(listRegDataIntDev1[i] /
                                                                     ADC_FULL_DATA * CELL_SCALE, 5)) + 'V'    # AUX
                        else:   # convert into celsius
                            listRegDataActualDev1[i] = str(round(self.cal_ntc_temp_value(listRegDataIntDev1[i + 8]), 2)) \
                                                       + '°C'        # ALTAUX
                            listRegDataActualDev1[i + 8] = str(round(self.cal_ntc_temp_value(listRegDataIntDev1[i]), 2)) \
                                                           + '°C'    # AUX

                # fill table
            for c in range(18, 2, -1):
                self.table_meaAcqDetailData_dataRegDev1.item(pHexRow, c).setText(listRegDataHexDev1[18 - c])
                self.table_meaAcqDetailData_dataRegDev1.item(pValRow, c).setText(listRegDataActualDev1[18 - c])


    def update_diagnostic_data_table(self, pDiagMode):
        """
        更新 diagnostic data table
        :param pDiagMode: 因在不同 diagnostic 模式下，diagnostic data polarity 是不同的
                       所以，这里需要传入 diagnostic mode，然后根据不同 mode 设置输出数据 polarity
        :return:
        """
        ''' read device 0 DIAGNOSITC DATA block '''
        rtData = pb01_read_block(self.hidBdg, 17, 0, 0xD6, 0x00)
        if rtData == "message return RX error" or rtData == "pec check error":
            self.message_box(rtData)
            return
        else:
            regData0Dev0  =  (rtData[4] << 8)  | rtData[3]
            regData1Dev0  =  (rtData[6] << 8)  | rtData[5]
            regData2Dev0  =  (rtData[8] << 8)  | rtData[7]
            regData3Dev0  =  (rtData[10] << 8) | rtData[9]
            regData4Dev0  =  (rtData[12] << 8) | rtData[11]
            regData5Dev0  =  (rtData[14] << 8) | rtData[13]
            regData6Dev0  =  (rtData[16] << 8) | rtData[15]
            regData7Dev0  =  (rtData[18] << 8) | rtData[17]
            regData8Dev0  =  (rtData[20] << 8) | rtData[19]
            regData9Dev0  =  (rtData[22] << 8) | rtData[21]
            regData10Dev0 = (rtData[24] << 8) | rtData[23]
            regData11Dev0 = (rtData[26] << 8) | rtData[25]
            regData12Dev0 = (rtData[28] << 8) | rtData[27]
            regData13Dev0 = (rtData[30] << 8) | rtData[29]
            regData14Dev0 = (rtData[32] << 8) | rtData[31]
            regData15Dev0 = (rtData[34] << 8) | rtData[33]
            regData16Dev0 = (rtData[36] << 8) | rtData[35]

            listRegDataHexDev0 = [hex(regData0Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData1Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData2Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData3Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData4Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData5Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData6Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData7Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData8Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData9Dev0 )[2:].upper().zfill(4) ,
                                  hex(regData10Dev0)[2:].upper().zfill(4) ,
                                  hex(regData11Dev0)[2:].upper().zfill(4) ,
                                  hex(regData12Dev0)[2:].upper().zfill(4) ,
                                  hex(regData13Dev0)[2:].upper().zfill(4) ,
                                  hex(regData14Dev0)[2:].upper().zfill(4) ,
                                  hex(regData15Dev0)[2:].upper().zfill(4),
                                  hex(regData16Dev0)[2:].upper().zfill(4)]

            if pDiagMode == 0x4 or pDiagMode == 0x6 or pDiagMode == 0x8:    # unipolar value 76.3uV LSB
                listRegDataValDev0 =  [str(round(regData0Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData1Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData2Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData3Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData4Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData5Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData6Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData7Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData8Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData9Dev0  / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData10Dev0 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData11Dev0 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData12Dev0 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData13Dev0 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData14Dev0 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData15Dev0 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                       str(round(regData16Dev0 / ADC_FULL_DATA * CELL_SCALE, 5))]
            elif pDiagMode == 0x5 or pDiagMode == 0x7 or pDiagMode == 0x9:  # bipolar mode 76.3uV LSB
                listRegDataValDev0 = [
                    str(round(convert_complement_data(regData0Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData1Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData2Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData3Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData4Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData5Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData6Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData7Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData8Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData9Dev0 , 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData10Dev0, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData11Dev0, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData12Dev0, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData13Dev0, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData14Dev0, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData15Dev0, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                    str(round(convert_complement_data(regData16Dev0, 16) / ADC_FULL_DATA * CELL_SCALE, 5))]
            elif pDiagMode == 0xA or pDiagMode == 0xB or pDiagMode == 0xC:  # unipolar value 38.15uV LSB
                listRegDataValDev0 = [str(round(regData0Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData1Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData2Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData3Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData4Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData5Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData6Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData7Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData8Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData9Dev0  / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData10Dev0 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData11Dev0 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData12Dev0 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData13Dev0 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData14Dev0 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData15Dev0 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData16Dev0 / ADC_FULL_DATA * AUX_SCALE, 5))]
            else:   #pDiagMode == 0x3
                listRegDataValDev0 = [str(round(regData0Dev0 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                      str(round(convert_complement_data(regData1Dev0, 16) / ADC_FULL_DATA * CELL_SCALE,    5)),
                                      str(round(convert_complement_data(regData2Dev0, 16) / ADC_FULL_DATA * CELL_SCALE,    5)),
                                      str(round(convert_complement_data(regData3Dev0, 16) / ADC_FULL_DATA * AUX_SCALE,  5)),
                                      str(round(regData4Dev0 / ADC_FULL_DATA * CELL_SCALE,    5)),
                                      str(round(regData5Dev0 / ADC_FULL_DATA * AUX_SCALE,  5)),
                                      str(round(regData6Dev0 / ADC_FULL_DATA * PWR_SCALE,   5)),
                                      str(round(regData7Dev0 / ADC_FULL_DATA * PWR_SCALE,   5)),
                                      str(round(regData8Dev0 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                      str(round(convert_complement_data(regData9Dev0, 16) / ADC_FULL_DATA * CELL_SCALE,    5)),
                                      str(round(convert_complement_data(regData10Dev0, 16) / ADC_FULL_DATA * CELL_SCALE,   5)),
                                      str(round(convert_complement_data(regData11Dev0, 16) / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData12Dev0 / ADC_FULL_DATA * CELL_SCALE,   5)),
                                      str(round(regData13Dev0 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                      str(round(regData14Dev0 / ADC_FULL_DATA * PWR_SCALE,  5)),
                                      str(round(regData15Dev0 / ADC_FULL_DATA * PWR_SCALE,  5)),
                                      str(round(convert_complement_data(regData16Dev0, 16) / ADC_FULL_DATA * CELL_SCALE,   5))]

        # fill table
        for c in range(19, 2, -1):
            self.table_diagAcqPage_dataReg_dev0.item(1, c).setText(listRegDataHexDev0[19 - c])
            self.table_diagAcqPage_dataReg_dev0.item(2, c).setText(listRegDataValDev0[19 - c])

        ''' read device 1 alert register block  '''
        if not self.flagSingleAfe:
            rtData = pb01_read_block(self.hidBdg, 17, 1, 0xD6, 0x00)
            if rtData == "message return RX error" or rtData == "pec check error":
                self.message_box(rtData)
                return
            else:
                regData0Dev1 = (rtData[4] << 8) | rtData[3]
                regData1Dev1 = (rtData[6] << 8) | rtData[5]
                regData2Dev1 = (rtData[8] << 8) | rtData[7]
                regData3Dev1 = (rtData[10] << 8) | rtData[9]
                regData4Dev1 = (rtData[12] << 8) | rtData[11]
                regData5Dev1 = (rtData[14] << 8) | rtData[13]
                regData6Dev1 = (rtData[16] << 8) | rtData[15]
                regData7Dev1 = (rtData[18] << 8) | rtData[17]
                regData8Dev1 = (rtData[20] << 8) | rtData[19]
                regData9Dev1 = (rtData[22] << 8) | rtData[21]
                regData10Dev1 = (rtData[24] << 8) | rtData[23]
                regData11Dev1 = (rtData[26] << 8) | rtData[25]
                regData12Dev1 = (rtData[28] << 8) | rtData[27]
                regData13Dev1 = (rtData[30] << 8) | rtData[29]
                regData14Dev1 = (rtData[32] << 8) | rtData[31]
                regData15Dev1 = (rtData[34] << 8) | rtData[33]
                regData16Dev1 = (rtData[36] << 8) | rtData[35]

                listRegDataHexDev1 = [hex(regData0Dev1)[2:].upper().zfill(4),
                                      hex(regData1Dev1)[2:].upper().zfill(4),
                                      hex(regData2Dev1)[2:].upper().zfill(4),
                                      hex(regData3Dev1)[2:].upper().zfill(4),
                                      hex(regData4Dev1)[2:].upper().zfill(4),
                                      hex(regData5Dev1)[2:].upper().zfill(4),
                                      hex(regData6Dev1)[2:].upper().zfill(4),
                                      hex(regData7Dev1)[2:].upper().zfill(4),
                                      hex(regData8Dev1)[2:].upper().zfill(4),
                                      hex(regData9Dev1)[2:].upper().zfill(4),
                                      hex(regData10Dev1)[2:].upper().zfill(4),
                                      hex(regData11Dev1)[2:].upper().zfill(4),
                                      hex(regData12Dev1)[2:].upper().zfill(4),
                                      hex(regData13Dev1)[2:].upper().zfill(4),
                                      hex(regData14Dev1)[2:].upper().zfill(4),
                                      hex(regData15Dev1)[2:].upper().zfill(4),
                                      hex(regData16Dev1)[2:].upper().zfill(4)]

                if pDiagMode == 0x4 or pDiagMode == 0x6 or pDiagMode == 0x8:  # unipolar value 76.3uV LSB
                    listRegDataValDev1 = [str(round(regData0Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData1Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData2Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData3Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData4Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData5Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData6Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData7Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData8Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData9Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData10Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData11Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData12Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData13Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData14Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData15Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData16Dev1 / ADC_FULL_DATA * CELL_SCALE, 5))]
                elif pDiagMode == 0x5 or pDiagMode == 0x7 or pDiagMode == 0x9:  # bipolar mode 76.3uV LSB
                    listRegDataValDev1 = [
                        str(round(convert_complement_data(regData0Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData1Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData2Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData3Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData4Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData5Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData6Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData7Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData8Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData9Dev1 , 16)  / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData10Dev1, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData11Dev1, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData12Dev1, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData13Dev1, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData14Dev1, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData15Dev1, 16) / ADC_FULL_DATA * CELL_SCALE, 5)),
                        str(round(convert_complement_data(regData16Dev1, 16) / ADC_FULL_DATA * CELL_SCALE, 5))]
                elif pDiagMode == 0xA or pDiagMode == 0xB or pDiagMode == 0xC:  # unipolar value 38.15uV LSB
                    listRegDataValDev1 = [str(round(regData0Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData1Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData2Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData3Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData4Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData5Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData6Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData7Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData8Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData9Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData10Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData11Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData12Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData13Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData14Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData15Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData16Dev1 / ADC_FULL_DATA * AUX_SCALE, 5))]
                else:  # pDiagMode == 0x3
                    listRegDataValDev1 = [str(round(regData0Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(convert_complement_data(regData1Dev1, 16) / ADC_FULL_DATA * CELL_SCALE,
                                                    5)),
                                          str(round(convert_complement_data(regData2Dev1, 16) / ADC_FULL_DATA * CELL_SCALE,
                                                    5)),
                                          str(round(convert_complement_data(regData3Dev1, 16) / ADC_FULL_DATA * AUX_SCALE,
                                                    5)),
                                          str(round(regData4Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData5Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData6Dev1 / ADC_FULL_DATA * PWR_SCALE, 5)),
                                          str(round(regData7Dev1 / ADC_FULL_DATA * PWR_SCALE, 5)),
                                          str(round(regData8Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(convert_complement_data(regData9Dev1, 16) / ADC_FULL_DATA * CELL_SCALE,
                                                    5)),
                                          str(round(convert_complement_data(regData10Dev1, 16) / ADC_FULL_DATA * CELL_SCALE,
                                                    5)),
                                          str(round(convert_complement_data(regData11Dev1, 16) / ADC_FULL_DATA * AUX_SCALE,
                                                    5)),
                                          str(round(regData12Dev1 / ADC_FULL_DATA * CELL_SCALE, 5)),
                                          str(round(regData13Dev1 / ADC_FULL_DATA * AUX_SCALE, 5)),
                                          str(round(regData14Dev1 / ADC_FULL_DATA * PWR_SCALE, 5)),
                                          str(round(regData15Dev1 / ADC_FULL_DATA * PWR_SCALE, 5)),
                                          str(round(convert_complement_data(regData16Dev1, 16) / ADC_FULL_DATA * CELL_SCALE,
                                                    5))]

                # fill table
            for c in range(19, 2, -1):
                self.table_diagAcqPage_dataReg_dev1.item(1, c).setText(listRegDataHexDev1[19 - c])
                self.table_diagAcqPage_dataReg_dev1.item(2, c).setText(listRegDataValDev1[19 - c])


    def update_status_table_extend_register(self, pTable, pRegAddr, pRow):
        """
        更新 meaAcqSumPage, diagAcqPage status table 中除 status block 之外的寄存器，
        如，ACQLOG, DIAGLOG ... DAC2FSREG
        一次只读取一个寄存器，并更新
        所以有几个寄存器，就要调用该函数几次
        因为 status table，寄存器数据更新位置的列号是固定的（2 和 7），所以参数中不用传入
        :param pTable: 要更新的 status table name
        :param pRegAddr: 当前读取的寄存器地址，如 0xD1
        :param pRow: 读回的数据要填写位置的行号
        :return: 从指定寄存器读回的数据，int 格式 - 一个 AFE 返回一个数据；两个 AFE 返回两个数据。
                 none - 读取操作有错
        """
        if self.flagSingleAfe:  # dev0
            rtData = pb01_read_all(self.hidBdg, pRegAddr, 1, 0x00)
            if rtData == "message return RX error" or rtData == "pec check error":
                self.message_box(rtData)
                return
            else:
                regDataDev0 = (rtData[3] << 8) | rtData[2]
                pTable.item(pRow, 2).setText(hex(regDataDev0)[2:].upper().zfill(4))  # dev0
                return regDataDev0
        else:  # dev1
            rtData = pb01_read_all(self.hidBdg, pRegAddr, 2, 0x00)
            if rtData == "message return RX error" or rtData == "pec check error":
                self.message_box(rtData)
                return
            else:
                regDataDev0 = (rtData[5] << 8) | rtData[4]
                pTable.item(pRow, 2).setText(hex(regDataDev0)[2:].upper().zfill(4))  # dev0
                regDataDev1 = (rtData[3] << 8) | rtData[2]
                pTable.item(pRow, 7).setText(hex(regDataDev1)[2:].upper().zfill(4))  # dev1
                return regDataDev0, regDataDev1


    def update_cblCtrl_block_table(self, pDev0Col, pDev1Col,
                                   pLedListStatusDev0, pLedListStatusDev1,
                                   pLedListUvStaDev0, pLedListUvStaDev1):
        """
        这个函数执行 read block command 去读取 PB01 CELL BALANCE CONTROL Block 中 5 个寄存器的值
        是否读取 dev1 的 block, 在函数内根据 self.flagSingleAfe 自动判读，不需要额外输入参数
        :param pDev0Col: dev0 读取到的值填入到哪一列
        :param pDev1Col: dev1 读取到的值填入到哪一列
        :param pLedListStatusDev0: 该 table 对应的 dev0 status led 列表
        :param pLedListStatusDev1: 该 table 对应的 dev1 status led 列表
        :param pLedListUvStaDev0: 该 table 对应的 dev0 uvstatus led 列表
        :param pLedListUvStaDev1: 该 table 对应的 dev1 uvstatus led 列表
        :return: DC byte - DC byte has alert
                 True - operation well
                 False - read block fail
        """
        dcDev0 = 0
        dcDev1 = 0
        """ device 0 process """
        ''' read device 0 block '''
        rtDataDev0 = pb01_read_block(self.hidBdg, 5, 0, 0x4A, 0x00)  # read dev0 cell balance control block, alseed=0x00
        if (rtDataDev0 == "message return RX error" or rtDataDev0 == "pec check error"):
            self.message_box(rtDataDev0)
            return False
        else:
            cblCtrlDev0   = (rtDataDev0[4]  << 8) | rtDataDev0[3]
            cblStatusDev0 = (rtDataDev0[6]  << 8) | rtDataDev0[5]
            cblTimerDev0  = (rtDataDev0[8]  << 8) | rtDataDev0[7]
            cblCountDev0  = (rtDataDev0[10] << 8) | rtDataDev0[9]
            cblUvStatDev0 = (rtDataDev0[12] << 8) | rtDataDev0[11]
            dcDev0 = rtDataDev0[13]

            listCblHexDev0 = [hex(cblCtrlDev0)[2:].upper().zfill(4), hex(cblStatusDev0)[2:].upper().zfill(4),
                              hex(cblTimerDev0)[2:].upper().zfill(4), hex(cblCountDev0)[2:].upper().zfill(4),
                              hex(cblUvStatDev0)[2:].upper().zfill(4)]

            ''' fill data into cblPage simplified demonstration table '''
            self.table_cblPage_cblCtrlSimDemo.item(0, 4).setText(hex(cblCtrlDev0)[2:].upper().zfill(4))
            self.table_cblPage_cblCtrlSimDemo.item(0, 5).setText(hex(cblCtrlDev0)[2:].upper().zfill(4))

            ''' fill data into cblPage status information table '''
            # fill read back hex data
            for r in range(5):
                self.table_cblPage_cblCtrlStaInf.item(r+1, pDev0Col).setText(listCblHexDev0[r])

            # fill CBALTIMER convert value
            self.table_cblPage_cblCtrlStaInf.item(3, 3).setText(str(cblTimerDev0))
            # fill CBALCOUNT each convert value
            self.table_cblPage_cblCtrlStaInf.item(4, 3).setText(str((cblCountDev0 & 0xC000) >> 14))  # hours value
            self.table_cblPage_cblCtrlStaInf.item(4, 5).setText(str((cblCountDev0 & 0x3F00) >> 8))   # minute value
            self.table_cblPage_cblCtrlStaInf.item(4, 7).setText(str((cblCountDev0 & 0x003F)))        # second value

            ''' update dev0 led '''
            self.update_cblPage_led(cblStatusDev0, pLedListStatusDev0, True)
            self.update_cblPage_led(cblUvStatDev0, pLedListUvStaDev0, False)

        """ device 1 process """
        ''' read device 1 block '''
        if self.flagSingleAfe == False:
            rtDataDev1 = pb01_read_block(self.hidBdg, 5, 1, 0x4A,
                                         0x00)  # read dev1 cell balance control block, alseed=0x00
            if (rtDataDev1 == "message return RX error" or rtDataDev1 == "pec check error"):
                self.message_box(rtDataDev1)
                return False
            else:
                cblCtrlDev1   = (rtDataDev1[4] << 8)  | rtDataDev1[3]
                cblStatusDev1 = (rtDataDev1[6] << 8)  | rtDataDev1[5]
                cblTimerDev1  = (rtDataDev1[8] << 8)  | rtDataDev1[7]
                cblCountDev1  = (rtDataDev1[10] << 8) | rtDataDev1[9]
                cblUvStatDev1 = (rtDataDev1[12] << 8) | rtDataDev1[11]
                dcDev1 = rtDataDev1[13]

                listCblHexDev1 = [hex(cblCtrlDev1)[2:].upper().zfill(4), hex(cblStatusDev1)[2:].upper().zfill(4),
                                  hex(cblTimerDev1)[2:].upper().zfill(4), hex(cblCountDev1)[2:].upper().zfill(4),
                                  hex(cblUvStatDev1)[2:].upper().zfill(4)]

                ''' fill data into cblPage simplified demonstration table '''
                self.table_cblPage_cblCtrlSimDemo.item(1, 4).setText(hex(cblCtrlDev1)[2:].upper().zfill(4))
                self.table_cblPage_cblCtrlSimDemo.item(1, 5).setText(hex(cblCtrlDev0)[2:].upper().zfill(4))

                ''' fill data into cblPage status information table '''
                # fill read back hex data
                for r in range(5):
                    self.table_cblPage_cblCtrlStaInf.item(r+1, pDev1Col).setText(listCblHexDev1[r])

                # fill CBALTIMER convert value
                self.table_cblPage_cblCtrlStaInf.item(3, 10).setText(str(cblTimerDev1))
                # fill CBALCOUNT each convert value
                self.table_cblPage_cblCtrlStaInf.item(4, 10).setText(
                    str((cblCountDev1 & 0xC000) >> 14))  # hours value
                self.table_cblPage_cblCtrlStaInf.item(4, 12).setText(
                    str((cblCountDev1 & 0x3F00) >> 8))  # minute value
                self.table_cblPage_cblCtrlStaInf.item(4, 14).setText(str((cblCountDev1 & 0x003F)))  # second value


                ''' update dev1 led '''
                self.update_cblPage_led(cblStatusDev1, pLedListStatusDev1, True)
                self.update_cblPage_led(cblUvStatDev1, pLedListUvStaDev1, False)

        if dcDev0 != 0x00:
            return dcDev0
        elif dcDev1 != 0x00:
            return dcDev1
        else:
            return True

    def update_cblPage_led(self, pData, pLedList, pStatusFlag):
        """
        更新 cblPage 的 led
        根据 pData 各 bit 的值，更新对应 led 的颜色
        一次只更新一串 led
        :param pData: data value
        :param pLedList: 对应的 led 串
        :param pStatusFlag: 因 status 和  uvstatus led 颜色显示规则不同，用此参数做区分
                              True - 传入的是 status 数据
                              False - 传入的是 uvstatus 数据
        :return:
        """
        if pStatusFlag:
            for bitCnt in range(16):
                if pData & (0x8000 >> bitCnt):
                    if bitCnt < 4:
                        pLedList[bitCnt].setStyleSheet(led_green_style)
                    else:
                        pLedList[bitCnt].setStyleSheet(led_red_style)
                else:
                    pLedList[bitCnt].setStyleSheet(led_white_style)
        else:
            for bitCnt in range(16):
                if pData & (0x8000 >> bitCnt):
                    pLedList[bitCnt].setStyleSheet(led_green_style)
                else:
                    pLedList[bitCnt].setStyleSheet(led_white_style)


    def cal_ntc_temp_value(self, pAdcCode):
        """
        按 NTC 电阻公式，由 ADC code(测得的分压值）算出对应的温度值
        计算结果是摄氏度为单位
        :param pAdcCode: ADC 采样到的数据。十六进制或 int 格式均可以
        :return: 计算所得温度值，int 格式
        """
        if 65535 == pAdcCode:
            return -170
        elif 0 == pAdcCode:
            return 170
        else:
            return (NTC_B / (np.log((R_THERM / (65535/pAdcCode - 1)) * (1/R0_NTC)) + NTC_B/NTC_TO)) - 273.15


    def pushBtn_disable(self, pBtn):
        """
        disable push button and set its background color is gray
        :param pBtn: push button object
        :return:
        """
        current_style = pBtn.styleSheet()
        new_style = current_style + " QPushButton {background-color: #d0d0d0;}"
        pBtn.setStyleSheet(new_style)
        pBtn.setDisabled(True)

    def pushBtn_enable(self, pBtn, pBkgdColor):
        """
        enable push button and restore its background color
        :param pBtn: push button object
        :param pBkgdColor: restore color
        :return:
        """
        current_style = pBtn.styleSheet()
        # temStr = " QPushButton {background-color: " + pBkgdColor + ";}"
        # new_style = current_style + temStr
        new_style = current_style + " QPushButton {background-color: " + pBkgdColor + ";}"
        pBtn.setStyleSheet(new_style)
        pBtn.setDisabled(False)

    def slot_menu_load(self):
        ''' open file '''
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileNames(self, "选取文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")

        if SCRIPT_DEBUG:
            print("\r\n")
            print(f"file name is: ", fileName)

        ''' read device0 id '''
        if len(fileName) == 1:
            # At Initialization read devid and load alpha coefficents
            DEV0ID = (pb01_read_device(self.hidBdg, 0x00, 0x00, 0x00) << 32) \
                    + (pb01_read_device(self.hidBdg, 0x00, 0x01, 0x00) << 16) \
                    + pb01_read_device(self.hidBdg, 0x00, 0x02, 0x00)       # read DEVID0/1/2 registers
            alpha_coeff = json.load(open(fileName[0], "r"))
            dev0_afa2_adc1_p1 = -float(alpha_coeff[str(DEV0ID)]["afa2_adc1_p1"]) / 2 ** 40
            dev0_afa1_adc1_p1 = float(alpha_coeff[ str(DEV0ID)]["afa1_adc1_p1"]) / 2 ** 31
            dev0_afa0_adc1_p1 = float(alpha_coeff[ str(DEV0ID)]["afa0_adc1_p1"]) / 2 ** 16
            dev0_afa2_adc1_p2 = -float(alpha_coeff[str(DEV0ID)]["afa2_adc1_p2"]) / 2 ** 40
            dev0_afa1_adc1_p2 = float(alpha_coeff[ str(DEV0ID)]["afa1_adc1_p2"]) / 2 ** 31
            dev0_afa0_adc1_p2 = float(alpha_coeff[ str(DEV0ID)]["afa0_adc1_p2"]) / 2 ** 16
            dev0_afa2_adc2_p1 = -float(alpha_coeff[str(DEV0ID)]["afa2_adc2_p1"]) / 2 ** 40
            dev0_afa1_adc2_p1 = float(alpha_coeff[ str(DEV0ID)]["afa1_adc2_p1"]) / 2 ** 31
            dev0_afa0_adc2_p1 = float(alpha_coeff[ str(DEV0ID)]["afa0_adc2_p1"]) / 2 ** 16
            dev0_afa2_adc2_p2 = -float(alpha_coeff[str(DEV0ID)]["afa2_adc2_p2"]) / 2 ** 40
            dev0_afa1_adc2_p2 = float(alpha_coeff[ str(DEV0ID)]["afa1_adc2_p2"]) / 2 ** 31
            dev0_afa0_adc2_p2 = float(alpha_coeff[ str(DEV0ID)]["afa0_adc2_p2"]) / 2 ** 16
            self.dev0ParList = [dev0_afa2_adc1_p1,
                                dev0_afa1_adc1_p1,
                                dev0_afa0_adc1_p1,
                                dev0_afa2_adc1_p2,
                                dev0_afa1_adc1_p2,
                                dev0_afa0_adc1_p2,
                                dev0_afa2_adc2_p1,
                                dev0_afa1_adc2_p1,
                                dev0_afa0_adc2_p1,
                                dev0_afa2_adc2_p2,
                                dev0_afa1_adc2_p2,
                                dev0_afa0_adc2_p2]
            ''' read device1 id '''
        elif len(fileName) == 2:
            DEV1ID = (pb01_read_device(self.hidBdg, 0x01, 0x00, 0x00) << 32) \
                     + (pb01_read_device(self.hidBdg, 0x01, 0x01, 0x00) << 16) \
                     + pb01_read_device(self.hidBdg, 0x01, 0x02, 0x00)  # read DEVID0/1/2 registers
            alpha_coeff = json.load(open(fileName[1], "r"))
            dev1_afa2_adc1_p1 = -float(alpha_coeff[str(DEV1ID)]["afa2_adc1_p1"]) / 2 ** 40
            dev1_afa1_adc1_p1 = float(alpha_coeff[ str(DEV1ID)]["afa1_adc1_p1"]) / 2 ** 31
            dev1_afa0_adc1_p1 = float(alpha_coeff[ str(DEV1ID)]["afa0_adc1_p1"]) / 2 ** 16
            dev1_afa2_adc1_p2 = -float(alpha_coeff[str(DEV1ID)]["afa2_adc1_p2"]) / 2 ** 40
            dev1_afa1_adc1_p2 = float(alpha_coeff[ str(DEV1ID)]["afa1_adc1_p2"]) / 2 ** 31
            dev1_afa0_adc1_p2 = float(alpha_coeff[ str(DEV1ID)]["afa0_adc1_p2"]) / 2 ** 16
            dev1_afa2_adc2_p1 = -float(alpha_coeff[str(DEV1ID)]["afa2_adc2_p1"]) / 2 ** 40
            dev1_afa1_adc2_p1 = float(alpha_coeff[ str(DEV1ID)]["afa1_adc2_p1"]) / 2 ** 31
            dev1_afa0_adc2_p1 = float(alpha_coeff[ str(DEV1ID)]["afa0_adc2_p1"]) / 2 ** 16
            dev1_afa2_adc2_p2 = -float(alpha_coeff[str(DEV1ID)]["afa2_adc2_p2"]) / 2 ** 40
            dev1_afa1_adc2_p2 = float(alpha_coeff[ str(DEV1ID)]["afa1_adc2_p2"]) / 2 ** 31
            dev1_afa0_adc2_p2 = float(alpha_coeff[ str(DEV1ID)]["afa0_adc2_p2"]) / 2 ** 16
            self.dev1ParList = [dev1_afa2_adc1_p1,
                                dev1_afa1_adc1_p1,
                                dev1_afa0_adc1_p1,
                                dev1_afa2_adc1_p2,
                                dev1_afa1_adc1_p2,
                                dev1_afa0_adc1_p2,
                                dev1_afa2_adc2_p1,
                                dev1_afa1_adc2_p1,
                                dev1_afa0_adc2_p1,
                                dev1_afa2_adc2_p2,
                                dev1_afa1_adc2_p2,
                                dev1_afa0_adc2_p2]


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


    def slot_pushBtn_chainCfg_cfg(self):
        time.sleep(BTN_OP_DELAY)

        """ re-setup chainCfgPage cfgWarn bar """
        self.set_default_warn_bar(self.lineEdit_chainCfg_cfgWarn)
        self.set_default_warn_bar(self.lineEdit_chainCfg_pwrUpWarn)

        """ initial daisy chain """
        daisyChainReturn = pb01_daisy_chain_initial(self.hidBdg, 0x00)
        if ((daisyChainReturn == "transaction5 time out") or
            (daisyChainReturn == "transaction7 time out") or
            (daisyChainReturn == "transaction13 time out") or
            (daisyChainReturn == "HELLOALL message return error") or
            (daisyChainReturn == "clear bridge rx buffer time out")):
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
            else:
                if SCRIPT_DEBUG:
                    print(f"initial daisy-chain successfully")
                else:
                    pass

        """ write and read all UIFCFG register """
        ''' set uppath, enable dc byte & alive count '''
        rtUifCfg = self.afe_write_read_all(0x10, 0x2600)  # write all A10=0x2600
        if rtUifCfg != False:
            if self.flagSingleAfe:  # single afe
                rdDataDev0 = (rtUifCfg[1]<<8) | rtUifCfg[0]
                self.update_table_item_data(self.table_chainCfg_uifcfgReg, 0, 3, hex(rdDataDev0)[2:].upper())

                bitsDev0 = (rdDataDev0>>7) & 0x1FF
                for i in range(9):
                    bitValue = (bitsDev0>>i) & 1
                    self.update_table_item_data(self.table_chainCfg_uifcfgReg, 0, 12-i, str(bitValue))
            else:   # dual afe
                rdDataDev0 = (rtUifCfg[3] << 8) | rtUifCfg[2]
                rdDataDev1 = (rtUifCfg[1] << 8) | rtUifCfg[0]
                self.update_table_item_data(self.table_chainCfg_uifcfgReg, 0, 3,
                                            hex(rdDataDev0)[2:].upper())  # device 0
                self.update_table_item_data(self.table_chainCfg_uifcfgReg, 1, 3,
                                            hex(rdDataDev1)[2:].upper())  # device 1

                bitsDev0 = (rdDataDev0 >> 7) & 0x1FF
                bitsDev1 = (rdDataDev1 >> 7) & 0x1FF
                for i in range(9):
                    bitValueDev0 = (bitsDev0 >> i) & 1
                    self.update_table_item_data(self.table_chainCfg_uifcfgReg, 0, 12-i, str(bitValueDev0)) # device 0
                    bitValueDev1 = (bitsDev1 >> i) & 1
                    self.update_table_item_data(self.table_chainCfg_uifcfgReg, 1, 12-i, str(bitValueDev1)) # device 1
        else:
            return

        """ write and read all ADDRCFG register """
        ''' set top & bottom address '''
        if self.flagSingleAfe:
            rtAddrCfg = self.afe_write_read_all(0x11, 0x0000)   # write all A11=0x0020
                                                                    # (topDevAddr = 0, botDevAddr = 0)
                                                                    # alseed=0x00
        else:
            rtAddrCfg = self.afe_write_read_all(0x11, 0x0020)   # write all A11=0x0020
                                                                    # (topDevAddr = 1, botDevAddr = 0)
                                                                    # alseed=0x00

        if rtAddrCfg != False:
            if self.flagSingleAfe:  # single afe
                rdDataDev0 = (rtAddrCfg[1] << 8) | rtAddrCfg[0]
                unlockBitDev0 = rdDataDev0 >> 15
                botAddrDev0 = (rdDataDev0 & 0x7C00) >> 10
                topAddrDev0 = (rdDataDev0 & 0x03E0) >> 5
                devAddrDev0 = rdDataDev0 & 0x001F
                listDataDev0 = [hex(rdDataDev0)[2:].upper().zfill(4), hex(unlockBitDev0)[2:].upper(),
                                hex(botAddrDev0)[2:].upper().zfill(2),
                                hex(topAddrDev0)[2:].upper().zfill(2), hex(devAddrDev0)[2:].upper().zfill(2)]
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
                listDataDev0 = [hex(rdDataDev0)[2:].upper().zfill(4), hex(unlockBitDev0)[2:].upper(),
                                hex(botAddrDev0)[2:].upper().zfill(2),
                                hex(topAddrDev0)[2:].upper().zfill(2), hex(devAddrDev0)[2:].upper().zfill(2)]
                listDataDev1 = [hex(rdDataDev1)[2:].upper().zfill(4), hex(unlockBitDev1)[2:].upper(),
                                hex(botAddrDev1)[2:].upper().zfill(2),
                                hex(topAddrDev1)[2:].upper().zfill(2), hex(devAddrDev1)[2:].upper().zfill(2)]
                for i in range(3, 8):
                    self.update_table_item_data(self.table_chainCfg_addcfgReg, 0, i,
                                                listDataDev0[i - 3])  # device 0
                    self.update_table_item_data(self.table_chainCfg_addcfgReg, 1, i,
                                                listDataDev1[i - 3])  # device 1
        else:
            return

        """ wait 10ms to complete FEMA2 BIST """
        time.sleep(0.01)

        """ read device 0 id block """
        rtIdBlkDev0 = pb01_read_block(self.hidBdg, 4, 0, 0x00, 0x00)  # read dev0 id block, alseed=0x00
        if rtIdBlkDev0 == "message return RX error" or rtIdBlkDev0 == "pec check error":
            self.message_box(rtIdBlkDev0)
            return
        else:
            devid0 =  (rtIdBlkDev0[4] << 8) | rtIdBlkDev0[3]
            devid1 =  (rtIdBlkDev0[6] << 8) | rtIdBlkDev0[5]
            devid2 =  (rtIdBlkDev0[8] << 8) | rtIdBlkDev0[7]
            version = (rtIdBlkDev0[10] << 8) | rtIdBlkDev0[9]
            generation = (version & 0xE000) >> 13
            chCnt = (version & 0x1F00) >> 8
            swVer = (version & 0x00F0) >> 4
            hwVer = version & 0x000F
            listIdDev0 = [hex(devid0)[2:].upper().zfill(4), hex(devid1)[2:].upper().zfill(4),
                          hex(devid2)[2:].upper().zfill(4), hex(version)[2:].upper().zfill(4),
                          str(generation), str(chCnt),
                          hex(swVer)[2:].upper(), hex(hwVer)[2:].upper()]
            for i in range(3, 11):
                self.update_table_item_data(self.table_chainCfg_devIdBlk, 0, i,
                                            listIdDev0[i - 3])  # device 0

        """ read device 1 id block """
        if self.flagSingleAfe == False:
            rtIdBlkDev1 = pb01_read_block(self.hidBdg, 4, 1, 0x00, 0x00)  # read dev1 id block, alseed=0x00
            if rtIdBlkDev1 == "message return RX error" or rtIdBlkDev1 == "pec check error":
                self.message_box(rtIdBlkDev1)
                return
            else:
                devid0 = (rtIdBlkDev1[4] << 8) | rtIdBlkDev1[3]
                devid1 = (rtIdBlkDev1[6] << 8) | rtIdBlkDev1[5]
                devid2 = (rtIdBlkDev1[8] << 8) | rtIdBlkDev1[7]
                version = (rtIdBlkDev1[10] << 8) | rtIdBlkDev1[9]
                generation = (version & 0xE000) >> 13
                chCnt = (version & 0x1F00) >> 8
                swVer = (version & 0x00F0) >> 4
                hwVer = version & 0x000F
                listIdDev1 = [hex(devid0)[2:].upper().zfill(4), hex(devid1)[2:].upper().zfill(4),
                              hex(devid2)[2:].upper().zfill(4), hex(version)[2:].upper().zfill(4),
                              str(generation), str(chCnt),
                              hex(swVer)[2:].upper(), hex(hwVer)[2:].upper()]
                for i in range(3, 11):
                    self.update_table_item_data(self.table_chainCfg_devIdBlk, 1, i,
                                                listIdDev1[i - 3])  # device 0

        ''' update status block table '''
        # update chainCfgPage status block table
        if not self.update_status_block_table(self.table_chainCfg_pw, 3, 5,
                                              self.ledChainPageDev0, self.ledChainPageDev1, False):
            return
        # update devMgPage status block tables
        if not self.update_status_block_table(self.table_devMgPage_init, 2, 7,
                                              self.ledDevMgPageInitDev0, self.ledDevMgPageInitDev1, False):
            return
        if not self.update_status_block_table(self.table_devMgPage_cur, 2, 7,
                                              self.ledDevMgPageCurDev0, self.ledDevMgPageCurDev1, True):
            return

        ''' update buttons status '''
        # chainCfg page (page 1)
        self.pushBtn_disable(self.pushButton_chainCfg_cfg)                  # configure
        self.pushBtn_enable(self.pushButton_chainCfg_reset, "#e84d00")      # reset
        # devMg page (page 2)
        self.pushBtn_enable(self.pushButton_devMgPage_init, "#3072B3")      # initialize


    def slot_pushBtn_chainCfg_reset(self):
        time.sleep(BTN_OP_DELAY)

        # reset max17841
        max17841_init(self.hidBdg)

        time.sleep(0.05)

        # force por
        if not pb01_por(self.hidBdg):
            self.message_box("Set PB01 POR fail")
            return

        # re-initial ui
        self.init_tab_pages()

        # reset max17841
        max17841_init(self.hidBdg)

        # delay 1s before enable configure button
        time.sleep(0.05)

        # enable configure button
        self.pushBtn_enable(self.pushButton_chainCfg_cfg, "#3072B3")
        # disable reset button
        self.pushBtn_disable(self.pushButton_chainCfg_reset)


    def slot_pushBtn_devMgPage_init(self):
        time.sleep(BTN_OP_DELAY)

        """ re-setup chainCfgPage cfgWarn bar """
        self.set_default_warn_bar(self.lineEdit_devMgPage_initWarn)

        """ clear status2 expected alerts """
        wrAllReturn = pb01_write_all(self.hidBdg, 0x05, 0x0080, 0x00)   # write all Reg05 = 0x0080, alseed=0x00
        if wrAllReturn == "message return RX error" or wrAllReturn == "pec check error":
            self.message_box(wrAllReturn)
            return

        """ clear status1 expected alerts """
        wrAllReturn = pb01_write_all(self.hidBdg, 0x04, 0x4000, 0x00)  # write all Reg05 = 0x4000, alseed=0x00
        if wrAllReturn == "message return RX error" or wrAllReturn == "pec check error":
            self.message_box(wrAllReturn)
            return

        """ delay before read status block back """
        time.sleep(0.01)

        """ update status block table """
        # update devMgPage status block tables
        if not self.update_status_block_table(self.table_devMgPage_init, 2, 7,
                                       self.ledDevMgPageInitDev0, self.ledDevMgPageInitDev1, False):
            return

        if not self.update_status_block_table(self.table_devMgPage_cur, 2, 7,
                                       self.ledDevMgPageCurDev0, self.ledDevMgPageCurDev1, True):
            return

        """ update buttons status """
        # disable
        self.pushBtn_disable(self.pushButton_devMgPage_init)                # initialize
        # enable
        self.pushBtn_enable(self.pushButton_devMgPage_reInit, "#ED7D31")    # reinitialize
        self.pushBtn_enable(self.pushButton_devMgPage_clear, "#FFC000")     # clear comm
        self.pushBtn_enable(self.pushButton_devMgPage_readBack, "#00B050")  # read back


    def slot_pushBtn_devMgPage_reinit(self):
        time.sleep(BTN_OP_DELAY)

        """ re-setup chainCfgPage cfgWarn bar """
        self.set_default_warn_bar(self.lineEdit_devMgPage_initWarn)

        """ clear fmea2 expected alerts """
        wrAllReturn = pb01_write_all(self.hidBdg, 0x07, 0x0004, 0x00)  # write all Reg07 = 0x0004, alseed=0x00
        if wrAllReturn == "message return RX error" or wrAllReturn == "pec check error":
            self.message_box(wrAllReturn)
            return

        """ clear fmea1 expected alerts """
        wrAllReturn = pb01_write_all(self.hidBdg, 0x06, 0x87FF, 0x00)  # write all Reg06 = 0x87FF, alseed=0x00
        if wrAllReturn == "message return RX error" or wrAllReturn == "pec check error":
            self.message_box(wrAllReturn)
            return

        """ clear status2 expected alerts """
        wrAllReturn = pb01_write_all(self.hidBdg, 0x05, 0xFF8F, 0x00)  # write all Reg05 = 0xFF8F, alseed=0x00
        if wrAllReturn == "message return RX error" or wrAllReturn == "pec check error":
            self.message_box(wrAllReturn)
            return

        """ clear status1 expected alerts """
        wrAllReturn = pb01_write_all(self.hidBdg, 0x04, 0x2000, 0x00)  # write all Reg04 = 0x2000, alseed=0x00
        if wrAllReturn == "message return RX error" or wrAllReturn == "pec check error":
            self.message_box(wrAllReturn)
            return

        """ clear status1 expected alerts """
        wrAllReturn = pb01_write_all(self.hidBdg, 0x04, 0x4000, 0x00)  # write all Reg04 = 0x4000, alseed=0x00
        if wrAllReturn == "message return RX error" or wrAllReturn == "pec check error":
            self.message_box(wrAllReturn)
            return

        """ delay before read status block back """
        time.sleep(0.01)

        """ update status block table """
        # update devMgPage status block tables
        if not self.update_status_block_table(self.table_devMgPage_init, 2, 7,
                                       self.ledDevMgPageInitDev0, self.ledDevMgPageInitDev1, False):
            return

        if not self.update_status_block_table(self.table_devMgPage_cur, 2, 7,
                                       self.ledDevMgPageCurDev0, self.ledDevMgPageCurDev1, True):
            return


    def slot_pushBtn_devMgPage_clear(self):
        time.sleep(BTN_OP_DELAY)

        """ re-setup chainCfgPage cfgWarn bar """
        self.set_default_warn_bar(self.lineEdit_devMgPage_initWarn)

        """ clear status2 expected alerts """
        wrAllReturn = pb01_write_all(self.hidBdg, 0x05, 0xFF8F, 0x00)  # write all Reg05 = 0xFF8F, alseed=0x00
        if wrAllReturn == "message return RX error" or wrAllReturn == "pec check error":
            self.message_box(wrAllReturn)
            return

        """ clear status1 expected alerts """
        wrAllReturn = pb01_write_all(self.hidBdg, 0x04, 0x2000, 0x00)  # write all Reg04 = 0x2000, alseed=0x00
        if wrAllReturn == "message return RX error" or wrAllReturn == "pec check error":
            self.message_box(wrAllReturn)
            return

        """ delay before read status block back """
        time.sleep(0.01)

        """ read each status register and update DC byte """
        self.read_dc_and_status(self.table_devMgPage_dc, self.ledDevMgPageDcByte, self.ledDevMgPageAlertPk,
                                self.table_devMgPage_cur, self.ledDevMgPageCurDev0, self.ledDevMgPageCurDev1)


    def slot_pushBtn_devMgPage_readBack(self):
        time.sleep(BTN_OP_DELAY)
        """ read each status register and update DC byte """
        self.read_dc_and_status(self.table_devMgPage_dc, self.ledDevMgPageDcByte, self.ledDevMgPageAlertPk,
                                self.table_devMgPage_cur, self.ledDevMgPageCurDev0, self.ledDevMgPageCurDev1)


    def slot_pushBtn_appCfgPage_appCfgWR(self):
        time.sleep(BTN_OP_DELAY)
        staCfgData = int(self.table_appCfgPage_appCfg.item(0, 2).text(), 16)
        self.update_write_read_op(0x12, staCfgData, self.table_appCfgPage_appCfg, 0, 7)     # STATUSCFG R12=0x3FFF

        devCfgData = int(self.table_appCfgPage_appCfg.item(1, 2).text(), 16)
        self.update_write_read_op(0x13, devCfgData, self.table_appCfgPage_appCfg, 1, 7)     # DEVCFG R13=0x2000

        self.polCfgValue = int(self.table_appCfgPage_appCfg.item(2, 2).text(), 16)
        self.update_write_read_op(0x14, self.polCfgValue, self.table_appCfgPage_appCfg, 2, 7)   # customize POLYCFG

        axGpioData = int(self.table_appCfgPage_appCfg.item(3, 2).text(), 16)
        self.update_write_read_op(0x15, axGpioData, self.table_appCfgPage_appCfg, 3, 7)    # customize AUXGPIOCFG

        self.auxRefCfgVal = int(self.table_appCfgPage_appCfg.item(4, 2).text(), 16)
        self.update_write_read_op(0x16, self.auxRefCfgVal, self.table_appCfgPage_appCfg, 4, 7)     # customize AUXREFCFG


    def slot_pushBtn_appCfgPage_appCfgRd(self):
        time.sleep(BTN_OP_DELAY)
        self.update_config_readback_op(0x12, self.table_appCfgPage_appCfg, 0, 7)    # STATUSCFG
        self.update_config_readback_op(0x13, self.table_appCfgPage_appCfg, 1, 7)    # DEVCFG
        self.update_config_readback_op(0x14, self.table_appCfgPage_appCfg, 2, 7)    # POLYCFG
        self.update_config_readback_op(0x15, self.table_appCfgPage_appCfg, 3, 7)    # AUXGPIOCFG
        self.update_config_readback_op(0x16, self.table_appCfgPage_appCfg, 4, 7)    # AUXREFCFG

    def slot_table_appCfgPage_appCfg_cellChange(self):
        """ POLARITYCFG content """
        polCfgText = self.table_appCfgPage_appCfg.item(2, 2).text()
        self.table_appCfgPage_appCfg.item(2, 3).setText(hex_to_bin(polCfgText[0:2]))     # msb
        self.table_appCfgPage_appCfg.item(2, 5).setText(hex_to_bin(polCfgText[2:]))     # lsb

        """ AUXGPIOCFG """
        auxGpioText = self.table_appCfgPage_appCfg.item(3, 2).text()
        self.table_appCfgPage_appCfg.item(3, 3).setText(hex_to_bin(auxGpioText[0:2]))  # msb
        self.table_appCfgPage_appCfg.item(3, 5).setText(hex_to_bin(auxGpioText[2:]))   # lsb

        """ AUXREFCFG """
        auxRefText = self.table_appCfgPage_appCfg.item(4, 2).text()
        self.table_appCfgPage_appCfg.item(4, 3).setText(hex_to_bin(auxRefText[0])[0:2])  # msb
        self.table_appCfgPage_appCfg.item(4, 5).setText(hex_to_bin(auxRefText[2:]))   # lsb



    def slot_pushBtn_appCfgPage_alertCfgWR(self):
        time.sleep(BTN_OP_DELAY)

        altOvCfgData = int(self.table_appCfgPage_alertCfg.item(0, 2).text(), 16)
        self.update_write_read_op(0x18, altOvCfgData, self.table_appCfgPage_alertCfg, 0, 7)  # ALRTOVCFG R18=0xFFFF

        altUvCfgData = int(self.table_appCfgPage_alertCfg.item(1, 2).text(), 16)
        self.update_write_read_op(0x19, altUvCfgData, self.table_appCfgPage_alertCfg, 1, 7)  # ALRTUVCFG R19=0xFFFF

        altAuxOvCfgData = int(self.table_appCfgPage_alertCfg.item(2, 2).text(), 16)
        self.update_write_read_op(0x1A, altAuxOvCfgData, self.table_appCfgPage_alertCfg, 2, 7)  # ALRTAUXOVCFG R1A=0xFFFF

        altAuxUvCfgData = int(self.table_appCfgPage_alertCfg.item(3, 2).text(), 16)
        self.update_write_read_op(0x1B, altAuxUvCfgData, self.table_appCfgPage_alertCfg, 3, 7)  # ALRTAUXUVCFG R1B=0xFFFF


    def slot_pushBtn_appCfgPage_alertCfgRd(self):
        time.sleep(BTN_OP_DELAY)
        self.update_config_readback_op(0x18, self.table_appCfgPage_alertCfg, 0, 7)  # ALRTOVCFG
        self.update_config_readback_op(0x19, self.table_appCfgPage_alertCfg, 1, 7)  # ALRTUVCFG
        self.update_config_readback_op(0x1A, self.table_appCfgPage_alertCfg, 2, 7)  # ALRTAUXOVCFG
        self.update_config_readback_op(0x1B, self.table_appCfgPage_alertCfg, 3, 7)  # ALRTAUXUVCFG


    def slot_pushBtn_appCfgPage_thresholdRegWR(self):
        time.sleep(BTN_OP_DELAY)

        ovThRegData = int(self.table_appCfgPage_thresholdReg.item(0, 2).text(), 16)
        self.update_write_read_op(0x20, ovThRegData, self.table_appCfgPage_thresholdReg, 0, 7)  # OVTHREG

        uvThRegData = int(self.table_appCfgPage_thresholdReg.item(1, 2).text(), 16)
        self.update_write_read_op(0x21, uvThRegData, self.table_appCfgPage_thresholdReg, 1, 7)  # UVTREG

        bipOvThRegData = int(self.table_appCfgPage_thresholdReg.item(2, 2).text(), 16)
        self.update_write_read_op(0x22, bipOvThRegData, self.table_appCfgPage_thresholdReg, 2, 7)  # BIPOVTHREG

        bipUvThRegData = int(self.table_appCfgPage_thresholdReg.item(3, 2).text(), 16)
        self.update_write_read_op(0x23, bipUvThRegData, self.table_appCfgPage_thresholdReg, 3, 7)  # BIPUVTHREG

        altOvThRegData = int(self.table_appCfgPage_thresholdReg.item(4, 2).text(), 16)
        self.update_write_read_op(0x24, altOvThRegData, self.table_appCfgPage_thresholdReg, 4, 7)  # ALTOVTHREG

        altUvThRegData = int(self.table_appCfgPage_thresholdReg.item(5, 2).text(), 16)
        self.update_write_read_op(0x25, altUvThRegData, self.table_appCfgPage_thresholdReg, 5, 7)  # ALTUVTHREG

        altBipOvThRegData = int(self.table_appCfgPage_thresholdReg.item(6, 2).text(), 16)
        self.update_write_read_op(0x26, altBipOvThRegData, self.table_appCfgPage_thresholdReg, 6, 7)  # ALTBIPOVTHREG

        altBipUvThRegData = int(self.table_appCfgPage_thresholdReg.item(7, 2).text(), 16)
        self.update_write_read_op(0x27, altBipUvThRegData, self.table_appCfgPage_thresholdReg, 7, 7)  # ALTBIPUVTHREG

        auxrOvThRegData = int(self.table_appCfgPage_thresholdReg.item(8, 2).text(), 16)
        self.update_write_read_op(0x28, auxrOvThRegData, self.table_appCfgPage_thresholdReg, 8, 7)  # AUXROVTHREG

        auxrUvThRegData = int(self.table_appCfgPage_thresholdReg.item(9, 2).text(), 16)
        self.update_write_read_op(0x29, auxrUvThRegData, self.table_appCfgPage_thresholdReg, 9, 7)  # AUXRUVTHREG

        auxaOvThRegData = int(self.table_appCfgPage_thresholdReg.item(10, 2).text(), 16)
        self.update_write_read_op(0x2A, auxaOvThRegData, self.table_appCfgPage_thresholdReg, 10, 7) # AUXAOVTHREG

        auxaUvThRegData = int(self.table_appCfgPage_thresholdReg.item(11, 2).text(), 16)
        self.update_write_read_op(0x2B, auxaUvThRegData, self.table_appCfgPage_thresholdReg, 11, 7) # AUXAUVTHREG

        mmThRegData = int(self.table_appCfgPage_thresholdReg.item(12, 2).text(), 16)
        self.update_write_read_op(0x2C, mmThRegData, self.table_appCfgPage_thresholdReg, 12, 7) # MMTHREG

        tempThData = int(self.table_appCfgPage_thresholdReg.item(13, 2).text(), 16)
        self.update_write_read_op(0x2D, tempThData, self.table_appCfgPage_thresholdReg, 13, 7)  # TEMPTHREG customized


    def slot_pushBtn_appCfgPage_thresholdRegRd(self):
        time.sleep(BTN_OP_DELAY)
        self.update_config_readback_op(0x20, self.table_appCfgPage_thresholdReg, 0,  7)  # OVTHREG
        self.update_config_readback_op(0x21, self.table_appCfgPage_thresholdReg, 1,  7)  # UVTREG
        self.update_config_readback_op(0x22, self.table_appCfgPage_thresholdReg, 2,  7)  # BIPOVTHREG
        self.update_config_readback_op(0x23, self.table_appCfgPage_thresholdReg, 3,  7)  # BIPUVTHREG
        self.update_config_readback_op(0x24, self.table_appCfgPage_thresholdReg, 4,  7)  # ALTOVTHREG
        self.update_config_readback_op(0x25, self.table_appCfgPage_thresholdReg, 5,  7)  # ALTUVTHREG
        self.update_config_readback_op(0x26, self.table_appCfgPage_thresholdReg, 6,  7)  # ALTBIPOVTHREG
        self.update_config_readback_op(0x27, self.table_appCfgPage_thresholdReg, 7,  7)  # ALTBIPUVTHREG
        self.update_config_readback_op(0x28, self.table_appCfgPage_thresholdReg, 8,  7)  # AUXROVTHREG
        self.update_config_readback_op(0x29, self.table_appCfgPage_thresholdReg, 9,  7)  # AUXRUVTHREG
        self.update_config_readback_op(0x2A, self.table_appCfgPage_thresholdReg, 10, 7)  # AUXAOVTHREG
        self.update_config_readback_op(0x2B, self.table_appCfgPage_thresholdReg, 11, 7)  # AUXAUVTHREG
        self.update_config_readback_op(0x2C, self.table_appCfgPage_thresholdReg, 12, 7)  # MMTHREG
        self.update_config_readback_op(0x2D, self.table_appCfgPage_thresholdReg, 13, 7)  # TEMPTHREG


    def slot_table_appCfgPage_thReg_cellChange(self):
        """ TEMPTHREG """
        temThText = self.table_appCfgPage_thresholdReg.item(13, 2).text()
        temC = str(round(int(temThText,16) / 8 - 273.15, 2))
        temF = str(round((int(temThText,16) / 8 - 273.15) * 9 / 5 + 32, 2))

        self.table_appCfgPage_thresholdReg.item(13, 3).setText(temC)
        self.table_appCfgPage_thresholdReg.item(13, 5).setText(temF)


    def slot_pushBtn_appCfgPage_acqRegWr(self):
        time.sleep(BTN_OP_DELAY)

        acqDly1Data = int(self.table_appCfgPage_acqReg.item(0, 2).text(), 16)
        self.update_write_read_op(0x40, acqDly1Data, self.table_appCfgPage_acqReg, 0, 7)  # ACQDLY1

        acqDly2Data = int(self.table_appCfgPage_acqReg.item(1, 2).text(), 16)
        self.update_write_read_op(0x41, acqDly2Data, self.table_appCfgPage_acqReg, 1, 7)  # ACQDLY2

        acqChSelData = int(self.table_appCfgPage_acqReg.item(2, 2).text(), 16)
        self.update_write_read_op(0x42, acqChSelData, self.table_appCfgPage_acqReg, 2, 7)  # ACQCHSEL

        acqAuxSelData = int(self.table_appCfgPage_acqReg.item(3, 2).text(), 16)
        self.update_write_read_op(0x43, acqAuxSelData, self.table_appCfgPage_acqReg, 3, 7)  # ACQAUXSEL


    def slot_pushBtn_appCfgPage_acqRegRd(self):
        time.sleep(BTN_OP_DELAY)
        self.update_config_readback_op(0x40, self.table_appCfgPage_acqReg, 0, 7)  # ACQDLY1
        self.update_config_readback_op(0x41, self.table_appCfgPage_acqReg, 1, 7)  # ACQDLY2
        self.update_config_readback_op(0x42, self.table_appCfgPage_acqReg, 2, 7)  # ACQCHSEL
        self.update_config_readback_op(0x43, self.table_appCfgPage_acqReg, 3, 7)  # ACQAUXSEL


    def slot_pushBtn_diagCfgPage_curCfgWR(self):
        time.sleep(BTN_OP_DELAY)

        ctstCfg1Data = int(self.table_diagCfgPage_testCurCfgReg.item(0, 2).text(), 16)
        self.update_write_read_op(0x1C, ctstCfg1Data, self.table_diagCfgPage_testCurCfgReg, 0, 11)  # CTSTCFG1

        ctstCfg2Data = int(self.table_diagCfgPage_testCurCfgReg.item(1, 2).text(), 16)
        self.update_write_read_op(0x1D, ctstCfg2Data, self.table_diagCfgPage_testCurCfgReg, 1, 11)  # CTSTCFG2

        auxTstCfgData = int(self.table_diagCfgPage_testCurCfgReg.item(2, 2).text(), 16)
        self.update_write_read_op(0x1E, auxTstCfgData, self.table_diagCfgPage_testCurCfgReg, 2, 11)  # AUXTSTCFG


    def slot_pushBtn_diagCfgPage_curCfgRd(self):
        time.sleep(BTN_OP_DELAY)
        self.update_config_readback_op(0x1C, self.table_diagCfgPage_testCurCfgReg, 0, 11)  # CTSTCFG1
        self.update_config_readback_op(0x1D, self.table_diagCfgPage_testCurCfgReg, 1, 11)  # CTSTCFG1
        self.update_config_readback_op(0x1E, self.table_diagCfgPage_testCurCfgReg, 2, 11)  # AUXTSTCFG


    def slot_pushBtn_diagCfgPage_diagThWR(self):
        time.sleep(BTN_OP_DELAY)

        balShrtUvThRegData = int(self.table_diagCfgPage_diagThresReg.item(0, 2).text(), 16)
        self.update_write_read_op(0x2F, balShrtUvThRegData, self.table_diagCfgPage_diagThresReg, 0, 7)  # BALSHRTUVTHREG

        balOvThRegData = int(self.table_diagCfgPage_diagThresReg.item(1, 2).text(), 16)
        self.update_write_read_op(0x30, balOvThRegData, self.table_diagCfgPage_diagThresReg, 1, 7)  # BALOVTHREG

        balUvThRegData = int(self.table_diagCfgPage_diagThresReg.item(2, 2).text(), 16)
        self.update_write_read_op(0x31, balUvThRegData, self.table_diagCfgPage_diagThresReg, 2, 7)  # BALUVTHREG

        cellOpnOvThRegData = int(self.table_diagCfgPage_diagThresReg.item(3, 2).text(), 16)
        self.update_write_read_op(0x32, cellOpnOvThRegData, self.table_diagCfgPage_diagThresReg, 3, 7)  # CELLOPNOVTHREG

        cellOpnUvThRegData = int(self.table_diagCfgPage_diagThresReg.item(4, 2).text(), 16)
        self.update_write_read_op(0x33, cellOpnUvThRegData, self.table_diagCfgPage_diagThresReg, 4, 7)  # CELLOPNUVTHREG

        busOpnOvThRegData = int(self.table_diagCfgPage_diagThresReg.item(5, 2).text(), 16)
        self.update_write_read_op(0x34, busOpnOvThRegData, self.table_diagCfgPage_diagThresReg, 5, 7)  # BUSOPNOVTHREG

        busOpnUvThRegData = int(self.table_diagCfgPage_diagThresReg.item(6, 2).text(), 16)
        self.update_write_read_op(0x35, busOpnUvThRegData, self.table_diagCfgPage_diagThresReg, 6, 7)  # BUSOPNUVTHREG

        cellHvmOvThRegData = int(self.table_diagCfgPage_diagThresReg.item(7, 2).text(), 16)
        self.update_write_read_op(0x36, cellHvmOvThRegData, self.table_diagCfgPage_diagThresReg, 7, 7)  # CELLHVMOVTHREG

        cellHvmUvThRegData = int(self.table_diagCfgPage_diagThresReg.item(8, 2).text(), 16)
        self.update_write_read_op(0x37, cellHvmUvThRegData, self.table_diagCfgPage_diagThresReg, 8, 7)  # CELLHVMUVTHREG

        busHvmOvThRegData = int(self.table_diagCfgPage_diagThresReg.item(9, 2).text(), 16)
        self.update_write_read_op(0x38, busHvmOvThRegData, self.table_diagCfgPage_diagThresReg, 9, 7)  # BUSHVMOVTHREG

        busHvmUvThRegData = int(self.table_diagCfgPage_diagThresReg.item(10, 2).text(), 16)
        self.update_write_read_op(0x39, busHvmUvThRegData, self.table_diagCfgPage_diagThresReg, 10, 7)  # BUSHVMUVTHREG

        auxrDiagOvThRegData = int(self.table_diagCfgPage_diagThresReg.item(11, 2).text(), 16)
        self.update_write_read_op(0x3A, auxrDiagOvThRegData, self.table_diagCfgPage_diagThresReg, 11, 7)  # AUXRDIAGOVTHREG

        auxrDiagUvThRegData = int(self.table_diagCfgPage_diagThresReg.item(12, 2).text(), 16)
        self.update_write_read_op(0x3B, auxrDiagUvThRegData, self.table_diagCfgPage_diagThresReg, 12, 7)  # AUXRDIAGUVTHREG


    def slot_pushBtn_diagCfgPage_diagThRd(self):
        time.sleep(BTN_OP_DELAY)
        self.update_config_readback_op(0x2F, self.table_diagCfgPage_diagThresReg, 0, 7)  # BALSHRTUVTHREG
        self.update_config_readback_op(0x30, self.table_diagCfgPage_diagThresReg, 1, 7)  # BALOVTHREG
        self.update_config_readback_op(0x31, self.table_diagCfgPage_diagThresReg, 2, 7)  # BALUVTHREG
        self.update_config_readback_op(0x32, self.table_diagCfgPage_diagThresReg, 3, 7)  # CELLOPNOVTHREG
        self.update_config_readback_op(0x33, self.table_diagCfgPage_diagThresReg, 4, 7)  # CELLOPNUVTHREG
        self.update_config_readback_op(0x34, self.table_diagCfgPage_diagThresReg, 5, 7)  # BUSOPNOVTHREG
        self.update_config_readback_op(0x35, self.table_diagCfgPage_diagThresReg, 6, 7)  # BUSOPNUVTHREG
        self.update_config_readback_op(0x36, self.table_diagCfgPage_diagThresReg, 7, 7)  # CELLHVMOVTHREG
        self.update_config_readback_op(0x37, self.table_diagCfgPage_diagThresReg, 8, 7)  # CELLHVMUVTHREG
        self.update_config_readback_op(0x38, self.table_diagCfgPage_diagThresReg, 9, 7)  # BUSHVMOVTHREG
        self.update_config_readback_op(0x39, self.table_diagCfgPage_diagThresReg, 10, 7)  # BUSHVMUVTHREG
        self.update_config_readback_op(0x3A, self.table_diagCfgPage_diagThresReg, 11, 7)  # AUXRDIAGOVTHREG
        self.update_config_readback_op(0x3B, self.table_diagCfgPage_diagThresReg, 12, 7)  # AUXRDIAGUVTHREG


    def slot_pushBtn_diagCfgPage_aluTeWR(self):
        time.sleep(BTN_OP_DELAY)

        aluTestARegData = int(self.table_diagCfgPage_aluTestDiagReg.item(0, 2).text(), 16)
        self.update_write_read_op(0x3C, aluTestARegData, self.table_diagCfgPage_aluTestDiagReg, 0, 7)  # ALUTESTAREG

        aluTestBRegData = int(self.table_diagCfgPage_aluTestDiagReg.item(1, 2).text(), 16)
        self.update_write_read_op(0x3D, aluTestBRegData, self.table_diagCfgPage_aluTestDiagReg, 1, 7)  # ALUTESTBREG

        aluTestCRegData = int(self.table_diagCfgPage_aluTestDiagReg.item(2, 2).text(), 16)
        self.update_write_read_op(0x3E, aluTestCRegData, self.table_diagCfgPage_aluTestDiagReg, 2, 7)  # ALUTESTCREG

        aluTestDRegData = int(self.table_diagCfgPage_aluTestDiagReg.item(3, 2).text(), 16)
        self.update_write_read_op(0x3F, aluTestDRegData, self.table_diagCfgPage_aluTestDiagReg, 3, 7)  # ALUTESTDREG


    def slot_pushBtn_diagCfgPage_aluTeRd(self):
        time.sleep(BTN_OP_DELAY)
        self.update_config_readback_op(0x3C, self.table_diagCfgPage_aluTestDiagReg, 0, 7)  # ALUTESTAREG
        self.update_config_readback_op(0x3D, self.table_diagCfgPage_aluTestDiagReg, 1, 7)  # ALUTESTBREG
        self.update_config_readback_op(0x3E, self.table_diagCfgPage_aluTestDiagReg, 2, 7)  # ALUTESTCREG
        self.update_config_readback_op(0x3F, self.table_diagCfgPage_aluTestDiagReg, 3, 7)  # ALUTESTDREG


    def pb01_read_reg(self, pRegAddr):
        """
        读取 pb01 dev0 某个寄存器的值
        该函数由 acqReqPage 和 cblPage 页面中各 radio 槽函数使用
        用于通过点击 radio 配置对应的寄存器前先读取该寄存器的值
        :param pRegAddr: 寄存器地址
        :return: 按 int 格式返回寄存器中数据，即寄存器数据的 int 值
        """
        rdData = pb01_read_device(self.hidBdg, 0x00, pRegAddr, 0x00)
        if rdData == "message return RX error" or rdData == "pec check error":
            self.message_box(rdData)
            return False
        else:
            return rdData


    def solt_radioBtn_acqReqPage_acqcbalint(self):
        if self.radioButton_acqReqPage_acqcbalint.isChecked():
            if not self.flag_radio_acqReqPage_acqcbalint:  # 之前是 check 状态会进到这里，执行后变成 uncheck 状态
                self.radioButton_acqReqPage_acqcbalint.setAutoExclusive(False)
                self.radioButton_acqReqPage_acqcbalint.setChecked(False)
                self.radioButton_acqReqPage_acqcbalint.setAutoExclusive(True)
                self.flag_radio_acqReqPage_acqcbalint = True
                self.acqCtrlVal &= 0xF7FF
                self.table_acqReqPage_acqReq.item(0,2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))
                if not self.flagSingleAfe:
                    self.table_acqReqPage_acqReq.item(1, 2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))
            else:   # 之前是 uncheck 状态会进到这里，执行后变成 check 状态
                self.flag_radio_acqReqPage_acqcbalint = False
                self.radioButton_acqReqPage_acqcbalint.setChecked(True)
                self.acqCtrlVal |= 0x0800
                self.table_acqReqPage_acqReq.item(0, 2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))
                if not self.flagSingleAfe:
                    self.table_acqReqPage_acqReq.item(1, 2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))


    def solt_radioBtn_acqReqPage_acqiirinit(self):
        if self.radioButton_acqReqPage_acqiirinit.isChecked():
            if not self.flag_radio_acqReqPage_acqiirinit:  # 之前是 check 状态会进到这里，执行后变成 uncheck 状态
                self.radioButton_acqReqPage_acqiirinit.setAutoExclusive(False)
                self.radioButton_acqReqPage_acqiirinit.setChecked(False)
                self.radioButton_acqReqPage_acqiirinit.setAutoExclusive(True)
                self.flag_radio_acqReqPage_acqiirinit = True
                self.acqCtrlVal &= 0xFDFF
                self.table_acqReqPage_acqReq.item(0, 2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))
                if not self.flagSingleAfe:
                    self.table_acqReqPage_acqReq.item(1, 2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))
            else:  # 之前是 uncheck 状态会进到这里，执行后变成 check 状态
                self.flag_radio_acqReqPage_acqiirinit = False
                self.radioButton_acqReqPage_acqiirinit.setChecked(True)
                self.acqCtrlVal |= 0x0200
                self.table_acqReqPage_acqReq.item(0, 2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))
                if not self.flagSingleAfe:
                    self.table_acqReqPage_acqReq.item(1, 2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))


    def solt_radioGroup_acqReqPage_acqMode(self, button):
        """ 判断 Acquisition Mode group 中选择了哪个 radio button """
        self.acqMode = self.radioGroup_acqReqPage_acqMode.id(button)

        if self.acqMode == 1:       # normal acquisition acquisition
            ''' check ACQCBALINT & ACQIIRINT radio buttons and update self.acqCtrlVal '''
            # check ACQCBALINT
            self.radioButton_acqReqPage_acqcbalint.setChecked(True)
            self.flag_radio_acqReqPage_acqcbalint = False
            # check ACQIIRINT
            self.radioButton_acqReqPage_acqiirinit.setChecked(True)
            self.flag_radio_acqReqPage_acqiirinit = False
            # update self.acqCtrlVal
            self.acqCtrlVal = 0x0B40  # 工作在 normal acquisition mode 时 ACQCTRL[4:11] =0xB4
            self.acqCtrlVal |= self.acqMode  # 根据当前选择的 radio 设置 acquisition mode value
        elif self.acqMode == 2:     # redundant acquistion mode
            ''' check ACQCBALINT & ACQIIRINT radio buttons and update self.acqCtrlVal '''
            # check ACQCBALINT
            self.radioButton_acqReqPage_acqcbalint.setChecked(True)
            self.flag_radio_acqReqPage_acqcbalint = False
            # uncheck ACQIIRINT
            self.radioButton_acqReqPage_acqiirinit.setAutoExclusive(False)
            self.radioButton_acqReqPage_acqiirinit.setChecked(False)
            self.radioButton_acqReqPage_acqiirinit.setAutoExclusive(True)
            self.flag_radio_acqReqPage_acqiirinit = True
            # update self.acqCtrlVal
            self.acqCtrlVal = 0x0840  # 工作在 redundant acquisition mode 时 ACQCTRL[4:11] =0x84
            self.acqCtrlVal |= self.acqMode  # 根据当前选择的 radio 设置 acquisition mode value
        else:   # diagnostic mode
            ''' uncheck ACQCBALINT & ACQIIRINT radio buttons and update self.acqCtrlVal '''
            # uncheck ACQCBALINT
            self.radioButton_acqReqPage_acqcbalint.setAutoExclusive(False)
            self.radioButton_acqReqPage_acqcbalint.setChecked(False)
            self.radioButton_acqReqPage_acqcbalint.setAutoExclusive(True)
            self.flag_radio_acqReqPage_acqcbalint = True
            # uncheck ACQIIRINT
            self.radioButton_acqReqPage_acqiirinit.setAutoExclusive(False)
            self.radioButton_acqReqPage_acqiirinit.setChecked(False)
            self.radioButton_acqReqPage_acqiirinit.setAutoExclusive(True)
            self.flag_radio_acqReqPage_acqiirinit = True
            # update self.acqCtrlVal
            self.acqCtrlVal = 0x0000    # 工作在 diagnostic mode 时 ACQCTRL[4:11] =0x00
            self.acqCtrlVal |= self.acqMode  # 根据当前选择的 radio 设置 diagnostic mode value

        """ update acquisition mode table """
        self.table_acqReqPage_acqReq.item(0, 2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))
        if not self.flagSingleAfe:
            self.table_acqReqPage_acqReq.item(1, 2).setText(hex(self.acqCtrlVal)[2:].upper().zfill(4))


    def solt_pushBtn_acqReqPage_request(self):
        """
        启动采样：ACQCTRL(0x44) 中写入对应的值
        读取各采样或诊断数据，并将数据更新到对应页面
        :return:
        """
        """ re-setup acqReqPage acquisition mode warning bar """
        self.set_default_warn_bar(self.lineEdit_acqReqPage_acqctrlWarn)

        """ step1: kick off the acquisition (write data to R44) """
        rtData = self.afe_write_read_all(0x44, self.acqCtrlVal)  # configure A13 = 0x2000

        """ wait 250ms for acquisition to complete """
        time.sleep(0.25)

        """ step2: update acqReqPage acquisition mode table """
        if rtData != False:
            if self.flagSingleAfe:  # single afe
                rdDataDev0 = (rtData[1] << 8) | rtData[0]
                self.update_table_item_data(self.table_acqReqPage_acqReq, 0, 3, hex(rdDataDev0)[2:].upper().zfill(4))  # dev0
                ''' fill each bit '''
                bitsDev0 = rdDataDev0 >> 7      # other bits
                for i in range(9):
                    bitValueDev0 = (bitsDev0 >> i) & 1
                    self.table_acqReqPage_acqReq.item(0, 12-i).setText(str(bitValueDev0))

                osrBitsDev0 = (rdDataDev0 & 0x0070) >> 4    # ACQOSR bits
                self.table_acqReqPage_acqReq.item(0, 13).setText(hex_to_bin(hex(osrBitsDev0))[-3:])
                acqModeBitsDev0 = rdDataDev0 & 0x000F       # ACQMODE bits
                self.table_acqReqPage_acqReq.item(0, 14).setText(hex_to_bin(hex(acqModeBitsDev0))[-4:])

                ''' set warn bar '''
                if rdDataDev0 != (self.acqCtrlVal | 0xC000):
                    self.set_warning_message(self.lineEdit_acqReqPage_acqctrlWarn,
                                             "Unexpected Acquisition Status – Confirm Setup")
            else:  # dual afe
                rdDataDev0 = (rtData[3] << 8) | rtData[2]
                rdDataDev1 = (rtData[1] << 8) | rtData[0]
                self.update_table_item_data(self.table_acqReqPage_acqReq, 0, 3, hex(rdDataDev0)[2:].upper().zfill(4))  # dev0
                self.update_table_item_data(self.table_acqReqPage_acqReq, 1, 3, hex(rdDataDev1)[2:].upper().zfill(4))  # dev1
                ''' fill each bit '''
                bitsDev0 = rdDataDev0 >> 7      # other bits
                bitsDev1 = rdDataDev1 >> 7      # other bits
                for i in range(9):
                    bitValueDev0 = (bitsDev0 >> i) & 1
                    self.table_acqReqPage_acqReq.item(0, 12 - i).setText(str(bitValueDev0))  # dev0
                    bitValueDev1 = (bitsDev1 >> i) & 1
                    self.table_acqReqPage_acqReq.item(1, 12 - i).setText(str(bitValueDev1))  # dev1

                osrBitsDev0 = (rdDataDev0 & 0x0070) >> 4  # ACQOSR bits
                osrBitsDev1 = (rdDataDev1 & 0x0070) >> 4  # ACQOSR bits
                self.table_acqReqPage_acqReq.item(0, 13).setText(hex_to_bin(hex(osrBitsDev0))[-3:])
                self.table_acqReqPage_acqReq.item(1, 13).setText(hex_to_bin(hex(osrBitsDev1))[-3:])
                acqModeBitsDev0 = rdDataDev0 & 0x000F  # ACQMODE bits
                acqModeBitsDev1 = rdDataDev1 & 0x000F  # ACQMODE bits
                self.table_acqReqPage_acqReq.item(0, 14).setText(hex_to_bin(hex(acqModeBitsDev0))[-4:])
                self.table_acqReqPage_acqReq.item(1, 14).setText(hex_to_bin(hex(acqModeBitsDev1))[-4:])

                ''' set warn bar '''
                if (rdDataDev0 != (self.acqCtrlVal | 0xC000)) or rdDataDev1 != (self.acqCtrlVal | 0xC000):
                    self.set_warning_message(self.lineEdit_acqReqPage_acqctrlWarn,
                                             " Unexpected Acquisition Status – Confirm Setup")
        else:
            return

        """ step3(cell acquisition mode): read each status register and update DC byte """
        ''' cell acquisition mode '''
        if self.acqMode == 1 or self.acqMode == 2:
            # read status block and update dc table
            self.read_dc_and_status(
                    self.table_meaAcqSumPage_dc, self.ledMeaAcqSumPageDc, self.ledMeaAcqSumPageAlert,
                    self.table_meaAcqSumPage_status, self.ledMeaAcqSumPageStaDev0, self.ledMeaAcqSumPageStaDev1)

            # read ACQLOG
            if self.flagSingleAfe:  # dev0
                acqDataDev0 = self.update_status_table_extend_register(self.table_meaAcqSumPage_status, 0xD0, 8)

                acqTypeDev0 = hex((acqDataDev0 & 0xF000) >> 12)
                acqCountDev0 = str(acqDataDev0 & 0x03FF)
                self.table_meaAcqSumPage_status.item(8, 3).setText(acqTypeDev0)
                self.table_meaAcqSumPage_status.item(8, 5).setText(acqCountDev0)

            else:   # dev0 & dev1
                acqDataDev0, acqDataDev1 = self.update_status_table_extend_register(
                                                                        self.table_meaAcqSumPage_status, 0xD0, 8)

                acqTypeDev0 = hex((acqDataDev0 & 0xF000) >> 12)
                acqCountDev0 = str(acqDataDev0 & 0x03FF)
                self.table_meaAcqSumPage_status.item(8, 3).setText(acqTypeDev0)
                self.table_meaAcqSumPage_status.item(8, 5).setText(acqCountDev0)

                acqTypeDev1 = hex((acqDataDev1 & 0xF000) >> 12)
                acqCountDev1 = str(acqDataDev1 & 0x03FF)
                self.table_meaAcqSumPage_status.item(8, 8).setText(acqTypeDev1)
                self.table_meaAcqSumPage_status.item(8, 10).setText(acqCountDev1)


            """ step4(cell acquisition mode): read meaAcqSumPage summary data block """
            self.update_meaAcqSumPage_sumDataTable()

            """ step5(cell acquisition mode): read meaAcqDetailPage alert register block """
            self.update_meaAcqDetailPage_alertTable()

            """ step6(cell acquisition mode): read meaAcqDetailPage CELL IIR DATA block """
            self.update_meaAcqDetailPage_dataTable(1, 2, 0x90, self.polCfgValue, False)
            """ step7(cell acquisition mode): read meaAcqDetailPage CELL DATA block """
            self.update_meaAcqDetailPage_dataTable(4, 5, 0xA0, self.polCfgValue, False)
            """ step8(cell acquisition mode): read meaAcqDetailPage AUXILIARY DATA block """
            self.update_meaAcqDetailPage_dataTable(7, 8, 0xB0, self.auxRefCfgVal, True)
            """ step9(cell acquisition mode): read meaAcqDetailPage ALTERNATE DATA block """
            self.update_meaAcqDetailPage_dataTable(10, 11, 0xC0, self.polCfgValue, False)

            """ step3(diagnostic mode): read each status register and update DC byte """
            ''' diagnostic mode '''
        else:   # diagnostic mode
            # read status block and update dc table
            self.read_dc_and_status(
                self.table_diagAcqPage_dc, self.ledDiagAcqDataPageDc, self.ledDiagAcqDataPageAlert,
                self.table_diagAcqPage_status, self.ledDiagAcqDataPageStaDev0, self.ledDiagAcqDataPageStaDev1)

            # read ACQLOG, ADC1ZSREG, ADC1FSREG, ADC2ZSREG, ADC2FSREG
            ''' ACQLOG '''
            if self.flagSingleAfe:  # dev0
                acqDataDev0 = self.update_status_table_extend_register(self.table_diagAcqPage_status, 0xD1, 8)

                acqTypeDev0 = hex((acqDataDev0 & 0xF000) >> 12)
                acqCountDev0 = str(acqDataDev0 & 0x03FF)
                self.table_diagAcqPage_status.item(8, 3).setText(acqTypeDev0)
                self.table_diagAcqPage_status.item(8, 5).setText(acqCountDev0)
            else:   # dev0 & dev1
                acqDataDev0, acqDataDev1 = self.update_status_table_extend_register(
                                                                        self.table_diagAcqPage_status, 0xD1, 8)

                acqTypeDev0 = hex((acqDataDev0 & 0xF000) >> 12)
                acqCountDev0 = str(acqDataDev0 & 0x03FF)
                self.table_diagAcqPage_status.item(8, 3).setText(acqTypeDev0)
                self.table_diagAcqPage_status.item(8, 5).setText(acqCountDev0)

                acqTypeDev1 = hex((acqDataDev1 & 0xF000) >> 12)
                acqCountDev1 = str(acqDataDev1 & 0x03FF)
                self.table_diagAcqPage_status.item(8, 8).setText(acqTypeDev1)
                self.table_diagAcqPage_status.item(8, 10).setText(acqCountDev1)

            ''' ADC1ZSREG, ADC1FSREG, ADC2ZSREG, ADC2FSREG '''
            self.update_status_table_extend_register(self.table_diagAcqPage_status, 0xE7, 9)
            self.update_status_table_extend_register(self.table_diagAcqPage_status, 0xE8, 10)
            self.update_status_table_extend_register(self.table_diagAcqPage_status, 0xE9, 11)
            self.update_status_table_extend_register(self.table_diagAcqPage_status, 0xEA, 12)

            # read diagnostic alert block
            '''  step4(diagnostic mode): read device 0 diagnostic alert block '''
            rtData = pb01_read_block(self.hidBdg, 4, 0, 0xD2, 0x00)     # dev0
            if rtData == "message return RX error" or rtData == "pec check error":
                self.message_box(rtData)
                return
            else:
                alertOvDev0 = ((rtData[5] & 0x01) << 16) | (rtData[4] << 8) | rtData[3]
                alertUvDev0 = ((rtData[9] & 0x01) << 16) | (rtData[8] << 8) | rtData[7]

                # fill value column
                listAlertRegDev0 = [hex(alertOvDev0)[2:].upper().zfill(5),
                                    hex(alertUvDev0)[2:].upper().zfill(5)]
                for r in range(2):
                    self.table_diagAcqPage_alertReg_dev0.item(r+1, 2).setText(listAlertRegDev0[r])

                # update led
                self.update_diagnostic_alert_regiser_led([alertOvDev0, alertUvDev0],
                                                         self.ledDiagAcqDataPageDev0)

                if not self.flagSingleAfe:  # dev1
                    rtData = pb01_read_block(self.hidBdg, 4, 1, 0xD2, 0x00)  # dev0
                    if rtData == "message return RX error" or rtData == "pec check error":
                        self.message_box(rtData)
                        return
                    else:
                        alertOvDev1 = ((rtData[5] & 0x01) << 16) | (rtData[4] << 8) | rtData[3]
                        alertUvDev1 = ((rtData[9] & 0x01) << 16) | (rtData[8] << 8) | rtData[7]

                        # fill value column
                        listAlertRegDev1 = [hex(alertOvDev1)[2:].upper().zfill(5),
                                            hex(alertUvDev1)[2:].upper().zfill(5)]
                        for r in range(2):
                            self.table_diagAcqPage_alertReg_dev1.item(r + 1, 2).setText(listAlertRegDev1[r])

                        # update led
                        self.update_diagnostic_alert_regiser_led([alertOvDev1, alertUvDev1],
                                                                 self.ledDiagAcqDataPageDev1)

            # read diagnositc register block data
            self.update_diagnostic_data_table(self.acqMode)


    def solt_radioGroup_cblPage_cblMode(self, button):
        """ 判断 Cell Balance Mode group 中选择了哪个 radio button """
        self.cblMode = self.radioGroup_cblPage_cblMode.id(button)
        self.cblCfgVal = (self.cblCfgVal & 0x0FFF) | (self.cblMode << 12)
        self.table_cblPage_cblCfgReg.item(4, 2).setText(hex(self.cblCfgVal)[2:].zfill(4).upper())


    def solt_table_cblPage_cblExpTime_cellChange(self):
        curExpTime = self.table_cblPage_cblExpTime.item(0, 0).text()

        if int(curExpTime) < 1 or int(curExpTime) > 5:  # 设置值超出 1 ~ 5 的允许范围
            self.message_box("configure value should in range 1 ~ 5\r\n"
                             "please re-configure")
            # 将 expire time 设成 default 值
            self.table_cblPage_cblExpTime.item(0, 0).setText('002')
            # 更新 CBALTIMECFG (0x46) 对应位置的值为 default 值
            self.table_cblPage_cblCfgReg.item(1, 2).setText(
                hex(((self.cblTime & 0xF800) | 2))[2:].zfill(4).upper())
        else:   # 设置值在允许范围内
            # 将 expire time 更新成新设置值
            self.table_cblPage_cblExpTime.item(0, 0).setText(hex(int(curExpTime))[2:].zfill(3))
            # 更新 CBALTIMECFG (0x46) 对应位置的值为新设置值
            self.table_cblPage_cblCfgReg.item(1, 2).setText(
                                hex(((self.cblTime & 0xF800) | int(curExpTime)))[2:].zfill(4).upper())


    def solt_pushBtn_cblPage_cblCfgWr(self):
        """ configure CBALSEL """
        cbalSelData = int(self.table_cblPage_cblCfgReg.item(0, 2).text(), 16)
        self.update_write_read_op(0x45, cbalSelData, self.table_cblPage_cblCfgReg, 0, 4)

        """ configure CBALTIMECFG """
        cbalTimeCfgData = int(self.table_cblPage_cblCfgReg.item(1, 2).text(), 16)
        self.update_write_read_op(0x46, cbalTimeCfgData, self.table_cblPage_cblCfgReg, 1, 4)

        """ configure CBALACQCFG """
        cbalAcqCfgData = int(self.table_cblPage_cblCfgReg.item(2, 2).text(), 16)
        self.update_write_read_op(0x47, cbalAcqCfgData, self.table_cblPage_cblCfgReg, 2, 4)

        """ configure CBALUVTHREG """
        cbalUvThRegData = int(self.table_cblPage_cblCfgReg.item(3, 2).text(), 16)
        self.update_write_read_op(0x48, cbalUvThRegData, self.table_cblPage_cblCfgReg, 3, 4)

        """ configure CBALCFG """
        cablCfgValue = int(self.table_cblPage_cblCfgReg.item(4, 2).text(), 16)
        self.update_write_read_op(0x49, cablCfgValue, self.table_cblPage_cblCfgReg, 4, 4)


    def solt_pushBtn_cblPage_cblCfgRd(self):
        """ read CBALSEL  """
        self.update_config_readback_op(0x45, self.table_cblPage_cblCfgReg, 0, 4)

        """ read CBALTIMECFG  """
        self.update_config_readback_op(0x46, self.table_cblPage_cblCfgReg, 1, 4)

        """ read CBALACQCFG  """
        self.update_config_readback_op(0x47, self.table_cblPage_cblCfgReg, 2, 4)

        """ read CBALUVTHREG  """
        self.update_config_readback_op(0x48, self.table_cblPage_cblCfgReg, 3, 4)

        """ read CBALCFG  """
        self.update_config_readback_op(0x49, self.table_cblPage_cblCfgReg, 4, 4)

    def solt_pushBtn_cblPage_cblCtrlStop(self):
        """ stop cell balance """
        rtData = pb01_write_all(self.hidBdg, 0x4A, 0x2000, 0x00)  # write all R4A = 0x2000, alseed=0x00
        if (rtData == "message return RX error" or rtData == "pec check error"):
            self.message_box(rtData)
            return False
        else:
            """ update cell balance control register table """
            self.update_cblCtrl_block_table(2, 9,
                                            self.ledCblPageStatusDev0, self.ledCblPageStatusDev1,
                                            self.ledCblPageUvStaDev0, self.ledCblPageUvStaDev1)

    def solt_pushBtn_cblPage_cblCtrlStart(self):
        """ start cell balance """
        rtData = pb01_write_all(self.hidBdg, 0x4A, 0x4000, 0x00)  # write all R4A = 0x4000, alseed=0x00
        if (rtData == "message return RX error" or rtData == "pec check error"):
            self.message_box(rtData)
            return False
        else:
            """ update cell balance control register table """
            self.update_cblCtrl_block_table(2, 9,
                                            self.ledCblPageStatusDev0, self.ledCblPageStatusDev1,
                                            self.ledCblPageUvStaDev0, self.ledCblPageUvStaDev1)

    def solt_pushBtn_cblPage_cblCtrlRd(self):
        """ update cell balance control register table """
        self.update_cblCtrl_block_table(2, 9,
                                        self.ledCblPageStatusDev0, self.ledCblPageStatusDev1,
                                        self.ledCblPageUvStaDev0, self.ledCblPageUvStaDev1)


    def open_hid(self):
        try:
            if self.hidStatus == False:
                self.hidBdg.open(target_vid, target_pid)  # VendorID/ProductID
                self.hidStatus = True
                self.statusMessage.setStyleSheet("QLabel { color : blue; }")  # 设置字体颜色为蓝色
                self.statusMessage.setText("bridge board connect successfully ")

                # reset max17841
                max17841_init(self.hidBdg)
                time.sleep(0.05)
                return self.hidStatus
            else:
                return self.hidStatus
        except:
            self.hidStatus = False
            self.statusMessage.setStyleSheet("QLabel { color : red; }")  # 设置字体颜色为蓝色
            self.statusMessage.setText("bridge board connect fail ")
            return self.hidStatus


    def close_hid(self):
        try:
            if self.hidStatus == True:
                self.hidBdg.close()
                self.hidStatus = False
                self.statusMessage.setStyleSheet("QLabel { color : red; }")  # 设置字体颜色为红色
                self.statusMessage.setText("bridge board removed ")
                return self.hidStatus
            else:
                return self.hidStatus
        except:
            self.statusMessage.setStyleSheet("QLabel { color : red; }")  # 设置字体颜色为红色
            self.statusMessage.setText("close hid failed ")
            self.hidStatus = True



""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01MainWindow()
    win.show()

    sys.exit(app.exec_())

