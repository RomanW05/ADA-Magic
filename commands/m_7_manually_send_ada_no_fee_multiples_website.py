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




def clear_tx(project_address):
    craft_tx = f'/home/yop/Downloads/cardano-node1.30.0/cardano-cli query utxo --mainnet --address {project_address}'
    craft_tx = subprocess.check_output(craft_tx,shell=True)
    
    # Clean results
    craft_tx = craft_tx.decode('utf-8')
    craft_tx = craft_tx.split('\n')
    craft_tx = craft_tx[2:]
    if craft_tx[-1:] == '':
        craft_tx = craft_tx[:-1]

    return craft_tx


def get_tx_info(craft_tx):
    utxo_lovelace = []
    for x, utxo in enumerate(craft_tx):
        utxo = utxo.split(' ')

        # More than 17 small fields after utxo been splitted in ' ' is a token or NFT.
        if len(utxo) > 17:
            continue

        # tx hashes are always 64 bits in length
        hashes = utxo[0]
        if len(hashes) != 64:
            continue

        for data in utxo[:14]:
            try:
                if int(data) < 4:
                    tx_in = data
            except:
                pass
            try:
                if int(data) > 5:
                    lovelaces = data
            except:
                pass
        utxo_lovelace.append([hashes, tx_in, lovelaces])

    return utxo_lovelace


def validate_address(walletReveiver):
    if walletReveiver[:4] != 'addr':
        return False

    query = f'/home/yop/Downloads/cardano-node1.30.0/cardano-cli query utxo --mainnet --address {walletReveiver}'
    query = subprocess.check_output(query,shell=True)
    query = query.decode('utf-8')
    if 'invalid address' in query:
        return False
    else:
        return True


def transfer_funds(user1, walletReveiver):
    if not validate_address(walletReveiver):  # if not True, return False
        return False

    try:
        with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{user1}/{user1}.addr') as text:
            user_address = text.read()
            user_address = user_address.replace('\n', '')

        craft_tx = clear_tx(user_address)

        # Get tx_hash, tx_in, lovelaces in an array for this wallet [tx_hash, tx_in, lovelaces]
        utxo_lovelace = get_tx_info(craft_tx)
        txs_in = len(utxo_lovelace)

        homePath = '/home/yop/Downloads/cardano-node1.30.0/'
        mainnet = '--mainnet'
        mainTest = mainnet
        with open(f'{homePath}/keys/{user1}/{user1}.addr') as text:
            userAddress = text.read()
            userAddress = userAddress.replace('\n', '')

        txs_hash = ''
        send_money = 0
        for elem in utxo_lovelace:
            txs_hash = txs_hash + f' --tx-in {elem[0]}#{elem[1]}'
            send_money += int(elem[2])


        currentSlot             = currentSlotD(homePath, mainTest)
        ttl                     = str(int(currentSlot) + 200)
        fee                     = 300000
        output                  = str(int(send_money) - int(fee))


        #Create draft
        draft                   = homePath + 'cardano-cli transaction build-raw' + \
        txs_hash + \
        ' --tx-out ' + walletReveiver + '+' + str(output) + \
        ' --invalid-hereafter '+ ttl + \
        ' --fee ' + str(fee) + \
        ' --out-file ' + homePath + 'keys/' + user1 + '/tx.draft'
        draft = subprocess.check_output(draft,shell=True)

        #calculate fee
        feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
        ' --tx-body-file ' + homePath + 'keys/' + user1 + '/tx.draft' + \
        ' --tx-in-count ' + str(txs_in) + \
        ' --tx-out-count 1' + \
        ' --witness-count ' + str(1) + \
        ' --byron-witness-count 2 ' + \
        mainTest + \
        ' --protocol-params-file ' + f'{homePath}/keys/{user1}/protocol.json'
        feeCalculation = subprocess.check_output(feeCalculation,shell=True)
        feeCalculation = feeCalculation.decode('utf-8')
        fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')

        output                  = str(int(send_money) - int(fee))
        # print(fee, output, send_money)

        #Create draft with real ADA
        draft                   = homePath + 'cardano-cli transaction build-raw' + \
        txs_hash + \
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

        return True
    except Exception as e:
        # print(f'{e}')

        return False



