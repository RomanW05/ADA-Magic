import os
import sys
import subprocess
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

try:
    path = sys.argv[1]
    result = os.listdir(path)
    print(f'key666word{len(result)}key666word')
except:
    logging.exception('Got exception on main handler')
    raise