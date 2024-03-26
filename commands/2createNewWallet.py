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
from orderedCommands import createWallet
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet

try:
    user = sys.argv[1]

    #1 Generate the ROOT private key from the recovery phrase
    seed = 'cat ' + homePath + 'keys/' + user + '/' + 'SeedPhrase.txt | ' + homePath + 'cardano-wallet key from-recovery-phrase Shelley > ' + homePath + 'keys/' + user + '/' + user + '.root.prv'
    seed = subprocess.check_output(seed,shell=True)

    #2 Generate the private and public Payment keys using the root private key for the first address
    seed = homePath + 'cardano-wallet key child 1852H/1815H/0H/0/0 < ' + homePath + 'keys/' + user + '/' + user + '.root.prv > ' + homePath + 'keys/' + user + '/' + user + '.payment-0.prv '
    seed = subprocess.check_output(seed,shell=True)
    seed = homePath + 'cardano-wallet key public --without-chain-code < ' + homePath + 'keys/' + user + '/' + user + '.payment-0.prv > ' + homePath + 'keys/' + user + '/' + user + '.payment-0.pub'
    seed = subprocess.check_output(seed,shell=True)

    #3 Generate the signing key for the payment address
    seed = homePath + 'cardano-cli key convert-cardano-address-key --shelley-payment-key \
                                                --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.payment-0.prv \
                                                --out-file ' + homePath + 'keys/' + user + '/' + user + '.skey'
    seed = subprocess.check_output(seed,shell=True)

    #4 Generate the stake keys. The process is similar to above
    seed = homePath + 'cardano-wallet key child 1852H/1815H/0H/2/0    < ' + homePath + 'keys/' + user + '/' + user + '.root.prv  > ' + homePath + 'keys/' + user + '/' + user + '.stake.prv' 
    seed = subprocess.check_output(seed,shell=True)
    seed = homePath + 'cardano-wallet key public --without-chain-code < ' + homePath + 'keys/' + user + '/' + user + '.stake.prv > ' + homePath + 'keys/' + user + '/' + user + '.stake.pub'
    seed = subprocess.check_output(seed,shell=True)

    seed = homePath + 'cardano-cli key convert-cardano-address-key --shelley-payment-key \
                                                --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.stake.prv \
                                                --out-file ' + homePath + 'keys/' + user + '/' + user + '.stake.skey'
    seed = subprocess.check_output(seed,shell=True)
    seed = homePath + 'cardano-cli key verification-key --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.stake.skey \
                                     --verification-key-file ' + homePath + 'keys/' + user + '/' + user + '.vkey'
    seed = subprocess.check_output(seed,shell=True)

    #5 Generate the addresses by computing the payment key and the stake key
    seed = homePath + 'cardano-cli address build ' + mainTest + \
                              ' --payment-verification-key $(cat ' + homePath + 'keys/' + user + '/' + user + '.payment-0.pub) \
                              --stake-verification-key $(cat ' + homePath + 'keys/' + user + '/' + user + '.stake.pub) \
                              --out-file ' + homePath + 'keys/' + user + '/' + user + '.addr'
    seed = subprocess.check_output(seed,shell=True)

    with open(homePath + 'keys/' + user + '/' + user + '.addr', 'r') as text:
        userAddress = text.read()
    exportParams(homePath, mainTest, user, userAddress)

except:
    logging.exception('Got exception on main handler')
    raise

