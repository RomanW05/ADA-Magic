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


homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet
user = 'testo'
policyName = 'Try8'
timeLock = 315360000#315360000=10years
NFTDescription = 'Testing the code for NFT minting functionality continuity'
NFTName = 'NFTTest'
NFTAmount = 1
NFTID = 2
NFTImageUrl = 'not yet'
NFTRoyaltiesPercentage = "0.2"
userAddress = loadAddress(homePath, user)
NFTRoyaltiesAddress = userAddress
platformAddress = 'addr_test1qzvplvlu0pqd0spm7ev5pp9vdsuydjgycdcr2qct8xcapgz9thnazclfq274u9l74cjre46as2rpn3jwx7xw8vxy8hass0kdpa'

userAddress = loadAddress(homePath, user)
print(balance(homePath, mainTest, userAddress))
walletReceiver = userAddress
# selfSendTokens(homePath, mainTest, user, userAddress)
# print(userAddress)
# sys.exit()

#export parameters, still no clue what that is
exportParams(homePath, mainTest, user, userAddress)

#4 generate policy Signing files (skey, vkey)
generatePolicy(homePath, mainTest, user, policyName)

#5 create new policy
createNewPolicy(homePath, mainTest, user, policyName, timeLock)

#6 create new policyID
createPolicyID(homePath, mainTest, user, policyName)

#Create no-name token with policyID for royalties and burn such token
path = homePath + 'keys/' + user + '/' + policyName + 'LOADED.txt'
# print(path)
# sys.exit()
if exists(path):
	pass
	print('NonameToken exists, exiting function')
else:
	createNoNameTokens(homePath, mainTest, user, userAddress, policyName, 1, 1)
	checkForCreatedDeletedNoNameToken(homePath, mainTest, user, userAddress, policyName, 0)
	createNoNameTokens(homePath, mainTest, user, userAddress, policyName, 0, -1)
	checkForCreatedDeletedNoNameToken(homePath, mainTest, user, userAddress, policyName, 1)
	with open(path, 'w') as text:
		text.write('policy LOADED')

#7 create metadata
metadataCreation(homePath, mainTest, user, policyName, NFTDescription, NFTName, NFTID, NFTImageUrl, NFTRoyaltiesPercentage, NFTRoyaltiesAddress)

# sendTokens(homePath, mainTest, user, userAddress, policyName, userAddress)
# mintSplit(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, timeLock)
mint1(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, timeLock, platformAddress)
sys.exit()

#8 mint that shit
mintWithPlatformFee()
mint(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, timeLock)