""" step1: 导入必须的库和 layout 文件 """
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor

from pb01_dan import Ui_MainWindow

class Pb01DanWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()  # 定义初始化函数

    def initTableWidget(self, pTableWidget, pListHeader=[], pListItem=[], pGreenCol=3, pYellowCol=3):
        """
        used to initial own tablewidget
        :param pTableWidget: tablewidget object
        :param pListHeader: 标题栏内容，列表格式
        :param pListItem: 各单元格内容
        :param pGreenCol: 绿色填充的列号
        :param pYellowCol: 黄色填充列号的前一个列号
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
                if column == pGreenCol:  # 设置第 4 列的背景色
                    item.setBackground(QColor("#b5e6aa"))
                if column > pYellowCol:  # 设置第 5 ~ 14 列的背景色
                    item.setBackground(QColor("#fff0b3"))

        # 列宽自适应等
        pTableWidget.resizeColumnsToContents()


    ''' GUI 初始化函数 '''
    def initUI(self):
        ''' 初始化 uart interface configure table1 '''
        uartif_table1_headers = ["Address", "Register", "Expected {hex}", "Actual {hex}", "UARTDUAL", "UARTLPBK", "UARTWRPATH",
                          "TXUIDLEHIZ", "TXLIDLEHIZ", "UARTDCEN", "UARTALVCNTEN", "(Logic Zero)", "DBLBUFEN",
                          "Reserved/SPI[6:0]"]
        uartif_table1_items = [
            ["0x10", "UIFCFG (Single AFE)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"],
            ["0x10", "UIFCFG (Dual, Device 0)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"],
            ["0x10", "UIFCFG (Dual, Device 1)", "2600", "A410", "0", "0", "1", "0", "0", "1", "1", "0", "0", "0000000"]
        ]

        self.initTableWidget(self.tableWidget_uart_if_cfg1, uartif_table1_headers, uartif_table1_items, 3, 3)




""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01DanWindow()
    win.show()

    sys.exit(app.exec_())