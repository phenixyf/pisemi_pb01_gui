# -*- coding: utf-8 -*-
# @Time    : 2024/1/28 14:49
# @Author  : yifei.su
# @File    : pb01_bridge_driver.py

import time

SCRIPT_DEBUG = False                 # Ture: 使能 debug print; False: 关闭 debug print
UART_MSG_RETURN_TIMEOUT  = 2        # 等待菊花链消息传回 bridge RX 的 timeout 时间 （5s)

from hid_driver import *


def debug_fun(pDebugData):
    if (pDebugData != "message return RX error" and pDebugData != "pec check error"):
        hex_return_data = [hex(n) for n in pDebugData]
        print("operation done and received returned data", hex_return_data)
    elif pDebugData == "pec check error":
        print(f"operation error code is:{pDebugData}")
    else:
        print(f"operation error code is:{pDebugData}")
    # ''' check bridge read status registers '''
    # print(f"bridge A01 = {hex(max17841_reg_read(hidBridge, 0x01))}")
    # print(f"bridge A09 = {hex(max17841_reg_read(hidBridge, 0x09))}")

def max17841_reg_read(pHidDev, pAddr):
    """
    max17841 spi 寄存器读操作
    max17841 寄存器位宽 1 byte (8bit)
    :param pHidDev: hid bridge object
    :param pAddr: 要读的 max17841 寄存器地址
    :return: 读回的数据, 注意只返回 1 个 byte
    """
    sdoData = ch32_spi_full_duplex(pHidDev, [pAddr, 0], 2)  # max17841 寄存器位宽为 1 个 byte
                                                            # 所以在发送完地址后，只要再发送一个 dummy byte
                                                            # 用于 MISO 上读取数据即可
    if len(sdoData) == 0:
        return "max17841 register read error"
    else:
        return sdoData[1]   # 只返回 1 个 byte


def max17841_reg_write(pHidDev, pAddr, pData):
    """
    max17841 spi 寄存器写操作
    :param pHidDev: hid bridge object
    :param pAddr: 要写的寄存器地址
    :param pData: 要写的寄存器数据
    :return: none
    """
    ch32_spi_full_duplex(pHidDev, [pAddr, pData], 2)


def max17841_reg_command(pHidDev, pAddr):
    """
    max17841 spi 只发送 register address (command)
    :param pHidDev: hid bridge object
    :param pAddr: 要写的寄存器地址 (command)
    :return: none
    """
    ch32_spi_full_duplex(pHidDev, [pAddr], 1)


def max17841_buf_write(pHidDev, pLdLoc, pMesLen, pUartMsg):
    """
    max17841 spi 向 transmit buffer 写操作
    :param pHidDev: hid bridge object
    :param pLdLoc: transmit buffer LD_Q location
    :param pMesLen: message length
    :param pUartMsg: uart 线上要发送的 message data, list format
    :return:
    """
    send_data = [pLdLoc, pMesLen]
    send_data.extend(pUartMsg)
    ch32_spi_full_duplex(pHidDev, send_data, len(send_data))


def max17841_buf_read(pHidDev, pLdLoc, pReadNum):
    """
    max17841 读 receive buffer 或 transmit buffer 操作
    :param pHidDev: hid bridge object
    :param pLdLoc: 读取的位置
                   如果是读 receive buffer,这个参数就是 0x93 或 0x91
                   如果是读 transmit buffer, 这个参数就是 0xC1 ~ 0xCD
    :param pReadNum: 读取的个数
    :return:
    """
    send_data = [pLdLoc]
    for _ in range(pReadNum):
        send_data.append(0)

    read_data = ch32_spi_full_duplex(pHidDev, send_data, pReadNum+1)

    if len(read_data) == 0:
        return "max17841 read buf error"
    else:
        return read_data[1:]


