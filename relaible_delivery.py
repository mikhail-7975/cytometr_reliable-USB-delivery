import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import time

import random

count = 0

porNameList = [i.device for i in serial.tools.list_ports.comports()]
print(porNameList)

port = serial.Serial(porNameList[0])


print(port.write_timeout)
port.write_timeout = 2
print(port.write_timeout)
while(1):

    data = []

    while len(data) < 1002:
        rrr = port.readable()
        if (rrr != True):
            print("not redable")
        wrr = port.writable()
        if (wrr != True):
            print("not writable")
        try:
            port.write(b"req")#<====================
        except serial.serialutil.SerialTimeoutException:
            print("time over")
        print("send request...")
        startTime = time.time()
        while not port.inWaiting():
            #print('.')
            if time.time() - startTime > 1:
                print("much time not in waiting")
                break

        i = 0
        inp = 0
        startTime = time.time()
        while(inp != 254):
            while port.inWaiting():
                #print(ord(port.read()), i)
                inp = ord(port.read())
                data.append(inp)
                #print("reading", i)
                i += 1
            if time.time() - startTime > 1:
                print("much time in trying to read")
                break
        '''
        testErrCode = 0#random.randint(0, 2)
        #print("err code ", testErrCode)
        if len(data) > 2:
            if(testErrCode == 1):
                i = random.randint(1, 500)
                data.pop(i)
                #print("loose ", i, "th value")
            elif(testErrCode == 2):
                data.clear()
                #print("loose all")
        #print(len(data), data)
        '''

        try:
            if data[0] == 255 and data[-1] == 254 and len(data) == 1002:
                break
            else:
                print("error", "start =", data[0] == 255, "stop =", data[-1] == 254, "len =", len(data))
                data = []
        except Exception:
            print(Exception)
            #a = 0

    port.write(b"ack")
    count += 1
    print(count, "FINAL", len(data), data)
    #plt.plot(data)
    #plt.show()
    #print(port)