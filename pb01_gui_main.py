# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 10:44
# @Author  : yifei.su
# @File    : pb01_gui_main.py


""" step1: 导入必须的库和 layout 文件 """
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor

from main_window import Ui_MainWindow

class Pb01MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()  # 定义初始化函数

    def initTableWidget(self, pTableWidget, pListHeader=[], pListItem=[], pListGreenCol=[], pListYellowCol=[]):
        """
        used to initial own tablewidget
        :param pTableWidget: tablewidget object
        :param pListHeader: 标题栏内容，列表格式
        :param pListItem: 各单元格内容，列表格式
        :param pListGreenCol: 绿色填充的列号，列表格式
        :param pListYellowCol: 黄色填充列号，列表格式
        :return:
        """
        # 设置列标题
        pTableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)  # 设置标题内容水平居中对齐
        pTableWidget.setHorizontalHeaderLabels(pListHeader)  # 设置标题栏内容

        # 设置单元格数据
        # 填充数据并设置背景色
        for row, row_data in enumerate(pListItem):
            for column, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignHCenter)  # 设置单元格内容水平居中对齐
                pTableWidget.setItem(row, column, item)
                # 根据条件设置背景色
                if column in pListGreenCol:  # 设置绿色背景色
                    item.setBackground(QColor("#b5e6aa"))
                if column in pListYellowCol:  # 设置黄色背景色
                    item.setBackground(QColor("#fff0b3"))

        # 列宽自适应等
        pTableWidget.resizeColumnsToContents()


    ''' GUI 初始化函数 '''
    def initUI(self):
        ''' 初始化 uart interface configure table1 '''
        uartIf_table1_headers = ["Address", "Register", "Expected (hex)", "Actual (hex)", "UARTDUAL", "UARTLPBK", "UARTWRPATH",
                          "TXUIDLEHIZ", "TXLIDLEHIZ", "UARTDCEN", "UARTALVCNTEN", "(Logic Zero)", "DBLBUFEN",
                          "Reserved/SPI[6:0]"]
        uartIf_table1_items = [
            ["0x10", "UIFCFG (Single AFE)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"],
            ["0x10", "UIFCFG (Dual, Device 0)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"],
            ["0x10", "UIFCFG (Dual, Device 1)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"]
        ]

        self.initTableWidget(self.tableWidget_uartIf_conf, uartIf_table1_headers, uartIf_table1_items, [3],
                             range(4, 14))

        ''' 初始化 uart interface configure table2 '''
        uartIf_table2_headers = ["Address", "Register", "Expected (hex)", "Actual (hex)", "ADDRUNLOCK", "BOTADDR[4:0]",
                                 "TOPADDR[4:0]", "DEVADDR[4:0]"]
        uartIf_table2_items = [
            ["0x11", "ADDRESSCFG (Single AFE)", "0000", "8000", "0", "0000", "0000", "0000"],
            ["0x11", "ADDRESSCFG (Dual, Device 0)", "0020", "8000", "0", "0000", "0001", "0001"],
            ["0x11", "ADDRESSCFG (Dual, Device 1)", "0021", "8000", "0", "0000", "0001", "0001"]
        ]

        self.initTableWidget(self.tableWidget_uartIf_addr, uartIf_table2_headers, uartIf_table2_items, [3], range(4, 8))

        ''' 初始化 status register table '''
        status_reg_table_headers = ["Address", "Register", "Condition", "Expect (hex)", "Actual (hex)"]
        status_reg_table_items = [
            ["0x04", "STATUS (Device 0)", "Power-Up", "4000", "4000"],
            ["0x04", "STATUS (Device 1)", "Power-Up", "4000", "4000"],
            ["0x04", "STATUS (Device 0)", "After Initialization", "0000", "0000"],
            ["0x04", "STATUS (Device 1)", "After Initialization", "0000", "0000"]
        ]

        self.initTableWidget(self.tableWidget_status_reg_init, status_reg_table_headers, status_reg_table_items, [4], [])


""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01MainWindow()
    win.show()

    sys.exit(app.exec_())