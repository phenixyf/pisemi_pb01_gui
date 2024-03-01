# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 10:42
# @Author  : yifei.su
# @File    : ui_configure.py


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QFont
import sys
import ctypes
from ctypes.wintypes import MSG
import ctypes.wintypes as wintypes
import hid

target_pid = 0xfe07  # 用你的目标PID替换这里
target_vid = 0x1a86  # 用你的目标VID替换这里

BTN_OP_DELAY = 0.05     # 防止 button 被连续点击 delay 时间

""" chainCfgPage configure push button style """
btn_blue_style = "QPushButton {\n"
"    background-color: #3072B3; /* 按钮背景颜色 */\n"
"    color: white; /* 文字颜色 */\n"
"    border-style: solid; /* 边框样式 */\n"
"    border-width: 2px; /* 边框宽度 */\n"
"    border-radius: 10px; /* 边框圆角半径 */\n"
"    border-color: #145289; /* 边框颜色 */\n"
"    padding: 5px; /* 内边距 */\n"
"    font: 10pt \"Calibri\"; /* 字体 */\n"
"    font-weight: 600; /* 字体粗细 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #5591D2; /* 悬停时的背景颜色 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1E5A97; /* 按下时的背景颜色 */\n"
"}\n"
""

btn_gray_style = "QPushButton {\n"
"    background-color: #c0c0c0; /* 按钮背景颜色 */\n"
"    color: white; /* 文字颜色 */\n"
"    border-style: solid; /* 边框样式 */\n"
"    border-width: 2px; /* 边框宽度 */\n"
"    border-radius: 10px; /* 边框圆角半径 */\n"
"    border-color: #145289; /* 边框颜色 */\n"
"    padding: 5px; /* 内边距 */\n"
"    font: 10pt \"Calibri\"; /* 字体 */\n"
"    font-weight: 600; /* 字体粗细 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #5591D2; /* 悬停时的背景颜色 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1E5A97; /* 按下时的背景颜色 */\n"
"}\n"
""

""" warning lineEdit style """
lineEdit_warn_style = "QLineEdit {" \
                      "font: 11pt 'Calibri'; /* 字体 */" \
                      "font-weight: 700; /* 字体粗细 */" \
                      "color: white; /* 文字颜色 */" \
                      "background-color: #ff0000; /* 按钮背景颜色 1*/" \
                      "border-color: #ce4500; /* 边框颜色 3*/" \
                      "border-width: 2px; /* 边框宽度 */" \
                      "border-radius: 10px; /* 边框圆角半径 */" \
                      "padding: 5px; /* 内边距 */" \
                      "}"

lineEdit_default_style = "QLineEdit {" \
                      "font: 11pt 'Calibri'; /* 字体 */" \
                      "font-weight: 700; /* 字体粗细 */" \
                      "color: white; /* 文字颜色 */" \
                      "background-color: lightblue; /* 按钮背景颜色 1*/" \
                      "border-color: #ce4500; /* 边框颜色 3*/" \
                      "border-width: 2px; /* 边框宽度 */" \
                      "border-radius: 10px; /* 边框圆角半径 */" \
                      "padding: 5px; /* 内边距 */" \
                      "}"

""" led string related """
''' led qss '''
led_green_style = "QLabel {\n" \
          "  border-radius: 5px; /* 使得QLabel成为圆形 */\n" \
          "  background: qradialgradient(\n" \
          "    cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5,\n" \
          "    stop: 0 #ffffff, /* 渐变的中心是白色 */\n" \
          "    stop: 0.4 #00aa00, /* 渐变为绿色 */\n" \
          "    stop: 0.5 #009900, /* 中间的圆环更浅的绿色 */\n" \
          "    stop: 1.0 #006600); /* 边缘是最浅的绿色 */\n" \
          "  box-shadow: 0px 0px 8px 0px #006600; /* 添加阴影以增强3D效果 */\n" \
          "}"

led_gray_style = "QLabel {\n" \
          "  border-radius: 5px; /* 使得QLabel成为圆形 */\n" \
          "  background: qradialgradient(\n" \
          "    cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5,\n" \
          "    stop: 0 #ffffff, /* 渐变的中心是白色 */\n" \
          "    stop: 0.4 #aaaaaa, /* 渐变为灰色 */\n" \
          "    stop: 0.5 #999999, /* 中间的圆环更浅的灰色 */\n" \
          "    stop: 1.0 #666666); /* 边缘是最浅的灰色 */\n" \
          "  box-shadow: 0px 0px 8px 0px #666666; /* 添加阴影以增强3D效果 */\n" \
          "}"

led_red_style = "QLabel {\n" \
          "  border-radius: 5px; /* 使得QLabel成为圆形 */\n" \
          "  background: qradialgradient(\n" \
          "    cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5,\n" \
          "    stop: 0 #ffffff, /* 渐变的中心是白色 */\n" \
          "    stop: 0.4 #ee0000, /* 渐变为红色 */\n" \
          "    stop: 0.5 #dd0000, /* 中间的圆环更浅的红色 */\n" \
          "    stop: 1.0 #cc0000); /* 边缘是最浅的红色 */\n" \
          "  box-shadow: 0px 0px 8px 0px #cc0000; /* 添加阴影以增强3D效果 */\n" \
          "}"

led_blue_style = "QLabel {\n" \
          "  border-radius: 5px; /* 使得QLabel成为圆形 */\n" \
          "  background: qradialgradient(\n" \
          "    cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5,\n" \
          "    stop: 0 #ffffff, /* 渐变的中心是白色 */\n" \
          "    stop: 0.4 #1E90FF, /* 渐变为蓝色 */\n" \
          "    stop: 0.5 #1E90FF, /* 中间的圆环更浅的蓝色 */\n" \
          "    stop: 1.0 #4169E1); /* 边缘是最浅的蓝色 */\n" \
          "  box-shadow: 0px 0px 8px 0px #4169E1; /* 添加阴影以增强3D效果 */\n" \
          "}"

led_white_style = "QLabel {\n" \
          "  border-radius: 5px; /* 使得QLabel成为圆形 */\n" \
          "  background: qradialgradient(\n" \
          "    cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5,\n" \
          "    stop: 0 #ffffff, /* 渐变的中心是白色 */\n" \
          "    stop: 0.4 #f0f0f0, /* 渐变为白色 */\n" \
          "    stop: 0.5 #e6e6e6, /* 中间的圆环更浅的白色 */\n" \
          "    stop: 1.0 #cccccc); /* 边缘是最浅的白色 */\n" \
          "  box-shadow: 0px 0px 8px 0px #aaaaaa; /* 添加阴影以增强3D效果 */\n" \
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
    label_led.setStyleSheet(led_gray_style)
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

""" HID """
NULL = 0
INVALID_HANDLE_VALUE = -1
DEVICE_NOTIFY_WINDOW_HANDLE = 0x00000000
WM_DEVICECHANGE = 0x0219            # windows 系统设备变动事件序号
DBT_DEVTYP_DEVICEINTERFACE = 5
DBT_DEVICEREMOVECOMPLETE = 0x8004   # windows 系统设备移出信息序号
DBT_DEVICEARRIVAL = 0x8000          # windows 系统设备插入信息序号

user32 = ctypes.windll.user32
RegisterDeviceNotification = user32.RegisterDeviceNotificationW
UnregisterDeviceNotification = user32.UnregisterDeviceNotification

class GUID(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("Data1", ctypes.c_ulong),
                ("Data2", ctypes.c_ushort),
                ("Data3", ctypes.c_ushort),
                ("Data4", ctypes.c_ubyte * 8)]


class DEV_BROADCAST_DEVICEINTERFACE(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("dbcc_size", wintypes.DWORD),
                ("dbcc_devicetype", wintypes.DWORD),
                ("dbcc_reserved", wintypes.DWORD),
                ("dbcc_classguid", GUID),
                ("dbcc_name", ctypes.c_wchar * 260)]


class DEV_BROADCAST_HDR(ctypes.Structure):
    _fields_ = [("dbch_size", wintypes.DWORD),
                ("dbch_devicetype", wintypes.DWORD),
                ("dbch_reserved", wintypes.DWORD)]

GUID_DEVINTERFACE_USB_DEVICE = GUID(0xA5DCBF10, 0x6530, 0x11D2,
                                    (ctypes.c_ubyte * 8)(0x90, 0x1F, 0x00, 0xC0, 0x4F, 0xB9, 0x51, 0xED))


""" CHAIN CONFIGURATION page tablewidget initial content """
CHAIN_CFG_TABLE_HEHG = 30       # table header row height
CHAIN_CFG_TABLE_ROWHG = 18      # table row height
CHAIN_CFG_TABLE_STAHG = 120     # status block 不显示 header 的 4 个 table 的高度
CHAIN_CFG_TABLE_RSTHG = 60      # reset block table 的高度

