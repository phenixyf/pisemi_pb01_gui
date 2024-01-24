
""" step1: 导入必须的库和 layout 文件 """
import sys
from PyQt5.QtWidgets import *
from pb01_gui_layout import Ui_PB01_Demo    # pb01_gui_layout 是 QtDesigner 文件转成的 .py 文件
                                            # Ui_PB01_Demo 是 QtDesigner 文件转成 .py 文件后生成的类
from PyQt5.QtCore import *


""" step2: 通过继承 layout 文件的类制作 GUI 的类
           这个类中，要实现下面的内容：
           1. 控件的初始化
           2. 控件信号和槽的连接
           3. 各控件槽函数的实现
           4. 自定义个函数
           5. GUI 要实现的其它事项等，比如 HID 的连接
"""
class Pb01DemoWindow(QMainWindow, Ui_PB01_Demo):
    def __init__(self, parent=None):
        super(Pb01DemoWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()       # 定义初始化函数

    ''' GUI 初始化函数 '''
    def initUI(self):
        self.pushButton_37.clicked.connect(self.btn_handle)     # 定义控件 pushButton_37 单击信号的槽函数为 btn_handle



""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01DemoWindow()
    win.show()

    sys.exit(app.exec_())