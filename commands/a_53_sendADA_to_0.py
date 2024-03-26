import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
import paramiko
from orderedCommands import loadAddress
from orderedCommands import send_ada_for_platform_users
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)



homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet
user = sys.argv[1]
amountToSend = sys.argv[2]
walletReceiver = sys.argv[3]
userAddress = loadAddress(homePath, user)
send_ada_for_platform_users(homePath, mainTest, user, userAddress, amountToSend, walletReceiver)
