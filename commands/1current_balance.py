import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
import paramiko
from orderedCommands import loadAddress
from orderedCommands import balance
from orderedCommands import exportParams
from orderedCommands import generatePolicy
from orderedCommands import createNewPolicy
from orderedCommands import createPolicyID
from orderedCommands import metadataCreation
from orderedCommands import mint
from orderedCommands import createNoNameTokens
from orderedCommands import sendTokens
from orderedCommands import checkForCreatedDeletedNoNameToken
from orderedCommands import sendTokens
from orderedCommands import mintWithPlatformFee
from orderedCommands import selfSendTokens
from orderedCommands import mintSplit
from orderedCommands import mint1
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)


homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet

try:
    user = sys.argv[1]
    # policyName = 'Try8'
    # timeLock = 315360000#315360000=10years
    # NFTDescription = 'Testing the code for NFT minting functionality continuity'
    # NFTName = 'NFTTest'
    # NFTAmount = 1
    # NFTID = 2
    # NFTImageUrl = 'not yet'
    # NFTRoyaltiesPercentage = "0.2"
    # userAddress = loadAddress(homePath, user)
    # NFTRoyaltiesAddress = userAddress
    # platformAddress = ''

    userAddress = loadAddress(homePath, user)
    balanceResult = balance(homePath, mainTest, userAddress)
    balanceResult = balanceResult.replace('\n', ' ')
    craftTx = balanceResult.split(' ')
    

    #clean data
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)
    craftTx.pop(0)#'TxHash'
    craftTx.pop(0)#'TxIx'
    craftTx.pop(0)#'Amount'
    craftTx.pop(0)#'--------------------------------------------------------------------------------------'

    #arrange data in transactions
    txs = []
    temp = []
    for data in craftTx:
        # print(data)
        if ((len(data) == 64) and ('.' not in data)):
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)

    #read balance and locked balance
    money = 0
    moneyLocked = 0
    for data in txs:
        if len(data) < 2: continue
        if len(data) == 6:
            money += int(data[2])
        else:
            moneyLocked += int(data[2])

    print(money, ',', moneyLocked)
except:
    logging.exception('Got exception on main handler')
    raise
