import socket
import re
import time
from NoIPlib import *
while True:
	try:
		server.hashRefresh()
		#Count of answers
		DGR_Count = 3

		while 1:
			if server.currentTime.day != datetime.now().day:
				server.hashRefresh()
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sock.bind((server.serverIP, server.serverPort))
				data, addr = sock.recvfrom(512)
				if data.decode("utf-8")  == server.messageHash:
					print("FOUNT IT! ",addr)
					for i in range(DGR_Count):
						time.sleep(0.05)
						sock.sendto(server.sendHash.encode('utf-8'), addr)
				sock.close()
			except:
				time.sleep(0.1)
				print("Fatal exception")
	except:
		time.sleep(0.1)
		print("Critical exception")
