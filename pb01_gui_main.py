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
        self.initUI()  # 定义初始化函数

    def initUI(self):
        """
        GUI 初始化函数
        :return:
        """
        self.open_hid()
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

        ledChainPageDev0, ledChainPageDev1 = adjust_chainPage_pw_rst_tables(self.table_chainCfg_pw,
                                                                            self.table_chainCfg_rstReg)

        ''' initial device manage page (page2) '''
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

        ledMeaAcqSumPageDc, ledMeaAcqSumPageAlert,\
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
        ledChainPageDev0[0][2].setStyleSheet(led_blue_style)

        ''' 配置信号和槽 '''
        self.radioButton_singleAfe.clicked.connect(self.slot_radio_single_dual_afe)
        self.radioButton_dualAfe.clicked.connect(self.slot_radio_single_dual_afe)
        self.pushButton_chainCfg_cfg.clicked.connect(self.slot_pushBtn_chainCfg_cfg)

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
        pWarnLineEdit.setStyleSheet(lineEdit_default_style)

    def slot_pushBtn_chainCfg_cfg(self):
        # reset max17841
        max17841_init(self.hidBdg)
        time.sleep(0.01)
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

        # configure UIFCFG
        rtWrUifCfg = pb01_write_all(self.hidBdg, 0x10, 0x00, 0x26, 0x00)  # write all A10=0x2600, alseed=0x00
        if (rtWrUifCfg == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_chainCfg_cfgWarn, rtWrUifCfg, "WARNING: Write UIFCFG ")
            return
        # read UIFCFG
        if self.flagSingleAfe:
            rtRdUifCfg = pb01_read_all(self.hidBdg, 0x10, 1, 0x00)  # read all A10, alseed=0x00
            if (rtRdUifCfg == ("message return RX error" or "pec check error")):
                self.set_warning_message(self.lineEdit_chainCfg_cfgWarn, rtWrUifCfg, "WARNING: Read UIFCFG ")
                return
        else:
            rtRdUifCfg = pb01_read_all(self.hidBdg, 0x10, 2, 0x00)  # read all A10, alseed=0x00
            if (rtRdUifCfg == ("message return RX error" or "pec check error")):
                self.set_warning_message(self.lineEdit_chainCfg_cfgWarn, rtWrUifCfg, "WARNING: Read UIFCFG ")
                return

        # configure ADDRESSCFG
        rtWrAddCfg = pb01_write_all(self.hidBdg, 0x11, 0x20, 0x00, 0x00)  # write all A11=0x0020
                                                                          # (topDevAddr = 1, botDevAddr = 0)
                                                                          # alseed=0x00
        if (rtWrAddCfg == ("message return RX error" or "pec check error")):
            self.set_warning_message(self.lineEdit_chainCfg_cfgWarn, rtWrUifCfg, "WARING: Write ADDRESSCFG ")

        #wait 10ms to complete FEMA2 BIST
        time.sleep(0.01)
        # re-setup chainCfgPage cfgWarn bar
        self.set_default_warn_bar(self.lineEdit_chainCfg_cfgWarn)


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

