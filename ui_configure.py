# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 10:42
# @Author  : yifei.su
# @File    : ui_configure.py


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor

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
CHAIN_CFG_TABLE_HEHG = 30       # table header row height
CHAIN_CFG_TABLE_ROWHG = 15      # table row height
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

''' '''
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

table_chainCfg_staHead_dev0 = ["Address", "Register", "Expect (hex)", "Device 0 (hex)", ""]
table_chainCfg_staItem_dev0 = [
    ["0x04", "STATUS1", "4000", "4000", ""],
    ["0x05", "STATUS2", "0000", "0000", ""],
    ["0x06", "FMEA1", "0000", "0000", ""],
    ["0x07", "FMEA2", "0000", "0000", ""]
]

table_chainCfg_staHead_dev1 = ["Device 1 (hex)", ""]
table_chainCfg_staItem_dev1 = [
    ["4000", ""],
    ["0000", ""],
    ["0000", ""],
    ["0000", ""]
]

table_chainCfg_rstHead_dev0 = ["Address", "Register", "FORCEPOR (hex)", "Device 0 (hex)", ""]
table_chainCfg_rstItem_dev0 = [
    ["0x0F", "RESETCTRL", "0001", "0000"]
]

table_chainCfg_rstHead_dev1 = ["Device 1 (hex)"]
table_chainCfg_rstItem_dev1 = [
    ["0000"]
]

""" APPLICATION CONFIGURATION page tablewidget initial content """
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
    pTableWidget.setFixedHeight(pTableHeight)  # 设置 table 高度


def set_table_item(pTableWidget, pShowRowCnt, pRowHeight, pItemData=[]):
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
    pTableWidget.setRowCount(pShowRowCnt)
    for row in range(pShowRowCnt):
        for column in range(pTableWidget.columnCount()):
            # 设置单元格的初始值
            pTableWidget.setItem(row, column, QTableWidgetItem(pItemData[row][column]))
            pTableWidget.item(row, column).setTextAlignment(Qt.AlignCenter)  # 设置单元格内容水平垂直居中对齐
        # 设置行高度
        pTableWidget.setRowHeight(row, pRowHeight)

    # 设置列宽自适应
    pTableWidget.resizeColumnsToContents()



def init_status_led_table_dev0(pTableWidget, pTableHeight):
    """
    初始化 chain configuration page，status dev0 的 3 个 table
    这三个 table 会在最后一列插入 led 串
    :param pTableWidget: 要初始化的 table
                         有 powerup, initial, current 3 个 table，每个 tabale 初始化时分别调用该函数
    :param pTableHeight: 设置 table 的总高度
                         powerup 会显示标题栏，另外两个不用，所以总高度不一样
    :return: 该函数会返回 4 行 led 串的 4 个列表，每个列表对应一行 led 串。
             返回各列表中的每个元素，分别对应各 led 对象，进而可以用来更新 led 的颜色
             ledList0 - STATUS1 led 串
             ledList1 - STATUS2 led 串
             ledList2 - FMEA1 led 串
             ledList3 - FMEA2 led 串
    """
    pTableWidget.setHorizontalHeaderLabels(table_chainCfg_staHead_dev0)  # 设置标题内容
    pTableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)  # 设置标题内容水平居中对齐
    pTableWidget.horizontalHeader().setFixedHeight(CHAIN_CFG_TABLE_HEHG)  # 设置标题行高度
    pTableWidget.setFixedHeight(pTableHeight)  # 设置 table 高度

    pTableWidget.setRowCount(4)
    for row in range(4):
        for column in range(pTableWidget.columnCount()):
            # 设置单元格的初始值
            pTableWidget.setItem(row, column, QTableWidgetItem(table_chainCfg_staItem_dev0[row][column]))
            pTableWidget.item(row, column).setTextAlignment(Qt.AlignCenter)  # 设置单元格内容水平垂直居中对齐
        # 设置行高度
        pTableWidget.setRowHeight(row, CHAIN_CFG_TABLE_ROWHG)
        # 设置背景
        pTableWidget.item(row, 3).setBackground(QColor("#E2F0D9"))  # 设置绿色背景色
        pTableWidget.item(row, 4).setBackground(QColor("#FFF2CC"))  # 设置黄色背景色

    # 设置列宽自适应
    pTableWidget.resizeColumnsToContents()

    # 插入 LED 图标对象
    ledList0 = add_led_txt(16, pTableWidget, 0, 4, LED_STA1_LAB)  # 第一行插入
    ledList1 = add_led_txt(16, pTableWidget, 1, 4, LED_STA2_LAB)  # 第二行插入
    ledList2 = add_led_txt(16, pTableWidget, 2, 4, LED_FME1_LAB)  # 第三行插入
    ledList3 = add_led_txt(16, pTableWidget, 3, 4, LED_FME2_LAB)  # 第四行插入
    # 设置 LED 列宽度
    pTableWidget.setColumnWidth(4, 450)

    # 返回各 led 对象
    return ledList0, ledList1, ledList2, ledList3


