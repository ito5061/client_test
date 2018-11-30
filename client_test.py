# -*- coding: utf-8 -*-
# client_test.py

from socket import *
import time
import sys

import pbl2018


server_name = str(sys.argv[1])    #localhost
server_port = int(sys.argv[2])    #用意されているサーバーのポート番号：60623
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name,server_port))

file_name = str(sys.argv[3])
token_str = str(sys.argv[4])

getarg = pbl2018.genkey(token_str)


if __name__ == '__main__':
    # main program
    
    #SIZE実行
    send_str_SIZE = 'SIZE ' + file_name + '\n'

    client_socket.send(send_str_SIZE.encode())
    ans_SIZE = client_socket.recv(102400).decode()
    print(ans_SIZE)

    
    ans_datasize = int(ans_SIZE.split()[2])  #ファイルのサイズ
    
    #GET実行
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name,server_port))

    send_str_GET = 'GET ' + file_name +' '+ getarg + ' ALL\n'
    client_socket.send(send_str_GET.encode())
    
    
    recv_bytearray = bytearray()
    while True:
      b = client_socket.recv(1)
      recv_bytearray.append(b[0])
      if b== b'\n':
        ans_GET = recv_bytearray.decode()
        ans_GET_file = client_socket.recv(ans_datasize).decode()
        break
        
    print(ans_GET)
    
    f = open('GET_file.txt','w')
    f.write(ans_GET_file)
    f.close()
    

    ans_GET_time = int(ans_GET.split()[14][0:2]) * 3600 + int(ans_GET.split()[14][3:5]) * 60 + int(ans_GET.split()[14][6:8])  #1日トータル秒
    
    #print(ans_GET_time)
    
    
    #REP実行
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name,server_port))
    
    
    REP_key = pbl2018.repkey(token_str, 'GET_file.txt' )
    send_str_REP = 'REP ' + file_name + ' ' + REP_key + '\n'
    client_socket.send(send_str_REP.encode())
    
    ans_REP = client_socket.recv(102400).decode() 
    print(ans_REP)
    

    ans_REP_time = int(ans_REP.split()[11][0:2]) * 3600 + int(ans_REP.split()[11][3:5]) * 60 + int(ans_REP.split()[11][6:8]) #1日トータル秒
    
    #print(ans_REP_time)
    
    TIME = ans_REP_time - ans_GET_time
    
    TIME_h = TIME // 3600
    TIME_m = (TIME - TIME_h * 3600) // 60
    TIME_s = (TIME - TIME_h * 3600 - TIME_m * 60) 
    
    print('経過時間：' + str(TIME_h) + '時間' + str(TIME_m) + '分' + str(TIME_s) + '秒')
    
    
    
    client_socket.close()
    
    
