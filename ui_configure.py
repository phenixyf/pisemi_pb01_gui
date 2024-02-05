# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 10:42
# @Author  : yifei.su
# @File    : ui_configure.py


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor

from uiset import *


""" CHAIN CONFIGURATION page tablewidget initial content """
CHAIN_CFG_TABLE_HEHG = 30       # table header row height
CHAIN_CFG_TABLE_ROWHG = 15      # table row height
CHAIN_CFG_TABLE_STAHG = 120     # status block 不显示 header 的 4 个 table 的高度
CHAIN_CFG_TABLE_RSTHG = 60      # reset block table 的高度

table_chainCfg_uartIfHead = ["Address", "Register", "Expected (hex)", "Actual (hex)", "UARTDUAL", "UARTLPBK",
                         "UARTWRPATH",
                         "TXUIDLEHIZ", "TXLIDLEHIZ", "UARTDCEN", "UARTALVCNTEN", "(Logic Zero)", "DBLBUFEN",
                         "Reserved/SPI[6:0]"]
table_chainCfg_uartIfItem = [
    ["0x10", "UIFCFG (Single AFE)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"],
    ["0x10", "UIFCFG (Dual, Device 0)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"],
    ["0x10", "UIFCFG (Dual, Device 1)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"]
]

table_chainCfg_uartAddrHead = ["Address", "Register", "Expected (hex)", "Actual (hex)", "ADDRUNLOCK", "BOTADDR[4:0]",
                         "TOPADDR[4:0]", "DEVADDR[4:0]"]