''' 16 led label '''
LED_STA1_LAB = ["ACQ", "RESET", "RJCT", "UIF", "OV", "UV", "ALTOV", "ALTUV",
                "AUXOV", "AUXUV", "DIAGOV", "DIAGUV", "MM", "CBAL", "FMEA2", "FMEA1"]
LED_STA2_LAB = ["PECUP", "PECDN", "MANUP", "MANDN", "PARUP", "PARDN", "REGUP", "REGDN",
                "DUAL", "CBNTFY", "CBDONE", "CBERR", "SPIRW", "SPICLK", "SPICRC", "SPIREG"]
LED_FME1_LAB = ["OSC", "----", "----", "----", "----", "VAA", "VDD", "VIO",
                "AGND2", "AGND", "DGND", "IOGND", "HVOV", "HVUV", "TEMP2", "TEMP1"]
LED_FME2_LAB = ["HVHDRM", "ACQTO", "----", "----", "ADC1ZS", "ADC1FS", "ADC2ZS", "ADC2FS",
                "USER", "MODE", "AINIT", "DINIT", "OTPERR", "REGECC", "MBIST", "CBIST"]
LED_DC_LAB = ["INTFC", "FMEA", "PROC", "DIAG", "OV", "UV", "AUXOV", "AUXUV"]
LED_ALERT0_LAB = ["ACQ", "RESET", "RJCT", "UIF", "OV", "UV", "ALTOV", "ALTUV",
                "AUXOV", "AUXUV", "DIAGOV", "DIAGUV", "MM", "CBAL", "FMEA2", "FMEA1"]
LED_ALERT1_LAB = ["LOC31", "LOC30", "LOC29", "LOC28", "LOC27", "LOC26", "LOC25", "LOC24",
                "LOC23", "LOC22", "LOC21", "LOC20", "LOC19", "LOC18", "LOC17", "LOC16"]
LED_ALERT2_LAB = ["LOC15", "LOC14", "LOC13", "LOC12", "LOC11", "LOC10", "LOC9", "LOC8",
                "LOC7", "LOC6", "LOC5", "LOC4", "LOC3", "LOC2", "LOC1", "LOC0"]
LED_16_LAB = ["15", "14", "13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0"]
LED_8_LAB = ["LED7", "LED6", "LED5", "LED4", "LED3", "LED2", "LED1", "LED0"]
LED_17_LAB = ["LED16", "LED15", "LED14", "LED13", "LED12", "LED11", "LED10", "LED9", "LED8",
                "LED7", "LED6", "LED5", "LED4", "LED3", "LED2", "LED1", "LED0"]
LED_CBALSTAT_LAB = ["CBON", "CBACT", "CBDEXP", "CBDUV", "CBETMP", "CBEHV", "CBEATO", "CBEAZF",
                   "CBETO", "CBAOV", "CBAUV", "CBAALTOV", "CBAALTUV", "CBAAUXOV", "CBAAUXUV", "CBAMM"]
LED_CBALUVSTAT_LAB = ["CBUV15", "CBUV14", "CBUV13", "CBUV12", "CBUV11", "CBUV10", "CBUV9", "CBUV8",
                      "CBUV7", "CBUV6", "CBUV5", "CBUV4", "CBUV3", "CBUV2", "CBUV1", "CBUV0"]


''' chain configuration page tablewidget initial content (page1) '''
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

# table_chainCfg_pwHeaders = ["Address", "Register", "FORCEPOR (hex)", "Device 0 (hex)", "", "Device 1 (hex)", ""]
table_chainCfg_pwItems = [
    ["Address", "Register", "FORCEPOR (hex)", "Device 0 (hex)", "", "Device 1 (hex)", ""],
    ["0x04", "STATUS1", "5000", "5000", "", "5000", ""],
    ["0x05", "STATUS2", "0080", "0080", "", "0080", ""],
    ["0x06", "FMEA1",   "0000", "0000", "", "0000", ""],
    ["0x07", "FMEA2",   "0000", "0000", "", "0000", ""]
]

# table_chainCfg_rstHeaders = ["Address", "Register", "Expect (hex)", "Device 0 (hex)", "", "Device 1 (hex)", ""]
table_chainCfg_rstItems = [
["Address", "Register", "Expect (hex)", "Device 0 (hex)", "", "Device 1 (hex)", ""],
["0x0F", "RESETCTRL", "0001", "0000", " ", "0000", " "]
]

""" device manage page tablewidget initial content  (page2) """
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
    ["ALERTPACKET", "5000_0000_0001/3", " "],
    ["ALERTPACKET", "5000_0000_0001/3", " "],
    ["ALERTPACKET", "5000_0000_0001/3", " "]
]

table_devMg_curItems = [
    ["Address", "Register", "Device 0 (hex)", " ", " ", " ", " ",
                                "Device 1 (hex)", " ", " ", " ", " "],
    ["0x04", "STATUS1",     "5000", " ", " ", " ", "", "5000", " ", " ", " ", ""],
    ["0x05", "STATUS2",     "0080", " ", " ", " ", "", "0080", " ", " ", " ", ""],
    ["0x06", "FMEA1",       "0000", " ", " ", " ", "", "0000", " ", " ", " ", ""],
    ["0x07", "FMEA2",       "0000", " ", " ", " ", "", "0000", " ", " ", " ", ""],
    ["0x08", "TEMPREG1",    "0960", "26.9", "°C", "80.3", "°F", "0960", "26.9", "°C", "80.3", "°F"],
    ["0x09", "TEMPREG2",    "0960", "26.9", "°C", "80.3", "°F", "0960", "26.9", "°C", "80.3", "°F"],
    ["0x0A", "GPIODATA",    "0000", "00", "GPIODOUT[7:0]", "00", "GPIODIN[7:0]",
                            "0000", "00", "GPIODOUT[7:0]", "00", "GPIODIN[7:0]", "0000"]
]

""" application configuration page tablewidget initial content  (page3) """
table_appCfgPage_headers = ["Address", "Register", "Pending (hex)", "Pending Value (bin)", "Pending Field",
                           "Pending Value (bin)", "Pending Field", "Device 0 (hex)", "Device 1 (hex)"]
table_appCfgPage_appCfgReg_items = [
    ["0x12", "STATUSCFG",   "3FFF", "00111111",  "STATUSCFG[15:8]", "11111111", "STATUSCFG[7:0]", "3FFF", "3FFF"],
    ["0x13", "DEVCFG",      "2000", "010",       "IIRFC[2:0]",      "000",      "DEVCFG[10:8]",   "2000", "2000"],
    ["0x14", "POLARITYCFG", "0000", "00000000",  "POLARITY[15:8]",  "00000000", "POLARITY[7:0]",  "0000", "0000"],
    ["0x15", "AUXGPIOCFG",  "0000", "00000000",  "GPIOEN[7:0]",     "00000000", "GPIOMODE[7:0]",  "FF00", "FF00"],
    ["0x16", "AUXREFCFG",   "0000", "00",        "THERMMODE[1:0]",  "00000000", "AUXREFSEL[7:0]", "0000", "0000"]
]

table_appCfgPage_alertCfgReg_items = [
    ["0x18", "ALRTOVCFG",    "FFFF", "11111111", "ALRTOVEN[15:8]",    "11111111", "ALRTOVEN[7:0]",       "0000", "0000"],
    ["0x19", "ALRTUVCFG",    "FFFF", "11111111", "ALRTUVEN[15:8]",    "11111111", "ALRTUVEN[7:0]",       "0000", "0000"],
    ["0x1A", "ALRTAUXOVCFG", "FFFF", "11111111", "ALRTAUXOVEN[7:0]",  "11111111", "ALRTALTAUXOVEN[7:0]", "0000", "0000"],
    ["0x1B", "ALRTAUXUVCFG", "FFFF", "11111111", "ALRTAUXUVEN[7:0]",  "11111111", "ALRTALTAUXUVEN[7:0]", "0000", "0000"]
]

