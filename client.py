#!/usr/bin/python3
import socket
import threading
import os.path
from os import path
import time

localhost = '127.0.0.1'
control_port = 1700
transfer_port = 1800


def start_transfer():
    # create TCP transfer socket on client to use for connecting to remote
    # server. Indicate the server's remote listening port
    clientSocket_transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # open the TCP transfer connection
    clientSocket_transfer.connect((localhost, transfer_port))

    # connection prompt
    print("TCP transfer connected. | Server: %s, Port: %d" %
          (localhost, transfer_port))

    # get the data back from the server
    filedata = clientSocket_transfer.recv(5000)

    # creat a file named "filename" and ready to write binary data to the file
    filehandler = open(filename, 'wb')

    # write the data to the file
    filehandler.write(filedata)

    # close the file
    filehandler.close()

    # close the TCP transfer connection
    return clientSocket_transfer.close()


# create TCP socket on client to use for connecting to remote
# server. Indicate the server's remote listening port
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# open the TCP control connection
clientSocket.connect((localhost, control_port))

# connection prompt
print("TCP transfer connected. | Server: %s, Port: %d" %
      (localhost, control_port))

# input the file name client wants
filename = input("Input file name: ")

# check if file exists in current directory
if path.exists(filename):
    print("File already exists on local machine. Proceeding to open...")
    time.sleep(2)
    # write code to open file

# send the file name to the server
clientSocket.send(bytes(filename, "utf-8"))

# get the status of the file from server: "yes" or "No"
filestatus = clientSocket.recv(1024).decode("utf-8").strip()

# check whether the file is on the server. If yes, receive the file.
# If no, do give a prompt
if filestatus == "yes":
    # download prompt
    print("Start downloading..")

    # start using TCP transfer
    start_transfer()

    # success prompt
    print("Done!")
else:
    # cannot find the file on the server
    print("No such file found on the server!")

# close the TCP control connection
clientSocket.close()
