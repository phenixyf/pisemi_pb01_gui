""" step1: 导入必须的库和 layout 文件 """
import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import QColor

from dan_chain_cfg_page import Ui_MainWindow

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
        ''' inital CHAIN CONFIGURATION page '''
        # uart interface configuration tables
        initial_tablewidget(self.table_chainCfg_uartIfCfg, table_chainCfg_uartIfHead,
                            CHAIN_CFG_TABLE_HEHG, 150)
        initial_tablewidget(self.table_chainCfg_uartIfAddr, table_chainCfg_uartAddrHead,
                            CHAIN_CFG_TABLE_HEHG, 130)
        self.radioButton_singleAfe.setChecked(True)
        self.slot_radio_single_dual_afe()
        # status register tables
        initial_tablewidget(self.table_chainCfg_statusBlk_pwrUpDev0, table_chainCfg_staHead_dev0,
                            CHAIN_CFG_TABLE_HEHG, 150)
        set_table_item_data_and_background_color(self.table_chainCfg_statusBlk_pwrUpDev0, 4, CHAIN_CFG_TABLE_ROWHG,
                                                      table_chainCfg_staItem_dev0, [3], [])
        initial_tablewidget(self.table_chainCfg_statusBlk_initDev0, table_chainCfg_staHead_dev0,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_STAHG)
        set_table_item_data_and_background_color(self.table_chainCfg_statusBlk_initDev0, 4, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_staItem_dev0, [3], [])
        initial_tablewidget(self.table_chainCfg_statusBlk_curDev0, table_chainCfg_staHead_dev0,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_STAHG)
        set_table_item_data_and_background_color(self.table_chainCfg_statusBlk_curDev0, 4, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_staItem_dev0, [3], [])
        initial_tablewidget(self.table_chainCfg_rstBlk_Dev0, table_chainCfg_rstHead_dev0,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_RSTHG)
        set_table_item_data_and_background_color(self.table_chainCfg_rstBlk_Dev0, 1, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_rstItem_dev0, [3], [])

        initial_tablewidget(self.table_chainCfg_statusBlk_pwrUpDev1, table_chainCfg_staHead_dev1,
                            CHAIN_CFG_TABLE_HEHG, 150)
        set_table_item_data_and_background_color(self.table_chainCfg_statusBlk_pwrUpDev1, 4, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_staItem_dev1, [0], [])
        initial_tablewidget(self.table_chainCfg_statusBlk_initDev1, table_chainCfg_staHead_dev1,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_STAHG)
        set_table_item_data_and_background_color(self.table_chainCfg_statusBlk_initDev1, 4, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_staItem_dev1, [0], [])
        initial_tablewidget(self.table_chainCfg_statusBlk_curDev1, table_chainCfg_staHead_dev1,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_STAHG)
        set_table_item_data_and_background_color(self.table_chainCfg_statusBlk_curDev1, 4, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_staItem_dev1, [0], [])
        initial_tablewidget(self.table_chainCfg_rstBlk_Dev1, table_chainCfg_rstHead_dev1,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_RSTHG)
        set_table_item_data_and_background_color(self.table_chainCfg_rstBlk_Dev1, 1, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_rstItem_dev1, [0], [])


        # update_led_color(self.label_186, "#aa0000")

        ''' 配置信号和槽 '''
        self.radioButton_singleAfe.clicked.connect(self.slot_radio_single_dual_afe)
        self.radioButton_dualAfe.clicked.connect(self.slot_radio_single_dual_afe)
        self.pushButton_uartIfConf.clicked.connect(self.cfg_uart_if)

    def cfg_uart_if(self):
        self.table_chainCfg_uartIfCfg.item(1,6).setText("try")

    def slot_radio_single_dual_afe(self):
        """
        根据 single afe 和 dual afe radio button 被选择的状态，
        设置 QTableWidget 显示不同的行数
        :return:
        """
        if self.radioButton_singleAfe.isChecked():
            set_table_item_data_and_background_color(self.table_chainCfg_uartIfCfg, 2, CHAIN_CFG_TABLE_ROWHG,
                                                     table_chainCfg_uartIfItem	, [3], range(4, 14))
            set_table_item_data_and_background_color(self.table_chainCfg_uartIfAddr, 2, CHAIN_CFG_TABLE_ROWHG,
                                                          table_chainCfg_uartAddrItem, [3], range(4, 8))
            self.table_chainCfg_statusBlk_pwrUpDev1.hide()
            self.table_chainCfg_statusBlk_initDev1.hide()
            self.frame_statusReg_pwrUp_ledArray.hide()
            self.frame_statusReg_init_ledArray.hide()
        elif self.radioButton_dualAfe.isChecked():
            set_table_item_data_and_background_color(self.table_chainCfg_uartIfCfg, 3, CHAIN_CFG_TABLE_ROWHG,
                                                     table_chainCfg_uartIfItem	, [3], range(4, 14))
            set_table_item_data_and_background_color(self.table_chainCfg_uartIfAddr, 3, CHAIN_CFG_TABLE_ROWHG,
                                                          table_chainCfg_uartAddrItem, [3], range(4, 8))
            self.table_chainCfg_statusBlk_pwrUpDev1.show()
            self.table_chainCfg_statusBlk_initDev1.show()
            self.frame_statusReg_pwrUp_ledArray.show()
            self.frame_statusReg_init_ledArray.show()


""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01DanWindow()
    win.show()

    sys.exit(app.exec_())