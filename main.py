import serial
import time
import signal
import threading
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from PMS7003 import PMS7003

dust = PMS7003()

# Baud Rate
Speed = 9600

# UART / USB Serial
USB0 = '/dev/ttyUSB0'
UART = '/dev/tty.usbserial-14320'

exitThread = False   # 쓰레드 종료용 변수



#쓰레드 종료용 시그널 함수
def handler(signum, frame):
     exitThread = True

#본 쓰레드
def readThread(ser):
    global exitThread

    # 쓰레드 종료될때까지 계속 돌림
    while not exitThread:
        buffer = ser.read(1024)

        if (dust.protocol_chk(buffer)):
            data = dust.unpack_data(buffer)

            print("PMS 7003 dust data")
            print("PM 1.0 : %s" % (data[dust.DUST_PM1_0_ATM]))
            print("PM 2.5 : %s" % (data[dust.DUST_PM2_5_ATM]))
            print("PM 10.0 : %s" % (data[dust.DUST_PM10_0_ATM]))

        else:
            print("data read Err")

if __name__ == "__main__":
    #종료 시그널 등록
    signal.signal(signal.SIGINT, handler)

    # USE PORT
    SERIAL_PORT = UART

    # serial setting
    ser = serial.Serial(SERIAL_PORT, Speed, timeout=1)

    #시리얼 읽을 쓰레드 생성
    thread = threading.Thread(target=readThread, args=(ser,))

    #시작!
    thread.start()

# import serial
#
# PORT = '/dev/tty.usbserial-14320'
# baudrate = 9600
# device = serial.Serial(PORT, baudrate=baudrate)
# print(device.name)
# y = device.readline()
# print(y.decode(encoding='cp949'))
#
