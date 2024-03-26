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
# from orderedCommands import createNoNameTokens
from orderedCommands import sendTokens
from orderedCommands import checkForCreatedDeletedNoNameToken
from orderedCommands import sendTokens
from orderedCommands import mintWithPlatformFee
from orderedCommands import selfSendTokens
from orderedCommands import mintSplit
from orderedCommands import mint1
from orderedCommands import transactionGatherer2
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet
user = sys.argv[1]
policyName = 'WaldenMassage'
# policyName = 'Try8'
timeLock = 315360000#315360000=10years
NFTDescription = 'Testing the code for NFT minting functionality continuity'
NFTName = 'WaldenMassageWeeklyAbo'
NFTAmount = 1
NFTID = 2
NFTImageUrl = 'not yet'
NFTRoyaltiesPercentage = "0.2"
userAddress = loadAddress(homePath, user)
print(userAddress)
# NFTRoyaltiesAddress = userAddress
platformAddress = 'addr_test1qzvplvlu0pqd0spm7ev5pp9vdsuydjgycdcr2qct8xcapgz9thnazclfq274u9l74cjre46as2rpn3jwx7xw8vxy8hass0kdpa'


gabrielaNami = 'addr1qyd40pvlw4vnjxr5nv0f7x7xhjrmgu48ptg2v3kyrjnktmydn4f3p75egmlns2lm0mr7lgh9ghr5n3jvkrqr5rs2v8fsvqr5tx'
# gabrielaNami = platformAddress

def createNoNameTokens(homePath, mainTest, user, userAddress, policyName, totalTokenAmmount, amountToMint):
	#CREATE NO NAME TOKENS
	#Gather basic info
	path = homePath + 'keys/' + user + '/' + policyName + '.txt'
	with open(path, 'r') as text:
		policyID = text.read()
	with open(homePath + 'keys/' + user + '/' + policyName + '.script', 'r') as read:
		policyString = read.read()
		policyJSON = json.loads(policyString)
	herafter = policyJSON['scripts'][0]['slot']
	#2.1 Make raw Transaction with OUT real fee
	craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
	craftTx = subprocess.check_output(craftTx,shell=True)
	print(craftTx)
	sys.exit()
	# print(craftTx)
	# sys.exit()
	#Clean the info and get only what matters
	fee = 300000
	if amountToMint == 1:
		craftTx2 = craftTx.decode('utf-8')
		# if policyID in craftTx2:
		# 	return
		txIn, funds = transactionGatherer2(craftTx, fee)
	if amountToMint == -1:
		txIn, funds = transactionGathererForMintingTokens1(craftTx, fee, policyID)
		# print('Burning Token')
	NumberOfTxIn = len(txIn.split('--'))-1
	cardanoFees = 1600000
	output = str(int(funds) - int(fee) - cardanoFees)

	# #create raw file
	getRawTx = homePath + 'cardano-cli transaction build-raw' + \
	' --fee ' + str(fee) + \
	txIn + \
	' --tx-out ' + gabrielaNami + '+' +  str(cardanoFees) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
	' --tx-out ' + userAddress + '+' + output + \
	' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
	' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
	' --invalid-hereafter ' + str(herafter) + \
	' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
	getRawTx = getRawTx.replace('\n', '')
	getRawTx = subprocess.check_output(getRawTx,shell=True)


	# #2.2 Calculate fee
	fee = homePath + 'cardano-cli transaction calculate-min-fee' + \
	' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' +\
	' --tx-in-count ' + '1' + \
	' --tx-out-count 2' + \
	' --witness-count ' + '2 ' + \
	mainTest + \
	' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
	fee = subprocess.check_output(fee,shell=True)
	
	fee = str(fee.decode('utf-8'))
	fee = fee.replace('\n', '')
	output = str(int(funds) - int(fee) - cardanoFees)

	# #Make raw Transaction with real fee
	getRawTx = homePath + 'cardano-cli transaction build-raw' + \
	' --fee ' + str(fee) + \
	txIn + \
	' --tx-out ' + gabrielaNami + '+' +  str(cardanoFees) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
	' --tx-out ' + userAddress + '+' + output + \
	' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
	' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
	' --invalid-hereafter ' + str(herafter) + \
	' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
	getRawTx = getRawTx.replace('\n', '')
	getRawTx = subprocess.check_output(getRawTx,shell=True)

	output = str(int(funds) - int(fee) - cardanoFees)

	# #2.3 Sign the Transaction
	signTx = homePath + 'cardano-cli transaction sign' + \
	' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey' +\
	' --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + \
	mainTest + \
	' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' +\
	' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
	signTx = subprocess.check_output(signTx,shell=True)

	# sys.exit()

	# #Send the REAL Transaction
	sendRealTx = homePath + 'cardano-cli transaction submit' + \
	' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest
	sendRealTx = subprocess.check_output(sendRealTx,shell=True)

createNoNameTokens(homePath, mainTest, user, userAddress, policyName, 1, 1)





