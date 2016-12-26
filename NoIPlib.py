import socket
import hashlib
import time
from datetime import datetime

#Tools for creating hash
class tools(object):
    @staticmethod
    def getPort(time):
        return 45286 + time.weekday()

    @staticmethod
    def getFirstHashRaw(messageMask):
        #Create original protected digdest
        messageHash = hashlib.sha256(("Hello, home" + messageMask).encode(encoding='utf_8')).hexdigest()
        for i in range(255):
            messageHash = hashlib.sha256(messageHash.encode(encoding='utf_8')).hexdigest()
        return messageHash

    @staticmethod
    def getFirstHash(time, serverIP):
        messageMask = str(time.year) + " " + str(time.month) + " " + str(time.day) + " " + str(serverIP) + " " + str(tools.getPort(time))
        return tools.getFirstHashRaw(messageMask)

    @staticmethod
    def getSecondHashRaw(messageMask):
        sendHash = hashlib.sha256(("I`m here" + messageMask).encode(encoding='utf_8')).hexdigest()
        for i in range(255):
            sendHash = hashlib.sha256(sendHash.encode(encoding='utf_8')).hexdigest()
        return sendHash

    @staticmethod
    def getSecondHash(time, serverIP):
        serverPort = 45286 + time.weekday()
        messageMask = str(time.year) + " " + str(time.month) + " " + str(time.day) + " " + str(serverIP) + " " + str(tools.getPort(time))
        return tools.getSecondHashRaw(messageMask)
    
    #Return List of IP address, mask xx.xx.xx (e.x. 127.0.0)
    @staticmethod
    def gatherIP(fileName = "IPs.txt", incAddr = 0, decAddr = 0):
        f = open(fileName)
        data = f.read().splitlines()
        data.reverse()
        f.close()
        newData = []
        for ip in data:
            a,b,c,d = ip.split('.')
            a = int(a)
            b = int(b)
            #Localhost
            if (a == 192) and (b == 168):
                pass
            else:
                c = int(c)
                d = int(d)
                #Mask sometimes equal 23, not 24
                newData.append((a, b, c))
                newData.append((a, b, c + incAddr))
                newData.append((a, b, c - decAddr))
        #Delete twice values
        newData = list(set(newData))
        newData = dict(zip(newData, newData)).values()
        data = []
        #Convert to List
        for i in newData:
            data.append(i)
        return data

class server(object):
    currentTime = None
    serverPort = 0
    messageHash = None
    sendHash = None
    serverIP = None

    #update time and date. Every day hash changes
    @staticmethod
    def timeRefresh():
        server.currentTime = datetime.now()

    #Update ports
    @staticmethod
    def portRefresh():
        server.timeRefresh()
        server.serverPort = tools.getPort(server.currentTime)

    #Update IP
    @staticmethod
    def IPRefresh():
        server.serverIP = socket.gethostbyname(socket.gethostname())

    #Update hash
    @staticmethod
    def hashRefresh():
        server.portRefresh()
        server.IPRefresh()
        server.messageHash = tools.getFirstHash(server.currentTime, server.serverIP)
        server.sendHash = tools.getSecondHash(server.currentTime, server.serverIP)
