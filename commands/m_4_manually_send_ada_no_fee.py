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



user1 = 'GabrielaShel'
user2 = 'ADA_Magic_io'
walletReveiver = ''
tx_hash1 = ''
tx_in1 = '2'
tx_hash2 ='' 
tx_in2 = '2'
tx_hash3 ='' 
tx_in3 = '2'
tx_hash4 ='' 
tx_in4 = '2'
tx_hash5 ='' 
tx_in5 = '2'
tx_hash6 ='' 
tx_in6 = '2'
tx_hash7 ='' 
tx_in7 = '2'
tx_hash8 ='' 
tx_in8 = '2'
tx_hash9 ='' 
tx_in9 = '2'
tx_hash10 ='' 
tx_in10 = '2'
tx_hash11 ='' 
tx_in11 = '2'
tx_hash12 ='' 
tx_in12 = '2'
tx_hash13 ='' 
tx_in13 = '2'
tx_hash14 ='' 
tx_in14 = '2'
tx_hash15 ='' 
tx_in15 = '2'
tx_hash16 ='' 
tx_in16 = '2'
tx_hash17 ='' 
tx_in17 = '1'
tx_hash18 ='' 
tx_in18 = '1'


funds = 279727738
send_money = 279727738

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
f' --tx-in {tx_hash4}#{tx_in4}' + \
f' --tx-in {tx_hash5}#{tx_in5}' + \
f' --tx-in {tx_hash6}#{tx_in6}' + \
f' --tx-in {tx_hash7}#{tx_in7}' + \
f' --tx-in {tx_hash8}#{tx_in8}' + \
f' --tx-in {tx_hash9}#{tx_in9}' + \
f' --tx-in {tx_hash10}#{tx_in10}' + \
f' --tx-in {tx_hash11}#{tx_in11}' + \
f' --tx-in {tx_hash12}#{tx_in12}' + \
f' --tx-in {tx_hash13}#{tx_in13}' + \
f' --tx-in {tx_hash14}#{tx_in14}' + \
f' --tx-in {tx_hash15}#{tx_in15}' + \
f' --tx-in {tx_hash16}#{tx_in16}' + \
f' --tx-in {tx_hash17}#{tx_in17}' + \
f' --tx-in {tx_hash18}#{tx_in18}' + \
' --tx-out ' + walletReveiver + '+' + str(output) + \
' --invalid-hereafter '+ ttl + \
' --fee ' + str(fee) + \
' --out-file ' + homePath + 'keys/' + user1 + '/tx.draft'
draft = subprocess.check_output(draft,shell=True)

#calculate fee
feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
' --tx-body-file ' + homePath + 'keys/' + user1 + '/tx.draft' + \
' --tx-in-count ' + str(18) + \
' --tx-out-count 2' + \
' --witness-count ' + str(2) + \
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
f' --tx-in {tx_hash4}#{tx_in4}' + \
f' --tx-in {tx_hash5}#{tx_in5}' + \
f' --tx-in {tx_hash6}#{tx_in6}' + \
f' --tx-in {tx_hash7}#{tx_in7}' + \
f' --tx-in {tx_hash8}#{tx_in8}' + \
f' --tx-in {tx_hash9}#{tx_in9}' + \
f' --tx-in {tx_hash10}#{tx_in10}' + \
f' --tx-in {tx_hash11}#{tx_in11}' + \
f' --tx-in {tx_hash12}#{tx_in12}' + \
f' --tx-in {tx_hash13}#{tx_in13}' + \
f' --tx-in {tx_hash14}#{tx_in14}' + \
f' --tx-in {tx_hash15}#{tx_in15}' + \
f' --tx-in {tx_hash16}#{tx_in16}' + \
f' --tx-in {tx_hash17}#{tx_in17}' + \
f' --tx-in {tx_hash18}#{tx_in18}' + \
' --tx-out ' + walletReveiver + '+' + str(output) + \
' --invalid-hereafter '+ ttl + \
' --fee ' + str(fee) + \
' --out-file ' + homePath + 'keys/' + user1 + '/tx.draft'
draft = subprocess.check_output(draft,shell=True)


#sign the motherfucker
signTx = homePath + 'cardano-cli transaction sign' + \
' --signing-key-file ' + f'{homePath}/keys/{user1}/{user1}.skey ' + \
' --signing-key-file ' + f'{homePath}/keys/{user2}/{user2}.skey ' + \
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