table_chainCfg_uartAddrItem = [
    ["0x11", "ADDRESSCFG (Single AFE)", "0000", "8000", "0", "0000", "0000", "0000"],
    ["0x11", "ADDRESSCFG (Dual, Device 0)", "0020", "8000", "0", "0000", "0001", "0001"],
    ["0x11", "ADDRESSCFG (Dual, Device 1)", "0021", "8000", "0", "0000", "0001", "0001"]
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
appCfgReg_table_headers = ["Address", "Register", "Pending (hex)", "Device 0 (hex)", "Device 1 (hex)"]
appCfgReg_table_items = [
    ["0x12", "STATUSCFG", "3FF", "3FF", "3FFF"],
    ["0x13", "DEVCFG", "2000", "2000", "2000"],
    ["0x14", "POLARITYCFG", "0000", "0000", "0000"],
    ["0x15", "AUXGPIOCFG", "2000", "FF00", "FF00"],
    ["0x16", "AUXREFCFG", "0000", "0000", "0000"]
]

alertCfgReg_table_headers = ["Address", "Register", "Pending (hex)", "Device 0 (hex)", "Device 1 (hex)"]
alertCfgReg_table_items = [
    ["0x18", "ALRTOVCFG", "FFFF", "0000", "0000"],
    ["0x19", "ALRTUVCFG", "FFFF", "0000", "0000"],
    ["0x1A", "ALRTAUXOVCFG", "FFFF", "0000", "0000"],
    ["0x1G", "ALRTAUXUVCFG", "FFFF", "0000", "0000"]
]

acquistionReg_table_headers = ["Address", "Register", "Pending (hex)",
                               "Pending Field", "Pending Value", "Pending Unit",
                               "Pending Field", "Pending Value", "Pending Unit",
                               "Device 0 (hex)", "Device 1 (hex)"]
acquistionReg_table_items = [
    ["0x40", "ACQDLY1", "1501", "CELLDLY", "2.106", "ms", "SWDLY", "0.096", "ms", "0000", "0000"],
    ["0x41", "ACQDLY2", "3220", "AUXDLY", "1.200", "ms", "CELLOPNDLY", "12.768", "ms", "0000", "0000"],
    ["0x42", "ACQCHSEL", "FFFF", "--",  "--",  "--", "--",  "--",  "--", "0000", "0000"],
    ["0x43", "ACQAUXSEL", "00FF", "--",  "--",  "--", "--",  "--",  "--", "0000", "0000"]
]

theresholdReg_table_headers = ["Address", "Register", "Pending (hex)",
                               "Pending Value", "Pending Unit",
                               "Device 0 (hex)", "Device 1 (hex)"]
theresholdReg_table_items = [
    ["0x20", "OVTHREG",         "E667",     "4.500",    "V",            "FFFF",   "FFFF"],
    ["0x21", "UVTREG",          "8A3D",     "2.700",    "V",            "0000",   "0000"],
    ["0x22", "BIPOVTHREG",      "051F",     "+0.100",   "V (Bipolar)",  "7FFF",   "7FFF"],
    ["0x23", "BIPUVTHREG",      "FAE1",     "-0.100",   "V (Bipolar)",  "8000",   "8000"],
    ["0x24", "ALTOVTHREG",      "E667",     "4.500",    "V",            "FFFF",   "FFFF"],
    ["0x25", "ALTUVTHREG",      "8A3D",     "2.700",    "V",            "0000",   "0000"],
    ["0x26", "ALTBIPOVTHREG",   "051F",     "+0.100",   "V (Bipolar)",  "7FFF",   "7FFF"],
    ["0x27", "ALTBIPUVTHREG",   "FAE1",     "-0.100",   "V (Bipolar)",  "8000",   "8000"],
    ["0x28", "AUXROVTHREG",     "TBD",      "TBD",      "Ratiometric",  "FFFF",   "FFFF"],
    ["0x29", "AUXRUVTHREG",     "TBD",      "TBD",      "Ratiometric",  "0000",   "0000"],
    ["0x2A", "AUXAOVTHREG",     "FFFF",     "2.500",    "V",            "FFFF",   "FFFF"],
    ["0x2B", "AUXAUVTHREG",     "0000",     "0.000",    "V",            "0000",   "0000"],
    ["0x2C", "MMTHREG",         "0CCD",     "0.250",    "V",            "FFFF",   "FFFF"],
    ["0x2D", "TEMPTHREG",       "0C48",     "120",      "C",            "0C48",   "0C48"]
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
    ledList0 = add_led_txt(16, pTableWidget, 0, 4)  # 第一行插入
    ledList1 = add_led_txt(16, pTableWidget, 1, 4)  # 第二行插入
    ledList2 = add_led_txt(16, pTableWidget, 2, 4)  # 第三行插入
    ledList3 = add_led_txt(16, pTableWidget, 3, 4)  # 第四行插入
    # 设置 LED 列宽度
    pTableWidget.setColumnWidth(4, 450)

    return ledList0, ledList1, ledList2, ledList3


def init_status_led_table_dev1(pTableWidget, pTableHeight):
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
    ledList0 = add_led_txt(16, pTableWidget, 0, 1)  # 第一行插入
    ledList1 = add_led_txt(16, pTableWidget, 1, 1)  # 第二行插入
    ledList2 = add_led_txt(16, pTableWidget, 2, 1)  # 第三行插入
    ledList3 = add_led_txt(16, pTableWidget, 3, 1)  # 第四行插入
    # 设置 LED 列宽度
    pTableWidget.setColumnWidth(1, 450)

    return ledList0, ledList1, ledList2, ledList3


def set_led_table(pTableWidget, pShowRowCnt, pRowHeight,
                  pItemData=[], pListGreenCol=[], pListYellowCol=[], pListBlueCol=[]):
    pTableWidget.setRowCount(pShowRowCnt)
    for row in range(pShowRowCnt):
        for column in range(pTableWidget.columnCount()-1):
            # 设置单元格的初始值
            pTableWidget.setItem(row, column, QTableWidgetItem(pItemData[row][column]))
            pTableWidget.item(row, column).setTextAlignment(Qt.AlignCenter)  # 设置单元格内容水平垂直居中对齐
            # 设置单元格背景色
            if column in pListGreenCol:
                pTableWidget.item(row, column).setBackground(QColor("#E2F0D9"))  # 设置绿色背景色
            if column in pListYellowCol:
                pTableWidget.item(row, column).setBackground(QColor("#FFF2CC"))  # 设置黄色背景色
            if column in pListBlueCol:
                pTableWidget.item(row, column).setBackground(QColor("#DAE3F3"))  # 设置蓝色背景色
        # 设置行高度
        pTableWidget.setRowHeight(row, pRowHeight)

    # 设置列宽自适应
    pTableWidget.resizeColumnsToContents()

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