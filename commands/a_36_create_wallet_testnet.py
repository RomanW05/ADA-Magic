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


nft_name = sys.argv[1]
# project_path = sys.argv[1]
homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet

try:

    #1 Generate the ROOT private key from the recovery phrase
    seed = f'cat /home/yop/Downloads/cardano/temp_keys/{nft_name}/SeedPhrase.txt | {homePath}cardano-wallet key from-recovery-phrase Shelley > /home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.root.prv'
    seed = subprocess.check_output(seed,shell=True)

    #2 Generate the private and public Payment keys using the root private key for the first address
    seed = homePath + 'cardano-wallet key child 1852H/1815H/0H/0/0 < ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.root.prv > /home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.payment-0.prv'
    seed = subprocess.check_output(seed,shell=True)
    seed = homePath + 'cardano-wallet key public --without-chain-code < ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.payment-0.prv > /home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.payment-0.pub'
    seed = subprocess.check_output(seed,shell=True)

    #3 Generate the signing key for the payment address
    seed = homePath + 'cardano-cli key convert-cardano-address-key --shelley-payment-key \
                                                --signing-key-file ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.payment-0.prv \
                                                --out-file ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.skey'
    seed = subprocess.check_output(seed,shell=True)

    #4 Generate the stake keys. The process is similar to above
    seed = homePath + 'cardano-wallet key child 1852H/1815H/0H/2/0    < ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.root.prv  > ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.stake.prv' 
    seed = subprocess.check_output(seed,shell=True)
    seed = homePath + 'cardano-wallet key public --without-chain-code < ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.stake.prv > ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.stake.pub'
    seed = subprocess.check_output(seed,shell=True)

    seed = homePath + 'cardano-cli key convert-cardano-address-key --shelley-payment-key \
                                                --signing-key-file ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.stake.prv \
                                                --out-file ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.stake.skey'
    seed = subprocess.check_output(seed,shell=True)
    seed = homePath + 'cardano-cli key verification-key --signing-key-file ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.stake.skey \
                                     --verification-key-file ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.vkey'
    seed = subprocess.check_output(seed,shell=True)

    #5 Generate the addresses by computing the payment key and the stake key
    seed = homePath + 'cardano-cli address build ' + mainTest + \
                              ' --payment-verification-key $(cat ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.payment-0.pub) \
                              --stake-verification-key $(cat ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.stake.pub) \
                              --out-file ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{nft_name}.addr'
    seed = subprocess.check_output(seed,shell=True)
except Exception as e:
    print(e)
    logging.exception('Got exception on main handler')
    raise