def max17841_clear_rx_buf(pHidDev):
    """
    pb01 api 在执行操作前，都先调用此函数，清空一下 17841 rx buffer
    清空的方法是通过判断当前 rx 中数据量，然后全部读出的方法
    :param pHidDev:
    :return: Ture - clear successfully
             False - time out
    """
    rxEtyNum = 0x00
    start_time = time.time()
    while rxEtyNum != 0x3E:
        bufData = max17841_buf_read(pHidDev, 0x93, 0x3E - rxEtyNum)  # through read RX to clear this buffer
        if bufData == "max17841 read buf error":
            if SCRIPT_DEBUG:
                print(f"clear 17841 rx: read buf error")
            continue    # rx buf 读取失败重新读取 rx buf

        time.sleep(0.01)
        if SCRIPT_DEBUG:
            print(f"clear 17841 rx: rx data is", bufData)

        rxEtyNum = max17841_reg_read(pHidDev, 0x1B)  # read current rx space register

        if rxEtyNum != "max17841 register read error":
            # check if timeout
            if time.time() - start_time > UART_MSG_RETURN_TIMEOUT:
                if SCRIPT_DEBUG:
                    print(f"clear 17841 rx: time out")
                return False    # clear rx buffer time out

            if SCRIPT_DEBUG:
                print(f"clear 17841 rx: current rx space is: {rxEtyNum}")

        else:   # read 17841 register fail
            if SCRIPT_DEBUG:
                print("clear 17841 rx: read max17841 R1B get none")
            if time.time() - start_time > UART_MSG_RETURN_TIMEOUT:  # Check if wait has timeout
                if SCRIPT_DEBUG:
                    print(f"clear 17841 rx: read R01 fail and time out")
                return False    # read max17841 register time out

    return True     # clear 17841 rx successfully


def max17841_check_msg_return_bridge(pHidDev):
    """
    判断之前发出的 message 是否从菊花链返回 bridge
    max17841 可以通过判断读取 R01 是否等于 0x12 来判断是否有 message 返回
    :param pHidDev:
    :return: True - return
             False - timeout
    """
    start_time = time.time()
    curReg = 0x00
    while curReg != 0x12:
        curReg = max17841_reg_read(pHidDev, 0x01)
        if curReg != "max17841 register read error":  # read 17841 register ok
            # Check if wait has timeout
            if time.time() - start_time > UART_MSG_RETURN_TIMEOUT:
                if SCRIPT_DEBUG:
                    print(f"check message return: wait time out")
                return False  # return false because wait time out

            if SCRIPT_DEBUG:
                print(f"check message return: current 17841 R01 = {hex(curReg)}")

        else:   # read 17841 R01 fail
            if SCRIPT_DEBUG:
                print("check message return: read max17841 R01 get none")
            if time.time() - start_time > UART_MSG_RETURN_TIMEOUT:
                if SCRIPT_DEBUG:
                    print(f"read R01 fail and time out")
                return False  # return false because read R01 fail

    return True   # get message back


def max17841_set_shdn(pHidDev, pValue):
    """
    configure max17841 SHDN pin status
    :param pHidDev: hid bridge object
    :param pValue: SHDN pin status value
                   0: SHDN pin is low
                   1: SHDN pin is high
    :return:
    """
    gpio_write(pHidDev, 6, [pValue])


def max17841_reset(pHidDev):
    max17841_set_shdn(pHidDev, 0)   # pull down shdn pin
    time.sleep(0.05)
    max17841_set_shdn(pHidDev, 1)   # pull up shdn pin
    time.sleep(0.05)


def max17841_init(pHidDev):
    max17841_reset(pHidDev)
    max17841_reg_write(pHidDev, 0x04, 0x01)     # A04=0x01 enable RX_Empty_INT
    max17841_reg_command(pHidDev, 0x20)         # Clear transmit buffer
    max17841_reg_command(pHidDev, 0xE0)         # Clear receive buffer


def cal_pec(pByteList, poly=0xB2):
    """
    计算 PB01 (max17854) 芯片 uart 协议要求的 crc8 验证码函数
    该函数根据输入的 16 进制数据列表，生成对应的 crc8 校验码
    :param byte_list: 要计算校验码的原数据 （通常是发送到 bridge transmit buffer 中的数据）
                      列表格式，比如：[0x02, 0x12, 0xB1, 0xB2]
    :param poly: 计算验证码用的 crc8 多项式
                 在 PB01 uart 协议中，这个值为 0xB2
                 所以在调用该函数时，poly 参数就使用默认值即可，不用传任何值给这个参数
    :return: 返回和输入 byte_list 对应的校验码
    """
    crc_byte = 0
    for byte in pByteList:
        crc_byte ^= byte
        for _ in range(8):
            if crc_byte & 1:
                crc_byte = (crc_byte >> 1) ^ poly
            else:
                crc_byte = crc_byte >> 1
            crc_byte &= 0xFF
    return crc_byte


