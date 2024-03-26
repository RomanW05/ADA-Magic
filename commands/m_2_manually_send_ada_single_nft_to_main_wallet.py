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
from orderedCommands import balance




homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet
user = sys.argv[1]
single_nft = sys.argv[2]
amountToSend = sys.argv[3]
walletReveiver = loadAddress(homePath, user)
with open(f'/home/yop/Downloads/cardano/single_nfts/{user}/{single_nft}/{single_nft}.addr') as text:
	single_nft_address = text.read()
print(balance(homePath, mainTest, single_nft_address))
tx_hash = input('tx_hash')
tx_in = input('tx_in')
send_ada_penalized_transaction_single_nft(homePath, mainTest, user, single_nft, amountToSend, walletReveiver, tx_hash, tx_in)