table_appCfgPage_theresholdReg_items = [
    ["0x20", "OVTHREG",         "E667",     "4.500",    "V",           " ",   " ",  "FFFF",   "FFFF"],
    ["0x21", "UVTREG",          "8A3D",     "2.700",    "V",           " ",   " ",  "0000",   "0000"],
    ["0x22", "BIPOVTHREG",      "051F",     "+0.100",   "V (Bipolar)", " ",   " ",  "7FFF",   "7FFF"],
    ["0x23", "BIPUVTHREG",      "FAE1",     "-0.100",   "V (Bipolar)", " ",   " ",  "8000",   "8000"],
    ["0x24", "ALTOVTHREG",      "E667",     "4.500",    "V",           " ",   " ",  "FFFF",   "FFFF"],
    ["0x25", "ALTUVTHREG",      "8A3D",     "2.700",    "V",           " ",   " ",  "0000",   "0000"],
    ["0x26", "ALTBIPOVTHREG",   "051F",     "+0.100",   "V (Bipolar)", " ",   " ",  "7FFF",   "7FFF"],
    ["0x27", "ALTBIPUVTHREG",   "FAE1",     "-0.100",   "V (Bipolar)", " ",   " ",  "8000",   "8000"],
    ["0x28", "AUXROVTHREG",     "TBD",      "TBD",      "Ratiometric", " ",   " ",  "FFFF",   "FFFF"],
    ["0x29", "AUXRUVTHREG",     "TBD",      "TBD",      "Ratiometric", " ",   " ",  "0000",   "0000"],
    ["0x2A", "AUXAOVTHREG",     "FFFF",     "2.500",    "V",           " ",   " ",  "FFFF",   "FFFF"],
    ["0x2B", "AUXAUVTHREG",     "0000",     "0.000",    "V",           " ",   " ",  "0000",   "0000"],
    ["0x2C", "MMTHREG",         "0CCD",     "0.250",    "V",           " ",   " ",  "FFFF",   "FFFF"],
    ["0x2D", "TEMPTHREG",       "0C48",     "120",      "°C",          "248", "°F", "0C48",   "0C48"]
]

table_appCfgPage_acqReg_items = [
    ["0x40", "ACQDLY1",   "1501", "2.106",    "CELLDLY(ms)",        "0.096",    "SWDLY(ms)",         "0000", "0000"],
    ["0x41", "ACQDLY2",   "3220", "1.200",    "AUXDLY (ms)",        "12.768",   "CELLOPNDLY (ms)",   "0000", "0000"],
    ["0x42", "ACQCHSEL",  "FFFF", "11111111", "CELLEN[15:8] (bin)", "11111111", "CELLEN[7:0] (bin)", "0000", "0000"],
    ["0x43", "ACQAUXSEL", "00FF", " ",        " ",                  "11111111", "AUXEN[7:0] (bin)",  "0000", "0000"]
]

"""  diagnostic configuration page tablewidget initial content  (page4) """
table_diagCfgPage_testCfg_headers = ["Address", "Register", "Pending (hex)", "Pending Value (bin)", "Pending Field",
                           "Pending Value (bin)", "Pending Field", "Pending Value (bin)", "Pending Field",
                            "Pending Value (bin)", "Pending Field", "Device 0 (hex)", "Device 1 (hex)"]

table_diagCfgPage_testCfg_items = [
    ["0x1C", "CTSTCFG1",  "0001", "00",   "HVMUXTSTEN[1:0]", "0",    "CTSTPOL1",     "0",    "CTSTMAN",       "1",    "CTSTEN[16]",    "0000", "0000"],
    ["0x1D", "CTSTCFG2",  "FFFF", "1111", "CTSTEN[15:12]",   "1111", "CTSTEN[11:8]", "1111", "CTSTEN[7:5]",   "1111", "CTSTEN[3:0]",   "0000", "0000"],
    ["0x1E", "AUXTSTCFG", "00FF", "00",   "AUXTSTPOL",       "0",    "AUXTSTMAN",    "1111", "AUXTSTEN[7:4]", "1111", "AUXTSTEN[3:0]", "0000", "0000"]
]

table_diagCfgPage_diagThre_headers = ["Address", "Register", "Pending (hex)", "Pending Value", "Pending Unit",
                                      "Pending Value", "Pending Unit", "Device 0 (hex)", "Device 1 (hex)"]
table_diagCfgPage_diagThre_items = [
    ["0x2F", "BALSHRTUVTHREG",  "0000", "0.000",   "V",           " ", " ", "0000", "0000"],
    ["0x30", "BALOVTHREG",      "7FFF", "+2.500",  "V(Bipolar)",  " ", " ", "7FFF", "7FFF"],
    ["0x31", "BALUVTHREG",      "8000", "-2.500",  "V(Bipolar)",  " ", " ", "8000", "8000"],
    ["0x32", "CELLOPNOVTHREG",  "FFFF", "5.000",   "V",           " ", " ", "FFFF", "FFFF"],
    ["0x33", "CELLOPNUVTHREG",  "0000", "0.000",   "V",           " ", " ", "0000", "0000"],
    ["0x34", "BUSOPNOVTHREG",   "7FFF", "+2.500",  "V(Bipolar)",  " ", " ", "7FFF", "7FFF"],
    ["0x35", "BUSOPNUVTHREG",   "8000", "-2.500",  "V(Bipolar)",  " ", " ", "8000", "8000"],
    ["0x36", "CELLHVMOVTHREG",  "FFFF", "5.000",   "V",           " ", " ", "FFFF", "FFFF"],
    ["0x37", "CELLHVMUVTHREG",  "0000", "0.000",   "V",           " ", " ", "0000", "0000"],
    ["0x38", "BUSHVMOVTHREG",   "7FFF", "+2.500",  "V(Bipolar)",  " ", " ", "7FFF", "7FFF"],
    ["0x39", "BUSHVMUVTHREG",   "8000", "-2.500",  "V(Bipolar)",  " ", " ", "8000", "8000"],
    ["0x3A", "AUXRDIAGOVTHREG", "FFFF", "2.500",   "V(Absolute)", " ", " ", "FFFF", "FFFF"],
    ["0x3B", "AUXRDIAGUVTHREG", "0000", "0.000",   "V(Absolute)", " ", " ", "0000", "0000"]
]

table_diagCfgPage_aluTeDiag_headers = ["Address", "Register", "Pending (hex)", "Pending Value", "Pending Unit",
                                      "Pending Value", "Pending Unit", "Device 0 (hex)", "Device 1 (hex)"]
table_diagCfgPage_aluTeDiag_items = [
    ["0x3C", "ALUTESTAREG", "0000", " ", " ", " ", " ", "0000", "0000"],
    ["0x3D", "ALUTESTBREG", "0000", " ", " ", " ", " ", "0000", "0000"],
    ["0x3E", "ALUTESTCREG", "0000", " ", " ", " ", " ", "0000", "0000"],
    ["0x3F", "ALUTESTDREG", "0000", " ", " ", " ", " ", "0000", "0000"]
]

""" acquisition request page tablewidget initial content (page5) """
table_acqReqPage_headers = ["Address", "Register", "Pending (hex)", "Actual (hex)",
                            "ACQDONE", "DATARDY", "ACQERR", "(Logic Zero)", "ACQCBALINT",
                            "ACQIIRBYP", "ACQIIRINIT", "ACQIIRPROC", "ALUTESTEN", "ACQOSR[2:0]", "ACQMODE[3:0]"]

table_acqReqPage_items = [
    ["0x44", "ACQCTRL (Device 0)", "0B41", "CB41", "1", "1", "0", "0", "1", "0", "1", "1", "0", "100", "0001"],
    ["0x44", "ACQCTRL (Device 1)", "0B41", "CB41", "1", "1", "0", "0", "1", "0", "1", "1", "0", "100", "0001"]
]

""" measurement acquisition summary data page tablewidget initial content (page6) """
table_meaAcqSumDataPage_statusTableItems = [
    ["Address", "Register", "Device 0 (hex)", " ",    " ",             " ",    " ",             "Device 1 (hex)", " ",    " ",             " ",    " "],
    ["0x04",    "STATUS1",  "5000",           " ",    " ",             " ",    " ",             "5000",           " ",    " ",             " ",    " "],
    ["0x05",    "STATUS2",  "0080",           " ",    " ",             " ",    " ",             "0080",           " ",    " ",             " ",    " "],
    ["0x06",    "FMEA1",    "0000",           " ",    " ",             " ",    " ",             "0000",           " ",    " ",             " ",    " "],
    ["0x07",    "FMEA2",    "0000",           " ",    " ",             " ",    " ",             "0000",           " ",    " ",             " ",    " "],
    ["0x08",    "TEMPREG1", "0960",           "26.9", "°C",            "80.3", "°F",            "0960",           "26.9", "°C",            "80.3", "°F"],
    ["0x09",    "TEMPREG2", "0960",           "26.9", "°C",            "80.3", "°F",            "0960",           "26.9", "°C",            "80.3", "°F"],
    ["0x0A",    "GPIODATA", "0000",           "00",   "GPIODOUT[7:0]", "00",   "GPIODIN[7:0]",  "0000",           "00",   "GPIODOUT[7:0]", "00",   "GPIODIN[7:0]"],
    ["0xD0",    "ACQLOG",   "0000",           "0",    "ACQTYPE[3:0]",  "000",  "ACQCOUNT[9:0]", "0000",           "0",    "ACQTYPE[3:0]",  "000",  "ACQCOUNT[9:0]"]
]

