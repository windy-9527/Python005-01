import time
import logging
from pathlib import Path


def call_log():
    print("This is my first week's homework.")
    #文件路径设置
    filepath = 'E:/var/log/python-{}/'.format(time.strftime('%Y%m%d',time.localtime()))
    #创建文件目录
    Path(filepath).mkdir(parents = True , exist_ok = True)
    #日志格式配置
    logging.basicConfig(
                        filename = filepath + 'call.log' ,
                        level = logging.INFO ,
                        datefmt="%Y-%m-%d %H:%M:%S" ,
                        format = '%(asctime)s %(message)s'
                        )
    logging.info('is when this function was called')
    
if __name__ == '__main__':
    call_log()



