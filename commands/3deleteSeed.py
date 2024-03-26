import os
import sys
from os.path import exists
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

homePath = '/home/yop/Downloads/cardano-node1.30.0/'

try:
    user = sys.argv[1]
    os.remove(homePath + 'keys/' + user + '/' + user + 'SeedPhrase.txt') 
except:
    logging.exception('Got exception on main handler')
    raise