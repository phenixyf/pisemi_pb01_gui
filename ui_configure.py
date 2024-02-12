# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 10:42
# @Author  : yifei.su
# @File    : ui_configure.py


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QFont

""" led string related """
''' led qss '''
led_qss = "QLabel {\n" \
          "  border-radius: 5px; /* 使得QLabel成为圆形 */\n" \
          "  background: qradialgradient(\n" \
          "    cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5,\n" \
          "    stop: 0 #ffffff, /* 渐变的中心是白色 */\n" \
          "    stop: 0.4 #00aa00, /* 渐变为绿色 */\n" \
          "    stop: 0.5 #009900, /* 中间的圆环更浅的绿色 */\n" \
          "    stop: 1.0 #006600); /* 边缘是最浅的绿色 */\n" \
          "  box-shadow: 0px 0px 8px 0px #006600; /* 添加阴影以增强3D效果 */\n" \
          "}"

font = QtGui.QFont()
# 设置字体的大小
font.setPointSize(7)  # 20是字体的大小，你可以根据需要调整这个值

def led_generator():
    label_led = QtWidgets.QLabel()
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(label_led.sizePolicy().hasHeightForWidth())
    label_led.setSizePolicy(sizePolicy)
    label_led.setMinimumSize(QtCore.QSize(10, 10))
    label_led.setMaximumSize(QtCore.QSize(10, 10))
    label_led.setStyleSheet(led_qss)
    return label_led

def txt_generator(pTxt):
    label_txt = QtWidgets.QLabel(pTxt)
    label_txt.setFont(font)
    return label_txt

def add_led_txt(pLedNum, pTableWidget, pRow, pCol, pLabelList):
    """
    将 led 及其上标插入到 table 表的某个单元格内
    :param pLedNum: 要插入的 led 数量
    :param pTableWidget: 要插入的 table 控件名
    :param pRow: 插入位置行号
    :param pCol: 插入位置列号
    :param pLabelList: led 上标
    :return: 返回插入的 led 对象列表
             通过返回的 led 对象列表，可以控制各 led，比如修改 led 的颜色
    """
    pList_led = []
    pList_txt = []
    for i in range(0, pLedNum):
        pList_led.append(led_generator())

    for i in range(0, pLedNum):
        pList_txt.append(txt_generator(pLabelList[i]))

    # for i in range(0, pLedNum):
    #     pList_txt.append(txt_generator("LED"+str(i)))

    pFrame = QtWidgets.QFrame()
    pLayout = QtWidgets.QGridLayout(pFrame)
    pLayout.setSpacing(0)
    # 为布局设置外边距：左、上、右、下
    pLayout.setContentsMargins(0, 0, 0, 0)

    for i in range(0, pLedNum):
        pLayout.addWidget(pList_txt[i], 0, i)
        pLayout.addWidget(pList_led[i], 1, i)
        pLayout.setAlignment(pList_txt[i], Qt.AlignCenter)
        pLayout.setAlignment(pList_led[i], Qt.AlignCenter)

    pTableWidget.setCellWidget(pRow, pCol, pFrame)

    return pList_led


""" CHAIN CONFIGURATION page tablewidget initial content """
CHAIN_CFG_TABLE_HEHG = 28       # table header row height
CHAIN_CFG_TABLE_ROWHG = 18      # table row height
CHAIN_CFG_TABLE_STAHG = 120     # status block 不显示 header 的 4 个 table 的高度
CHAIN_CFG_TABLE_RSTHG = 60      # reset block table 的高度

''' 16 led label '''
LED_STA1_LAB = ["ACQ", "RESET", "RJCT", "UIF", "OV", "UV", "ALTOV", "ALTUV",
                "AUXOV", "AUXUV", "DIAGOV", "DIAGUV", "MM", "CBAL", "FMEA1", "FMEA2"]
LED_STA2_LAB = ["PECUP", "PECDN", "MANUP", "MANDN", "PARUP", "PARDN", "REGUP", "REGDN",
                "DUAL", "CBNTFY", "CBDONE", "CBERR", "SPIRW", "SPICLK", "SPICRC", "SPIREG"]
LED_FME1_LAB = ["OSC", "----", "----", "----", "----", "VAA", "VDD", "VIO",
                "AGND2", "AGND", "DGND", "IOGND", "HVOV", "HVUV", "TEMP2", "TEMP1"]
LED_FME2_LAB = ["HVHDRM", "ACQTO", "----", "----", "ADC1ZS", "ADC1FS", "ADC2ZS", "ADC2FS",
                "USER", "MODE", "AINIT", "DINIT", "OTPERR", "REGECC", "MBIST", "CBIST"]
LED_LAB_DC = ["INTFC", "FMEA", "PROC", "DIAG", "OV", "UV", "AUXOV", "AUXUV"]
LED_LAB_ALERT0 = ["ACQ", "RESET", "RJCT", "UIF", "OV", "UV", "ALTOV", "ALTUV",
                "AUXOV", "AUXUV", "DIAGOV", "DIAGUV", "MM", "CBAL", "FMEA2", "FMEA1"]
LED_LAB_ALERT1 = ["LOC31", "LOC30", "LOC29", "LOC28", "LOC27", "LOC26", "LOC25", "LOC24",
                "LOC23", "LOC22", "LOC21", "LOC20", "LOC19", "LOC18", "LOC17", "LOC16"]
LED_LAB_ALERT2 = ["LOC15", "LOC14", "LOC13", "LOC12", "LOC11", "LOC10", "LOC9", "LOC8",
                "LOC7", "LOC6", "LOC5", "LOC4", "LOC3", "LOC2", "LOC1", "LOC0"]
LED_LAB_16 = ["LED15", "LED14", "LED13", "LED12", "LED11", "LED10", "LED9", "LED8",
                "LED7", "LED6", "LED5", "LED4", "LED3", "LED2", "LED1", "LED0"]
LED_LAB_8 = ["LED7", "LED6", "LED5", "LED4", "LED3", "LED2", "LED1", "LED0"]
LED_LAB_17 = ["LED16", "LED15", "LED14", "LED13", "LED12", "LED11", "LED10", "LED9", "LED8",
                "LED7", "LED6", "LED5", "LED4", "LED3", "LED2", "LED1", "LED0"]
LED_LAB_32 = ["LED31", "LED30", "LED29", "LED28", "LED27", "LED26", "LED25", "LED24",
                "LED23", "LED22", "LED21", "LED20", "LED19", "LED18", "LED17", "LED16",
              "LED15", "LED14", "LED13", "LED12", "LED11", "LED10", "LED9", "LED8",
                "LED7", "LED6", "LED5", "LED4", "LED3", "LED2", "LED1", "LED0"]


''' chain configuration page tablewidget initial content '''
table_chainCfg_devidHead = ["Address", "Register", "Expected (hex)","DEVIDD (hex)", "DEVID1 (hex)", "DEVID2 (hex)",
                            "VERSION (hex)", "GENERATION[2:0] (dec)", "CHANNEL_COUNT[4:0] (dec)", "SWVER[3:0] (hex)",
                            "HWVER[3:0] (hex)"]
table_chainCfg_devidItem = [
    ["0x00 - 0x03", "DEVID0,1,2 & VERSION (Device0)", "Unique ID", "????", "????", "????", "????", "1", "16", "0", "1"],
    ["0x00 - 0x03", "DEVID0,1,2 & VERSION (Device1)", "Unique ID", "????", "????", "????", "????", "1", "16", "0", "1"]
]

table_chainCfg_uartIfHead = ["Address", "Register", "Expected (hex)", "Actual (hex)", "UARTDUAL", "UARTLPBK",
                            "UARTWRPATH", "TXUIDLEHIZ", "TXLIDLEHIZ", "UARTDCEN", "UARTALVCNTEN", "(Logic Zero)",
                            "DBLBUFEN", "Reserved/SPI[6:0] (bin)"]