def init_status_led_table_dev1(pTableWidget, pTableHeight):
    """
    初始化 chain configuration page，status dev1 的 3 个 table
    这三个 table 会在最后一列插入 led 串
    :param pTableWidget: 要初始化的 table
                         有 powerup, initial, current 3 个 table，每个 tabale 初始化时分别调用该函数
    :param pTableHeight: 设置 table 的总高度
                         powerup 会显示标题栏，另外两个不用，所以总高度不一样
    :return: 该函数会返回 4 行 led 串的 4 个列表，每个列表对应一行 led 串。
             返回各列表中的每个元素，分别对应各 led 对象，进而可以用来更新 led 的颜色
             ledList0 - STATUS1 led 串
             ledList1 - STATUS2 led 串
             ledList2 - FMEA1 led 串
             ledList3 - FMEA2 led 串
    """
    pTableWidget.setHorizontalHeaderLabels(table_chainCfg_staHead_dev1)  # 设置标题内容
    pTableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)  # 设置标题内容水平居中对齐
    pTableWidget.horizontalHeader().setFixedHeight(CHAIN_CFG_TABLE_HEHG)  # 设置标题行高度
    pTableWidget.setFixedHeight(pTableHeight)  # 设置 table 高度

    pTableWidget.setRowCount(4)
    for row in range(4):
        for column in range(pTableWidget.columnCount()):
            # 设置单元格的初始值
            pTableWidget.setItem(row, column, QTableWidgetItem(table_chainCfg_staItem_dev1[row][column]))
            pTableWidget.item(row, column).setTextAlignment(Qt.AlignCenter)  # 设置单元格内容水平垂直居中对齐
        # 设置行高度
        pTableWidget.setRowHeight(row, CHAIN_CFG_TABLE_ROWHG)
        # 设置背景
        pTableWidget.item(row, 0).setBackground(QColor("#E2F0D9"))  # 设置绿色背景色
        pTableWidget.item(row, 1).setBackground(QColor("#FFF2CC"))  # 设置黄色背景色

    # 设置列宽自适应
    pTableWidget.resizeColumnsToContents()

    # 插入 LED 图标对象
    ledList0 = add_led_txt(16, pTableWidget, 0, 1, LED_STA1_LAB)  # 第一行插入
    ledList1 = add_led_txt(16, pTableWidget, 1, 1, LED_STA2_LAB)  # 第二行插入
    ledList2 = add_led_txt(16, pTableWidget, 2, 1, LED_FME1_LAB)  # 第三行插入
    ledList3 = add_led_txt(16, pTableWidget, 3, 1, LED_FME2_LAB)  # 第四行插入
    # 设置 LED 列宽度
    pTableWidget.setColumnWidth(1, 450)

    # 返回各 led 对象
    return ledList0, ledList1, ledList2, ledList3


def adjust_if_id_tables(pDevIdTable, puifCfgTable, paddCfgTable):
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


def set_if_id_tables_color(pRowNum, pDevIdTable, puifCfgTable, paddCfgTable):
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
                color = QColor("#E2F0D9")
            else:  # 4 到 13 列
                color = QColor("#FFF2CC")
            puifCfgTable.item(r, c).setBackground(color)

        # 设置 paddCfgTable 的背景颜色
        for c in range(3, 8):  # 列索引从 3 到 7
            if c == 3:
                color = QColor("#E2F0D9")
            else:  # 4 到 7 列
                color = QColor("#FFF2CC")
            paddCfgTable.item(r, c).setBackground(color)


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