def check_pec(pByteList, pPecCode):
    """
    验证 PB01 uart 协议要求的 crc8 验证码
    用于比对 bridge receive buffer 收到的数据和 PEC 码
    :param pByteList: receive buffer 收到的除 PEC 码之外的数据
                      列表格式，比如：[0x02, 0x12, 0xB1, 0xB2]
    :param pPecCode: receive buffer 收到的 PEC 码
    :return: 比对结果
             Ture - pByteList 的 crc8 校验码是 pPecCode
             False - pBytgList 的 crc8 校验码不是 pPecCode
    """
    return cal_pec(pByteList) == pPecCode


# def daisy_chain_initial_sequence_example(pHidDev):
#     print("------- TRANSACTION1: Enable keep-alive mode ------")
#     max17841_reg_write(pHidDev, 0x10, 0x05)  # write configuration 3,set keep-alive period to 160μs
#     print("------- TRANSACTION2: Enable Rx Interrupt flags for RX_Error and RX_Overflow ------")
#     max17841_reg_write(pHidDev, 0x04, 0x88)  # Write RX_Interrupt_Enable register
#     print("------- TRANSACTION3: Clear receive buffer ------")
#     max17841_reg_command(pHidDev, 0xE0)  # Clear receive buffer
#     print("------- TRANSACTION4: Wake-up UART slave devices (transmit preambles) ------")
#     max17841_reg_write(pHidDev, 0x0E, 0x30)         # Write Configuration 2 register
#                                                     # Enable Transmit Preambles mode
#
#     print("------- TRANSACTION5: Wait for all UART slave devices to wake up (poll RX_Busy_Status bit bit[5]) ------")
#     while max17841_reg_read(pHidDev,
#                             0x01) != 0x21:  #Read RX_Status register (RX_Busy_Status and RX_Empty_Status should be true)
#         print(f"current Reg0x01 is: {hex(max17841_reg_read(pHidDev, 0x01))}")
#
#     print("------- TRANSACTION6: End of UART slave device wake-up period ------")
#     max17841_reg_write(pHidDev, 0x0E, 0x10)     # Write Configuration 2 register
#                                                 # Disable Transmit Preambles mode
#
#     print("------- TRANSACTION7: Wait for null message to be received (poll RX_Empty_Status bit bit[0]) ------")
#     while max17841_reg_read(pHidDev,
#                             0x01) != 0x11:  # Read RX_Status register (RX_Empty_Status bit should be true)
#         print("RX_Empty_Status bit is not 1, clear RX buffer")
#         max17841_reg_command(pHidDev, 0xE0)  # Clear receive buffer
#         print(f"current Reg0x01 is: {hex(max17841_reg_read(pHidDev, 0x01))}")
#
#     print("------- TRANSACTION8: Clear transmit buffer ------")
#     max17841_reg_command(pHidDev, 0x20)  # Clear transmit buffer
#
#     print("------- TRANSACTION9: Clear receive buffer ------")
#     max17841_reg_command(pHidDev, 0xE0)  # Clear receive buffer
#
#     print("------- TRANSACTION10: Load the HELLOALL command sequence into the load queue ------")
#     max17841_buf_write(pHidDev, 0xC0, 0x03, [0x57, 0x00, 0x00])  # Load the HELLOALL command sequence into the load queue
#                                                                  # seed address is 0x00
#
#     print("------- TRANSACTION11: Verify contents of the load queue ------")
#     return_data = [hex(n) for n in max17841_buf_read(pHidDev, 0xC1, 4)]
#     print(f"current transmit buffer queue value is:{return_data}")
#
#     print("------- TRANSACTION12: Transmit HELLOALL sequence ------")
#     max17841_reg_command(pHidDev, 0xB0)  # WR_NXT_LD_Q SPI command byte (write the next load queue)
#
#     print("------- TRANSACTION13: Wait for HELLOALL message return to bridge (poll RX_Stop_Status bit bit[1]) ------")
#     while max17841_reg_read(pHidDev, 0x01) != 0x12:  # If RX_Stop_Status bit is true, continue
#         print(f" current reg0x01 value is: {hex(max17841_reg_read(pHidDev, 0x01))}")
#         print("If RX_Stop_Status bit is false, then re-send HELLOALL message")
#         max17841_buf_write(pHidDev, 0xC0, 0x03, [0x57, 0x00, 0x00])
#         return_data = [hex(n) for n in max17841_buf_read(pHidDev, 0xC1, 4)]
#         print(f"current transmit buffer queue value is:{return_data}")
#         max17841_reg_command(pHidDev, 0xB0)
#
#     print("------- TRANSACTION14: Read the returned HELLOALL message from bridge receive buffer ------")
#     return_data = [hex(n) for n in max17841_buf_read(pHidDev, 0x93, 3)]
#     print(f"from read buffer get returned HELLOALL message is: {return_data}")
#
#     print("------- TRANSACTION15: Check for receive buffer errors ------")
#     print(f"RX_Interrupt_Flags register 0x09 = {hex(max17841_reg_read(pHidDev, 0x09))}")


