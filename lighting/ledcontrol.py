#!/usr/bin/python
import serial
import time
import array
from ola.ClientWrapper import ClientWrapper

usepuck = 0
iso2enable = 0

def DmxSent(state):
  wrapper.Stop()

while True:
    intensity = int(raw_input('Enter Light Level: '))
    cct       = int(raw_input('Enter Color temp level: '))
   
    universe = 1
    data      = array.array('B') 
    data.append(intensity)
    data.append(cct)
    data.append(intensity)
    data.append(cct)
    wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(universe, data, DmxSent)
    wrapper.Run()
    time.sleep(2)
    baud = 115200
    if usepuck:
        iso1 = serial.Serial('/dev/ttyUSB1',baud) #puck1

        iso1.write('GRL<LF>\r')
        time.sleep(1)
        msg10 = iso1.readline()#.split(' ')[1].lstrip('0')
    
        iso1.write('GRCCT<LF>\r')
        time.sleep(1)
        msg11 = iso1.readline()#.split(' ')[1].lstrip('0') 

        print '\n'
        print 'Right puck \n'   
        print msg10 , msg11
	iso1.close()

    if iso2enable:
        iso2 = serial.Serial('/dev/ttyUSB2',baud) #puck2
        iso2.write('GRL<LF>\r')
        time.sleep(1)
        msg20 = iso2.readline()#.split(' ')[1].lstrip('0') 

        iso2.write('GRCCT<LF>\r')
        time.sleep(1)
        msg21 = iso2.readline()#.split(' ')[1].lstrip('0') 

        iso2.write('GRCCT<LF>\r')
        time.sleep(1)
        msg21 = iso2.readline()#.split(' ')[1].lstrip('0') 

        print '\n'
        print 'Left puck \n'
        print msg20 , msg21
        iso2.close()


    reset = raw_input('reset? (y/n) ') 
    if reset == 'y':
        continue
    else:
        universe = 1
        data      = array.array('B') 
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(0)
        wrapper = ClientWrapper()
        client = wrapper.Client()
        client.SendDmx(universe, data, DmxSent)
        wrapper.Run()
       
        break
