#!/usr/bin/env python

import vrep
import time
import sys
import serial
import serial.tools.list_ports
import struct
import pyHook
import pythoncom
import threading
import socket



global data1 #Global Variable:where used where declare
global data2 #Global Variable:where used where declare
motor_angle = [150.0,156.0,155.0,150.0,152.0,150.0]
data1 = [0,0]
data2 = 1
event_close = threading.Event()
event_mouse = threading.Event()

class RobotTest(threading.Thread):
    def _int_(self):
        threading.Thread.__init__(self)
    def run(self):
        global event_close
        while True:
            if event_close.isSet():  
                print"RobotTest Running!"
                
                time.sleep(1)  
            else:  
                print"RobotTest Stopped!" 
                break;
            
class Menu(threading.Thread):
    def _int_(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
                print "Welcome!Please Input Command!"
                print "1:ArmRobot Test"
                print "2:ArmRobot Motion In Path Mode"
                print "3:ArmRobot Motion In Mouse Mode"
                print "4:Exit"
                str = raw_input()
                if str == '1':
                    print "Test1"
                    event_close.clear()
                elif str == '2':
                    print "Test2"
                elif str == '3':
                    print "Test3"    
                elif str == '4':
                    event_close.clear()
                    break
                else:
                    print "Please Input again"
    
def OnMouseEvent(event):
    global event_close
    global data1,data2
    #print 'Position:',event.Position
    data1 = event.Position
    data2 = event.Wheel
    event_close.set()
    # 返回 True 可将事件传给其它处理程序，否则停止传播事件 
    return True

def fun1(event):
    global data1
    threadEvent = event
    for i in range(5):
        signal.set()
        print "fun1"
        time.sleep(1)
def fun2(event):
    global event_close
    while True:
        event_close.wait()
        print data1
        signal.clear()

def fun3():
    try:
        # 创建钩子管理对象 
        hm = pyHook.HookManager() 
        # 监听所有鼠标事件 
        hm.MouseAll = OnMouseEvent # 等效于hm.SubscribeMouseAll(OnMouseEvent) 
        # 开始监听鼠标事件 
        hm.HookMouse() 
        # 一直监听，直到手动退出程序 
        pythoncom.PumpMessages()
        pass

    except KeyboardInterrupt:
        print "Exit"
        pass

def TCPConnect( ):
    global motor_angle
    SERVER_IP = "192.168.31.21"
    SERVER_PORT = 8888
    print("Starting socket: TCP...")
    server_addr = (SERVER_IP, SERVER_PORT)
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
            try:
                    print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
                    socket_tcp.connect(server_addr)
                    break
            except Exception:
                    print("Can't connect to server,try it latter!")
                    time.sleep(1)
                    continue   
    while True:
        ID = '1'
        command = ID + ' ' + '%f'%motor_angle[0]
        socket_tcp.send(command)
        time.sleep(0.01)
        ID = '2'
        command = ID + ' ' + '%f'%motor_angle[1]
        socket_tcp.send(command)
        time.sleep(0.01)
        ID = '3'
        command = ID + ' ' + '%f'%motor_angle[2]
        socket_tcp.send(command)
        time.sleep(0.01)
        ID = '4'
        command = ID + ' ' + '%f'%motor_angle[3]
        socket_tcp.send(command)
        time.sleep(0.01)
        ID = '5'
        command = ID + ' ' + '%f'%motor_angle[4]
        socket_tcp.send(command)
        time.sleep(0.01)
        ID = '6'
        command = ID + ' ' + '%f'%motor_angle[5]
        socket_tcp.send(command)
        time.sleep(0.01)

        
threads = [] #Create Thread Array
signal = threading.Event()
t1 = threading.Thread(target = fun1,args=(signal,)) # Add Thread1
threads.append(t1)#Thread Append
t2 = threading.Thread(target = fun2,args=(signal,)) # Add Thread2
threads.append(t2)#Thread Append
t3 = threading.Thread(target = RobotTest) # Add Thread3
threads.append(t3)#Thread Append
t4 = threading.Thread(target = Menu) # Add Thread4
threads.append(t4)#Thread Append
t5 = threading.Thread(target = fun3) # Add Thread5
threads.append(t5)#Thread Append
t6 = threading.Thread(target = TCPConnect) # Add Thread6
threads.append(t6)#Thread Append

def Motion(ser,motor_angle,packet):
    val1 = int((motor_angle[0]/300)*1023)
    val2 = int((motor_angle[1]/300)*1023)
    val3 = int((motor_angle[2]/300)*1023)
    val4 = int((motor_angle[3]/300)*1023)
    val5 = int((motor_angle[4]/300)*1023)
    val6 = int((motor_angle[5]/300)*1023)      
            
    packet[2] = val1/255
    packet[3] = val1%255        
    packet[4] = val2/255
    packet[5] = val2%255
    packet[6] = val3/255
    packet[7] = val3%255
    packet[8] = val4/255
    packet[9] = val4%255
    packet[10] = val5/255
    packet[11] = val5%255
    packet[12] = val6/255
    packet[13] = val6%255
    #print packet[2],packet[3]
    command = bytearray(packet)
    ser.write(command)
    
if __name__ == '__main__':

 
    global data1
    motor_angle = [150.0,150.0,150.0,150.0,150.0,150.0]
    for t in threads:
        t.setDaemon(True) # True:Parent Finsh->Child Finish. False:Parent Finsh->Child Keep.
        #t.start()
        
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        print "The Serial port can't find!"
    else:
        plist_0 =list(plist[0])
        serialName = plist_0[0]
        ser = serial.Serial(serialName,1000000,timeout = 60)
        print "check which port was really used >",ser.name
        packet = [255,255,01,244,01,244,01,244,01,244,01,244,01,244] #Reset Robot!
        motor_angle = [150.0,150.0,150.0,150.0,150.0,150.0]
        Motion(ser,motor_angle,packet)     
        print "Serial Init Ok!"
        print "Arm Reset!"
        print "1:Set Mode 2:Path Mode 3:Mouse Mode"
        str = raw_input()

        if str == '1':
            print "Set Mode"
            while True:
                str = raw_input()
                if str == '1':
                    motor_angle = [150.0,156.0,155.0,150.0,152.0,150.0]
                    Motion(ser,motor_angle,packet)
                    
                elif str == '2':
                    motor_angle = [135.0,150.0,150.0,150.0,150.0,150.0]
                    Motion(ser,motor_angle,packet)

                elif str == '3':
                    motor_angle = [150.0,136.0,155.0,150.0,152.0,150.0]
                    Motion(ser,motor_angle,packet)
                    
                else:
                    print "Input again"
        elif str == '2':
            print "Path Mode"
            threads[5].start()
            angle1a = 150
            angle2a = 156
            angle3a = 155
            angle4a = 150
            angle5a = 152
            angle6a = 150
            global motor_angle
            Motion(ser,motor_angle,packet)
            vrep.simxFinish(-1)
            clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)#start connect
            if clientID!=-1:
                print 'Connected to remote API server'
                vrep.simxLoadScene(clientID,'poppy_ergo_jr01.ttt',1,vrep.simx_opmode_oneshot_wait)
                vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot_wait) #start simulation
                res,m1Dyn = vrep.simxGetObjectHandle(clientID, "m1", vrep.simx_opmode_oneshot_wait)
                res,m2Dyn = vrep.simxGetObjectHandle(clientID, "m2", vrep.simx_opmode_oneshot_wait)
                res,m3Dyn = vrep.simxGetObjectHandle(clientID, "m3", vrep.simx_opmode_oneshot_wait)
                res,m4Dyn = vrep.simxGetObjectHandle(clientID, "m4", vrep.simx_opmode_oneshot_wait)
                res,m5Dyn = vrep.simxGetObjectHandle(clientID, "m5", vrep.simx_opmode_oneshot_wait)
                res,m6Dyn = vrep.simxGetObjectHandle(clientID, "m6", vrep.simx_opmode_oneshot_wait)

                res,m1Position = vrep.simxGetJointPosition(clientID, m1Dyn, vrep.simx_opmode_oneshot_wait)
                res,m2Position = vrep.simxGetJointPosition(clientID, m2Dyn, vrep.simx_opmode_oneshot_wait)
                res,m3Position = vrep.simxGetJointPosition(clientID, m3Dyn, vrep.simx_opmode_oneshot_wait)
                res,m4Position = vrep.simxGetJointPosition(clientID, m4Dyn, vrep.simx_opmode_oneshot_wait)
                res,m5Position = vrep.simxGetJointPosition(clientID, m5Dyn, vrep.simx_opmode_oneshot_wait)
                res,m6Position = vrep.simxGetJointPosition(clientID, m6Dyn, vrep.simx_opmode_oneshot_wait)
                try:
                    while 1:
                        res,m1Position = vrep.simxGetJointPosition(clientID, m1Dyn, vrep.simx_opmode_streaming)
                        res,m2Position = vrep.simxGetJointPosition(clientID, m2Dyn, vrep.simx_opmode_streaming)
                        res,m3Position = vrep.simxGetJointPosition(clientID, m3Dyn, vrep.simx_opmode_streaming)
                        res,m4Position = vrep.simxGetJointPosition(clientID, m4Dyn, vrep.simx_opmode_streaming)
                        res,m5Position = vrep.simxGetJointPosition(clientID, m5Dyn, vrep.simx_opmode_streaming)
                        res,m6Position = vrep.simxGetJointPosition(clientID, m6Dyn, vrep.simx_opmode_streaming)
                        motor_angle[0] = angle1a + m1Position*180/3.14
                        motor_angle[1] = angle2a + m2Position*180*1/3.14
                        motor_angle[2] = angle3a + m3Position*180*1/3.14
                        motor_angle[3] = angle4a - m4Position*180/3.14
                        motor_angle[4] = angle5a + m5Position*180*1/3.14
                        motor_angle[5] = angle6a - m6Position*180*1/3.14
                        #print motor_angle
                        Motion(ser,motor_angle,packet)  
                        time.sleep(0.0001)
                    pass
                except KeyboardInterrupt:
                    ser.close()
                    print "Serial Closed"
                    pass
                    
            
        elif str == '3':
            print "Mouse Mode"
            threads[5].start()
            angle1a = 150
            angle2a = 156
            angle3a = 155
            angle4a = 150
            angle5a = 152
            angle6a = 150
            angle2_comp = 1.0
            angle3_comp = 1.0
            
            threads[4].start()
            motor_angle = [150.0,156.0,155.0,150.0,152.0,150.0]
            Motion(ser,motor_angle,packet)
            #
            vrep.simxFinish(-1)
            clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)#start connect
            if clientID!=-1:
                print 'Connected to remote API server'
                vrep.simxLoadScene(clientID,'poppy_ergo_jr02.ttt',1,vrep.simx_opmode_oneshot_wait)
                vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot_wait) #start simulation            
                res,target = vrep.simxGetObjectHandle(clientID, "target", vrep.simx_opmode_oneshot_wait)
                res,base = vrep.simxGetObjectHandle(clientID, "base", vrep.simx_opmode_oneshot_wait)
                res,targetPosition = vrep.simxGetObjectPosition(clientID, target,base, vrep.simx_opmode_streaming)
                print targetPosition
                targetPosition[0]= 0.1
                targetPosition[1]= -0.04
                targetPosition[2]= 0.04 
                res = vrep.simxSetObjectPosition(clientID, target,base,targetPosition,vrep.simx_opmode_streaming)
                res,m1Dyn = vrep.simxGetObjectHandle(clientID, "m1", vrep.simx_opmode_oneshot_wait)
                res,m2Dyn = vrep.simxGetObjectHandle(clientID, "m2", vrep.simx_opmode_oneshot_wait)
                res,m3Dyn = vrep.simxGetObjectHandle(clientID, "m3", vrep.simx_opmode_oneshot_wait)
                res,m4Dyn = vrep.simxGetObjectHandle(clientID, "m4", vrep.simx_opmode_oneshot_wait)
                res,m5Dyn = vrep.simxGetObjectHandle(clientID, "m5", vrep.simx_opmode_oneshot_wait)
                res,m6Dyn = vrep.simxGetObjectHandle(clientID, "m6", vrep.simx_opmode_oneshot_wait)

                res,m1Position = vrep.simxGetJointPosition(clientID, m1Dyn, vrep.simx_opmode_oneshot_wait)
                res,m2Position = vrep.simxGetJointPosition(clientID, m2Dyn, vrep.simx_opmode_oneshot_wait)
                res,m3Position = vrep.simxGetJointPosition(clientID, m3Dyn, vrep.simx_opmode_oneshot_wait)
                res,m4Position = vrep.simxGetJointPosition(clientID, m4Dyn, vrep.simx_opmode_oneshot_wait)
                res,m5Position = vrep.simxGetJointPosition(clientID, m5Dyn, vrep.simx_opmode_oneshot_wait)
                res,m6Position = vrep.simxGetJointPosition(clientID, m6Dyn, vrep.simx_opmode_oneshot_wait)
                try:
                    while 1:
                        res,m1Position = vrep.simxGetJointPosition(clientID, m1Dyn, vrep.simx_opmode_streaming)
                        res,m2Position = vrep.simxGetJointPosition(clientID, m2Dyn, vrep.simx_opmode_streaming)
                        res,m3Position = vrep.simxGetJointPosition(clientID, m3Dyn, vrep.simx_opmode_streaming)
                        res,m4Position = vrep.simxGetJointPosition(clientID, m4Dyn, vrep.simx_opmode_streaming)
                        res,m5Position = vrep.simxGetJointPosition(clientID, m5Dyn, vrep.simx_opmode_streaming)
                        res,m6Position = vrep.simxGetJointPosition(clientID, m6Dyn, vrep.simx_opmode_streaming)
                        angle2_comp = 0.95 - data1[1]*0.1/768 - abs(683-abs(data1[0] - 683))*0.08/683
                        angle3_comp = 0.95 - data1[1]*0.1/768 - abs(683-abs(data1[0] - 683))*0.08/683
                        motor_angle[0] = angle1a + m1Position*180/3.14
                        motor_angle[1] = angle2a + m2Position*180*angle2_comp/3.14
                        motor_angle[2] = angle3a + m3Position*180*angle3_comp/3.14
                        motor_angle[3] = angle4a - m4Position*180/3.14
                        motor_angle[4] = angle5a + m5Position*180*1/3.14
                        motor_angle[5] = angle6a - m6Position*180*1/3.14
                        print motor_angle
                        Motion(ser,motor_angle,packet)  
                        print data1[0],data1[1]
                        print "Wheel"
                        print data2
                        if data2 == -1:
                            targetPosition[2] = 0.04
                        elif data2 == 0:
                            print " "
                        else:
                            targetPosition[2] = 0.1
                            
                        targetPosition[0]= -0.1 + data1[0]/6800.0
                        targetPosition[1]= -0.04 - data1[1]/6800.0
                        
                        res = vrep.simxSetObjectPosition(clientID, target,base,targetPosition,vrep.simx_opmode_streaming)
                        #res,targetPosition = vrep.simxGetObjectPosition(clientID, target,base, vrep.simx_opmode_streaming)
                        print targetPosition
                        time.sleep(0.05)
                    pass
                except KeyboardInterrupt:
                    ser.close()
                    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
                    vrep.simxFinish(clientID)
                    print "Simulation Finish"
                    print "Serial Closed"
                    pass                    
        else:
            print "Input Error"
    
    threads[3].start()
    threads[3].join() #Wait for Child Thread
    print "all over!"
    ser.close()
    print "Serial Closed"
