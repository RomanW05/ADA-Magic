import os
import sys
from os.path import exists
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)




path = sys.argv[1]

try:
    if exists(f'{path}'):
        pass
    else:
        os.mkdir(f'{path}')
except:
    pass