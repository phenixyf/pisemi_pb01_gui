""" step1: 导入必须的库和 layout 文件 """
import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import QColor

from dan_chain_configuration_page import Ui_MainWindow

from ui_configure import *

class Pb01DanWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()  # 定义初始化函数

    def initUI(self):
        """
        GUI 初始化函数
        :return:
        """
        initial_tablewidget(self.tableWidget_uart_if_cfg1, uartif_table1_headers, 30, 150)
        initial_tablewidget(self.tableWidget_uart_if_cfg2, uartif_table2_headers, 30, 150)
        initial_tablewidget(self.tableWidget_status_reg_init, status_reg_table_headers1, 30, 150)
        set_table_item_data_and_background_color(self.tableWidget_status_reg_init, 4, 20,
                                                      status_reg_table_items1, [3], [])

        self.radioButton_single_afe.setChecked(True)
        self.slot_radio_single_dual_afe()

        update_led_color(self.label_186, "#aa0000")

        ''' 配置信号和槽 '''
        self.radioButton_single_afe.clicked.connect(self.slot_radio_single_dual_afe)
        self.radioButton_dual_afe.clicked.connect(self.slot_radio_single_dual_afe)
        self.pushButton_cfg_uart_if.clicked.connect(self.cfg_uart_if)

    def cfg_uart_if(self):
        self.tableWidget_uart_if_cfg1.item(1,6).setText("try")

    def slot_radio_single_dual_afe(self):
        """
        根据 single afe 和 dual afe radio button 被选择的状态，
        设置 QTableWidget 显示不同的行数
        :return:
        """
        if self.radioButton_single_afe.isChecked():
            set_table_item_data_and_background_color(self.tableWidget_uart_if_cfg1, 2, 20,
                                                     uartif_table1_items, [3], range(4, 14))
            set_table_item_data_and_background_color(self.tableWidget_uart_if_cfg2, 2, 20,
                                                          uartif_table2_items, [3], range(4, 8))
        elif self.radioButton_dual_afe.isChecked():
            set_table_item_data_and_background_color(self.tableWidget_uart_if_cfg1, 3, 20,
                                                     uartif_table1_items, [3], range(4, 14))
            set_table_item_data_and_background_color(self.tableWidget_uart_if_cfg2, 3, 20,
                                                          uartif_table2_items, [3], range(4, 8))



""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01DanWindow()
    win.show()

    sys.exit(app.exec_())