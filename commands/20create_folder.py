import os
import sys
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

try:
    path = sys.argv[1]
    os.mkdir(path)
    print('success')
except Exception as e:
    print(f'{e} | already created')
