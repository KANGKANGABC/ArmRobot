#!/usr/bin/env python

#import vrep
import time
import socket
import sys

from pyxl320 import ServoSerial
from pyxl320 import Packet
from pyxl320 import DummySerial

port = '/dev/ttyUSB0'

serial = ServoSerial(port)  # use this if you want to talk to real servos
# serial = DummySerial(port)  # use this for simulation
serial.open()


ID = 254
angle = 150
pkt = Packet.makeServoPacket(ID, angle)  # move servo 1 to 158.6 degrees
err_no = serial.sendPkt(        pkt)  # send packet to servo
pkt = Packet.makeLEDPacket(ID,1)
err_no = serial.sendPkt(pkt)

HOST_IP = "192.168.2.123"
HOST_PORT = 8888
print("Starting socket: TCP...")
#1.create socket object:socket=socket.socket(family,type)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
host_addr = (HOST_IP, HOST_PORT)
#2.bind socket to addr:socket.bind(address)
socket_tcp.bind(host_addr)
#3.listen connection request:socket.listen(backlog)
socket_tcp.listen(1)
#4.waite for client:connection,address=socket.accept()
socket_con, (client_ip, client_port) = socket_tcp.accept()
print("Connection accepted from %s." %client_ip)
socket_con.send("Welcome to RPi TCP server!")
#5.handle
print("Receiving package...")
ID = 254
angle = 110
pkt = Packet.makeServoPacket(ID, angle)
err_no = serial.sendPkt(pkt)  # send packet to servo

while True:
    try:
        data=socket_con.recv(512)
        if len(data)>0:
            print("Received:%s"%data)
            command = data
            tmp = command.split()
            ID = int(tmp[0])
            angle = float(tmp[1])
            print ID
            print angle
            pkt = Packet.makeServoPacket(ID, angle)
            err_no = serial.sendPkt(pkt)  # send packet to servo

            if data=='1':
                time.sleep(1)
            elif data=='0':
                socket_tcp.close()
sys.exit(1)
            elif data=='action01':
                ID = 254
                angle = 110
                pkt = Packet.makeServoPacket(ID, angle)
                err_no = serial.sendPkt(pkt)  # send packet to servo
            elif data=='action02':
                ID = 254
                angle = 150
                pkt = Packet.makeServoPacket(ID, angle)
                err_no = serial.sendPkt(pkt)  # send packet to servo
            continue
    except Exception:
            socket_tcp.close()
            sys.exit(1)
time.sleep(2)
ID = 254
angle = 110
pkt = Packet.makeServoPacket(ID, angle)
err_no = serial.sendPkt(pkt)  # send packet to servo



#ID = 1

#vrep.simxFinish(-1)
#clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)#start connec
t

#if clientID!=-1:
#       print 'Connected to remote API server'
#       vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot_wait) #start 
simulation
#       res,m1Dyn = vrep.simxGetObjectHandle(clientID, "m1", vrep.simx_opmode_on
eshot_wait)
#       res,m2Dyn = vrep.simxGetObjectHandle(clientID, "m2", vrep.simx_opmode_on
eshot_wait)
#       res,m3Dyn = vrep.simxGetObjectHandle(clientID, "m3", vrep.simx_opmode_on
eshot_wait)
#       res,m4Dyn = vrep.simxGetObjectHandle(clientID, "m4", vrep.simx_opmode_on
eshot_wait)
#       res,m5Dyn = vrep.simxGetObjectHandle(clientID, "m5", vrep.simx_opmode_on
eshot_wait)
#
#
#       res,m1Position = vrep.simxGetJointPosition(clientID, m1Dyn, vrep.simx_op
mode_oneshot_wait)
#       res,m2Position = vrep.simxGetJointPosition(clientID, m2Dyn, vrep.simx_op
mode_oneshot_wait)
#       res,m3Position = vrep.simxGetJointPosition(clientID, m3Dyn, vrep.simx_op
mode_oneshot_wait)
#       res,m4Position = vrep.simxGetJointPosition(clientID, m4Dyn, vrep.simx_op
mode_oneshot_wait)
  #       res,m5Position = vrep.simxGetJointPosition(clientID, m5Dyn, vrep.simx_op
mode_oneshot_wait)
#       #print m1Position,m2Position,m3Position,m4Position,m5Position
#       while 1:
#               res,m1Position = vrep.simxGetJointPosition(clientID, m1Dyn, vrep
.simx_opmode_streaming)
#               res,m2Position = vrep.simxGetJointPosition(clientID, m2Dyn, vrep
.simx_opmode_streaming)
#               res,m3Position = vrep.simxGetJointPosition(clientID, m3Dyn, vrep
.simx_opmode_streaming)
#               res,m4Position = vrep.simxGetJointPosition(clientID, m4Dyn, vrep
.simx_opmode_streaming)
#               res,m5Position = vrep.simxGetJointPosition(clientID, m5Dyn, vrep
.simx_opmode_streaming)
#               angle1 = 150 + m1Position*180/3.14
#               angle2 = 150 + m2Position*180/3.14
#               angle3 = 150 + m3Position*180/3.14
#               angle4 = 150 - m4Position*180/3.14
#               angle5 = 150 + m5Position*180/3.14
#               ID = 1
#               pkt = Packet.makeServoPacket(ID, angle1)  # move servo 1 to 158.
6 degrees
#               err_no = serial.sendPkt(pkt)  # send packet to servo
#               ID = 2
#               pkt = Packet.makeServoPacket(ID, angle2)  # move servo 1 to 158.
6 degrees
#               err_no = serial.sendPkt(pkt)  # send packet to servo
#               ID = 3
#               pkt = Packet.makeServoPacket(ID, angle3)  # move servo 1 to 158.
6 degrees
#               err_no = serial.sendPkt(pkt)  # send packet to servo
#               ID = 4
#               pkt = Packet.makeServoPacket(ID, angle4)  # move servo 1 to 158.
6 degrees
#               err_no = serial.sendPkt(pkt)  # send packet to servo
#               ID = 5
#               pkt = Packet.makeServoPacket(ID, angle5)  # move servo 1 to 158.
6 degrees
#               err_no = serial.sendPkt(pkt)  # send packet to servo
#               time.sleep(0.1)
#
if err_no:
        print('Oops ... something went wrong!')






