# -*- coding: utf-8 -*-
# @Time    : 2024/1/28 14:33
# @Author  : yifei.su
# @File    : hid_driver.py

import time

CH32_SPI_TIME_DELAY = 0.01

def ch32_spi_full_duplex(pHidDev, pData, pNum):
    """
    ch32 bridge spi full duplex communication (used case like pb01)
    :param pData: send data which is transmitted in mosi line, list format
    :param pNum: the number of return data which in transmitted in miso line
    :return: return data which is from spi slave device
    """
    data = [0x1, len(pData) + 5, 0x03, 0x11, 0x0, 0x0, len(pData)]
    data.extend(pData)
    pHidDev.write(data)
    time.sleep(CH32_SPI_TIME_DELAY)
    read_data = pHidDev.read(pNum + 1)
    return read_data[1:]

def gpio_write(pHidBdg, gpio_pin, gpio_data=[]):
    """
    GPIO write function
    :param pHidBdg: hid object
    :param gpio_pin: gpio pin number
                      0 - gpio0 (PB4)
                      1 - gpio1 (PB5)
                      2 - gpio2 (PB15)
                      3 - gpio3 (PB14)
                      ...
                      7 - gpio7 (PB10)
    :param gpio_data: gpio toggle value
                      0 - gpio output low
                      1 - gpio output high
    :return:
    """
    data = [0x1, len(gpio_data) + 5, 0x01, 0x80, gpio_pin, 0x00, len(gpio_data)]
    data.extend(gpio_data)
    pHidBdg.write(data)
    time.sleep(CH32_SPI_TIME_DELAY)