def pb01_write(pHidDev, pLdLoc, pMsgLen, pUartMsg, pAliveSeed = 0):
    """
    write data to PB01 device
    :param pHidDev: hid bridge object
    :param pLdLoc: 17841 transmit buffer LD_Q location
    :param pMsgLen: message length （ 除 pLdLoc, pMsgLen 外的数据个数）
    :param pUartMsg: uart message 列表里面内容如下
                     [ uart_command(如 WRITEALL), register_address, register_data_lsb, register_data_msb]
                     注意，上面列表中各数据的位置，不能更改，要符合 PB01 uart 协议要求
    :param pAliveSeed: alive count seed
    :return: 返回值分三种情况
             "message return RX error": 发出的数据没有正常返回 bridge receive buffer
             "pec check error"： pec check fail
             数据列表：发出的数据返回 bridger receive buffer，并被读出，返回的就是从 receive buffer 读出的 Loopback 数据
    """
    """ check bridge RX is empty """
    if max17841_clear_rx_buf(pHidDev) == False:
        return "message return RX error"

    """ uart operation """
    ''' calculate pec '''
    pec = cal_pec(pUartMsg)

    ''' send message queue into transmit buffer '''
    max17841_buf_write(pHidDev, pLdLoc, pMsgLen, pUartMsg + [pec] + [pAliveSeed])

    ''' start transmit from uart '''
    max17841_reg_command(pHidDev, 0xB0)

    ''' check message return back to bridge '''
    if max17841_check_msg_return_bridge(pHidDev) == False:
        if SCRIPT_DEBUG:
            print("pb01_write: check message return read R01 fail")
        return "message return RX error"

    ''' read return data '''
    return_data = max17841_buf_read(pHidDev, 0x93, len(pUartMsg + [pec]+ [pAliveSeed]))
    if return_data == "max17841 read buf error":
        if SCRIPT_DEBUG:
            print("pb01_write: check message return read rx buf fail")
        return "message return RX error"

    ''' check pec '''
    if check_pec( return_data[:-2], return_data[-2]):
        return return_data  # operation success
    else:
        if SCRIPT_DEBUG:
            print("pb01_write: check pec fail")
            hex_return_data = [hex(n) for n in return_data]
            print("pb01_write: return data ", hex_return_data)
        return "pec check error"    # pec check fail



