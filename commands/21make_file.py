import os
import sys
import subprocess
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

try:
    path = sys.argv[1]
    total_nfts = sys.argv[2]
    query = 'echo "' + total_nfts +  '" > ' + path
    subprocess.check_output(query,shell=True)
except:
    logging.exception('Got exception on main handler')
    raise