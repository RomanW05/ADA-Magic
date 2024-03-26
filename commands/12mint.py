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

try:
    user = sys.argv[1]
    NFTName = sys.argv[2]
    NFTID = sys.argv[3]
    NFTDescription = sys.argv[4]
    NFTRoyaltiesPercentage = sys.argv[5]
    NFTRoyaltiesAddress = sys.argv[6]
    policyName = sys.argv[7]
    NFTImageUrl = sys.argv[8]
    NFTImageUrlThumbnail = sys.argv[9]
    plaformFee = sys.argv[10]

    userAddress = loadAddress(homePath, user)
    NFTRoyaltiesAddress = userAddress
    platformAddress = ''

    userAddress = loadAddress(homePath, user)
    walletReceiver = userAddress


    #7 create metadata
    if int(NFTRoyaltiesPercentage) == 0:
        metadataCreationWithOutRoyalties(homePath, mainTest, user, policyName, NFTDescription, NFTName, NFTID, NFTImageUrl, NFTImageUrlThumbnail)
    else:
        NFTRoyaltiesPercentage = '0.' + str(NFTRoyaltiesPercentage)
        metadataCreation(homePath, mainTest, user, policyName, NFTDescription, NFTName, NFTID, NFTImageUrl, NFTRoyaltiesPercentage, NFTRoyaltiesAddress, NFTImageUrlThumbnail)

    mint1(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, timeLock, platformAddress, plaformFee)
    
except:
    logging.exception('Got exception on main handler')
    raise
    