import os
import sys
import json
import subprocess
import time
from os.path import exists
# import mysql.connector
# import paramiko
# from orderedCommands import send_single_nft
from orderedCommands import currentSlotD
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)



user = sys.argv[1]
walletReveiver = sys.argv[2]
NFTName = sys.argv[3]
policy_name = sys.argv[4]
tx_hash = sys.argv[5]
tx_in = sys.argv[6]
funds = sys.argv[7]





def send_single_nft(user, walletReveiver, NFTName, policy_name, tx_hash, tx_in, funds):
    homePath = '/home/yop/Downloads/cardano-node1.30.0/'
    mainnet = '--mainnet'
    mainTest = mainnet
    with open(f'{homePath}/keys/{user}/{user}.addr') as text:
        userAddress = text.read()
        userAddress = userAddress.replace('\n', '')
    with open(f'{homePath}/keys/{user}/{policy_name}.txt') as text:
        policy_id = text.read()
        policy_id = policy_id.replace('\n', '')

    
    currentSlot             = currentSlotD(homePath, mainTest)
    ttl                     = str(int(currentSlot) + 200)
    fee                     = 300000
    output                  = str(int(funds) - int(fee))
    constant_nft_price      = 1500000
    output = str(int(funds) - int(fee) - constant_nft_price)

    #Create draft
    draft                   = homePath + 'cardano-cli transaction build-raw' + \
    f' --tx-in {tx_hash}#{tx_in}' + \
    ' --tx-out ' + walletReveiver + '+' + str(constant_nft_price) + '+"1 ' + policy_id + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + output + '+"0 ' + policy_id + '.' + NFTName + '"' +  \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)

    #calculate fee
    feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/tx.draft' + \
    ' --tx-in-count ' + str(1) + \
    ' --tx-out-count 2' + \
    ' --witness-count ' + str(1) + \
    ' --byron-witness-count 0 ' + \
    mainTest + \
    ' --protocol-params-file ' + f'{homePath}/keys/{user}/protocol.json'
    feeCalculation = subprocess.check_output(feeCalculation,shell=True)
    feeCalculation = feeCalculation.decode('utf-8')
    fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')
    
    output = str(int(funds) - int(fee) - constant_nft_price)


    #Create draft with real ADA
    draft                   = homePath + 'cardano-cli transaction build-raw' + \
    f' --tx-in {tx_hash}#{tx_in}' + \
    ' --tx-out ' + walletReveiver + '+' + str(constant_nft_price) + '+"1 ' + policy_id + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + output + '+"0 ' + policy_id + '.' + NFTName + '"' +  \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)


    #sign the motherfucker
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + f'{homePath}/keys/{user}/{user}.skey ' + \
    mainTest + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/tx.draft' + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = signTx.replace('\n', '')
    signTx = subprocess.check_output(signTx,shell=True)

    #Send the REAL Transaction
    sendRealTx = homePath + 'cardano-cli transaction submit' + \
    ' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest
    sendRealTx = sendRealTx.replace('\n', '')
    sendRealTx = subprocess.check_output(sendRealTx,shell=True)



send_single_nft(user, walletReveiver, NFTName, policy_name, tx_hash, tx_in, funds)