table_chainCfg_uartIfItem = [
    ["0x10", "UIFCFG (Device 0)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"],
    ["0x10", "UIFCFG (Device 1)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"]
]

table_chainCfg_uartAddrHead = ["Address", "Register", "Expected (hex)", "Actual (hex)", "ADDRUNLOCK",
                               "BOTADDR[4:0] (hex)", "TOPADDR[4:0] (hex)", "DEVADDR[4:0] (hex)"]
table_chainCfg_uartAddrItem = [
    ["0x11", "ADDRESSCFG (Device 0)", "0000/0020", "8000", "0", "0000", "00/01", "00"],
    ["0x11", "ADDRESSCFG (Device 1)", "0021", "8000", "0", "0000", "01", "01"]
]

table_chainCfg_pwHeaders = ["Address", "Register", "FORCEPOR (hex)", "Device 0 (hex)", "", "Device 1 (hex)", ""]
table_chainCfg_pwItems = [
    ["0x04", "STATUS1", "5000", "5000", "", "5000", ""],
    ["0x05", "STATUS2", "0080", "0080", "", "0080", ""],
    ["0x06", "FMEA1",   "0000", "0000", "", "0000", ""],
    ["0x07", "FMEA2",   "0000", "0000", "", "0000", ""]
]

table_chainCfg_rstHeaders = ["Address", "Register", "Expect (hex)", "Device 0 (hex)", "", "Device 1 (hex)", ""]
table_chainCfg_rstItems = [
["0x0F", "RESTCTRL", "0001", "0000", " ", "0000", " "]
]

""" device manage page tablewidget initial content """
table_devMg_iniItems = [
    ["Address", "Register", "Device 0 (hex)", " ", " ", " ", " ",
                            "Device 1 (hex)", " ", " ", " ", " "],
    ["0x04", "STATUS1", "5000", " ", " ", " ", "", "5000", " ", " ", "", ""],
    ["0x05", "STATUS2", "0080", " ", " ", " ", "", "0080", " ", " ", "", ""],
    ["0x06", "FMEA1",   "0000", " ", " ", " ", "", "0000", " ", " ", "", ""],
    ["0x07", "FMEA2",   "0000", " ", " ", " ", "", "0000", " ", " ", "", ""]
]

table_devMg_dcItems = [
    ["DCBYTE", "80", " "],
    ["ALERTPACKET", "5000_0000_0000_0001/3", " "],
    ["ALERTPACKET", "5000_0000_0000_0001/3", " "],
    ["ALERTPACKET", "5000_0000_0000_0001/3", " "]
]

table_devMg_curItems = [
    ["Address", "Register", "Device 0 (hex)", " ", " ", " ", " ",
                                "Device 1 (hex)", " ", " ", " ", " "],
    ["0x04", "STATUS1",     "5000", " ", " ", " ", "", "5000", " ", " ", " ", ""],
    ["0x05", "STATUS2",     "0080", " ", " ", " ", "", "0080", " ", " ", " ", ""],
    ["0x06", "FMEA1",       "0000", " ", " ", " ", "", "0000", " ", " ", " ", ""],
    ["0x07", "FMEA2",       "0000", " ", " ", " ", "", "0000", " ", " ", " ", ""],
    ["0x08", "TEMPREG1",    "0960", "26.9", "C", "80.3", "F", "0960", "26.9", "C", "80.3", "F"],
    ["0x09", "TEMPREG2",    "0960", "26.9", "C", "80.3", "F", "0960", "26.9", "C", "80.3", "F"],
    ["0x0A", "GPIODATA",    "0000", "00", "GPIODOUT[7:0]", "00", "GPIODIN[7:0]",
                            "0000", "00", "GPIODOUT[7:0]", "00", "GPIODIN[7:0]", "0000"]
]

""" application configuration page tablewidget initial content """
table_appCfgPage_headers = ["Address", "Register", "Pending (hex)", "Pending Value (bin)", "Pending Field",
                           "Pending Value (bin)", "Pending Field", "Device 0 (hex)", "Device 1 (hex)"]
table_appCfgPage_appCfgReg_items = [
    ["0x12", "STATUSCFG", "3FF", "0111111", "STATUSCFG[15:8]", "1111111", "STATUSCFG[7:0]", "3FFF", "3FFF"],
    ["0x13", "DEVCFG", "2000", "010", "IIRFC[2:0]", "000", "DEVCFG[10:8]", "2000", "2000"],
    ["0x14", "DEVCFG", "2000", "010", "IIRFC[2:0]", "000", "DEVCFG[10:8]", "2000", "2000"],
    ["0x15", "DEVCFG", "2000", "010", "IIRFC[2:0]", "000", "DEVCFG[10:8]", "2000", "2000"],
    ["0x16", "DEVCFG", "2000", "010", "IIRFC[2:0]", "000", "DEVCFG[10:8]", "2000", "2000"]
]

table_appCfgPage_alertCfgReg_items = [
    ["0x18", "ALRTOVCFG", "FFFF", "1111111", "ALRTAUXUVEN[7:0]", "1111111", "ALRTAUXUVEN[7:0]", "0000", "0000"],
    ["0x19", "ALRTUVCFG", "FFFF", "1111111", "ALRTAUXUVEN[7:0]", "1111111", "ALRTAUXUVEN[7:0]", "0000", "0000"],
    ["0x1A", "ALRTAUXOVCFG", "FFFF", "1111111", "ALRTAUXUVEN[7:0]", "1111111", "ALRTAUXUVEN[7:0]", "0000", "0000"],
    ["0x1G", "ALRTAUXUVCFG", "FFFF", "1111111", "ALRTAUXUVEN[7:0]", "1111111", "ALRTAUXUVEN[7:0]", "0000", "0000"]
]

table_appCfgPage_acqReg_items = [
    ["0x40", "ACQDLY1", "1501", "2.106", "CELLDLY(ms)", "0.096", "SWDLY(ms)", "0000", "0000"],
    ["0x41", "ACQDLY2", "3220", "2.106", "CELLDLY(ms)", "0.096", "SWDLY(ms)", "0000", "0000"],
    ["0x42", "ACQCHSEL", "FFFF", "2.106", "CELLDLY(ms)", "0.096", "SWDLY(ms)", "0000", "0000"],
    ["0x43", "ACQAUXSEL", "FFFF", "2.106", "CELLDLY(ms)", "0.096", "SWDLY(ms)", "0000", "0000"]
]

table_appCfgPage_theresholdReg_items = [
    ["0x20", "OVTHREG",         "E667",     "4.500",    "V",           " ", " ", "FFFF",   "FFFF"],
    ["0x21", "UVTREG",          "8A3D",     "2.700",    "V",           " ", " ", "0000",   "0000"],
    ["0x22", "BIPOVTHREG",      "051F",     "+0.100",   "V (Bipolar)", " ", " ", "7FFF",   "7FFF"],
    ["0x23", "BIPUVTHREG",      "FAE1",     "-0.100",   "V (Bipolar)", " ", " ", "8000",   "8000"],
    ["0x24", "ALTOVTHREG",      "E667",     "4.500",    "V",           " ", " ", "FFFF",   "FFFF"],
    ["0x25", "ALTUVTHREG",      "8A3D",     "2.700",    "V",           " ", " ", "0000",   "0000"],
    ["0x26", "ALTBIPOVTHREG",   "051F",     "+0.100",   "V (Bipolar)", " ", " ", "7FFF",   "7FFF"],
    ["0x27", "ALTBIPUVTHREG",   "FAE1",     "-0.100",   "V (Bipolar)", " ", " ", "8000",   "8000"],
    ["0x28", "AUXROVTHREG",     "TBD",      "TBD",      "Ratiometric", " ", " ", "FFFF",   "FFFF"],
    ["0x29", "AUXRUVTHREG",     "TBD",      "TBD",      "Ratiometric", " ", " ", "0000",   "0000"],
    ["0x2A", "AUXAOVTHREG",     "FFFF",     "2.500",    "V",           " ", " ", "FFFF",   "FFFF"],
    ["0x2B", "AUXAUVTHREG",     "0000",     "0.000",    "V",           " ", " ", "0000",   "0000"],
    ["0x2C", "MMTHREG",         "0CCD",     "0.250",    "V",           " ", " ", "FFFF",   "FFFF"],
    ["0x2D", "TEMPTHREG",       "0C48",     "120",      "C",           " ", " ", "0C48",   "0C48"]
]

