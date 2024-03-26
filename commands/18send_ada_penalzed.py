import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
import paramiko
from orderedCommands import loadAddress
from orderedCommands import send_ada_penalized_transaction
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)



homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet

try:
    user = sys.argv[1]
    project_address = sys.argv[2]
    amountToSend = sys.argv[3]
    wallet_receiver = sys.argv[4]
    tx_hash = sys.argv[5]
    ix_in = sys.argv[6]


    send_ada_penalized_transaction_vending_machine(homePath, mainTest, user, project_address, amountToSend, wallet_receiver, tx_hash, ix_in)
except:
    logging.exception('Got exception on main handler')
    raise