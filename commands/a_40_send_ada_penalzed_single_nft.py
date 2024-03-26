import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
import paramiko
from orderedCommands import loadAddress
from orderedCommands import send_ada_penalized_transaction_single_nft
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)



homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet

try:
    username = sys.argv[1]
    project_address = sys.argv[2]
    amountToSend = sys.argv[3]
    wallet_receiver = sys.argv[4]
    tx_hash = sys.argv[5]
    tx_in = sys.argv[6]
    single_nft = sys.argv[7]
    
    send_ada_penalized_transaction_single_nft(homePath, mainTest, username, single_nft, project_address, amountToSend, wallet_receiver, tx_hash, tx_in)
    print('ada sent bacl')
except:
    logging.exception('Got exception on main handler')
    raise