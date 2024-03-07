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

def convert_complement_data(pInt, pBitWidth):
    """
    将传入的无符号数，转成对应的有符号数。
    必须指定判断是否有符号数数据的位宽。
    :param pInt: 待转换的无符号数。即可以用十六机制格式，如 0x8001, 也可以用十进制格式，如32769
    :param pBitWidth: 位宽
    :return:
    """
    if pInt >= 2**(pBitWidth -1):
        convertData = pInt - 2**pBitWidth
    else:
        convertData = pInt

    return convertData


# print(f"0x0000 complement is: {convert_complement_data(0x0000, 16)}")
# print(f"0x0001 complement is: {convert_complement_data(0x0001, 16)}")
# print(f"0x0002 complement is: {convert_complement_data(0x0002, 16)}")
# print(f"0x0003 complement is: {convert_complement_data(0x0003, 16)}")
# print(f"0x7ffd complement is: {convert_complement_data(32765, 16)}")
# print(f"0x7ffe complement is: {convert_complement_data(32766, 16)}")
# print(f"0x7fff complement is: {convert_complement_data(32767, 16)}")
# print(f"0x8000 complement is: {convert_complement_data(32768, 16)}")
# print(f"0x8001 complement is: {convert_complement_data(32769, 16)}")
# print(f"0x8002 complement is: {convert_complement_data(32770, 16)}")
# print(f"0x8003 complement is: {convert_complement_data(0x8003, 16)}")
# print(f"0xfffd complement is: {convert_complement_data(0xfffd, 16)}")
# print(f"0xfffe complement is: {convert_complement_data(0xfffe, 16)}")
# print(f"0xffff complement is: {convert_complement_data(0xffff, 16)}")