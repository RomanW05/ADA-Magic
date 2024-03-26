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
user = sys.argv[1]
policyName = 'WaldenMassage'
timeLock = 315360000#315360000=10years
NFTDescription = 'Testing the code for NFT minting functionality continuity'
NFTName = 'NFTTest'
NFTAmount = 1
NFTID = 2
NFTImageUrl = 'not yet'
NFTRoyaltiesPercentage = "0.2"



user = sys.argv[1]
policyName = sys.argv[2]

userAddress = loadAddress(homePath, user)

#Create no-name token with policyID for royalties and burn such token
path = homePath + 'keys/' + user + '/' + policyName + 'LOADED.txt'

if exists(path):
    pass
    print('NonameToken exists, exiting function')
else:
    createNoNameTokens(homePath, mainTest, user, userAddress, policyName, 0, -1)
    checkForCreatedDeletedNoNameToken(homePath, mainTest, user, userAddress, policyName, 1)
    with open(path, 'w') as text:
        text.write('policy LOADED')