def pb01_read(pHidDev, pLdLoc, pMsgLen, pUartMsg, pAliveSeed):
    """
    从 PB01 device 读数据
    :param pHidDev: hid bridge object
    :param pLdLoc: 17841 transmit buffer LD_Q location
    :param pMsgLen: message length （ 除 pLdLoc, pMsgLen 外的数据个数）
    :param pUartMsg: uart message 列表里面内容如下
                     [ uart_command(如 READALL), register_address, DC（0x00）]
                     注意，上面列表中各数据的位置，不能更改，要符合 PB01 uart 协议要求
    :param pAliveSeed: alive count seed
    :return: 返回值分三种情况
             "message return RX error": 发出的数据没有正常返回 bridge receive buffer
             "pec check error"： pec check fail
             数据列表：要读取的数据返回 bridger receive buffer，并被读出，返回的就是从 receive buffer 读出的数据
    """
    """ check bridge RX is empty """
    if max17841_clear_rx_buf(pHidDev) == False:
        return "message return RX error"

    """ uart operation """
    pec = cal_pec(pUartMsg)

    ''' send message queue into transmit buffer '''
    max17841_buf_write(pHidDev, pLdLoc, pMsgLen, pUartMsg + [pec] + [pAliveSeed])

    ''' start transmit from uart '''
    max17841_reg_command(pHidDev, 0xB0)

    ''' check message return back to bridge '''
    if max17841_check_msg_return_bridge(pHidDev) == False:
        if SCRIPT_DEBUG:
            print("pb01_read: check message return read R01 fail")
        return "message return RX error"

    ''' read return data '''
    return_data = max17841_buf_read(pHidDev, 0x93, pMsgLen)
    if return_data == "max17841 read buf error":
        if SCRIPT_DEBUG:
            print("pb01_read: check message return read rx buf fail")
        return "message return RX error"

    ''' check pec '''
    if check_pec(return_data[:-2], return_data[-2]):
        return return_data  # operation success
    else:
        if SCRIPT_DEBUG:
            print("pb01_read: check pec fail")
            hex_return_data = [hex(n) for n in return_data]
            print("pb01_read: return data ", hex_return_data)
        return "pec check error"    # pec check fail


def pb01_write_por(pHidDev, pLdLoc, pMsgLen, pUartMsg, pAliveSeed = 0):
    """
    pb01_write 的简化版，pb01_por 需要调用的底层 API
    因 AFE POR 后无法再透传 uart 数据，所以要把 pb01_write 后面的确认 daisy-chain 返回的步骤去掉，否则会报 timeout
    :param pHidDev: hid bridge object
    :param pLdLoc: 17841 transmit buffer LD_Q location
    :param pMsgLen: message length （ 除 pLdLoc, pMsgLen 外的数据个数）
    :param pUartMsg: uart message 列表里面内容如下
                     [ uart_command(如 WRITEALL), register_address, register_data_lsb, register_data_msb]
                     注意，上面列表中各数据的位置，不能更改，要符合 PB01 uart 协议要求
    :param pAliveSeed: alive count seed
    :return: True - success
             False - fail
    """
    """ check bridge RX is empty """
    if max17841_clear_rx_buf(pHidDev) == False:
        return False

    """ uart operation """
    ''' calculate pec '''
    pec = cal_pec(pUartMsg)

    ''' send message queue into transmit buffer '''
    max17841_buf_write(pHidDev, pLdLoc, pMsgLen, pUartMsg + [pec] + [pAliveSeed])

    ''' start transmit from uart '''
    max17841_reg_command(pHidDev, 0xB0)

    return True


def pb01_por(pHidDev):
    """
    专门用来发送 POR （Reg0F = 0x0001).
    :param pHidDev: hid bridge object
    :return:
    """
    return pb01_write_por(pHidDev, 0xC0, 0x06, [0x02, 0x0F, 0x01, 0x00], 0x00)



