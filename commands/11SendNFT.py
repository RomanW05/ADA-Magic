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
from orderedCommands import sendNFT
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)


homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet

try:
    user = sys.argv[1]
    walletReceiver = sys.argv[2]
    NFTName = sys.argv[3]
    policyName = sys.argv[4]


    sendNFT(homePath, mainTest, user, walletReceiver, NFTName, policyName)
except:
    logging.exception('Got exception on main handler')
    raise
