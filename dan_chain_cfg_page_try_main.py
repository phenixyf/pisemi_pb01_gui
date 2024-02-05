""" step1: 导入必须的库和 layout 文件 """
import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import QColor

from dan_chain_cfg_page import Ui_MainWindow

from ui_configure import *
from uiset import *

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
        set_table_head(self.table_chainCfg_uartIfCfg, table_chainCfg_uartIfHead,
                            CHAIN_CFG_TABLE_HEHG, 150)
        set_table_head(self.table_chainCfg_uartIfAddr, table_chainCfg_uartAddrHead,
                            CHAIN_CFG_TABLE_HEHG, 130)
        self.radioButton_singleAfe.setChecked(True)
        self.slot_radio_single_dual_afe()

        # status power up dev0 table initial
        ledList_pageChain_st1_dev0, ledList_pageChain_st1_dev1, ledList_pageChain_st1_dev2,\
        ledList_pageChain_st1_dev3 = init_status_led_table_dev0(self.table_chainCfg_statusBlk_pwrUpDev0, 150)

        update_led_color(ledList_pageChain_st1_dev0[3], "#aa0000")

        init_status_led_table_dev1(self.table_chainCfg_statusBlk_pwrUpDev1, 150)



        # set_table_head(self.table_chainCfg_statusBlk_pwrUpDev0, table_chainCfg_staHead_dev0,
        #                     CHAIN_CFG_TABLE_HEHG, 150)
        #
        # set_led_table(self.table_chainCfg_statusBlk_pwrUpDev0, 4, CHAIN_CFG_TABLE_ROWHG,
        #                                               table_chainCfg_staItem_dev0, [3], [])
        # add_led_txt(16, self.table_chainCfg_statusBlk_pwrUpDev0, 0, 4)
        # self.table_chainCfg_statusBlk_pwrUpDev0.setColumnWidth(4, 450)

        set_table_head(self.table_chainCfg_statusBlk_initDev0, table_chainCfg_staHead_dev0,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_STAHG)
        set_table_item(self.table_chainCfg_statusBlk_initDev0, 4, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_staItem_dev0)
        set_table_head(self.table_chainCfg_statusBlk_curDev0, table_chainCfg_staHead_dev0,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_STAHG)
        set_table_item(self.table_chainCfg_statusBlk_curDev0, 4, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_staItem_dev0)
        set_table_head(self.table_chainCfg_rstBlk_Dev0, table_chainCfg_rstHead_dev0,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_RSTHG)
        set_table_item(self.table_chainCfg_rstBlk_Dev0, 1, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_rstItem_dev0)

        # set_table_head(self.table_chainCfg_statusBlk_pwrUpDev1, table_chainCfg_staHead_dev1,
        #                     CHAIN_CFG_TABLE_HEHG, 150)
        # set_led_table(self.table_chainCfg_statusBlk_pwrUpDev1, 4, CHAIN_CFG_TABLE_ROWHG,
        #                                          table_chainCfg_staItem_dev1, [0], [])
        set_table_head(self.table_chainCfg_statusBlk_initDev1, table_chainCfg_staHead_dev1,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_STAHG)
        set_table_item(self.table_chainCfg_statusBlk_initDev1, 4, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_staItem_dev1)
        set_table_head(self.table_chainCfg_statusBlk_curDev1, table_chainCfg_staHead_dev1,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_STAHG)
        set_table_item(self.table_chainCfg_statusBlk_curDev1, 4, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_staItem_dev1)
        set_table_head(self.table_chainCfg_rstBlk_Dev1, table_chainCfg_rstHead_dev1,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_RSTHG)
        set_table_item(self.table_chainCfg_rstBlk_Dev1, 1, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_rstItem_dev1)


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
            set_table_item(self.table_chainCfg_uartIfCfg, 2, CHAIN_CFG_TABLE_ROWHG,
                                                     table_chainCfg_uartIfItem	)
            set_table_item(self.table_chainCfg_uartIfAddr, 2, CHAIN_CFG_TABLE_ROWHG,
                                                          table_chainCfg_uartAddrItem)
            self.table_chainCfg_statusBlk_pwrUpDev1.hide()
            self.table_chainCfg_statusBlk_initDev1.hide()
            self.frame_statusReg_init_ledArray.hide()
        elif self.radioButton_dualAfe.isChecked():
            set_table_item(self.table_chainCfg_uartIfCfg, 3, CHAIN_CFG_TABLE_ROWHG,
                                                     table_chainCfg_uartIfItem)
            set_table_item(self.table_chainCfg_uartIfAddr, 3, CHAIN_CFG_TABLE_ROWHG,
                                                          table_chainCfg_uartAddrItem)
            self.table_chainCfg_statusBlk_pwrUpDev1.show()
            self.table_chainCfg_statusBlk_initDev1.show()
            self.frame_statusReg_init_ledArray.show()


""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01DanWindow()
    win.show()

    sys.exit(app.exec_())