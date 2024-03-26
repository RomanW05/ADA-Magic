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
from orderedCommands import sendSimpleTransactionWithOutRoyalties
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)



homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet

try:
    user = sys.argv[1]
    amountToSend = sys.argv[2]
    walletReveiver = sys.argv[3]
    platformAddress = sys.argv[4]
    platformFee = sys.argv[5]

    userAddress = loadAddress(homePath, user)
    sendSimpleTransactionWithOutRoyalties(homePath, mainTest, user, userAddress, amountToSend, walletReveiver, platformAddress, platformFee)
except:
    logging.exception('Got exception on main handler')
    raise