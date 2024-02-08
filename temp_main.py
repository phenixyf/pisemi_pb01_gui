# -*- coding: utf-8 -*-
# @Time    : 2024/2/8 14:31
# @Author  : yifei.su
# @File    : temp_main.py

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor

from temporary import Ui_MainWindow


class TempWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.initUI()  # 定义初始化函数


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = TempWindow()
    win.show()

    sys.exit(app.exec_())