"""  diagnostic configuration page tablewidget initial content """
table_diagCfgPage_testCfg_headers = ["Address", "Register", "Pending (hex)", "Pending Value (bin)", "Pending Field",
                           "Pending Value (bin)", "Pending Field", "Pending Value (bin)", "Pending Field",
                            "Pending Value (bin)", "Pending Field", "Device 0 (hex)", "Device 1 (hex)"]

table_diagCfgPage_testCfg_items = [
    ["0x1C", "CTSTCFG1", "0001", "00", "HVMUXTSTEN[1:0]", "0", "CTSTPOL1", "0", "CTSTMAN", "1",
                                                "CTSTEN[16]", "0000", "0000","0000"],
    ["0x1D", "CTSTCFG1", "0001", "00", "HVMUXTSTEN[1:0]", "0", "CTSTPOL1", "0", "CTSTMAN", "1",
                                                "CTSTEN[16]", "0000", "0000","0000"],
    ["0x1E", "CTSTCFG1", "0001", "00", "HVMUXTSTEN[1:0]", "0", "CTSTPOL1", "0", "CTSTMAN", "1",
                                                "CTSTEN[16]", "0000", "0000","0000"]
]

table_diagCfgPage_diagThre_headers = ["Address", "Register", "Pending (hex)", "Pending Value", "Pending Unit",
                                      "Pending Value", "Pending Unit", "Device 0 (hex)", "Device 1 (hex)"]
table_diagCfgPage_diagThre_items = [
    ["0x2F", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x30", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x31", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x32", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x33", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x34", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x35", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x36", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x37", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x38", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x39", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x3A", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"],
    ["0x3B", "BALSHTUVTHREG", "0000", "0.000", "V", " ", " ", "0000", "0000"]
]

table_diagCfgPage_aluTeDiag_headers = ["Address", "Register", "Pending (hex)", "Pending Value", "Pending Unit",
                                      "Pending Value", "Pending Unit", "Device 0 (hex)", "Device 1 (hex)"]
table_diagCfgPage_aluTeDiag_items = [
    ["0x3C", "BALSHTUVTHREG", "0000", " ", " ", " ", " ", "0000", "0000"],
    ["0x3D", "BALSHTUVTHREG", "0000", " ", " ", " ", " ", "0000", "0000"],
    ["0x3E", "BALSHTUVTHREG", "0000", " ", " ", " ", " ", "0000", "0000"],
    ["0x3F", "BALSHTUVTHREG", "0000", " ", " ", " ", " ", "0000", "0000"]
]

""" measurement acquisition detailed data page tablewidget initial content """
table_meaAcqDetailPage_alertRegItems = [
    ["0x80", "ALRTALTOVREG", "0000", " "],
    ["0x80", "ALRTALTOVREG", "0000", " "],
    ["0x80", "ALRTALTOVREG", "0000", " "],
    ["0x80", "ALRTALTOVREG", "0000", " "],
    ["0x80", "ALRTALTOVREG", "0000", " "],
    ["0x80", "ALRTALTOVREG", "0000", " "]
]

table_meaAcqDetailPage_dataRegItems = [
    ["0x90 ~ - 0x9F", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0x90 ~ - 0x9F", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0x90 ~ - 0x9F", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0xA0 ~ - 0xAF", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0xA0 ~ - 0xAF", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0xA0 ~ - 0xAF", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0xB0 ~ - 0xBF", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0xB0 ~ - 0xBF", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0xB0 ~ - 0xBF", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0xC0 ~ - 0xCF", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0xC0 ~ - 0xCF", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],
    ["0xC0 ~ - 0xCF", "AUXILIARY DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"]
]

""" measurement acquisition summary data page tablewidget initial content """
table_meaAcqSumDataPage_sumDataItems = [
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"],
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"],
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"],
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"],
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"],
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"],
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"],
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"],
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"],
    ["0x86", "ALTTOTALREG", "0000", "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]",
     "0", "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]"]

]

""" diagnostic acquisition data page tablewidget initial content """
table_diagAcqDataPage_statusTableItems = [
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"],
    ["ALERTPACKTE", "0000_0000_0001/3", "Device 0 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]",
     "Device 1 (hex)", "26.9", "GPIODOUT[7:0]", "80.3", "DIAGCOUNT[9:0]"]
]