table_meaAcqSumDataPage_sumDataItems = [
["0x86", "MINMAXLOC",   "0000", "0",  "MAXCELLLOC[3:0]", "0", "MINCELLLOC[3:0]", "0", "MAXCELLLOC[3:0]", "0", "MINAUXLOC[3:0]"],
["0x87", "MAXCELLREG",  "0000", "0",  " ",  " ", " ",                             "V (5V Full Scale, 76.3uV LSB)", " ", " ", " "],
["0x88", "MINCELLREG",  "0000", "0",  " ",  " ", " ",                             "V (5V Full Scale, 76.3uV LSB)", " ", " ", " "],
["0x89", "MAXAUXREG",   "0000", "0",  " ",  " ", " ",                             "% (Ratiometric 100% Full Scale, 1.526e-3% LSB)", " ", " ", " "],
["0x8A", "MINAUXREG",   "0000", "0",  " ",  " ", " ",                             "% (Ratiometric 100% Full Scale, 1.526e-3% LSB)", " ", " ", " "],
["0x8B", "TOTALREG",    "0000", "0",  " ",  " ", " ",                             "V (80V Full Scale 1.221mV LSB)", " ", " ", " "],
["0x8C", "ALTTOTALREG", "0000", "0",  " ",  " ", " ",                             "V (80V Full Scale 1.221mV LSB)", " ", " ", " "],
["0x8D", "PMMLOC",      "0000", "--", "--", "0", "PMMCELLLOC[3:0]",               "--", "--", "0", "PMMAUXLOC[3:0]"],
["0x8E", "PMMCELLREG",  "0000", "0",  " ",  " ", " ",                             "V (5V Full Scale, 76.3uV LSB)", " ", " ", " "],
["0x8F", "PMMAUXREG",   "0000", "0",  " ",  " ", " ",                             "% (Ratiometric 100% Full Scale, 1.526e-3% LSB)", " ", " ", " "],
]

""" measurement acquisition detailed data page tablewidget initial content (page7) """
table_meaAcqDetailPage_alertRegItems = [
    ["Address", "Register",  "Value (hex)",   " "],
    ["0x80", "ALRTOVREG",    "0000",          " "],
    ["0x81", "ALRTUVREG",    "0000",          " "],
    ["0x82", "ALRTALTOVREG", "0000",          " "],
    ["0x83", "ALRTALTUVREG", "0000",          " "],
    ["0x84", "ALRTAUXOVREG", "0000",          " "],
    ["0x85", "ALRTAUXUVREG", "0000",          " "]
]

