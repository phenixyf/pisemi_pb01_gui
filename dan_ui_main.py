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


    ''' GUI 初始化函数 '''
    def initUI(self):
        ''' 初始化 uart interface configure table1 '''
        for row in range(3):
            for column in range(14):
                item = self.tableWidget_uart_if_cfg1.item(row, column)
                # 单元格内容水平居中对齐
                if item:  # 确保单元格不为空
                    item.setTextAlignment(Qt.AlignHCenter | item.textAlignment() & ~Qt.AlignHorizontal_Mask)
                # 填充单元格背景
                if column == 3:  # 设置第4列的背景色
                    item.setBackground(QColor("#b5e6aa"))
                # if column > 3:  # 设置第4列的背景色
                #     item.setBackground(QColor("#fff0b3"))

        self.tableWidget_uart_if_cfg1.resizeColumnsToContents()     # 设置 uart if cfg1 table 随内容自动设置列宽




""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01DanWindow()
    win.show()

    sys.exit(app.exec_())