def pb01_daisy_chain_initial(pHidDev, pDevAddSeed):
    """
    daisy-chain initial process, complete below procedures
    1. send keep alive
    2. wake up all device in daisy-chain
    3. send HELLOALL command which distribute device address
    4. read returned HELLOALL command message
    :param pHidDev: hid bridge object
    :param pDevAddSeed: device seed address (should make top device address less than 32)
    :return: initial faile: error message
             initial success: HELLOALL message returned back data
    """
    ''' TRANSACTION1: Enable keep-alive mode '''
    max17841_reg_write(pHidDev, 0x10, 0x05)  # write configuration 3,set keep-alive period to 160μs
    ''' TRANSACTION2: Enable Rx Interrupt flags for RX_Error and RX_Overflow '''
    max17841_reg_write(pHidDev, 0x04, 0x88)  # Write RX_Interrupt_Enable register
    ''' TRANSACTION3: Clear receive buffer '''
    max17841_reg_command(pHidDev, 0xE0)  # Clear receive buffer
    ''' TRANSACTION4: Wake-up UART slave devices (transmit preambles) '''
    max17841_reg_write(pHidDev, 0x0E, 0x30)         # Write Configuration 2 register
                                                    # Enable Transmit Preambles mode

    ''' TRANSACTION5: Wait for all UART slave devices to wake up (poll RX_Busy_Status bit bit[5]) '''
    start_time = time.time()
    while max17841_reg_read(pHidDev,
                            0x01) != 0x21:  #Read RX_Status register (RX_Busy_Status and RX_Empty_Status should be true)
        print("TRANSACTION5 fail, preamble doesn't transmit back to bridge RX")
        print(f"current Reg0x01 is: {hex(max17841_reg_read(pHidDev, 0x01))}")
        if time.time() - start_time > UART_MSG_RETURN_TIMEOUT:  # Check if wait has timeout
            return "transaction5 time out"                      # return timeout message

    ''' TRANSACTION6: End of UART slave device wake-up period '''
    max17841_reg_write(pHidDev, 0x0E, 0x10)     # Write Configuration 2 register
                                                # Disable Transmit Preambles mode

    ''' TRANSACTION7: Wait for null message to be received (poll RX_Empty_Status bit bit[0]) '''
    start_time = time.time()
    while max17841_reg_read(pHidDev,
                            0x01) != 0x11:  # Read RX_Status register (RX_Empty_Status bit should be true)
        # print("TRANSACTION7 fail, after disable preamble RX is not empty, clear RX")
        max17841_reg_command(pHidDev, 0xE0)  # Clear receive buffer
        # print(f"current Reg0x01 is: {hex(max17841_reg_read(pHidDev, 0x01))}")
        if time.time() - start_time > UART_MSG_RETURN_TIMEOUT:  # Check if wait has timeout
            return "transaction7 time out"                      # return timeout message

    ''' TRANSACTION8: Clear transmit buffer '''
    max17841_reg_command(pHidDev, 0x20)  # Clear transmit buffer

    ''' TRANSACTION9: Clear receive buffer '''
    max17841_reg_command(pHidDev, 0xE0)  # Clear receive buffer
    time.sleep(0.05)    # wait clear operation done

    ''' TRANSACTION10: Load the HELLOALL command sequence into the load queue '''
    max17841_buf_write(pHidDev, 0xC0, 0x03, [0x57, 0x00, pDevAddSeed])  # Load the HELLOALL command sequence into the load queue
                                                                        # seed address is 0x00

    ''' TRANSACTION11: Verify contents of the load queue '''
    return_data = [hex(n) for n in max17841_buf_read(pHidDev, 0xC1, 4)]
    print(f"current transmit buffer queue value is:{return_data}")

    ''' TRANSACTION12: Transmit HELLOALL sequence '''
    max17841_reg_command(pHidDev, 0xB0)  # WR_NXT_LD_Q SPI command byte (write the next load queue)

    ''' TRANSACTION13: Wait for HELLOALL message return to bridge (poll RX_Stop_Status bit bit[1]) '''
    start_time = time.time()
    while max17841_reg_read(pHidDev, 0x01) != 0x12:  # If RX_Stop_Status bit is true, continue
        print("TRANSACTION13 fail, HELLOALL doesn't return back to bridge RX")
        print(f" current reg0x01 value is: {hex(max17841_reg_read(pHidDev, 0x01))}")
        print("If RX_Stop_Status bit is false, then re-send HELLOALL message")
        max17841_buf_write(pHidDev, 0xC0, 0x03, [0x57, 0x00, 0x00])
        return_data = [hex(n) for n in max17841_buf_read(pHidDev, 0xC1, 4)]
        print(f"current transmit buffer queue value is:{return_data}")
        max17841_reg_command(pHidDev, 0xB0)
        if time.time() - start_time > UART_MSG_RETURN_TIMEOUT:      # Check if wait has timeout
            return "transaction13 time out"                         # return timeout message

    ''' TRANSACTION14: Read the returned HELLOALL message from bridge receive buffer '''
    return_data = max17841_buf_read(pHidDev, 0x93, 3)   # read returned message
    if return_data == "max17841 read buf error":
        if SCRIPT_DEBUG:
            print("daisy-chain initial: check HELLOALL message return read rx buf fail")
        return "HELLOALL message return error"

    ''' check bridge RX is empty '''
    if max17841_clear_rx_buf(pHidDev) == False:
        return "clear bridge rx buffer time out"

    return [hex(n) for n in return_data]