table_meaAcqDetailPage_dataRegItems = [
    ["0x90 ~ - 0x9F", "CELL IIR DATA", " ",
     "CELLIIR 15", "CELLIIR 14","CELLIIR 13", "CELLIIR 12", "CELLIIR 11", "CELLIIR 10", "CELLIIR 9", "CELLIIR 8",
     "CELLIIR 7", "CELLIIR 6","CELLIIR 5", "CELLIIR 4", "CELLIIR 3", "CELLIIR 2", "CELLIIR 1", "CELLIIR 0"],

    ["0x90 ~ - 0x9F", "Device 0 (hex)", " ",
     "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000"],

    ["0xA0 ~ - 0xAF", "Device 0 (V)", " ",
     "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],

    ["0x90 ~ - 0x9F", "CELL DATA", " ",
     "CELL 15", "CELL 14", "CELL 13", "CELL 12", "CELL 11", "CELL10", "CELL 9", "CELL 8",
     "CELL 7",  "CELL 6",  "CELL 5",  "CELL 4",  "CELL 3",  "CELL2",  "CELL 1", "CELL 0"],

    ["0x90 ~ - 0x9F", "Device 0 (hex)", " ",
     "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000",
     "0000", "0000"],

    ["0xA0 ~ - 0xAF", "Device 0 (V)", " ",
     "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],

    ["0x90 ~ - 0x9F", "AUXILIARY DATA", " ",
     "AUX 7",     "AUX 6",     "AUX 5",     "AUX 4",     "AUX 3",     "AUX 2",     "AUX 1",    "AUX 0",
     "ALTAUX 7",  "ALTAUX 6",  "ALTAUX 5",  "ALTAUX 4",  "ALTAUX 3",  "ALTAUX 2",  "ALTAUX 1", "ALTAUX 0"],

    ["0x90 ~ - 0x9F", "Device 0 (hex)", " ",
     "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000",
     "0000", "0000"],

    ["0xA0 ~ - 0xAF", "Device 0 (V)", " ",
     "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],

    ["0x90 ~ - 0x9F", "ALTERNATE DATA", " ",
     "ALT 15", "ALT 14", "ALT 13", "ALT 12", "ALT 11", "ALT 10", "ALT 9", "ALT 8",
     "ALT 7",  "ALT 6",  "ALT 5",  "ALT 4",  "ALT 3",  "ALT 2",  "ALT 1", "ALT 0"],

    ["0x90 ~ - 0x9F", "Device 0 (hex)", " ",
     "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000",
     "0000", "0000"],

    ["0xA0 ~ - 0xAF", "Device 0 (V)", " ",
     "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
]

""" diagnostic acquisition data page tablewidget initial content (page8) """
table_diagAcqDataPage_statusTableItems = [
    ["Address", "Register",  "Device 0 (hex)", " ",    " ",             " ",    " ",             "Device 1 (hex)", " ",    " ",             " ",    " "],
    ["0x04",    "STATUS1",   "5000",           " ",    " ",             " ",    " ",             "5000",           " ",    " ",             " ",    " "],
    ["0x05",    "STATUS2",   "0080",           " ",    " ",             " ",    " ",             "0080",           " ",    " ",             " ",    " "],
    ["0x06",    "FMEA1",     "0000",           " ",    " ",             " ",    " ",             "0000",           " ",    " ",             " ",    " "],
    ["0x07",    "FMEA2",     "0000",           " ",    " ",             " ",    " ",             "0000",           " ",    " ",             " ",    " "],
    ["0x08",    "TEMPREG1",  "0960",           "26.9", "°C",            "80.3", "°F",            "0960",           "26.9", "°C",            "80.3", "°F"],
    ["0x09",    "TEMPREG2",  "0960",           "26.9", "°C",            "80.3", "°F",            "0960",           "26.9", "°C",            "80.3", "°F"],
    ["0x0A",    "GPIODATA",  "0000",           "00",   "GPIODOUT[7:0]", "00",   "GPIODIN[7:0]",  "0000",           "00",   "GPIODOUT[7:0]", "00",   "GPIODIN[7:0]"],
    ["0xD1",    "DIAGLOG",   "0000",           "0",    "DIAGTYPE[3:0]", "000",  "DIAGCOUNT[9:0]","0000",           "0",    "DIAGTYPE[3:0]", "000",  "DIAGCOUNT[9:0]"],
    ["0xE7",    "ADC1ZSREG", "0000",           " ",    " ",             " ",    " ",             "0000",           " ",    " ",             " ",    " "],
    ["0xE8",    "ADC1FSREG", "FFFF",           " ",    " ",             " ",    " ",             "FFFF",           " ",    " ",             " ",    " "],
    ["0xE9",    "ADC2ZSREG", "0000",           " ",    " ",             " ",    " ",             "0000",           " ",    " ",             " ",    " "],
    ["0xEA",    "ADC2FSREG", "FFFF",           " ",    " ",             " ",    " ",             "FFFF",           " ",    " ",             " ",    " "]
]

table_diagAcqDataPage_alertItems = [
    ["Address",     "Register",         " ",    " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    ["0xD2 – 0xD3", "ALRTDIAGOVREG1/2", "0000", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    ["0xD4 – 0xD5", "ALRTDIAGUVREG1/2", "0000", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]

]

table_diagAcqDataPage_dev0DataItems = [
    ["0xD6 – 0xE6", "DIAGNOSTIC DATA", " ", "DIAG 16", "DIAG 15", "DIAG 14", "DIAG 13", "DIAG 12", "DIAG 11", "DIAG 10", "DIAG 9",
                             "DIAG 8", "DIAG 7", "DIAG 6", "DIAG 5", "DIAG 4", "DIAG 3", "DIAG 2", "DIAG 1","DIAG 0"],
    ["0xD6 – 0xE6", "Device 0 (hex)", " ", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000",
                             "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000"],
    ["0xD6 – 0xE6", "Device 0 (V)", " ", "0", "0", "0", "0", "0", "0", "0", "0",
                             "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]

table_diagAcqDataPage_dev1DataItems = [
    ["0xD6 – 0xE6", "DIAGNOSTIC DATA", " ", "DIAG 16", "DIAG 15", "DIAG 14", "DIAG 13", "DIAG 12", "DIAG 11", "DIAG 10", "DIAG 9",
                             "DIAG 8", "DIAG 7", "DIAG 6", "DIAG 5", "DIAG 4", "DIAG 3", "DIAG 2", "DIAG 1","DIAG 0"],
    ["0xD6 – 0xE6", "Device 0 (hex)", " ", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000",
                             "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000"],
    ["0xD6 – 0xE6", "Device 0 (V)", " ", "0", "0", "0", "0", "0", "0", "0", "0",
                             "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]

""" cell balance page tablewidget initial content (page9) """
table_cblPage_cblExpTimHeaders = ["CBEXP[10:0] (hex)", "CBEXP (dec)"]
table_cblPage_cblCfgRegHeaders =["Address", "Register", "Pending (hex)", "Comment", "Device 0 (hex)", "Device 1 (hex)"]
table_cblPage_cblCtrlDemoHeaders =["Address", "Register", "Pending (hex)", "Comment", "Device 0 (hex)", "Device 1 (hex)"]

table_cblPage_cblExpTimItems = [["002", "0"]]
table_cblPage_cblCfgRegItems = [
    ["0x45", "CBALSEL", "FFFF",
     "Enable all BALSW for Diagnostics and basic Demonstration.", "0000", "0000"],
    ["0x46", "CBALTIMECFG", "0002",
     "Applies selected Real-Time Limit to Manual operations, Effective-Time Limit to Semi-Automatic operations."
     "  CBEXP is capped at 0x005 for demonstration purposes.", "0000", "0000"],
    ["0x47", "CBALACQCFG", "2400",
     "Apply defaults.  This register is not used in Manual or Semi-Automatic modes of operation.", "2400", "2400"],
    ["0x48", "CBALUVTHREG", "FFFF",
     "Apply defaults (5V Unipolar).  This register is not used in Manual or Semi-Automatic modes of operation.", "FFFF", "FFFF"],
    ["0x49", "CBALCFG", "01F0",
     "CBMODE[2:0] is determined by selection.  CBTEMPEN=0b1 for safety.  CBDUTY[3:0]=0xF (50%) for Semi-Automatic Mode."
     "  All other options are not used in this Demo.", "01F0", "01F0"]
]
table_cblPage_cblCtrlDemoItems = [
    ["0x4A", "BALCTRL (START)", "4000", "This is the command issued for a Cell Balancing Start Request.", " ", " "],
    ["0x4A", "BALCTRL (STOP)",  "2000", "This is the command issued for a Cell Balancing Stop Request.",  " ", " "]
]
table_cblPage_cblCtrlInfItems = [
    ["Address", "Register",     "Device 0 (hex)", " ", " ", " ", " ", " ", " ",
                                "Device 1 (hex)", " ", " ", " ", " ", " ", " "],
    ["0x4A", "CBALCTRL (READ)", "0007",           "Current CBAL details, updated in response to a Start, Stop, or Read Back request.", " ", " ", " ", " ", " ",
                                "0007",           "Current CBAL details, updated in response to a Start, Stop, or Read Back request.", " ", " ", " ", " ", " "],
    ["0x4B", "CBALSTATUS",      "0000",           " ", " ", " ", " ", " ", " ",
                                "0000",           " ", " ", " ", " ", " ", " "],
    ["0x4C", "CBALTIMER",       "0000",           "0", " ", " ", "Time per Channel Group (Minutes, decimal)"," ", " ",
                                "0000",           "0", " ", " ", "Time per Channel Group (Minutes, decimal)"," ", " "],
    ["0x4D", "CBALCOUNT",       "0000",           "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)",
                                "0000",           "0", "Hours (dec)", "0", "Min (dec)", "0", "Sec (dec)"],
    ["0x4E", "CBALUVSTAT",      "0000",           " ", " ", " ", " ", " ", " ",
                                "0000",           " ", " ", " ", " ", " ", " "]
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
    """
    设置 chain configuration page power-up status table 和 reset table 的单元格尺寸和背景；
    在 power-up status table 中插入 led
    :param pPwTable:
    :param pRstTable:
    :return: 返回两个二维列表 ledDev0[4][16], ledDev1[4][16]
             这两个二位列表中的元素分别是对应的各 led label 对象
    """
    ''' adjust table column size '''
    for c in range(7):
        if c == 0:
            pPwTable.setColumnWidth(c, 90)
            pRstTable.setColumnWidth(c, 90)
        elif c == 2:
            pPwTable.setColumnWidth(c, 140)
            pRstTable.setColumnWidth(c, 140)
        elif c == 4 or c == 6:
            pPwTable.setColumnWidth(c, 650)
            pRstTable.setColumnWidth(c, 650)
        else:
            pPwTable.setColumnWidth(c, 110)
            pRstTable.setColumnWidth(c, 110)

    ''' fill background color and font '''
    for r in range(1, 5):
        if r != 0:
            if r < 2:
                pRstTable.item(r, 3).setBackground(QColor("#E2F0D9"))  # 绿色
                pRstTable.item(r, 5).setBackground(QColor("#E2F0D9"))  # 绿色
            pPwTable.item(r, 3).setBackground(QColor("#E2F0D9"))  # 绿色
            pPwTable.item(r, 5).setBackground(QColor("#E2F0D9"))  # 绿色
            pPwTable.item(r, 4).setBackground(QColor("#FFF2CC"))  # 黄色
            pPwTable.item(r, 6).setBackground(QColor("#FFF2CC"))  # 黄色

    boldFont = QFont()
    boldFont.setBold(True)
    for c in range(7):
        pPwTable.item(0, c).setFont(boldFont)  # 字体加粗
        pRstTable.item(0, c).setFont(boldFont)  # 字体加粗

    ''' insert leds '''
    ledSta1Dev0 = add_led_txt(16, pPwTable, 1, 4, LED_STA1_LAB)
    ledSta1Dev1 = add_led_txt(16, pPwTable, 1, 6, LED_STA1_LAB)
    ledSta2Dev0 = add_led_txt(16, pPwTable, 2, 4, LED_STA2_LAB)
    ledSta2Dev1 = add_led_txt(16, pPwTable, 2, 6, LED_STA2_LAB)
    ledFem1Dev0 = add_led_txt(16, pPwTable, 3, 4, LED_FME1_LAB)
    ledFem1Dev1 = add_led_txt(16, pPwTable, 3, 6, LED_FME1_LAB)
    ledFem2Dev0 = add_led_txt(16, pPwTable, 4, 4, LED_FME2_LAB)
    ledFem2Dev1 = add_led_txt(16, pPwTable, 4, 6, LED_FME2_LAB)

    ledDev0 = [ledSta1Dev0, ledSta2Dev0, ledFem1Dev0, ledFem2Dev0]
    ledDev1 = [ledSta1Dev1, ledSta2Dev1, ledFem1Dev1, ledFem2Dev1]

    return ledDev0, ledDev1


def adjust_devMgPage_tables(pInit, pDC, pCur):
    ''' adjust size '''
    # status tables
    for c in range(12):
        if c == 0 or c == 2 or c == 7:
            pInit.setColumnWidth(c, 120)
            pCur.setColumnWidth(c, 120)
        elif c == 1:
            pInit.setColumnWidth(c, 200)
            pCur.setColumnWidth(c, 200)
        elif c == 4 or c == 6 or c == 9 or c == 11:
            pInit.setColumnWidth(c, 150)
            pCur.setColumnWidth(c, 150)
        else:
            pInit.setColumnWidth(c, 170)
            pCur.setColumnWidth(c, 170)
    # dc tabble
    for c in range(3):
        if c == 0:
            pDC.setColumnWidth(c, 120)
        elif c == 1:
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

    # DC table
    pDC.setSpan(1, 0, 3, 1)
    pDC.setSpan(1, 1, 3, 1)
    for r in range(4):
        if r < 2:
            pDC.item(r, 1).setBackground(QColor("#E2F0D9"))  # 绿色
            pDC.item(r, 0).setFont(boldFont)  # 字体加粗
        pDC.item(r, 2).setBackground(QColor("#FFF2CC"))  # 黄色

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

    ''' insert leds '''
    # dc table
    ledDcByte = add_led_txt(8, pDC, 0, 2, LED_DC_LAB)
    ledAlert0 = add_led_txt(16, pDC, 1, 2, LED_ALERT0_LAB)
    ledAlert1 = add_led_txt(16, pDC, 2, 2, LED_ALERT1_LAB)
    ledAlert2 = add_led_txt(16, pDC, 3, 2, LED_ALERT2_LAB)
    ledAlert = ledAlert0 + ledAlert1 + ledAlert2
    # status initial table
    ledInitSta1Dev0 = add_led_txt(16, pInit, 1, 3, LED_STA1_LAB)
    ledInitSta1Dev1 = add_led_txt(16, pInit, 1, 8, LED_STA1_LAB)
    ledInitSta2Dev0 = add_led_txt(16, pInit, 2, 3, LED_STA2_LAB)
    ledInitSta2Dev1 = add_led_txt(16, pInit, 2, 8, LED_STA2_LAB)
    ledInitFem1Dev0 = add_led_txt(16, pInit, 3, 3, LED_FME1_LAB)
    ledInitFem1Dev1 = add_led_txt(16, pInit, 3, 8, LED_FME1_LAB)
    ledInitFem2Dev0 = add_led_txt(16, pInit, 4, 3, LED_FME2_LAB)
    ledInitFem2Dev1 = add_led_txt(16, pInit, 4, 8, LED_FME2_LAB)
    # status current table
    ledCurSta1Dev0 = add_led_txt(16, pCur, 1, 3, LED_STA1_LAB)
    ledCurSta1Dev1 = add_led_txt(16, pCur, 1, 8, LED_STA1_LAB)
    ledCurSta2Dev0 = add_led_txt(16, pCur, 2, 3, LED_STA2_LAB)
    ledCurSta2Dev1 = add_led_txt(16, pCur, 2, 8, LED_STA2_LAB)
    ledCurFem1Dev0 = add_led_txt(16, pCur, 3, 3, LED_FME1_LAB)
    ledCurFem1Dev1 = add_led_txt(16, pCur, 3, 8, LED_FME1_LAB)
    ledCurFem2Dev0 = add_led_txt(16, pCur, 4, 3, LED_FME2_LAB)
    ledCurFem2Dev1 = add_led_txt(16, pCur, 4, 8, LED_FME2_LAB)

    ledInitDev0 = [ledInitSta1Dev0, ledInitSta2Dev0, ledInitFem1Dev0, ledInitFem2Dev0]
    ledInitDev1 = [ledInitSta1Dev1, ledInitSta2Dev1, ledInitFem1Dev1, ledInitFem2Dev1]
    ledCurDev0 = [ledCurSta1Dev0, ledCurSta2Dev0, ledCurFem1Dev0, ledCurFem2Dev0]
    ledCurDev1 = [ledCurSta1Dev1, ledCurSta2Dev1, ledCurFem1Dev1, ledCurFem2Dev1]

    return ledInitDev0, ledInitDev1, ledCurDev0, ledCurDev1, ledDcByte, ledAlert




def adjust_appCfgPage_tables(pAppCfgTable, pAlertTable, pThreTable, pAcqTable):
    pAppCfgTable.setColumnWidth(0, 120)
    pAppCfgTable.setColumnWidth(1, 150)
    pAppCfgTable.setColumnWidth(2, 120)
    pAppCfgTable.setColumnWidth(3, 300)
    pAppCfgTable.setColumnWidth(4, 300)
    pAppCfgTable.setColumnWidth(5, 300)
    pAppCfgTable.setColumnWidth(6, 300)
    pAppCfgTable.setColumnWidth(7, 120)
    pAppCfgTable.setColumnWidth(8, 120)

    for c in range(10):
        pAlertTable.setColumnWidth(c, pAppCfgTable.columnWidth(c))
        pThreTable.setColumnWidth(c, pAppCfgTable.columnWidth(c))
        pAcqTable.setColumnWidth(c, pAppCfgTable.columnWidth(c))

def set_appCfgPage_table_color(pAppCfgTable, pAlertTable, pThreTable, pAcqTable):
    for r in range(5):
        for c in range(2, 9):
            pAppCfgTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            if r < 2:
                pAppCfgTable.item(r, 2).setFlags(pAppCfgTable.item(r, 2).flags()
                                                & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)  # disable cell
            pAppCfgTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pAppCfgTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pAppCfgTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pAppCfgTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色

    for r in range(4):
        for c in range(2, 9):
            pAlertTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            pAlertTable.item(r, 2).setFlags(pAlertTable.item(r, 2).flags()
                                             & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)  # disable cell
            pAlertTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pAlertTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pAlertTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pAlertTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色
            pAcqTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            pAcqTable.item(r, 2).setFlags(pAcqTable.item(r, 2).flags()
                                            & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)  # disable cell
            if r != 3:
                pAcqTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pAcqTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pAcqTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pAcqTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色

    for r in range(14):
        for c in range(2, 9):
            pThreTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            if r != 13:
                pThreTable.item(r, 2).setFlags(pThreTable.item(r, 2).flags()
                                              & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)  # disable cell
            pThreTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pThreTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pThreTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色
    pThreTable.item(13, 5).setBackground(QColor("#FFF2CC"))  # 黄色



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
    # test current table
    for r in range(3):
        for c in range(2, 13):
            if c == 2:
                pTeCurTable.item(r, c).setBackground(QColor("#DAE3F3"))     # 紫色
                pTeCurTable.item(r, 2).setFlags(pTeCurTable.item(r, 2).flags()
                                                 & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)  # disable cell
            elif c == 3 or c == 5 or c == 7 or c == 9:
                pTeCurTable.item(r, c).setBackground(QColor("#FFF2CC"))     # 黄色
            elif c == 11 or c == 12:
                pTeCurTable.item(r, c).setBackground(QColor("#E2F0D9"))     # 绿色

    # threshold and alu register table
    for r in range(13):
        if r < 4:
            pAluTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
            pAluTable.item(r, 2).setFlags(pAluTable.item(r, 2).flags()
                                              & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)  # disable cell
            pAluTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
            pAluTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色
        pDiagThrTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 紫色
        pDiagThrTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
        pDiagThrTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色
        pDiagThrTable.item(r, 8).setBackground(QColor("#E2F0D9"))  # 绿色
        pDiagThrTable.item(r, 2).setFlags(pDiagThrTable.item(r, 2).flags()
                                        & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)  # disable cell


def adjust_acqReqPage_tables(pOsrTable, pAcqReqTable):
    pOsrTable.item(0, 0).setBackground(QColor("#DAE3F3"))  # 紫色
    pOsrTable.item(0, 0).setFlags(pOsrTable.item(0, 0).flags()
                                  & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)  # disable cell
    pOsrTable.item(0, 1).setBackground(QColor("#FFF2CC"))  # 黄色

    for r in range(2):
        for c in range(3,15):
            if c == 3:
                pAcqReqTable.item(r, c).setBackground(QColor("#E2F0D9"))  # 绿色
            else:
                pAcqReqTable.item(r, c).setBackground(QColor("#FFF2CC"))  # 黄色



def adjust_meaAcqDetailPage_tables(pAlertRegDev0, pDataRegDev0, pAlertRegDev1, pDataRegDev1):
    pAlertRegDev0.setColumnWidth(0, 140)
    pAlertRegDev0.setColumnWidth(1, 140)
    pAlertRegDev0.setColumnWidth(2, 120)
    pDataRegDev0.setColumnWidth(0,  140)
    pDataRegDev0.setColumnWidth(1,  140)
    pDataRegDev0.setColumnWidth(2,  120)
    pAlertRegDev1.setColumnWidth(0, 140)
    pAlertRegDev1.setColumnWidth(1, 140)
    pAlertRegDev1.setColumnWidth(2, 120)
    pDataRegDev1.setColumnWidth(0,  140)
    pDataRegDev1.setColumnWidth(1,  140)
    pDataRegDev1.setColumnWidth(2,  120)

    for c in range(3, 19):
        pDataRegDev0.setColumnWidth(c, 90)
        pDataRegDev1.setColumnWidth(c, 90)

    pAlertRegDev0.setColumnWidth(3, 90 * 16)
    pAlertRegDev1.setColumnWidth(3, 90 * 16)

def set_meaAcqDetailPage_table_color(pAlertRegDev0, pDataRegDev0, pAlertRegDev1, pDataRegDev1):
    for r in range(1,7):
        pAlertRegDev0.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
        pAlertRegDev1.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
        pAlertRegDev0.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
        pAlertRegDev1.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色

    boldFont = QFont()
    boldFont.setBold(True)
    for c in range(4):
        pAlertRegDev0.item(0, c).setFont(boldFont)  # 字体加粗
        pAlertRegDev1.item(0, c).setFont(boldFont)  # 字体加粗

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

def insert_txt_frame(pNum, pLableList):
    """
    该函数生成一个 frame 控件，此 frame 控件中包含一行用 gridlayout 布局的 label 列表。
    此 frame 控件可以作为独立的控件被填入到 tableWidget 的某一行中。
    本工程中用作在 tableWidget 中某行填充 led label
    :param pNum: 要填入的 label 个数
    :param pLableList: 要填入的 label 列表
    :return: 包含输入 label 列表且做好布局的 frame 控件
    """
    frameTxt = QtWidgets.QFrame()
    layoutTxt = QtWidgets.QGridLayout(frameTxt)
    layoutTxt.setSpacing(0)
    layoutTxt.setContentsMargins(0, 0, 0, 0)    # 为布局设置外边距：左、上、右、下

    listTxt = []
    for i in range(0, pNum):
        label_txt = QtWidgets.QLabel(pLableList[i])
        label_txt.setFont(QtGui.QFont("Calibri", 9, QtGui.QFont.Bold))
        listTxt.append(label_txt)
        layoutTxt.addWidget(listTxt[i], 0, i)
        layoutTxt.setAlignment(listTxt[i], Qt.AlignCenter)

    return frameTxt

def insert_led_frame(pNum):
    """
        该函数生成一个 frame 控件，此 frame 控件中包含一行用 gridlayout 布局的 led 串。
        此 frame 控件可以作为独立的控件被填入到 tableWidget 的某一行中。
        本工程中用作在 tableWidget 中某行填充 led 串。
        :param pNum: led 串中 led 的个数
        :return: 包含 led 串且做好布局的 frame 控件
        """
    frameLed = QtWidgets.QFrame()
    layoutLed = QtWidgets.QGridLayout(frameLed)
    layoutLed.setSpacing(0)
    layoutLed.setContentsMargins(0, 0, 0, 0)  # 为布局设置外边距：左、上、右、下

    listLed = []
    for i in range(0,pNum):
        listLed.append(led_generator())
        layoutLed.addWidget(listLed[i], 0, i)
        layoutLed.setAlignment(listLed[i], Qt.AlignCenter)

    return frameLed, listLed

def meaAcqDetailPage_insert_led(pAlertRegDev0, pAlertRegDev1):
    """
    Measurement acquisition detailed page insert led
    :param pAlertRegDev0: alert dev0 table
    :param pAlertRegDev1: alert dev1 table
    :return: 返回的是两个二维列表：dev0LedList[6][16], dev1LedList[6][16]
    """
    ''' insert led lable '''
    pAlertRegDev0.setCellWidget(0, 3, insert_txt_frame(16, LED_16_LAB))
    pAlertRegDev1.setCellWidget(0, 3, insert_txt_frame(16, LED_16_LAB))

    ''' insert led '''
    rows, cols = 6, 16  # 定义行数和列数
    dev0LedList = [[None for _ in range(cols)] for _ in range(rows)]
    dev1LedList = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range(1, 7):
        ledFrame, ledList = insert_led_frame(16)
        dev0LedList[i - 1] = ledList
        pAlertRegDev0.setCellWidget(i, 3, ledFrame)

    for i in range(1, 7):
        ledFrame, ledList = insert_led_frame(16)
        dev1LedList[i - 1] = ledList
        pAlertRegDev1.setCellWidget(i, 3, ledFrame)

    return dev0LedList, dev1LedList

def adjust_diagAcqDataPage_tables(pDC, pStaTable, pAlerDev0Table, pDataDev0Table, pAlerDev1Table, pDataDev1Table):
    ''' adjust table size '''
    # dc tabble
    for c in range(3):
        if c == 1:
            pDC.setColumnWidth(c, 200)
        elif c == 2:
            pDC.setColumnWidth(c, 1530)
        else:
            pDC.setColumnWidth(c, 120)

    # adjust status table column size
    for c in range(12):
        if c == 0:
            pStaTable.setColumnWidth(c, 120)
        elif c == 1:
            pStaTable.setColumnWidth(c, 200)
        elif c == 2 or c == 7:
            pStaTable.setColumnWidth(c, 125)
        else:
            pStaTable.setColumnWidth(c, 160)

    # set diagnostic alert and data tables column size
    for c in range(20):
        if c == 0:
            pAlerDev0Table.setColumnWidth(c, 120)
            pDataDev0Table.setColumnWidth(c, 120)
            pAlerDev1Table.setColumnWidth(c, 120)
            pDataDev1Table.setColumnWidth(c, 120)
        elif c == 1:
            pAlerDev0Table.setColumnWidth(c, 200)
            pDataDev0Table.setColumnWidth(c, 200)
            pAlerDev1Table.setColumnWidth(c, 200)
            pDataDev1Table.setColumnWidth(c, 200)
        elif c == 2:
            pAlerDev0Table.setColumnWidth(c, 125)
            pDataDev0Table.setColumnWidth(c, 125)
            pAlerDev1Table.setColumnWidth(c, 125)
            pDataDev1Table.setColumnWidth(c, 125)
        else:
            pAlerDev0Table.setColumnWidth(c, 82)
            pDataDev0Table.setColumnWidth(c, 82)
            pAlerDev1Table.setColumnWidth(c, 82)
            pDataDev1Table.setColumnWidth(c, 82)

    ''' span table and fill background color '''
    boldFont = QFont()
    boldFont.setBold(True)
    # DC table
    pDC.setSpan(1, 0, 3, 1)
    pDC.setSpan(1, 1, 3, 1)
    for r in range(4):
        if r < 2:
            pDC.item(r, 1).setBackground(QColor("#E2F0D9"))  # 绿色
            pDC.item(r, 0).setFont(boldFont)  # 字体加粗
        pDC.item(r, 2).setBackground(QColor("#FFF2CC"))  # 黄色

    # status table
    for r in range(0, 13):
        if r < 5:
            pStaTable.setSpan(r, 3, 1, 4)
            pStaTable.item(r, 3).setText(' ')
            pStaTable.setSpan(r, 8, 1, 4)
            pStaTable.item(r, 8).setText(' ')
            if 0 < r < 5:
                pStaTable.setRowHeight(r, 28)  # 设置 led 行行高
                pStaTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
                pStaTable.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
        elif r < 9:
            pStaTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 10).setBackground(QColor("#FFF2CC"))  # 黄色
        if r != 0:
            pStaTable.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
            pStaTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色

    for c in range(12):
        pStaTable.item(0, c).setFont(boldFont)  # 字体加粗

    # diagnostic alert tables
    for r in range(3):
        pAlerDev0Table.setSpan(r, 3, 1, 17)
        pAlerDev0Table.item(r, 3).setText(' ')
        pAlerDev1Table.setSpan(r, 3, 1, 17)
        pAlerDev1Table.item(r, 3).setText(' ')
        if r != 0:
            pAlerDev0Table.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
            pAlerDev1Table.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
            pAlerDev0Table.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pAlerDev1Table.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色

    for c in range(2):
        pAlerDev0Table.item(0, c).setFont(boldFont)  # 字体加粗
        pAlerDev1Table.item(0, c).setFont(boldFont)  # 字体加粗

    # diagnostic data tables
    for c in range (20):
        if c > 2:
            pDataDev0Table.item(1, c).setBackground(QColor("#E2F0D9"))  # 绿色
            pDataDev1Table.item(1, c).setBackground(QColor("#E2F0D9"))  # 绿色
            pDataDev0Table.item(2, c).setBackground(QColor("#FFF2CC"))  # 黄色
            pDataDev1Table.item(2, c).setBackground(QColor("#FFF2CC"))  # 黄色
        pDataDev0Table.item(0, c).setBackground(QColor("#BFBFBF"))  # 灰色
        pDataDev1Table.item(0, c).setBackground(QColor("#BFBFBF"))  # 灰色

    for c in range(20):
        pDataDev0Table.item(0, c).setFont(boldFont)  # 字体加粗
        pDataDev1Table.item(0, c).setFont(boldFont)  # 字体加粗

    ''' insert led '''
    # dc table
    ledDcByte = add_led_txt(8, pDC, 0, 2, LED_DC_LAB)
    ledAlert0 = add_led_txt(16, pDC, 1, 2, LED_ALERT0_LAB)
    ledAlert1 = add_led_txt(16, pDC, 2, 2, LED_ALERT1_LAB)
    ledAlert2 = add_led_txt(16, pDC, 3, 2, LED_ALERT2_LAB)
    ledAlert = ledAlert0 + ledAlert1 + ledAlert2

    # status table
    ledSta1Dev0 = add_led_txt(16, pStaTable, 1, 3, LED_STA1_LAB)
    ledSta1Dev1 = add_led_txt(16, pStaTable, 1, 8, LED_STA1_LAB)
    ledSta2Dev0 = add_led_txt(16, pStaTable, 2, 3, LED_STA2_LAB)
    ledSta2Dev1 = add_led_txt(16, pStaTable, 2, 8, LED_STA2_LAB)
    ledFem1Dev0 = add_led_txt(16, pStaTable, 3, 3, LED_FME1_LAB)
    ledFem1Dev1 = add_led_txt(16, pStaTable, 3, 8, LED_FME1_LAB)
    ledFem2Dev0 = add_led_txt(16, pStaTable, 4, 3, LED_FME2_LAB)
    ledFem2Dev1 = add_led_txt(16, pStaTable, 4, 8, LED_FME2_LAB)
    ledStaTableDev0 = [ledSta1Dev0, ledSta2Dev0, ledFem1Dev0, ledFem2Dev0]
    ledStaTableDev1 = [ledSta1Dev1, ledSta2Dev1, ledFem1Dev1, ledFem2Dev1]

    # alert tables
    # insert led lable
    pAlerDev0Table.setCellWidget(0, 3, insert_txt_frame(17, LED_17_LAB))
    pAlerDev1Table.setCellWidget(0, 3, insert_txt_frame(17, LED_17_LAB))
    # insert led
    rows, cols = 2, 17  # 定义行数和列数
    dev0LedList = [[None for _ in range(cols)] for _ in range(rows)]
    dev1LedList = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range(1, 3):
        ledFrame, ledList = insert_led_frame(17)
        dev0LedList[i - 1] = ledList
        pAlerDev0Table.setCellWidget(i, 3, ledFrame)

    for i in range(1, 3):
        ledFrame, ledList = insert_led_frame(17)
        dev1LedList[i - 1] = ledList
        pAlerDev1Table.setCellWidget(i, 3, ledFrame)

    return ledDcByte, ledAlert, ledStaTableDev0, ledStaTableDev1, dev0LedList, dev1LedList


def adjust_meaAcqSumPage_tables(pDC, pStaTable, pSumDataDev0Table, pSumDataDev1Table):
    ''' adjust table size '''
    # dc tabble
    for c in range(3):
        if c == 1:
            pDC.setColumnWidth(c, 200)
        elif c == 2:
            pDC.setColumnWidth(c, 1530)
        else:
            pDC.setColumnWidth(c, 120)

    # adjust status table column size
    for c in range(12):
        if c == 0:
            pStaTable.setColumnWidth(c, 120)
        elif c == 1:
            pStaTable.setColumnWidth(c, 200)
        elif c == 2 or c == 7:
            pStaTable.setColumnWidth(c, 125)
        else:
            pStaTable.setColumnWidth(c, 160)

    # set summary data tables column size
    for c in range(11):
        if c == 0:
            pSumDataDev0Table.setColumnWidth(c, 120)
            pSumDataDev1Table.setColumnWidth(c, 120)
        elif c == 1:
            pSumDataDev0Table.setColumnWidth(c, 200)
            pSumDataDev1Table.setColumnWidth(c, 200)
        elif c == 2:
            pSumDataDev0Table.setColumnWidth(c, 132)
            pSumDataDev1Table.setColumnWidth(c, 132)
        else:
            pSumDataDev0Table.setColumnWidth(c, 175)
            pSumDataDev1Table.setColumnWidth(c, 175)

    ''' span table and fill background color '''
    boldFont = QFont()
    boldFont.setBold(True)
    # DC table
    pDC.setSpan(1, 0, 3, 1)
    pDC.setSpan(1, 1, 3, 1)
    for r in range(4):
        if r < 2:
            pDC.item(r, 1).setBackground(QColor("#E2F0D9"))  # 绿色
            pDC.item(r, 0).setFont(boldFont)  # 字体加粗
        pDC.item(r, 2).setBackground(QColor("#FFF2CC"))  # 黄色

    # status table
    for r in range(0, 9):
        if r < 5:
            pStaTable.setSpan(r, 3, 1, 4)
            pStaTable.item(r, 3).setText(' ')
            pStaTable.setSpan(r, 8, 1, 4)
            pStaTable.item(r, 8).setText(' ')
            if 0 < r < 5:
                pStaTable.setRowHeight(r, 28)   # 设置 led 行行高
                pStaTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
                pStaTable.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
        else:
            pStaTable.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 5).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 8).setBackground(QColor("#FFF2CC"))  # 黄色
            pStaTable.item(r, 10).setBackground(QColor("#FFF2CC"))  # 黄色
        if r != 0:
            pStaTable.item(r, 2).setBackground(QColor("#E2F0D9"))  # 绿色
            pStaTable.item(r, 7).setBackground(QColor("#E2F0D9"))  # 绿色

    for c in range(12):
        pStaTable.item(0, c).setFont(boldFont)  # 字体加粗

    # summary data tables
    for r in range(1, 10):
        if r != 7:
            # dev0
            pSumDataDev0Table.setSpan(r, 3, 1, 4)
            pSumDataDev0Table.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pSumDataDev0Table.setSpan(r, 7, 1, 4)
            # dev1
            pSumDataDev1Table.setSpan(r, 3, 1, 4)
            pSumDataDev1Table.item(r, 3).setBackground(QColor("#FFF2CC"))  # 黄色
            pSumDataDev1Table.setSpan(r, 7, 1, 4)

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

    ''' insert led '''
    #dc table
    ledDcByte = add_led_txt(8, pDC, 0, 2, LED_DC_LAB)
    ledAlert0 = add_led_txt(16, pDC, 1, 2, LED_ALERT0_LAB)
    ledAlert1 = add_led_txt(16, pDC, 2, 2, LED_ALERT1_LAB)
    ledAlert2 = add_led_txt(16, pDC, 3, 2, LED_ALERT2_LAB)
    ledAlert = ledAlert0 + ledAlert1 + ledAlert2
    # status table
    ledSta1Dev0 = add_led_txt(16, pStaTable, 1, 3, LED_STA1_LAB)
    ledSta1Dev1 = add_led_txt(16, pStaTable, 1, 8, LED_STA1_LAB)
    ledSta2Dev0 = add_led_txt(16, pStaTable, 2, 3, LED_STA2_LAB)
    ledSta2Dev1 = add_led_txt(16, pStaTable, 2, 8, LED_STA2_LAB)
    ledFem1Dev0 = add_led_txt(16, pStaTable, 3, 3, LED_FME1_LAB)
    ledFem1Dev1 = add_led_txt(16, pStaTable, 3, 8, LED_FME1_LAB)
    ledFem2Dev0 = add_led_txt(16, pStaTable, 4, 3, LED_FME2_LAB)
    ledFem2Dev1 = add_led_txt(16, pStaTable, 4, 8, LED_FME2_LAB)
    ledStaTableDev0 = [ledSta1Dev0, ledSta2Dev0, ledFem1Dev0, ledFem2Dev0]
    ledStaTableDev1 = [ledSta1Dev1, ledSta2Dev1, ledFem1Dev1, ledFem2Dev1]

    return ledDcByte, ledAlert, ledStaTableDev0, ledStaTableDev1


def adjust_cblPage_tables(pExpTable, pCfgTable, pCtrlDemoTable, pCtrlInfTable):
    ''' adjust table size '''
    # expiration time table
    pExpTable.setColumnWidth(1, 120)
    pExpTable.setColumnWidth(2, 120)

    # configure and control demo tables
    for c in range(6):
        if c == 0:
            pCfgTable.setColumnWidth(c, 90)
            pCtrlDemoTable.setColumnWidth(c, 90)
        elif c == 3:
            pCfgTable.setColumnWidth(c, 1100)
            pCtrlDemoTable.setColumnWidth(c, 1100)
        else:
            pCfgTable.setColumnWidth(c, 150)
            pCtrlDemoTable.setColumnWidth(c, 150)

    # control information table
    for c in range(16):
        if c == 0:
            pCtrlInfTable.setColumnWidth(c, 90)
        elif c == 1:
            pCtrlInfTable.setColumnWidth(c, 150)
        elif c == 2 or c == 9:
            pCtrlInfTable.setColumnWidth(c, 120)
        else:
            pCtrlInfTable.setColumnWidth(c, 115)

    ''' span table and fill background color '''
    # expiration time table
    pExpTable.item(0, 0).setBackground(QColor("#DAE3F3"))  # 蓝色
    pExpTable.item(0, 1).setBackground(QColor("#FFF2CC"))  # 黄色

    # configure and control demo tables
    for r in range(5):
        if r < 2:
            pCtrlDemoTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 蓝色
        pCfgTable.item(r, 2).setBackground(QColor("#DAE3F3"))  # 蓝色
        pCfgTable.item(r, 4).setBackground(QColor("#E2F0D9"))  # 绿色
        pCfgTable.item(r, 5).setBackground(QColor("#E2F0D9"))  # 绿色

    for c in range(3, 6):
        pCtrlDemoTable.item(0, c).setBackground(QColor("#FFC000"))  # 橙色
        pCtrlDemoTable.item(1, c).setBackground(QColor("#FF0000"))  # 红色

    # control information table
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

    ''' insert led '''
    led16StaDev0 = []
    led16StaDev1 = []
    led16UvDev0 = []
    led16UvDev1 = []
    led16StaDev0.append(add_led_txt(16, pCtrlInfTable, 2, 3, LED_CBALSTAT_LAB))
    led16StaDev1.append(add_led_txt(16, pCtrlInfTable, 2, 10, LED_CBALSTAT_LAB))
    led16UvDev0.append(add_led_txt(16, pCtrlInfTable, 5, 3, LED_CBALUVSTAT_LAB))
    led16UvDev1.append(add_led_txt(16, pCtrlInfTable, 5, 10, LED_CBALUVSTAT_LAB))

    return led16StaDev0, led16StaDev1, led16UvDev0, led16UvDev1

