# Markem-imaje AD 2023
# Jakub  Wojcik
# FTDI FT232H tests

import usb
import usb.util
import os
import time
import logging
import numpy as np
import binascii
import crcmod
import at_repo
# Setting environment variable, if you will now, check will fail
os.environ["BLINKA_FT232H"] = "1"
import board
import digitalio


def ftdi_test():
    # Try device availability
    dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    print(dev)
    if os.environ["BLINKA_FT232H"] == "1":
        print("Environment variable set correctly")
        # module "board" can be imported only when environmental variable is set to TRUE
        import board
        import digitalio
        dir(board)
        return True
    else:
        print("Environment variable NOT SET !!!")

    return False


def format_response(arr):
    res = str(binascii.hexlify(arr), 'ascii')
    form_response = ':'.join(res[i:i + 2] for i in range(0, len(res), 2))
    return form_response


if __name__ == '__main__':

    # check if board is available
    if ftdi_test():
        # time.sleep(1.0)

        # led0 = digitalio.DigitalInOut(board.C0)
        # led0.direction = digitalio.Direction.OUTPUT
        #
        # led1 = digitalio.DigitalInOut(board.C1)
        # led1.direction = digitalio.Direction.OUTPUT
        #
        # led0.value = False
        # led1.value = False
        # time.sleep(1)
        #
        # led0.value = True
        # led1.value = False
        # time.sleep(1)
        #
        # led0.value = False
        # led1.value = True
        # time.sleep(1)
        #
        # led0.value = False
        # led1.value = False

        i2c = board.I2C()
        send_buf = []

        #   Create empty array. Size of array determent the area to read
        #   shape= describes dimention of the array, in our case flat single row
        #   dtype= describes type of data, i=integer, b=byte
        read_buf = np.empty(shape=32, dtype='b')

        try:
            #   ping the board and test, long zero over Twlo time wakes the device up
            i2c.readfrom_into(0, read_buf)
        except Exception as e:
            pass

        i2c.readfrom_into(100, read_buf)  # ping the board and test
        response = str(binascii.hexlify(read_buf), 'ascii')
        formatted_response = ':'.join(response[i:i+2] for i in range(0, len(response), 2))

        # Check if device is ready to transfer
        if response[0:8] == '04113343':
            print("Device present")

        #   read device revision
        # read_buf = np.empty(shape=8, dtype='b')
        # #           cmd   cnt   opc    p1   p2_a  p2_b  Dat    tr
        # read_buf = [0x77, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00, 0x88]

        #             cmd   cnt   opc    p1   p2_a  p2_b
        # read_buf = [0x77, 0x01, 0x30, 0x00, 0x00, 0x00]
        # read_buf = b'\x77\x01\x30\x00\x00\x00\x00\x00'

        del (read_buf)

        # read_cmd[0] = 0x03; / *Command
        # byte * /
        # read_cmd[1] = 0x07; / *length * /
        # read_cmd[2] = 0x02; / *Read
        # command
        # opcode * /
        # read_cmd[3] = param1;
        # read_cmd[4] = cpu_to_le16(addr) & 0xFF;
        # read_cmd[5] = cpu_to_le16(addr) >> 8;
        #
        # crc = atsha204_crc16( & read_cmd[1], 5);
        #
        #
        # read_cmd[6] = cpu_to_le16(crc) & 0xFF;
        # read_cmd[7] = cpu_to_le16(crc) >> 8;

        #   https://github.com/cryptotronix/atsha204-i2c/blob/master/atsha204-i2c.c#L326

        read_buf = bytearray([0x03,     # [0] Command byte
                              0x07,     # [1] Count
                              0x02,     # [2] Read command opcode
                              0x80,     # [3] papram 1 low
                              0x00,     # [4] papram 2 high
                              0x00,     # [5] papram 2
                              0x00,     # [6] CRC16[0x8005] low
                              0x00,     # [7] CRC16[0x8005] high
                              ])

        crc16 = crcmod.mkCrcFun(0x18005, 0xFFFF, True)
        read_buf[6] = crc16(read_buf[1:5])[0]
        read_buf[7] = crc16(read_buf[1:5])[1]

        print(read_buf)
        i2c.readfrom_into(100, read_buf)  # ping the board and test
        print(format_response(read_buf))
