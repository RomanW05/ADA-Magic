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
    walletReceiver = sys.argv[2]
    NFTName = sys.argv[3]
    policyName = sys.argv[4]
    ADAMagic_fee = sys.argv[5]
    money_reminder = sys.argv[6]
    ADAMagic_wallet = sys.argv[7]
    nft_price = sys.argv[8]
    nft_utxo = sys.argv[9]
    nft_txin = sys.argv[10]
    send_single_nft(homePath, mainTest, user, walletReceiver, NFTName, policyName, ADAMagic_fee, money_reminder, ADAMagic_wallet, nft_price, nft_utxo, nft_txin)
except:
    logging.exception('Got exception on main handler')
    raise
