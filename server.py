#!/usr/bin/python3
import socket
import threading
import os.path
from os import path
from os import getcwd
import time

serverPort = 1700
filePort = 1800

# Creates TCP welcoming and file transfer socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fileSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serverSocket.bind(("", serverPort))
except:
    print("***** FTPServerUsingTCP: error: Port 1700 is not available, quitting...")
    exit(0)

try:
    fileSocket.bind(("", filePort))
except:
    print("***** FTPServerUsingTCP: error: Port 1800 is not available, quitting...")
    exit(0)

# Server begins listening for incoming TCP requests
serverSocket.listen(1)
print("The FTP Server running over TCP is listening on port %d ..." % serverPort)
fileSocket.listen(1)
print("The FTP Server running over TCP is listening on port %d ... \n" % filePort)

while 1:
    # Waits for incoming requests; new socket created on return
    connectionSocket, addr = serverSocket.accept()
    print("Connection established for client (IP, port) = %s" % str(addr))

    # Reads the filename from socket sent by the client.
    file_name = connectionSocket.recv(255)
    file_name = file_name.decode("utf-8").strip()
    file_name = getcwd() + "/" + file_name

    # Opens the desired file.
    # If success to open, send "yes" to the client, and closes the TCP control connection;
    #     otherwise, send "no" to the client, closes the TCP control connection, and continue to the next loop
    try:
        file_handler = open(file_name, 'rb')
    except:
        connectionSocket.send(b"no")
        print(
            "***** Server log: file %s is not found, sent no to the client.\n" % file_name)
        connectionSocket.close()
        print("Connection to (IP, addr) = %s closed." % str(addr))
        continue
    connectionSocket.send(b"yes")
    connectionSocket.close()
    print("Connection to (IP, addr) = %s closed." % str(addr))

    # accepts the new file transfer connection
    transferSocket, addr = fileSocket.accept()
    print("File Transfer connection established for client (IP, port) = %s" % str(addr))

    # Reads the content of the file
    file_content = file_handler.read()

    # Tries to send the file to the client using the TCP file transfer connection.
    #   On success, prints the success informtion on the screen;
    #       otherwise, prints the FAILURE information on the screen.
    try:
        transferSocket.send(file_content)
        file_handler.close()
        print("file \"%s\" sent successfully!" % file_name)
    except:
        print("***** Server log: file \"%s\" sent FAILED!!!" % file_name)

    # Closes the TCP file transfer connection.
    transferSocket.close()
    print("Connection to (IP, addr) = %s closed.\n" % str(addr))
