import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
import paramiko
from orderedCommands import loadAddress
from orderedCommands import sendSimpleTransaction
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)



homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet

try:
    user = sys.argv[1]
    amountToSend = sys.argv[2]
    walletReceiver = sys.argv[3]
    userAddress = loadAddress(homePath, user)
    sendSimpleTransaction(homePath, mainTest, user, userAddress, amountToSend, walletReceiver)
except:
    logging.exception('Got exception on main handler')
    raise