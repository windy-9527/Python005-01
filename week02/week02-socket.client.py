#!/usr/bin/env python
import socket
import os
import struct
import time
import logging
from pathlib import Path

HOST = 'localhost'
PORT = 11000


def echo_client():
    ''' Echo Server的 Client端 '''
    # 操作日志
    log_path = './{}/'.format(time.strftime('%Y%m%d', time.localtime()))
    Path(log_path).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_path + 'Client.log',
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format='%(asctime)s %(message)s'
    )
    try:
        # AF_INET为IPv4   STREAM为TCP协议
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        logging.info('Client connection successful.')
        print('Client connection successful.')
    except Exception as e:
        logging.error('Client connection failure.')
        print('Client connection failure.')
    while True:
        # 接收文件路径
        file_path = input('Input file path:')
        # 设定退出条件
        if file_path == 'exit':
            break
        # 发送文件到服务端
        if os.path.exists(file_path):
            file_info = struct.calcsize('128sl')
            filehead = struct.pack(
                '128sl',
                bytes(
                    os.path.basename(file_path).encode()),
                os.stat(file_path).st_size)
            # 发送文件信息到服务端
            s.send(filehead)
            # 以二进制方式打开文件
            file = open(file_path, 'rb')
            while True:
                data = file.read(1024)
                if not data:
                    break
                s.send(data)
            logging.info('The file was sended.')
            print('The file was sended.')
        else:
            print('The file does not exist.')
        # 接收服务端返回数据
        while True:
            data = s.recv(1024)
            if not data:
                break
            else:
                print(data.decode('gbk'))
    s.close()


if __name__ == '__main__':
    echo_client()
