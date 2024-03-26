import os
import sys
import subprocess
import time
from os.path import exists
from orderedCommands import balance
from orderedCommands import cleanCraftTx2
from orderedCommands import loadAddress
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
from orderedCommands import metadataCreationWithOutRoyalties
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

user = sys.argv[1]
NFTName = sys.argv[2]
policyName = sys.argv[3]

homePath = '/home/yop/Downloads/cardano-node1.30.0/'
def findPolicyIdAndTxHash(user, policyName, NFTName):
    #Load data for carcado-cli to work
    homePath = '/home/yop/Downloads/cardano-node1.30.0/'
    testnet = '--testnet-magic 1097911063'
    mainnet = '--mainnet'
    mainTest = testnet

    #load policyID
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    userAddress = loadAddress(homePath, user)
    with open(path, 'r') as text:
        policyID = text.read()

    code = policyID + '.' + NFTName#Any tx that matches this code will be txHash needed
    while True:
        #Load balance
        craftTx = balance(homePath, mainTest, userAddress)

        #Get single txs
        txs = cleanCraftTx2(craftTx)

        #Check for match
        for tx in txs:
            try:
                if (code in tx[6]):
                    return [policyID, tx[0]]
            except:
                pass
        time.sleep(2)

# data = findPolicyIdAndTxHash(user, policyName, NFTName)
# print(data)
path = homePath + 'keys/' + user + '/' + policyName + '.txt'
with open(path, 'r') as text:
    policyID = text.read()
    print(policyID)