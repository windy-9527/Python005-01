#!/usr/bin/env python
import socket
import struct
import os
import time
import logging
from pathlib import Path

HOST = 'localhost'
PORT = 11000


def echo_server():
    ''' Echo Server 的 Server 端 '''
    log_path = './{}/'.format(time.strftime('%Y%m%d', time.localtime()))
    Path(log_path).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_path + 'Server.log',
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format='%(asctime)s %(message)s'
    )
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 对象s绑定到指定的主机和端口上
    s.bind((HOST, PORT))
    # 只接收1个连接
    s.listen(1)

    while True:
        # accept表示接收客户端的连接
        conn, addr = s.accept()
        # 输出客户端地址
        print(f'Connected by {addr}')
        # logging.INFO('Connected by {}'.format(addr))
        while True:
            # 定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，此为文件大小
            file_info = struct.calcsize('128sl')
            buf = conn.recv(file_info)
            if buf:
                file_name, file_size = struct.unpack('128sl', buf)
                # strip方法用于删除字符串头部和尾部指定的字符，默认字符为所有空字符，包括空格、换行(\n)、制表符(\t)等。
                file_name = file_name.decode().strip('\00')
                new_filename = os.path.join('./', 'new_' + file_name)
                print(
                    'The new file name is {}, file size is {}'.format(
                        new_filename, file_size))
                file = open(new_filename, 'wb')
                print('Start receiving...')
                logging.info('Start receiving...')
                # 初始化已接收文件大小
                received_size = 0
                while not received_size == file_size:
                    if file_size > (received_size + received_size):
                        data = conn.recv(1024)
                        received_size += len(data)
                    else:
                        data = conn.recv(file_size - received_size)
                        received_size = file_size
                    file.write(data)
                file.close()
                conn.send('The file was received'.encode())
                print('End receive...')
                logging.info('End receive...')
        conn.close()
        break
    s.close()


if __name__ == '__main__':
    echo_server()
