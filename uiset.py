# -*- encoding: utf-8 -*-
"""
    @File: uiset.py \n
    @Contact: yafei.wang@pisemi.com \n
    @License: (C)Copyright {} \n
    @Modify Time: 2024/1/31 17:18 \n
    @Author: Pisemi Yafei Wang \n
    @Version: 1.0 \n
    @Description: None \n
    @Create Time: 2024/1/31 17:18 \n
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

LED_STA1_LAB = ["ACQ", "REST", "RJCT", "UIF", "OVST", "UVST", "ATOV", "ATUV",
                "AXOV", "AXUV", "DGOV", "DGUV", "MM", "CBAL", "FME1", "FME2"]
LED_STA2_LAB = ["PEUP", "PEDN", "MNUP", "MNDN", "PRUP", "PRDN", "RGUP", "RGDN",
                "DUAL", "CBTF", "CBDO", "CBER", "CBER", "SPCK", "SPCR", "SPRG"]
LED_FME1_LAB = ["OSC", "----", "----", "----", "----", "VAA", "VDD", "VIO",
                "AGD2", "AGND", "DGND", "IOGD", "HVOV", "HVUV", "TEM2", "TEM1"]
LED_FME2_LAB = ["HVHD", "AQTO", "----", "----", "A1ZS", "A1FS", "A2ZS", "A2FS",
                "USER", "MODE", "AQIN", "DVIN", "OTPE", "REGE", "MMBT", "CBBT"]


led_qss = "QLabel {\n" \
          "  border-radius: 5px; /* 使得QLabel成为圆形 */\n" \
          "  background: qradialgradient(\n" \
          "    cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5,\n" \
          "    stop: 0 #ffffff, /* 渐变的中心是白色 */\n" \
          "    stop: 0.4 #00aa00, /* 渐变为绿色 */\n" \
          "    stop: 0.5 #009900, /* 中间的圆环更浅的绿色 */\n" \
          "    stop: 1.0 #006600); /* 边缘是最浅的绿色 */\n" \
          "  box-shadow: 0px 0px 8px 0px #006600; /* 添加阴影以增强3D效果 */\n" \
          "}"

font = QtGui.QFont()
# 设置字体的大小
font.setPointSize(7)  # 20是字体的大小，你可以根据需要调整这个值


def led_generator():
    label_led = QtWidgets.QLabel()
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(label_led.sizePolicy().hasHeightForWidth())
    label_led.setSizePolicy(sizePolicy)
    label_led.setMinimumSize(QtCore.QSize(10, 10))
    label_led.setMaximumSize(QtCore.QSize(10, 10))
    label_led.setStyleSheet(led_qss)
    return label_led


def txt_generator(pTxt):
    label_txt = QtWidgets.QLabel(pTxt)
    label_txt.setFont(font)
    return label_txt

def page_rendering(pStatusTable):
    pStatusTable.setRowHeight(2, 20)
    pStatusTable.setRowHeight(0, 30)
    pStatusTable.setRowHeight(1, 30)

    for i in range(3, 7):
        pStatusTable.setRowHeight(i, 30)
    for i in range(7, 11):
        pStatusTable.setRowHeight(i, 20)

    pStatusTable.setSpan(0, 2, 1, 10)
    pStatusTable.setSpan(1, 2, 1, 10)

    for i in range(2, 7):
        pStatusTable.setSpan(i, 3, 1, 4)
        pStatusTable.setSpan(i, 8, 1, 4)

    led3ListArray = []
    led4ListArray = []

    led0List = add_led_txt(8, pStatusTable, 0, 2)
    led1List = add_led_txt(32, pStatusTable, 1, 2)

    for i in range(3, 7):
        led3ListArray.append(add_led_txt(16, pStatusTable, i, 3))

    for i in range(3, 7):
        led4ListArray.append(add_led_txt(16, pStatusTable, i, 8))

    return led0List, led1List, led3ListArray, led4ListArray


# def page_rendering(pStatusTable, pMea_ACQ_SUM_Led_List):
#     pStatusTable.setRowHeight(2, 20)
#     pStatusTable.setRowHeight(0, 30)
#     pStatusTable.setRowHeight(1, 30)
#
#     for i in range(3, 7):
#         pStatusTable.setRowHeight(i, 30)
#     for i in range(7, 11):
#         pStatusTable.setRowHeight(i, 20)
#
#     pStatusTable.setSpan(0, 2, 1, 10)
#     pStatusTable.setSpan(1, 2, 1, 10)
#
#     for i in range(2, 7):
#         pStatusTable.setSpan(i, 3, 1, 4)
#         pStatusTable.setSpan(i, 8, 1, 4)
#
#     pMea_ACQ_SUM_Led_List.append(add_led_txt(8, pStatusTable, 0, 2))
#     pMea_ACQ_SUM_Led_List.append(add_led_txt(32, pStatusTable, 1, 2))
#
#     for i in range(3, 7):
#         pMea_ACQ_SUM_Led_List.append(add_led_txt(16, pStatusTable, i, 3))
#
#     for i in range(3, 7):
#         pMea_ACQ_SUM_Led_List.append(add_led_txt(16, pStatusTable, i, 8))


def page_rendering_1(pSumTableDev0, pSumTableDev1):
    for i in range(0, 10):
        pSumTableDev0.setRowHeight(i, 20)
        pSumTableDev1.setRowHeight(i, 20)
    for i in range(1, 7):
        pSumTableDev0.setSpan(i, 3, 1, 4)
        pSumTableDev0.setSpan(i, 7, 1, 4)

        pSumTableDev1.setSpan(i, 3, 1, 4)
        pSumTableDev1.setSpan(i, 7, 1, 4)

    for i in range(8, 10):
        pSumTableDev0.setSpan(i, 3, 1, 4)
        pSumTableDev0.setSpan(i, 7, 1, 4)

        pSumTableDev1.setSpan(i, 3, 1, 4)
        pSumTableDev1.setSpan(i, 7, 1, 4)


def add_led_txt(pLedNum, pTableWidget, pRow, pCol, pLabelList):
    """
    将 led 及其上标插入到 table 表的某个单元格内
    :param pLedNum: 要插入的 led 数量
    :param pTableWidget: 要插入的 table 控件名
    :param pRow: 插入位置行号
    :param pCol: 插入位置列号
    :param pLabelList: led 上标
    :return: 返回插入的 led 对象列表
             通过返回的 led 对象列表，可以控制各 led，比如修改 led 的颜色
    """
    pList_led = []
    pList_txt = []
    for i in range(0, pLedNum):
        pList_led.append(led_generator())

    for i in range(0, pLedNum):
        pList_txt.append(txt_generator(pLabelList[i]))

    # for i in range(0, pLedNum):
    #     pList_txt.append(txt_generator("LED"+str(i)))

    pFrame = QtWidgets.QFrame()
    pLayout = QtWidgets.QGridLayout(pFrame)
    pLayout.setSpacing(0)
    # 为布局设置外边距：左、上、右、下
    pLayout.setContentsMargins(0, 0, 0, 0)

    for i in range(0, pLedNum):
        pLayout.addWidget(pList_txt[i], 0, i)
        pLayout.addWidget(pList_led[i], 1, i)
        pLayout.setAlignment(pList_txt[i], Qt.AlignCenter)
        pLayout.setAlignment(pList_led[i], Qt.AlignCenter)

    pTableWidget.setCellWidget(pRow, pCol, pFrame)

    return pList_led
