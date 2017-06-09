import mmap
import time 
import socket
import sys

HOST_IP = "192.168.31.21"
HOST_PORT = 8888

print(" I'm ArmRobot with Zybo SERVER_IP:%s PORT:%d" %(HOST_IP,HOST_PORT))

angle1_H = 2
angle1_L = 1
angle2_H = 2
angle2_L = 1
angle3_H = 2
angle3_L = 1
angle4_H = 2
angle4_L = 1
angle5_H = 2
angle5_L = 1
angle6_H = 2
angle6_L = 1

with open('/dev/uio0','r+b') as f:
		map = mmap.mmap(f.fileno(),4096)
		map.write_byte('A')
		map.write_byte('1')
		map.write_byte('1')
		map.write_byte('1')
		map.write_byte('1')
		map.write_byte('1')
		map.write_byte(chr(angle1_L))
		map.write_byte(chr(angle1_H))


		map.write_byte('2')
		map.write_byte('2')
		map.write_byte(chr(angle2_L))
		map.write_byte(chr(angle2_H))

		map.write_byte('2')
		map.write_byte('2')
		map.write_byte(chr(angle3_L))
		map.write_byte(chr(angle3_H))
		
		map.write_byte('2')
		map.write_byte('2')
		map.write_byte(chr(angle4_L))
		map.write_byte(chr(angle4_H))

		map.write_byte('2')
		map.write_byte('2')
		map.write_byte(chr(angle5_L))
		map.write_byte(chr(angle5_H))

		map.write_byte('2')
		map.write_byte('2')       
		map.write_byte(chr(angle6_L))
		map.write_byte(chr(angle6_H))

		map.write_byte(chr(2))
		map.write_byte(chr(1))
		map.write_byte(chr(1))
		map.write_byte(chr(1))

		map.seek(0)
		print map.readline()
		print map.size()
f.close()

print "ArmRobot Init OK!"
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







while True:
	try:
		data=socket_con.recv(512)
		if len(data)>0:
			#print("Received:%s"%data)
			command = data
			tmp = command.split()
			ID = int(tmp[0])
			angle = float(tmp[1])
			print ID
			print angle
			if ID == 1:
				angle1_L = int(angle*1023/300)%256;
				angle1_H = int(angle*1023/300)/256;
			elif ID == 2:
				angle2_L = int(angle*1023/300)%256;
				angle2_H = int(angle*1023/300)/256;
			elif ID == 3:
				angle3_L = int(angle*1023/300)%256;
				angle3_H = int(angle*1023/300)/256;
			elif ID == 4:
				angle4_L = int(angle*1023/300)%256;
				angle4_H = int(angle*1023/300)/256;
			elif ID == 5:
				angle5_L = int(angle*1023/300)%256;
				angle5_H = int(angle*1023/300)/256;
			elif ID == 6:
				angle6_L = int(angle*1023/300)%256;
				angle6_H = int(angle*1023/300)/256;


			if data=='1':
				time.sleep(0.01)
			elif data=='0':
				print "what!"
				#socket_tcp.close()

			elif data=='action01':
				ID = 254
				angle = 110
				angle1_L = 1
				angle1_H = 2
				angle2_L = 1
				angle2_H = 2
				print "action01"
		
			elif data=='action02':
				ID = 254
				angle = 150
				angle1_L = 1
				angle1_H = 3
				angle2_L = 1
				angle2_H = 3
	    
			with open('/dev/uio0','r+b') as f:
				map = mmap.mmap(f.fileno(),4096)
				map.write_byte('A')
				map.write_byte('1')
				map.write_byte('1')
				map.write_byte('1')
				map.write_byte('1')
				map.write_byte('1')
				map.write_byte(chr(angle1_L))
				map.write_byte(chr(angle1_H))


				map.write_byte('2')
				map.write_byte('2')
				map.write_byte(chr(angle2_L))
				map.write_byte(chr(angle2_H))
				print angle2_L,angle2_H

				map.write_byte('2')
				map.write_byte('2')
				map.write_byte(chr(angle3_L))
				map.write_byte(chr(angle3_H))

				map.write_byte('2')
				map.write_byte('2')
				map.write_byte(chr(angle4_L))
				map.write_byte(chr(angle4_H))

				map.write_byte('2')
				map.write_byte('2')
				map.write_byte(chr(angle5_L))
				map.write_byte(chr(angle5_H))

				map.write_byte('2')
				map.write_byte('2')       
				map.write_byte(chr(angle6_L))
				map.write_byte(chr(angle6_H))

				map.write_byte(chr(2))
				map.write_byte(chr(1))
				map.write_byte(chr(1))
				map.write_byte(chr(1))

				map.seek(0)
				#print map.readline()
				#print map.size()
			f.close()

	    
		continue
		socket_tcp.close()
		sys.exit(1)
		
	except Exception:
			socket_tcp.close()
			sys.exit(1)



with open('/dev/uio0','r+b') as f:
		map = mmap.mmap(f.fileno(),4096)
		map.write_byte('A')
		map.write_byte('1')
		map.write_byte('1')
		map.write_byte('1')
		map.write_byte('1')
		map.write_byte('1')
		map.write_byte(chr(angle1_L))
		map.write_byte(chr(angle1_H))


		map.write_byte('2')
		map.write_byte('2')
		map.write_byte(chr(angle2_L))
		map.write_byte(chr(angle2_H))

		map.write_byte('2')
		map.write_byte('2')
		map.write_byte(chr(angle3_L))
		map.write_byte(chr(angle3_H))
		
		map.write_byte('2')
		map.write_byte('2')
		map.write_byte(chr(angle4_L))
		map.write_byte(chr(angle4_H))

		map.write_byte('2')
		map.write_byte('2')
		map.write_byte(chr(angle5_L))
		map.write_byte(chr(angle5_H))

		map.write_byte('2')
		map.write_byte('2')       
		map.write_byte(chr(angle6_L))
		map.write_byte(chr(angle6_H))

		map.write_byte(chr(2))
		map.write_byte(chr(1))
		map.write_byte(chr(1))
		map.write_byte(chr(1))

		map.seek(0)
		print map.readline()
		print map.size()
f.close()


