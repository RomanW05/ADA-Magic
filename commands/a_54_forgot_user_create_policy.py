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
mainTest = mainnet
user = sys.argv[1]
policyName = 'Standard'
timeLock = 315360000#315360000=10years



user = sys.argv[1]
timeLock = 60*60*24*3650

userAddress = loadAddress(homePath, user)

#export parameters, still no clue what that is
exportParams(homePath, mainTest, user, userAddress)

#4 generate policy Signing files (skey, vkey)
generatePolicy(homePath, mainTest, user, policyName)

#5 create new policy
createNewPolicy(homePath, mainTest, user, policyName, str(timeLock))

#6 create new policyID
createPolicyID(homePath, mainTest, user, policyName)
path = homePath + 'keys/' + user + '/' + policyName + '.txt'
with open(path, 'r') as text:
    policyID = text.read()#return the policyID for app.py to read
    print(policyID)

