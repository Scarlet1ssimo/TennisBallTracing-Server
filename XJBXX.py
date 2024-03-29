import socket
import struct
import json

dataBuffer=bytes()
headerSize=12
bias = 0

def RECV(conn):
    global dataBuffer
    global headerSize
    #print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if data:
            dataBuffer += data
            while True:
                if len(dataBuffer) < headerSize:
                    break
                headPack = struct.unpack('!3I', dataBuffer[:headerSize])
                bodySize = headPack[1]
                if len(dataBuffer) < headerSize+bodySize:
                    break
                body = dataBuffer[headerSize:headerSize+bodySize]
                dataBuffer = dataBuffer[headerSize + bodySize:]
                jdata = json.loads(body)[0]
                diff = -jdata['time']+time.time()+bias
                print(diff, len(dataBuffer))
                if diff > 0.07:
                    # tmpdata = conn.recv(1)
                    dataBuffer = bytes()
                    print('clear')
                return headPack, body
        else:
            dataBuffer=bytes()
            return 0,dataBuffer

def SEND(client, body):
    ver = 1
    #body = json.dumps(dict(hello="world"))
    #print(body)
    cmd = 101
    header = [ver, body.__len__(), cmd]
    headPack = struct.pack("!3I", *header)
    sendData = headPack + body.encode()
    client.sendall(sendData)


def SENDI(client, body):
    ver = 2
    #body = json.dumps(dict(hello="world"))
    #print(body)
    cmd = 101
    header = [ver, body.__len__(), cmd]
    headPack = struct.pack("!3I", *header)
    client.sendall(headPack)
    client.sendall(body)

