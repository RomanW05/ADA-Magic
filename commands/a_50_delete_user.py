import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
import paramiko
from orderedCommands import send_single_nft
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)


homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet

try:
    user = sys.argv[1]
    path = f'/home/yop/Downloads/cardano-node1.30.0/keys/{user}'
    list_of_files = os.listdir(path)
    for file in list_of_files:
        if not os.path.isdir(f'{path}/{file}'):
            os.remove(f'{path}/{file}')
    os.rmdir(path)
    print(f'User {user} deleted')

except:
    logging.exception('Got exception on main handler')
    raise
