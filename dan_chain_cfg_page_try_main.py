""" step1: 导入必须的库和 layout 文件 """
import sys
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
        set_table_head(self.table_chainCfg_uartIfCfg, table_chainCfg_uartIfHead,
                            CHAIN_CFG_TABLE_HEHG, 150)
        set_table_head(self.table_chainCfg_uartIfAddr, table_chainCfg_uartAddrHead,
                            CHAIN_CFG_TABLE_HEHG, 130)

        self.radioButton_singleAfe.setChecked(True)
        self.slot_radio_single_dual_afe()

        # status power up dev0 table initial
        ledList_pageChain_st1pu_dev0, ledList_pageChain_st2pu_dev0, ledList_pageChain_fm1pu_dev0,\
        ledList_pageChain_fm2pu_dev0 = init_status_led_table_dev0(self.table_chainCfg_statusBlk_pwrUpDev0, 150)

        update_led_color(ledList_pageChain_st1pu_dev0[3], "#aa0000")

        # status power up dev1 table initial
        ledList_pageChain_st1pu_dev1, ledList_pageChain_st2pu_dev1, ledList_pageChain_fm1pu_dev1, \
        ledList_pageChain_fm2pu_dev1 = init_status_led_table_dev1(self.table_chainCfg_statusBlk_pwrUpDev1, 150)

        # status initial dev0 table initial
        ledList_pageChain_st1in_dev0, ledList_pageChain_st2in_dev0, ledList_pageChain_fm1in_dev0, \
        ledList_pageChain_fm2in_dev0 = init_status_led_table_dev0(self.table_chainCfg_statusBlk_initDev0, 120)

        # status initial dev1 table initial
        ledList_pageChain_st1in_dev1, ledList_pageChain_st2in_dev1, ledList_pageChain_fm1in_dev1, \
        ledList_pageChain_fm2in_dev1 = init_status_led_table_dev1(self.table_chainCfg_statusBlk_initDev1, 120)

        # status current dev0 table initial
        ledList_pageChain_st1cu_dev0, ledList_pageChain_st2cu_dev0, ledList_pageChain_fm1cu_dev0, \
        ledList_pageChain_fm2cu_dev0 = init_status_led_table_dev0(self.table_chainCfg_statusBlk_curDev0, 120)

        # status current dev1 table initial
        ledList_pageChain_st1cu_dev1, ledList_pageChain_st2cu_dev1, ledList_pageChain_fm1cu_dev1, \
        ledList_pageChain_fm2cu_dev1 = init_status_led_table_dev1(self.table_chainCfg_statusBlk_curDev1, 120)

        # reset dev0 table initial
        set_table_head(self.table_chainCfg_rstBlk_Dev0, table_chainCfg_rstHead_dev0,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_RSTHG)
        set_table_item(self.table_chainCfg_rstBlk_Dev0, 1, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_rstItem_dev0)
        self.table_chainCfg_rstBlk_Dev0.item(0,3).setBackground(QColor("#E2F0D9"))
        # reset dev1 table initial
        set_table_head(self.table_chainCfg_rstBlk_Dev1, table_chainCfg_rstHead_dev1,
                            CHAIN_CFG_TABLE_HEHG, CHAIN_CFG_TABLE_RSTHG)
        set_table_item(self.table_chainCfg_rstBlk_Dev1, 1, CHAIN_CFG_TABLE_ROWHG,
                                                 table_chainCfg_rstItem_dev1)
        self.table_chainCfg_rstBlk_Dev1.item(0, 0).setBackground(QColor("#E2F0D9"))


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
            self.table_chainCfg_statusBlk_curDev1.hide()
        elif self.radioButton_dualAfe.isChecked():
            set_table_item(self.table_chainCfg_uartIfCfg, 3, CHAIN_CFG_TABLE_ROWHG,
                                                     table_chainCfg_uartIfItem)
            set_table_item(self.table_chainCfg_uartIfAddr, 3, CHAIN_CFG_TABLE_ROWHG,
                                                          table_chainCfg_uartAddrItem)
            self.table_chainCfg_statusBlk_pwrUpDev1.show()
            self.table_chainCfg_statusBlk_initDev1.show()
            self.table_chainCfg_statusBlk_curDev1.show()


""" step3: 通过下面代码完成 GUI 的显示 """
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Pb01DanWindow()
    win.show()

    sys.exit(app.exec_())