def pb01_write_all(pHidDev, pRegAddr, pData, pAliveSeed):
    """
    execute UART WRITEALL command
    :param pHidDev: hid bridge object
    :param pRegAddr: PB01 register address
    :param pData: write data
    :param pAliveSeed: alive count seed
    :return: 返回值分三种情况
             "message return RX error": 发出的数据没有正常返回 bridge receive buffer
             "pec check error"： pec check fail
             数据列表：发出的数据返回 bridger receive buffer，并被读出，返回的就是从 receive buffer 读出的 Loopback 数据
    """
    dataLsb = pData & 0x00FF
    dataMsb = (pData & 0xFF00) >> 8
    return pb01_write(pHidDev, 0xC0, 0x06, [0x02, pRegAddr, dataLsb, dataMsb], pAliveSeed)


def pb01_write_device(pHidDev, pDevAddr, pRegAddr, pData, pAliveSeed):
    """
    execute UART WRITEDEVICE command
    :param pHidDev: hid bridge object
    :param pDevAddr: device address (note: should be less than 31)
    :param pRegAddr: PB01 register address
    :param pData: write data
    :param pAliveSeed: alive count seed
    :return: 返回值分三种情况
             "message return RX error": 发出的数据没有正常返回 bridge receive buffer
             "pec check error"： pec check fail
             数据列表：发出的数据返回 bridger receive buffer，并被读出，返回的就是从 receive buffer 读出的 Loopback 数据
    """
    cmd = (pDevAddr << 3) | 0x4
    dataLsb = pData & 0x00FF
    dataMsb = (pData & 0xFF00) >> 8
    return pb01_write(pHidDev, 0xC0, 0x06, [cmd, pRegAddr, dataLsb, dataMsb], pAliveSeed)


def pb01_read_all(pHidDev, pRegAddr, pDevNum, pAliveSeed):
    """
    execute UART READALL command
    :param pHidDev: hid bridge object
    :param pRegAddr: PB01 register address
    :param pDevNum: 要读取的 device 数量 (注意不是要读取的寄存个数，而是菊花链中要读取的设备的数量)
    :param pAliveSeed: alive count seed
    :return: 返回值分三种情况
             "message return RX error": 发出的数据没有正常返回 bridge receive buffer
             "pec check error"： pec check fail
             数据列表：要读取的数据返回 bridger receive buffer，并被读出，返回的就是从 receive buffer 读出的数据
                     列表中每个成员都是 int 类型
    """
    return pb01_read(pHidDev, 0xC0, 5+pDevNum*2, [0x03, pRegAddr, 0x00], pAliveSeed)


def pb01_read_device(pHidDev, pDevAddr, pRegAddr, pAliveSeed):
    """
    execute UART READDEVICE command
    :param pHidDev: hid bridge object
    :param pDevAddr: device address
    :param pRegAddr: PB01 register address
    :param pAliveSeed: alive count seed
    :return: 返回值分三种情况
             "message return RX error": 发出的数据没有正常返回 bridge receive buffer
             "pec check error"： pec check fail
             数据列表：要读取的数据返回 bridger receive buffer，并被读出，返回的就是从 receive buffer 读出的数据
                     列表中每个成员都是 int 类型
    """
    cmd = (pDevAddr << 3) | 0x5
    return pb01_read(pHidDev, 0xC0, 7, [cmd, pRegAddr, 0x00], pAliveSeed)


def pb01_read_block(pHidDev, pBlockSize, pDevAddr, pRegAddr, pAliveSeed):
    """
    execute UART READBLOCK command
    :param pHidDev: hid bridge object
    :param pBlockSize: 要读取的 block size 大小 （一个 block 中寄存器的个数）
    :param pDevAddr: device address
    :param pRegAddr: block start register address
    :param pAliveSeed: alive count seed
    :return: 返回值分三种情况
             "message return RX error": 发出的数据没有正常返回 bridge receive buffer
             "pec check error"： pec check fail
             数据列表：要读取的数据返回 bridger receive buffer，并被读出，返回的就是从 receive buffer 读出的数据
                     列表中每个成员都是 int 类型
    """
    cmd = (pBlockSize << 3) | 0x6
    return pb01_read(pHidDev, 0xC0, 6+pBlockSize*2, [cmd, pDevAddr, pRegAddr, 0x00], pAliveSeed)


