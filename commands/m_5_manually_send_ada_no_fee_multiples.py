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



user1 = 'JoseCatala'
walletReveiver = ''
tx_hash1 = ''
tx_in1 = '1'
tx_hash2 ='' 
tx_in2 = '1'
tx_hash3 ='' 
tx_in3 = '1'



funds = 573315110
send_money = 573315110

# tx_in2 = '0'
# tx_hash2 = ''
# extra = '1179811'

# funds = str(int(funds) + int(extra))


# def send_ada(user, walletReveiver, tx_hash1, tx_in1, funds, send_money):
homePath = '/home/yop/Downloads/cardano-node1.30.0/'
mainnet = '--mainnet'
mainTest = mainnet
with open(f'{homePath}/keys/{user1}/{user1}.addr') as text:
    userAddress = text.read()
    userAddress = userAddress.replace('\n', '')


currentSlot             = currentSlotD(homePath, mainTest)
ttl                     = str(int(currentSlot) + 200)
fee                     = 300000
output                  = str(int(send_money) - int(fee))
reminder                = str(int(funds) - (int(output) ))

# ' --tx-out ' + userAddress + '+' + reminder + \

#Create draft
draft                   = homePath + 'cardano-cli transaction build-raw' + \
f' --tx-in {tx_hash1}#{tx_in1}' + \
f' --tx-in {tx_hash2}#{tx_in2}' + \
f' --tx-in {tx_hash3}#{tx_in3}' + \
' --tx-out ' + walletReveiver + '+' + str(output) + \
' --invalid-hereafter '+ ttl + \
' --fee ' + str(fee) + \
' --out-file ' + homePath + 'keys/' + user1 + '/tx.draft'
draft = subprocess.check_output(draft,shell=True)

#calculate fee
feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
' --tx-body-file ' + homePath + 'keys/' + user1 + '/tx.draft' + \
' --tx-in-count ' + str(3) + \
' --tx-out-count 1' + \
' --witness-count ' + str(1) + \
' --byron-witness-count 2 ' + \
mainTest + \
' --protocol-params-file ' + f'{homePath}/keys/{user1}/protocol.json'
feeCalculation = subprocess.check_output(feeCalculation,shell=True)
feeCalculation = feeCalculation.decode('utf-8')
fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')

output                  = str(int(send_money) - int(fee))
reminder                = str(int(funds) - (int(output)))

#Create draft with real ADA
draft                   = homePath + 'cardano-cli transaction build-raw' + \
f' --tx-in {tx_hash1}#{tx_in1}' + \
f' --tx-in {tx_hash2}#{tx_in2}' + \
f' --tx-in {tx_hash3}#{tx_in3}' + \
' --tx-out ' + walletReveiver + '+' + str(output) + \
' --invalid-hereafter '+ ttl + \
' --fee ' + str(fee) + \
' --out-file ' + homePath + 'keys/' + user1 + '/tx.draft'
draft = subprocess.check_output(draft,shell=True)


#sign the motherfucker
signTx = homePath + 'cardano-cli transaction sign' + \
' --signing-key-file ' + f'{homePath}/keys/{user1}/{user1}.skey ' + \
mainTest + \
' --tx-body-file ' + homePath + 'keys/' + user1 + '/tx.draft' + \
' --out-file ' + homePath + 'keys/' + user1 + '/matx.signed'
signTx = signTx.replace('\n', '')
signTx = subprocess.check_output(signTx,shell=True)

#Send the REAL Transaction
sendRealTx = homePath + 'cardano-cli transaction submit' + \
' --tx-file ' + homePath + 'keys/' + user1 + '/matx.signed ' + mainTest
sendRealTx = sendRealTx.replace('\n', '')
sendRealTx = subprocess.check_output(sendRealTx,shell=True)
print('TRANSACTION SENT')



# send_ada(user, walletReveiver, tx_hash1, tx_in1, funds, send_money)

