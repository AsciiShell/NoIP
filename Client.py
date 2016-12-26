#!python3
import socket
import re
import datetime
from NoIPlib import *
import threading
from queue import Queue
import time

# lock to serialize console output
lock = threading.Lock()
homes = []

def do_work(targerIP):
	with lock:
		try:
			print(threading.current_thread().name,targerIP)
			time = datetime.now()
			port = tools.getPort(time)
			fhash = tools.getFirstHash(time, targerIP)
			shash = tools.getSecondHash(time, targerIP)
			myIP = socket.gethostbyname(socket.gethostname())

			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			
			sock.sendto(bytes(fhash, "utf-8"), (targerIP, port))
			sock.settimeout(0.3)

			data, addr = sock.recvfrom(512)
			if data.decode("utf-8") == shash:
				print("Home found: ", addr)
				homes.append(addr)
		except:
			pass

# The worker thread pulls an item from the queue and processes it
def worker():
	while True:
		item = q.get()
		do_work(item)
		q.task_done()

# Create the queue and thread pool.
q = Queue()

tasks = tools.gatherIP()
for i in range(20):
	t = threading.Thread(target=worker)
	t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
	t.start()

# stuff work items on the queue (in this case, just a number).
start = time.perf_counter()
#tasks[0] = (192,168,43)
total = 0
for item in tasks:
	for i in range(256):
		q.put(str(item[0]) + "." + str(item[1]) + "." + str(item[2]) + "." + str(i))
		total += 1

print("Total", total, "tasks")
q.join()       # block until all tasks are done

print("Done")
print('time:',time.perf_counter() - start)
for i in homes:
	print(i)