def pb01_17841_alert_packet(pHidDev):
    """
        execute UART ALERTPACKET
        因 ALERTPACKET command message 的长度为 8， 超出了 max17841 tx buffer 最大的 message 长度 6
        所以，要用两个 tx queue 拼接 ALERTPACKET command.
        拼接的过程需要 disable keep-alive，容易引起 PB01 shut down，为缩短时间，在 shut down 前完成拼接，
        将拼接的流程放在 firmware 中完成。本函数会调用对应的命令启动该流程。
        :param pHidDev: hid bridge object
        :return: 返回值分三种情况
                 "message return RX error": 发出的数据没有正常返回 bridge receive buffer
                 "pec check error"： pec check fail
                 数据列表：发出的数据返回 bridger receive buffer，并被读出，返回的就是从 receive buffer 读出的 Loopback 数据
        """
    """ check bridge RX is empty """
    if max17841_clear_rx_buf(pHidDev) == False:
        return "message return RX error"

    """ 调用 firmware 中拼接 ALERTPACKET command 的流程 """
    data = [0x1, 5, 0x04, 0x0, 0x0, 0x0, 0x0]
    pHidDev.write(data)

    ''' check message return back to bridge '''
    if max17841_check_msg_return_bridge(pHidDev) == False:
        if SCRIPT_DEBUG:
            print("pb01_17841_alert_packet: check message return read R01 fail")
        return "message return RX error"

    ''' read return data '''
    return_data = max17841_buf_read(pHidDev, 0x93, 8)
    if return_data == "max17841 read buf error":
        if SCRIPT_DEBUG:
            print("pb01_17841_alert_packet: check message return read rx buf fail")
        return "message return RX error"

    ''' check pec '''
    if check_pec(return_data[:-1], return_data[-1]):
        return return_data  # operation success
    else:
        if SCRIPT_DEBUG:
            print("pb01_17841_alert_packet: check pec error")
        return "pec check error"  # pec check fail


def pb01_path_up(pHidDev, pDevCntSeed):
    """
    send PB01 WRPATHUP command
    :param pHidDev:
    :param pDevCntSeed: 菊花链中 device 数量
    :return: 1. returned command message
             2. "message return RX error"
    """
    """ check bridge RX is empty """
    if max17841_clear_rx_buf(pHidDev) == False:
        return "message return RX error"

    ''' send message queue into transmit buffer '''
    max17841_buf_write(pHidDev, 0xC0, 3, [0x08, 0x00, pDevCntSeed])

    ''' start transmit from uart '''
    max17841_reg_command(pHidDev, 0xB0)

    ''' check message return back to bridge '''
    if max17841_check_msg_return_bridge(pHidDev) == False:
        if SCRIPT_DEBUG:
            print("pb01_path_up: check message return read R01 fail")
        return "message return RX error"

    ''' read return data '''
    return_data = max17841_buf_read(pHidDev, 0x93, 3)
    if return_data == "max17841 read buf error":
        if SCRIPT_DEBUG:
            print("pb01_path_up: check message return read rx buf fail")
        return "message return RX error"
    else:
        return return_data


def pb01_path_down(pHidDev, pDevCntSeed):
    """
    send PB01 WRPATHDN command
    :param pHidDev:
    :param pDevCntSeed: 菊花链中 device 数量
    :return: 1. returned command message
             2. "message return RX error"
    """
    """ check bridge RX is empty """
    if max17841_clear_rx_buf(pHidDev) == False:
        return "message return RX error"

    ''' send message queue into transmit buffer '''
    max17841_buf_write(pHidDev, 0xC0, 3, [0x09, 0x00, pDevCntSeed])

    ''' start transmit from uart '''
    max17841_reg_command(pHidDev, 0xB0)

    ''' check message return back to bridge '''
    if max17841_check_msg_return_bridge(pHidDev) == False:
        if SCRIPT_DEBUG:
            print("pb01_path_down: check message return read R01 fail")
        return "message return RX error"

    ''' read return data '''
    return_data = max17841_buf_read(pHidDev, 0x93, 3)
    if return_data == "max17841 read buf error":
        if SCRIPT_DEBUG:
            print("pb01_path_down: check message return read rx buf fail")
        return "message return RX error"
    else:
        return return_data