table_diagAcqDataPage_alertItems = [
    ["0xD2 ~ 0xD3", "ALRTDIAGOVREG1/2", "0000", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16"],
    ["0xD2 ~ 0xD3", "ALRTDIAGOVREG1/2", "0000", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16"]
]

table_diagAcqDataPage_dataItems = [
    ["0xD2 ~ 0xD3", "ALRTDIAGOVREG1/2", "0000", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16"],
    ["0xD2 ~ 0xD3", "ALRTDIAGOVREG1/2", "0000", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16"],
    ["0xD2 ~ 0xD3", "ALRTDIAGOVREG1/2", "0000", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16",
     "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16", "DIAG 16"]
]

""" cell balance page tablewidget initial content """
table_cblPage_cblExpTimHeaders = ["CBEXP[10:0] (hex)", "CBEXP (dec)"]
table_cblPage_cblCfgRegHeaders =["Address", "Register", "Pending (hex)", "Comment", "Device 0 (hex)", "Device 1 (hex)"]
table_cblPage_cblCtrlDemoHeaders =["Address", "Register", "Pending (hex)", "Comment", "Device 0 (hex)", "Device 1 (hex)"]

table_cblPage_cblExpTimItems = ["002", "2"]
table_cblPage_cblCfgRegItems = [
    ["0x45", "CBALUVTHREG", "FFFF",
     "CBMODE[2:0] is determined by selection.  CBTEMPEN=0b1 for safety.  CBDUTY[3:0]=0xF (50%) for Semi-Automatic Mode."
     "  All other options are not used in this Demo.", "01F0", "01F0"],
    ["0x46", "CBALUVTHREG", "FFFF",
     "CBMODE[2:0] is determined by selection.  CBTEMPEN=0b1 for safety.  CBDUTY[3:0]=0xF (50%) for Semi-Automatic Mode."
     "  All other options are not used in this Demo.", "01F0", "01F0"],
    ["0x47", "CBALUVTHREG", "FFFF",
     "CBMODE[2:0] is determined by selection.  CBTEMPEN=0b1 for safety.  CBDUTY[3:0]=0xF (50%) for Semi-Automatic Mode."
     "  All other options are not used in this Demo.", "01F0", "01F0"],
    ["0x48", "CBALUVTHREG", "FFFF",
     "CBMODE[2:0] is determined by selection.  CBTEMPEN=0b1 for safety.  CBDUTY[3:0]=0xF (50%) for Semi-Automatic Mode."
     "  All other options are not used in this Demo.", "01F0", "01F0"],
    ["0x49", "CBALUVTHREG", "FFFF",
     "CBMODE[2:0] is determined by selection.  CBTEMPEN=0b1 for safety.  CBDUTY[3:0]=0xF (50%) for Semi-Automatic Mode."
     "  All other options are not used in this Demo.", "01F0", "01F0"]
]
table_cblPage_cblCtrlDemoItems = [
    ["0x4A","BALCTRL (START)", "4000", "This is the command issued for a Cell Balancing Start Request.", " ", " "],
    ["0x4A","BALCTRL (START)", "2000", "This is the command issued for a Cell Balancing Start Request.", " ", " "]
]
table_cblPage_cblCtrlInfItems = [
    ["Address", "Register", "Device 0 (hex)", " ", " ", " ", " ", " ", " ",
                                "Device 1 (hex)", " ", " ", " ", " ", " ", " "],
    ["0x4A", "CBALCTRL (READ)", "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)",
                                "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)"],
    ["0x4A", "CBALCTRL (READ)", "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)",
                                "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)"],
    ["0x4A", "CBALCTRL (READ)", "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)",
                                "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)"],
    ["0x4A", "CBALCTRL (READ)", "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)",
                                "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)"],
    ["0x4A", "CBALCTRL (READ)", "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)",
                                "0000", "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)"]
]


def set_table_head(pTableWidget, pListHeader, pHeaderHeight, pTableHeight):
    """
    初始化 tablewidget
    完成下面操作：
    1. 设置标题栏内容、
    2. 设置标题栏高度，
    3. 设置整个 tablewidget 固定高度
    4. 并设置标题栏水平和垂直居中对齐
    注意：该函数仅初始化了 tablewidget 的标题，一定要同时搭配调用 set_table_item 才能
    完成整个 tablewidget 的初始化动作
    :param pTableWidget: tablewidget 实例
    :param pListHeader: 标题栏内容
    :param pHeaderHeight: 设置标题行高度
    :param pTableHeight: 设置 tablewidget 高度
    :return:
    """
    pTableWidget.setHorizontalHeaderLabels(pListHeader)  # 设置标题内容
    pTableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)  # 设置标题内容水平居中对齐
    pTableWidget.horizontalHeader().setFixedHeight(pHeaderHeight)  # 设置标题行高度
    if pTableHeight != 0:
        pTableWidget.setFixedHeight(pTableHeight)  # 设置 table 高度


def set_table_item(pTableWidget, pRowHeight, pItemData=[]):
    """
    该函数用在 tablewidget 控件初始化过程中，实现 3 个功能：
    1. 显示指定的行数内容
    2. 设置单元格行高度
    3. 设置单元格内容初始值
    4. 设置单元格内数据水平和垂直居中对齐
    5. 设置列宽自适应宽度
    注意：调用该函数后，对应 tablewidget 内的所有数据都会恢复成初始值，这个函数仅用在 GUI 一开始初始化和
    CHAIN CONFIGURATION page 的 single afe 和 dual afe radio button 切换操作时
    :param pTableWidget: tablewidget 实例
    :param pShowRowCnt: 要显示的行数
    :param pRowHeight: 行高度值
    :param pItemData: 单元格填入的数据，列表格式
    :return:
    """
    r = pTableWidget.rowCount()
    c = pTableWidget.columnCount()
    for row in range(r):
        for column in range(c):
            # 设置单元格的初始值
            pTableWidget.setItem(row, column, QTableWidgetItem(pItemData[row][column]))
            pTableWidget.item(row, column).setTextAlignment(Qt.AlignCenter)  # 设置单元格内容水平垂直居中对齐
        # 设置行高度
        pTableWidget.setRowHeight(row, pRowHeight)

    # 设置列宽自适应
    pTableWidget.resizeColumnsToContents()


def adjust_chainPage_ifid_tables(pDevIdTable, puifCfgTable, paddCfgTable):
    """
    调整 chain configuration page device id, uart interface, address register tables 的尺寸，列宽
    :param pDevIdTable: device id table object name
    :param puifCfgTable: uart interface table object name
    :param paddCfgTable: address table object name
    :return: none
    """
    puifCfgTable.setColumnWidth(0, pDevIdTable.columnWidth(0))
    paddCfgTable.setColumnWidth(0, pDevIdTable.columnWidth(0))
    puifCfgTable.setColumnWidth(1, pDevIdTable.columnWidth(1))
    paddCfgTable.setColumnWidth(1, pDevIdTable.columnWidth(1))
    puifCfgTable.setColumnWidth(2, pDevIdTable.columnWidth(2))
    paddCfgTable.setColumnWidth(2, pDevIdTable.columnWidth(2))
    puifCfgTable.setColumnWidth(3, pDevIdTable.columnWidth(3))
    paddCfgTable.setColumnWidth(3, pDevIdTable.columnWidth(3))
    puifCfgTable.setColumnWidth(4, pDevIdTable.columnWidth(4))
    puifCfgTable.setColumnWidth(5, pDevIdTable.columnWidth(5))
    puifCfgTable.setColumnWidth(6, pDevIdTable.columnWidth(6))
    paddCfgTable.setColumnWidth(4, puifCfgTable.columnWidth(4)
                                + puifCfgTable.columnWidth(5))
    paddCfgTable.setColumnWidth(5, puifCfgTable.columnWidth(6)
                                + puifCfgTable.columnWidth(7))
    paddCfgTable.setColumnWidth(6, puifCfgTable.columnWidth(8)
                                + puifCfgTable.columnWidth(9))
    paddCfgTable.setColumnWidth(7, puifCfgTable.columnWidth(10)
                                + puifCfgTable.columnWidth(11))
    pDevIdTable.setColumnWidth(7, puifCfgTable.columnWidth(7)
                               + puifCfgTable.columnWidth(8))
    pDevIdTable.setColumnWidth(8, puifCfgTable.columnWidth(9)
                               + puifCfgTable.columnWidth(10))
    pDevIdTable.setColumnWidth(9, puifCfgTable.columnWidth(11)
                               + puifCfgTable.columnWidth(12))
    pDevIdTable.setColumnWidth(10, puifCfgTable.columnWidth(13))


def set_chainPage_ifid_color(pRowNum, pDevIdTable, puifCfgTable, paddCfgTable):
    """
     设置 chain configuration page device id, uart interface, address register tables 的背景颜色
    :param pRowNum: 因 single,dual AFE radio 的选择，显示的行数不同，所以这里用一个参数来区分
    :param pDevIdTable: device id table object name
    :param puifCfgTable: uart interface table object name
    :param paddCfgTable: address table object name
    :return: none
    """
    for r in range(pRowNum):
        # 设置 pDevIdTable 的背景颜色
        for c in range(3, 11):  # 列索引从 3 到 10
            if 3 <= c <= 6:
                color = QColor("#E2F0D9")
            else:  # 7 到 10 列
                color = QColor("#FFF2CC")
            pDevIdTable.item(r, c).setBackground(color)

        # 设置 puifCfgTable 的背景颜色
        for c in range(3, 14):  # 列索引从 3 到 13
            if c == 3:
                color = QColor("#E2F0D9")   # 绿色
            else:  # 4 到 13 列
                color = QColor("#FFF2CC")   # 黄色
            puifCfgTable.item(r, c).setBackground(color)

        # 设置 paddCfgTable 的背景颜色
        for c in range(3, 8):  # 列索引从 3 到 7
            if c == 3:
                color = QColor("#E2F0D9")
            else:  # 4 到 7 列
                color = QColor("#FFF2CC")
            paddCfgTable.item(r, c).setBackground(color)


def adjust_chainPage_pw_rst_tables(pPwTable, pRstTable):
    ''' adjust table column size '''
    for c in range(7):
        if c == 2:
            pPwTable.setColumnWidth(c, 150)
            pRstTable.setColumnWidth(c, 150)
        elif c == 4 or c == 6:
            pPwTable.setColumnWidth(c, 550)
            pRstTable.setColumnWidth(c, 550)
        else:
            pPwTable.setColumnWidth(c, 130)
            pRstTable.setColumnWidth(c, 130)

    ''' fill background color'''
    for r in range(4):
        if r < 1:
            pRstTable.item(r, 3).setBackground(QColor("#E2F0D9"))  # 绿色
            pRstTable.item(r, 5).setBackground(QColor("#E2F0D9"))  # 绿色
            pRstTable.item(r, 4).setBackground(QColor("#FFF2CC"))  # 黄色
            pRstTable.item(r, 6).setBackground(QColor("#FFF2CC"))  # 黄色
        pPwTable.item(r, 3).setBackground(QColor("#E2F0D9"))  # 绿色
        pPwTable.item(r, 5).setBackground(QColor("#E2F0D9"))  # 绿色
        pPwTable.item(r, 4).setBackground(QColor("#FFF2CC"))  # 黄色
        pPwTable.item(r, 6).setBackground(QColor("#FFF2CC"))  # 黄色

    ''' insert leds '''
    ledSta1Dev0 = add_led_txt(16, pPwTable, 0, 4, LED_STA1_LAB)
    ledSta1Dev1 = add_led_txt(16, pPwTable, 0, 6, LED_STA1_LAB)
    ledSta2Dev0 = add_led_txt(16, pPwTable, 1, 4, LED_STA2_LAB)
    ledSta2Dev1 = add_led_txt(16, pPwTable, 1, 6, LED_STA2_LAB)
    ledFem1Dev0 = add_led_txt(16, pPwTable, 2, 4, LED_FME1_LAB)
    ledFem1Dev1 = add_led_txt(16, pPwTable, 2, 6, LED_FME1_LAB)
    ledFem2Dev0 = add_led_txt(16, pPwTable, 3, 4, LED_FME2_LAB)
    ledFem2Dev1 = add_led_txt(16, pPwTable, 3, 6, LED_FME2_LAB)

    ledDev0 = [ledSta1Dev0, ledSta2Dev0, ledFem1Dev0, ledFem2Dev0]
    ledDev1 = [ledSta1Dev1, ledSta2Dev1, ledFem1Dev1, ledFem2Dev1]

    return ledDev0, ledDev1


def adjust_devMgPage_tables(pInit, pDC, pCur):
    ''' adjust size '''
    for c in range(12):
        if c == 1:
            pInit.setColumnWidth(c, 200)
            pCur.setColumnWidth(c, 200)
        elif c == 4 or c == 6 or c == 9 or c == 11:
            pInit.setColumnWidth(c, 150)
            pCur.setColumnWidth(c, 150)
        else:
            pInit.setColumnWidth(c, 120)
            pCur.setColumnWidth(c, 120)

    for c in range(3):
        if c == 1:
            pDC.setColumnWidth(c, 200)
        elif c == 2:
            pDC.setColumnWidth(c, 1320)
        else:
            pDC.setColumnWidth(c, 120)

    ''' fill background color and font'''
    boldFont = QFont()
    boldFont.setBold(True)
    # status initial table
    for r in range(5):
        for c in range(12):
            if r == 0:
                pInit.setSpan(0, 3, 1, 4)
                pInit.item(0, 3).setText(" ")
                pInit.setSpan(0, 8, 1, 4)
                pInit.item(0, 8).setText(" ")
                pInit.item(0, c).setFont(boldFont)  # 字体加粗
            elif c == 3 or c == 8:
                pInit.setSpan(r, c, 1, 4)
                pInit.item(r, 3).setText(" ")
                pInit.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
                pInit.item(r, 8).setText(" ")
                pInit.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
                pInit.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
                pInit.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
    # status current table
    for r in range(8):
        for c in range(12):
            if r == 0:
                pCur.setSpan(0, 3, 1, 4)
                pCur.item(0, 3).setText(" ")
                pCur.setSpan(0, 8, 1, 4)
                pCur.item(0, 8).setText(" ")
                pCur.item(0, c).setFont(boldFont)  # 字体加粗
            elif r > 4:
                pCur.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
                pCur.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
                pCur.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
                pCur.item(r, 10).setBackground(QColor("#FFF2CC"))  # 黄色
            elif c == 3 or c == 8:
                pCur.setSpan(r, c, 1, 4)
                pCur.item(r, 3).setText(" ")
                pCur.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
                pCur.item(r, 8).setText(" ")
                pCur.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
            if r != 0:
                pCur.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
                pCur.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色

    # DC table
    pDC.setSpan(1, 0, 3, 1)
    pDC.setSpan(1, 1, 3, 1)
    for r in range (4):
        if r < 2:
            pDC.item(r, 1).setBackground(QColor("#E2F0D9"))  # 绿色
            pDC.item(r, 0).setFont(boldFont)  # 字体加粗
        pDC.item(r, 2).setBackground(QColor("#FFF2CC"))  # 黄色

    ''' insert leds '''
    ledInitSta1Dev0 = add_led_txt(16, pInit, 1, 3, LED_STA1_LAB)
    ledInitSta1Dev1 = add_led_txt(16, pInit, 1, 8, LED_STA1_LAB)
    ledInitSta2Dev0 = add_led_txt(16, pInit, 2, 3, LED_STA2_LAB)
    ledInitSta2Dev1 = add_led_txt(16, pInit, 2, 8, LED_STA2_LAB)
    ledInitFem1Dev0 = add_led_txt(16, pInit, 3, 3, LED_FME1_LAB)
    ledInitFem1Dev1 = add_led_txt(16, pInit, 3, 8, LED_FME1_LAB)
    ledInitFem2Dev0 = add_led_txt(16, pInit, 4, 3, LED_FME2_LAB)
    ledInitFem2Dev1 = add_led_txt(16, pInit, 4, 8, LED_FME2_LAB)

    ledCurSta1Dev0 = add_led_txt(16, pCur, 1, 3, LED_STA1_LAB)
    ledCurSta1Dev1 = add_led_txt(16, pCur, 1, 8, LED_STA1_LAB)
    ledCurSta2Dev0 = add_led_txt(16, pCur, 2, 3, LED_STA2_LAB)
    ledCurSta2Dev1 = add_led_txt(16, pCur, 2, 8, LED_STA2_LAB)
    ledCurFem1Dev0 = add_led_txt(16, pCur, 3, 3, LED_FME1_LAB)
    ledCurFem1Dev1 = add_led_txt(16, pCur, 3, 8, LED_FME1_LAB)
    ledCurFem2Dev0 = add_led_txt(16, pCur, 4, 3, LED_FME2_LAB)
    ledCurFem2Dev1 = add_led_txt(16, pCur, 4, 8, LED_FME2_LAB)

    ledDcByte = add_led_txt(8, pDC, 0, 2, LED_LAB_DC)
    ledAlert0 = add_led_txt(16, pDC, 1, 2, LED_LAB_ALERT0)
    ledAlert1 = add_led_txt(16, pDC, 2, 2, LED_LAB_ALERT1)
    ledAlert2 = add_led_txt(16, pDC, 3, 2, LED_LAB_ALERT2)
    ledAlert = ledAlert0 + ledAlert1 + ledAlert2

    ledInitDev0 = [ledInitSta1Dev0, ledInitSta2Dev0, ledInitFem1Dev0, ledInitFem2Dev0]
    ledInitDev1 = [ledInitSta1Dev1, ledInitSta2Dev1, ledInitFem1Dev1, ledInitFem2Dev1]
    ledCurDev0 = [ledCurSta1Dev0, ledCurSta2Dev0, ledCurFem1Dev0, ledCurFem2Dev0]
    ledCurDev1 = [ledCurSta1Dev1, ledCurSta2Dev1, ledCurFem1Dev1, ledCurFem2Dev1]

    return ledInitDev0, ledInitDev1, ledCurDev0, ledCurDev1, ledDcByte, ledAlert




def adjust_appCfgPage_tables(pAppCfgTable, pAlertTable, pThreTable, pAcqTable):
    pAppCfgTable.setColumnWidth(0, 100)
    pAppCfgTable.setColumnWidth(1, 150)
    pAppCfgTable.setColumnWidth(2, 100)
    pAppCfgTable.setColumnWidth(3, 300)
    pAppCfgTable.setColumnWidth(4, 300)
    pAppCfgTable.setColumnWidth(5, 300)
    pAppCfgTable.setColumnWidth(6, 300)
    pAppCfgTable.setColumnWidth(7, 100)
    pAppCfgTable.setColumnWidth(8, 100)

    for c in range(10):
        pAlertTable.setColumnWidth(c, pAppCfgTable.columnWidth(c))
        pThreTable.setColumnWidth(c, pAppCfgTable.columnWidth(c))
        pAcqTable.setColumnWidth(c, pAppCfgTable.columnWidth(c))

def set_appCfgPage_table_color(pAppCfgTable, pAlertTable, pThreTable, pAcqTable):
    for r in range(5):
        for c in range(2, 9):
            pAppCfgTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            pAppCfgTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pAppCfgTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pAppCfgTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pAppCfgTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色

    for r in range(4):
        for c in range(2, 9):
            pAlertTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            pAlertTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pAlertTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pAlertTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pAlertTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色
            pAcqTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            pAcqTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pAcqTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pAcqTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pAcqTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色

    for r in range(14):
        for c in range(2, 9):
            pThreTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            pThreTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pThreTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pThreTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色



def adjust_diagCfgPage_tables(pTeCurTable, pDiagThrTable, pAluTable):
     pTeCurTable.setColumnWidth(0, pDiagThrTable.columnWidth(0))
     pAluTable.setColumnWidth(0, pDiagThrTable.columnWidth(0))
     pTeCurTable.setColumnWidth(1, pDiagThrTable.columnWidth(1))
     pAluTable.setColumnWidth(1, pDiagThrTable.columnWidth(1))
     pTeCurTable.setColumnWidth(2, pDiagThrTable.columnWidth(2))
     pAluTable.setColumnWidth(2, pDiagThrTable.columnWidth(2))
     pDiagThrTable.setColumnWidth(3, pTeCurTable.columnWidth(3)+pTeCurTable.columnWidth(4))
     pAluTable.setColumnWidth(3, pDiagThrTable.columnWidth(3))
     pDiagThrTable.setColumnWidth(4, pTeCurTable.columnWidth(5) + pTeCurTable.columnWidth(6))
     pAluTable.setColumnWidth(4, pDiagThrTable.columnWidth(4))
     pDiagThrTable.setColumnWidth(5, pTeCurTable.columnWidth(7) + pTeCurTable.columnWidth(8))
     pAluTable.setColumnWidth(5, pDiagThrTable.columnWidth(5))
     pDiagThrTable.setColumnWidth(6, pTeCurTable.columnWidth(9) + pTeCurTable.columnWidth(10))
     pAluTable.setColumnWidth(6, pDiagThrTable.columnWidth(6))


def set_diagCfgPage_table_color(pTeCurTable, pDiagThrTable, pAluTable):
    for r in range(3):
        for c in range(2, 13):
            if c == 2:
                pTeCurTable.item(r, c).setBackground(QColor("#DAE3F3"))     # 紫色
            elif c == 3 or c == 5 or c == 7 or c == 9:
                pTeCurTable.item(r, c).setBackground(QColor("#FFF2CC"))     # 黄色
            elif c == 11 or c == 12:
                pTeCurTable.item(r, c).setBackground(QColor("#E2F0D9"))     # 绿色

    for r in range(12):
        if r < 4:
            pAluTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            pAluTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pAluTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色
        pDiagThrTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
        pDiagThrTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
        pDiagThrTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
        pDiagThrTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色


def adjust_meaAcqDetailPage_tables(pAlertRegDev0, pDataRegDev0, pAlertRegDev1, pDataRegDev1):
    pAlertRegDev0.setColumnWidth(0, 100)
    pAlertRegDev0.setColumnWidth(1, 150)
    pAlertRegDev0.setColumnWidth(2, 100)
    pDataRegDev0.setColumnWidth(0, 100)
    pDataRegDev0.setColumnWidth(1, 150)
    pDataRegDev0.setColumnWidth(2, 100)
    pAlertRegDev1.setColumnWidth(0, 100)
    pAlertRegDev1.setColumnWidth(1, 150)
    pAlertRegDev1.setColumnWidth(2, 100)
    pDataRegDev1.setColumnWidth(0, 100)
    pDataRegDev1.setColumnWidth(1, 150)
    pDataRegDev1.setColumnWidth(2, 100)

    for i in range(3, 19):
        pDataRegDev0.setColumnWidth(i, 90)
        pDataRegDev1.setColumnWidth(i, 90)

    pAlertRegDev0.setColumnWidth(3, 90 * 16)
    pAlertRegDev1.setColumnWidth(3, 90 * 16)

def set_meaAcqDetailPage_table_color(pAlertRegDev0, pDataRegDev0, pAlertRegDev1, pDataRegDev1):
    for r in range(6):
        pAlertRegDev0.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
        pAlertRegDev1.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
        pAlertRegDev0.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
        pAlertRegDev1.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色

    boldFont = QFont()
    boldFont.setBold(True)
    for r in range(12):
        for c in range(0, 19):
            if r == 0 or r == 3 or r == 6 or r == 9:
                pDataRegDev0.item(r, c).setBackground(QColor("#BFBFBF"))  # 灰色
                pDataRegDev1.item(r, c).setBackground(QColor("#BFBFBF"))  # 灰色
                pDataRegDev0.item(r, c).setFont(boldFont)  # 字体加粗
                pDataRegDev1.item(r, c).setFont(boldFont)  # 字体加粗
            if c > 2:
                if r == 1 or r == 4 or r == 7 or r == 10:
                    pDataRegDev0.item(r, c).setBackground(QColor("#E2F0D9"))  # 绿色
                    pDataRegDev1.item(r, c).setBackground(QColor("#E2F0D9"))  # 绿色
                if r == 2 or r == 5 or r == 8 or r == 11:
                    pDataRegDev0.item(r, c).setBackground(QColor("#FFF2CC"))  # 黄色
                    pDataRegDev1.item(r, c).setBackground(QColor("#FFF2CC"))  # 黄色

def meaAcqDetailPage_insert_led(pAlertRegDev0, pAlertRegDev1):
        # 插入 LED 图标对象
        ledList0 = add_led_txt(16, pAlertRegDev0, 0, 3, LED_LAB_16)  # 第一行插入
        ledList1 = add_led_txt(16, pAlertRegDev0, 1, 3, LED_LAB_16)  # 第二行插入
        ledList2 = add_led_txt(16, pAlertRegDev0, 2, 3, LED_LAB_16)  # 第三行插入
        ledList3 = add_led_txt(16, pAlertRegDev0, 3, 3, LED_LAB_16)  # 第四行插入
        ledList4 = add_led_txt(16, pAlertRegDev0, 4, 3, LED_LAB_16)  # 第三行插入
        ledList5 = add_led_txt(16, pAlertRegDev0, 5, 3, LED_LAB_16)  # 第四行插入

        ledList6 = add_led_txt(16, pAlertRegDev1, 0, 3, LED_LAB_16)  # 第一行插入
        ledList7 = add_led_txt(16, pAlertRegDev1, 1, 3, LED_LAB_16)  # 第二行插入
        ledList8 = add_led_txt(16, pAlertRegDev1, 2, 3, LED_LAB_16)  # 第三行插入
        ledList9 = add_led_txt(16, pAlertRegDev1, 3, 3, LED_LAB_16)  # 第四行插入
        ledList10 = add_led_txt(16, pAlertRegDev1, 4, 3, LED_LAB_16)  # 第三行插入
        ledList11 = add_led_txt(16, pAlertRegDev1, 5, 3, LED_LAB_16)  # 第四行插入

        dev0_led_list = [ledList0, ledList1, ledList2, ledList3, ledList4, ledList5]
        dev1_led_list = [ledList6, ledList7, ledList8, ledList9, ledList10, ledList11]

        return dev0_led_list, dev1_led_list


def adjust_diagAcqDataPage_tables(pStaTable, pAlerDev0Table, pDataDev0Table, pAlerDev1Table, pDataDev1Table):
    ''' adjust status table '''
    # set status table column size
    for c in range(12):
        if c == 0 or c == 2 or c == 7:
            pStaTable.setColumnWidth(c, 111)
        elif c == 1:
            pStaTable.setColumnWidth(c, 150)
        else:
            pStaTable.setColumnWidth(c, 120)

    # span status table and set background color
    pStaTable.setSpan(0, 2, 1, 10)
    pStaTable.item(0,2).setText(' ')
    pStaTable.item(0,1).setBackground(QColor("#E2F0D9"))  # 绿色
    pStaTable.item(0,2).setBackground(QColor("#FFF2CC"))  # 黄色
    pStaTable.setSpan(1, 2, 1, 10)
    pStaTable.item(1, 2).setText(' ')
    pStaTable.item(1, 1).setBackground(QColor("#E2F0D9"))  # 绿色
    pStaTable.item(1, 2).setBackground(QColor("#FFF2CC"))  # 黄色

    # status table insert led
    led8List = add_led_txt(8, pStaTable, 0, 2, LED_LAB_8)
    led32List = add_led_txt(32, pStaTable, 1, 2, LED_LAB_32)

    led16Dev0 = []
    led16Dev1 = []

    for r in range(2, 15):
        if r != 7 and r!=8 and r!=9 and r!=10:
            pStaTable.setSpan(r, 3, 1, 4)
            pStaTable.item(r, 3).setText(' ')
            pStaTable.setSpan(r, 8, 1, 4)
            pStaTable.item(r, 8).setText(' ')
            if 2 < r < 7:
                pStaTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
                led16Dev0.append(add_led_txt(16, pStaTable, r, 3, LED_LAB_16))   # insert led
                pStaTable.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
                led16Dev1.append(add_led_txt(16, pStaTable, r, 8, LED_LAB_16))   # insert led
        else:
            pStaTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 10).setBackground(QColor("#FFF2CC"))  # 黄色
        if r != 2:
            pStaTable.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
            pStaTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色

    boldFont = QFont()
    boldFont.setBold(True)
    for c in range (12):
        pStaTable.item(2, c).setFont(boldFont)  # 字体加粗

    ''' adjust device tables '''
    # set device tables column size
    for c in range(20):
        if c == 0 or c == 2:
            pAlerDev0Table.setColumnWidth(c, 111)
            pDataDev0Table.setColumnWidth(c, 111)
            pAlerDev1Table.setColumnWidth(c, 111)
            pDataDev1Table.setColumnWidth(c, 111)
        elif c == 1:
            pAlerDev0Table.setColumnWidth(c, 150)
            pDataDev0Table.setColumnWidth(c, 150)
            pAlerDev1Table.setColumnWidth(c, 150)
            pDataDev1Table.setColumnWidth(c, 150)
        else:
            pAlerDev0Table.setColumnWidth(c, 63)
            pDataDev0Table.setColumnWidth(c, 63)
            pAlerDev1Table.setColumnWidth(c, 63)
            pDataDev1Table.setColumnWidth(c, 63)

    # set device tables background color
    for c in range (20):
        pDataDev0Table.item(0, c).setFont(boldFont)  # 字体加粗
        pDataDev1Table.item(0, c).setFont(boldFont)  # 字体加粗
        if c > 2:
            pDataDev0Table.item(1, c).setBackground(QColor("#E2F0D9"))  # 绿色
            pDataDev1Table.item(1, c).setBackground(QColor("#E2F0D9"))  # 绿色
            pDataDev0Table.item(2, c).setBackground(QColor("#FFF2CC"))  # 黄色
            pDataDev1Table.item(2, c).setBackground(QColor("#FFF2CC"))  # 黄色

    # device tables insert led
    led17Dev0 = []
    led17Dev1 = []

    for r in range(2):
        pAlerDev0Table.setSpan(r, 3, 1, 18)
        pAlerDev0Table.item(r, 3).setText(' ')
        pAlerDev0Table.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
        led17Dev0.append(add_led_txt(17, pAlerDev0Table, r, 3, LED_LAB_17))   # insert led
        pAlerDev1Table.setSpan(r, 3, 1, 18)
        pAlerDev1Table.item(r, 3).setText(' ')
        pAlerDev1Table.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
        led17Dev1.append(add_led_txt(17, pAlerDev1Table, r, 3, LED_LAB_17))  # insert led

    return led8List, led32List, led16Dev0, led16Dev1


def adjust_meaAcqSumPage_tables(pStaTable, pSumDataDev0Table, pSumDataDev1Table):
    ''' adjust status table '''
    # adjust status table column size
    for c in range(12):
        if c == 0 or c == 2 or c == 7:
            pStaTable.setColumnWidth(c, 104)
        elif c == 1:
            pStaTable.setColumnWidth(c, 150)
        else:
            pStaTable.setColumnWidth(c, 120)

    # span status table and set background color
    pStaTable.setSpan(0, 2, 1, 10)
    pStaTable.item(0,2).setText(' ')
    pStaTable.item(0,1).setBackground(QColor("#E2F0D9"))  # 绿色
    pStaTable.item(0,2).setBackground(QColor("#FFF2CC"))  # 黄色
    pStaTable.setSpan(1, 2, 1, 10)
    pStaTable.item(1, 2).setText(' ')
    pStaTable.item(1, 1).setBackground(QColor("#E2F0D9"))  # 绿色
    pStaTable.item(1, 2).setBackground(QColor("#FFF2CC"))  # 黄色

    # insert led
    led8List = add_led_txt(8, pStaTable, 0, 2, LED_LAB_8)
    led32List = add_led_txt(32, pStaTable, 1, 2, LED_LAB_32)

    led16Dev0 = []
    led16Dev1 = []

    for r in range(2, 15):
        if r != 7 and r!=8 and r!=9 and r!=10:
            pStaTable.setSpan(r, 3, 1, 4)
            pStaTable.item(r, 3).setText(' ')
            pStaTable.setSpan(r, 8, 1, 4)
            pStaTable.item(r, 8).setText(' ')
            if 2 < r < 7:
                pStaTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
                led16Dev0.append(add_led_txt(16, pStaTable, r, 3, LED_LAB_16))   # insert led
                pStaTable.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
                led16Dev1.append(add_led_txt(16, pStaTable, r, 8, LED_LAB_16))   # insert led
        else:
            pStaTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 10).setBackground(QColor("#FFF2CC"))  # 黄色
        if r != 2:
            pStaTable.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
            pStaTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色

    boldFont = QFont()
    boldFont.setBold(True)
    for c in range (12):
        pStaTable.item(2, c).setFont(boldFont)  # 字体加粗

    ''' adjust device tables '''
    # set device tables column size
    for c in range(20):
        if c == 0 or c == 2:
            pSumDataDev0Table.setColumnWidth(c, 104)
            pSumDataDev1Table.setColumnWidth(c, 104)
        elif c == 1:
            pSumDataDev0Table.setColumnWidth(c, 150)
            pSumDataDev1Table.setColumnWidth(c, 150)
        else:
            pSumDataDev0Table.setColumnWidth(c, 133)
            pSumDataDev1Table.setColumnWidth(c, 133)

    # span device tables and set background color
    for r in range(1,10):
        if r!= 7:
            # dev0
            pSumDataDev0Table.setSpan(r, 3, 1, 4)
            pSumDataDev0Table.item(r, 3).setText('0')
            pSumDataDev0Table.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pSumDataDev0Table.setSpan(r, 7, 1, 4)
            pSumDataDev0Table.item(r, 7).setText('% (Ratiometric 100% Full Scale, 1.526e-3% LSB)')
            # dev1
            pSumDataDev1Table.setSpan(r, 3, 1, 4)
            pSumDataDev1Table.item(r, 3).setText('0')
            pSumDataDev1Table.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pSumDataDev1Table.setSpan(r, 7, 1, 4)
            pSumDataDev1Table.item(r, 7).setText('% (Ratiometric 100% Full Scale, 1.526e-3% LSB)')

    pSumDataDev0Table.item(0, 3).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev0Table.item(0, 5).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev0Table.item(0, 7).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev0Table.item(0, 9).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev0Table.item(7, 5).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev0Table.item(7, 9).setBackground(QColor("#FFF2CC"))  # 黄色

    pSumDataDev1Table.item(0, 3).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev1Table.item(0, 5).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev1Table.item(0, 7).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev1Table.item(0, 9).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev1Table.item(7, 5).setBackground(QColor("#FFF2CC"))  # 黄色
    pSumDataDev1Table.item(7, 9).setBackground(QColor("#FFF2CC"))  # 黄色

    return led8List, led32List, led16Dev0, led16Dev1


def adjust_cblPage_tables(pExpTable, pCfgTable, pCtrlDemoTable, pCtrlInfTable):
    ''' adjust expiration time table '''
    pExpTable.setColumnWidth(1, 120)
    pExpTable.setColumnWidth(2, 120)
    pExpTable.item(0, 0).setBackground(QColor("#DAE3F3"))  # 蓝色
    pExpTable.item(0, 1).setBackground(QColor("#FFF2CC"))  # 黄色

    ''' adjust status information table '''
    # adjust status information table column size
    for c in range(16):
        if c == 1:
            pCtrlInfTable.setColumnWidth(c, 150)
        else:
            pCtrlInfTable.setColumnWidth(c, 100)

    # status information table set span and background color
    for r in range(6):
        if r!=3 and r!=4:
            pCtrlInfTable.setSpan(r, 3, 1, 6)
            pCtrlInfTable.setSpan(r, 10, 1, 6)
            if r == 1:
                pCtrlInfTable.item(r, 3).setText('Current CBAL details, updated in response to a Start, '
                                                 'Stop, or Read Back request.')
            else:
                pCtrlInfTable.item(r, 3).setText(' ')
        if r == 3:
            pCtrlInfTable.setSpan(r, 3, 1, 3)
            pCtrlInfTable.item(r, 3).setText('0')
            pCtrlInfTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pCtrlInfTable.setSpan(r, 6, 1, 3)
            pCtrlInfTable.item(r, 6).setText('Time per Channel Group (Minutes, decimal)')
            pCtrlInfTable.setSpan(r, 10, 1, 3)
            pCtrlInfTable.item(r, 10).setText('0')
            pCtrlInfTable.item(r, 10).setBackground(QColor("#FFF2CC"))  # 黄色
            pCtrlInfTable.setSpan(r, 13, 1, 3)
            pCtrlInfTable.item(r, 13).setText('Time per Channel Group (Minutes, decimal)')

    for r in range(6):
        if r == 2 or r == 5:
            pCtrlInfTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pCtrlInfTable.item(r, 10).setBackground(QColor("#FFF2CC"))  # 黄色
        if r != 0:
            pCtrlInfTable.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
            pCtrlInfTable.item(r, 9).setBackground(QColor("#E2F0D9"))  # 绿色
        if r == 4:
            pCtrlInfTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pCtrlInfTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pCtrlInfTable.item(r, 7).setBackground(QColor("#FFF2CC"))  # 黄色
            pCtrlInfTable.item(r, 10).setBackground(QColor("#FFF2CC"))  # 黄色
            pCtrlInfTable.item(r, 12).setBackground(QColor("#FFF2CC"))  # 黄色
            pCtrlInfTable.item(r, 14).setBackground(QColor("#FFF2CC"))  # 黄色

    boldFont = QFont()
    boldFont.setBold(True)
    for c in [0,1,2,3,9,10]:
        pCtrlInfTable.item(0, c).setFont(boldFont)  # 字体加粗

    # insert led
    led16StaDev0 = []
    led16StaDev1 = []
    led16UvDev0 = []
    led16UvDev1 = []
    led16StaDev0.append(add_led_txt(16, pCtrlInfTable, 2, 3, LED_LAB_16))
    led16StaDev1.append(add_led_txt(16, pCtrlInfTable, 2, 10, LED_LAB_16))
    led16UvDev0.append(add_led_txt(16, pCtrlInfTable, 5, 3, LED_LAB_16))
    led16UvDev1.append(add_led_txt(16, pCtrlInfTable, 5, 10, LED_LAB_16))

    ''' adjust cblCfg & ctrlDemo tables '''
    for c in range(6):
        if c == 1:
            pCfgTable.setColumnWidth(c, 150)
            pCtrlDemoTable.setColumnWidth(c, 150)
        elif c == 3:
            pCfgTable.setColumnWidth(c, 1100)
            pCtrlDemoTable.setColumnWidth(c, 1100)
        else:
            pCfgTable.setColumnWidth(c, 100)
            pCtrlDemoTable.setColumnWidth(c, 100)

    for r in range(5):
        if r < 2:
            pCtrlDemoTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 蓝色
        pCfgTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 蓝色
        pCfgTable.item(r, 4).setBackground(QColor("#E2F0D9"))  # 绿色
        pCfgTable.item(r, 5).setBackground(QColor("#E2F0D9"))  # 绿色

    for c in range(3,6):
        pCtrlDemoTable.item(0, c).setBackground(QColor("#FFC000"))  # 橙色
        pCtrlDemoTable.item(1, c).setBackground(QColor("#FF0000"))  # 红色

    return led16StaDev0, led16StaDev1, led16UvDev0, led16UvDev1



def update_led_color(label, color):
    """
    更新LED颜色的函数。

    :param label: 要更新的QLabel实例。
    :param color: 一个包含颜色代码的字符串，比如 "#FF0000" 表示红色。
    """
    style_sheet = f"""
          QLabel {{
              border-radius: 5px; /* 保持圆形 */
              background: qradialgradient(
                  cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5,
                  stop: 0 #ffffff, /* 渐变的中心是白色 */
                  stop: 0.4 {color}, /* 自定义颜色 */
                  stop: 0.5 {color}, /* 稍微改变颜色以实现渐变效果 */
                  stop: 1.0 {color}); /* 边缘颜色 */
              box-shadow: 0px 0px 8px 0px {color}; /* 阴影颜色 */
          }}
          """
    label.setStyleSheet(style_sheet)