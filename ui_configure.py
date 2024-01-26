from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor

""" tablewidget initial content """
uartif_table1_headers = ["Address", "Register", "Expected (hex)", "Actual (hex)", "UARTDUAL", "UARTLPBK",
                         "UARTWRPATH",
                         "TXUIDLEHIZ", "TXLIDLEHIZ", "UARTDCEN", "UARTALVCNTEN", "(Logic Zero)", "DBLBUFEN",
                         "Reserved/SPI[6:0]"]
uartif_table1_items = [
    ["0x10", "UIFCFG (Single AFE)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"],
    ["0x10", "UIFCFG (Dual, Device 0)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"],
    ["0x10", "UIFCFG (Dual, Device 1)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"]
]

uartif_table2_headers = ["Address", "Register", "Expected (hex)", "Actual (hex)", "ADDRUNLOCK", "BOTADDR[4:0]",
                         "TOPADDR[4:0]", "DEVADDR[4:0]"]
uartif_table2_items = [
    ["0x11", "ADDRESSCFG (Single AFE)", "0000", "8000", "0", "0000", "0000", "0000"],
    ["0x11", "ADDRESSCFG (Dual, Device 0)", "0020", "8000", "0", "0000", "0001", "0001"],
    ["0x11", "ADDRESSCFG (Dual, Device 1)", "0021", "8000", "0", "0000", "0001", "0001"]
]

status_reg_table_headers1 = ["Address", "Register", "Expect (hex)", "Device 0 (hex)"]
status_reg_table_items1 = [
    ["0x04", "STATUS1", "4000", "4000"],
    ["0x05", "STATUS2", "0000", "0000"],
    ["0x06", "FMEA1", "0000", "0000"],
    ["0x07", "FMEA2", "0000", "0000"]
]


def set_table_item_data_and_background_color(pTableWidget, pShowRowCnt, pRowHeight,
                                             pItemData=[], pListGreenCol=[], pListYellowCol=[]):
    """
    该函数用在 tablewidget 控件初始化过程中，实现 3 个功能：
    1. 设置单元格初始值
    2. 设置单元格指定列的背景颜色
    3. 设置单元格内数据水平和垂直居中对齐
    4. 设置单元格行高度
    5. 显示指定的行数内容
    6. 设置列宽自适应宽度
    注意：调用该函数后，对应 tablewidget 内的所有数据都会恢复成初始值，这个函数仅用在 GUI 一开始初始化和
    CHAIN CONFIGURATION page 的 single afe 和 dual afe radio button 切换操作时
    :param pTableWidget: tablewidget 实例
    :param pShowRowCnt: 要显示的行数
    :param pRowHeight: 行高度值
    :param pItemData: 单元格填入的数据，列表格式
    :param pListGreenCol: 要填充成绿色的列数，列表格式
    :param pListYellowCol: 要填充成黄色的列数，列表格式
    :return:
    """
    pTableWidget.setRowCount(pShowRowCnt)
    for row in range(pShowRowCnt):
        for column in range(pTableWidget.columnCount()):
            # 设置单元格的初始值
            pTableWidget.setItem(row, column, QTableWidgetItem(pItemData[row][column]))
            pTableWidget.item(row, column).setTextAlignment(Qt.AlignCenter)  # 设置单元格内容水平垂直居中对齐
            # 设置单元格背景色
            if column in pListGreenCol:
                pTableWidget.item(row, column).setBackground(QColor("#b5e6aa"))  # 设置绿色背景色
            if column in pListYellowCol:
                pTableWidget.item(row, column).setBackground(QColor("#fff0b3"))  # 设置黄色背景色
        # 设置行高度
        pTableWidget.setRowHeight(row, pRowHeight)

    # 设置列宽自适应
    pTableWidget.resizeColumnsToContents()


def initial_tablewidget(pTableWidget, pListHeader, pHeaderHeight, pTableHeight):
    """
    初始化 tablewidget
    完成下面操作：
    1. 设置标题栏内容、高度，并设置水平和垂直居中对齐
    2. 提供个单元格数据，用一个列表变量的格式
    3. 设置 tablewidget 固定高度
    注意：该函数仅初始化了 tablewidget 的标题，一定要同时搭配调用 set_table_item_data_and_background_color 才能
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


def update_led_color(label, color):
    """
    更新LED颜色的函数。

    :param label: 要更新的QLabel实例。
    :param color: 一个包含颜色代码的字符串，比如 "#FF0000" 表示红色。
    """
    style_sheet = f"""
          QLabel {{
              border-radius: 10px; /* 保持圆形 */
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