import os
import sys
from os.path import exists
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)




homePath = '/home/yop/Downloads/cardano-node1.30.0/'
user = sys.argv[1]

try:
    if exists(homePath + 'keys/' + user + '/' + user + '.addr'):
        pass
    if exists(homePath + 'keys/' + user):
        pass
    else:
        os.mkdir(homePath + 'keys/' + user)
except:
    logging.exception('Got exception on main handler')
    raise   