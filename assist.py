# -*- coding: utf-8 -*-
# @Time    : 2024/2/28 11:28
# @Author  : yifei.su
# @File    : assist.py.py

def hex_to_bin(hex_str):
    """
    将16进制字符串，转换为2进制字符串，移除"0b"前缀，并填充零以保持字节格式
    :param hex_str: 要转换的16进制字符串，如 ’1A3F'
    :return:
    """
    bin_str = bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)
    return bin_str

def convert_complement_data(pInt):
    if pInt >= 2**15:
        convertData = pInt - 2**16
    else:
        convertData = pInt

    return convertData

print(convert_complement_data(0xffff))