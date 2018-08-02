import serial
import time


delay = int(raw_input('delay between measurments: '))

baud = 115200

portR = '/dev/ttyUSB3'



puck1 = serial.Serial(portR, baud)

while True:
    puck1.write('GRCCT<LF>\r')
    time.sleep(delay)
    msg1 = puck1.readline()
    print msg1.split(' ')[1].lstrip('0').rstrip('\n')
