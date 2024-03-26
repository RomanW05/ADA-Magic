import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
import paramiko
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

#Execute this program
#python3 /home/yop/Downloads/cardano-node1.30.0/keys/constructPolicy.py test 2description.bla 3asd 4NFTID.bla 5imageHash.bla 0.2 7royaltyAddress.blabla True policyID False 11oldPolicyName.noOldPolicy

'''
GUIDE LINE:

MANDATORY ATTRIBUTE ORDER:
exampleFunction(homePath, mainTest, user, userAddress, policyName, timeLock, NFTDescription, NFTName, NFTID, NFTImageUrl, NFTRoyaltiesPercentage, NFTRoyaltiesAddress)

1.User creates new account
    1.0 Create user and password and store it in Database. Create folder keys/user
    1.1 Create new wallet
    1.2 Create seed-phrase
    1.3 Create paying password
    1.4 Transform account to cardano-cli

2.User login
    2.1 Enter username and password

3.User creates new NFT
    3.1 Check if policy exists
    3.2 Create new policy
    3.3 Upload image to ipfs
    3.4 Create metadata
    3.5 Create Tx, fee, redo, sign, send





'''

#INDEX OF ALL FUNCTIONS
'''
cleanCraftTx(craftTx). Used in mint()
loadAddress(homePath, user). Loads wallet address
balance(homePath, mainTest, userAddress)
createWallet(homePath, mainTest, user, passPhrase)



'''
homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet  #Choose the type of net
user = 'testo'
# passPhrase = '1234567890'
# with open(homePath + 'keys/' + user + '/' + user + 'SeedPhrase.txt', 'w') as text:
#     text.write('')
# seed = homePath + 'cardano-wallet recovery-phrase generate > ' + homePath + 'keys/' + user + '/' + user + 'SeedPhrase.txt'
# seed = subprocess.check_output(seed,shell=True)
# with open(homePath + 'keys/' + user + '/' + user + 'SeedPhrase.txt', 'a') as text:
#     passPhrase = '\n\n' + passPhrase + '\n' + passPhrase
#     text.write(passPhrase)
# seed = 'cat ' + homePath + 'keys/' + user + '/' + user + "SeedPhrase.txt | xargs -n50 -d'\n' " + homePath + 'cardano-wallet key from-recovery-phrase Shelley > ' + homePath + 'keys/' + user + '/' + user + '.prv'
# seed = subprocess.check_output(seed,shell=True)
# seed = seed.decode('utf-8')
# print(seed)


# user = 'here'
# user = sys.argv[1]
# description = sys.argv[2]
# NFTName = sys.argv[3]
# NFTID = sys.argv[4]
# imageHash = sys.argv[5]
# royaltiesPercentage = sys.argv[6]
# royaltyAddress = sys.argv[7]
# policyName = sys.argv[8]





def cleanCraftTx(craftTx):
    #Decode and clean Transactions
    craftTx = craftTx.decode('utf-8').replace('\n', ' ')
    craftTx = craftTx.split(' ')
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)

    #Order Transactions  
    txs = []
    temp = []
    for data in craftTx:
        if ((len(data) == 64) and ('.' not in data)):
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)
    txs.pop(0)

    #Select transaction with highest amount of ADAs
    amounts = 0
    greatestTx = []
    for x, bracket in enumerate(txs):
        if int(bracket[2]) > amounts:#bracket[2] is the Lovelace amount in string
            amounts = int(bracket[2])
            greatestTx = txs[x]#Select greater Transaction bracket

    return greatestTx

def cleanCraftTx1(craftTx):
    #Decode and clean Transactions
    craftTx = craftTx.decode('utf-8').replace('\n', ' ')
    craftTx = craftTx.split(' ')
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)

    #Order Transactions  
    txs = []
    temp = []
    for data in craftTx:
        if ((len(data) == 64) and ('.' not in data)):
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)
    txs.pop(0)

    return txs

def cleanCraftTx2(craftTx):
    #Decode and clean Transactions
    craftTx = craftTx.replace('\n', ' ')
    craftTx = craftTx.split(' ')
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)

    #Order Transactions  
    txs = []
    temp = []
    for data in craftTx:
        if ((len(data) == 64) and ('.' not in data)):
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)
    txs.pop(0)

    return txs

#Imperative
exportCardano = "export CARDANO_NODE_SOCKET_PATH=/home/yop/Downloads/cardano-node1.30.0/db/node.socket"
subprocess.call(exportCardano,shell=True)

def loadAddress(homePath, user):
    addressSSH = homePath + 'keys/' + user + '/' + user + '.addr'
    addressSSH = 'cat ' + addressSSH
    addressSSH = subprocess.check_output(addressSSH,shell=True)
    userAddress = addressSSH.decode('utf-8')
    return userAddress

def balance(homePath, mainTest, userAddress):
    query = homePath + 'cardano-cli query utxo ' + mainTest + ' --address ' + userAddress
    balanceResult = subprocess.check_output(query,shell=True)
    balanceResult = balanceResult.decode('utf-8')
    return balanceResult

def createWallet(homePath, mainTest, user):
    if exists(homePath + 'keys/' + user + '/' + user + '.addr'): return
    if exists(homePath + 'keys/' + user):
        pass
    else:
        os.mkdir(homePath + 'keys/' + user)

    seed = homePath + 'cardano-wallet recovery-phrase generate > ' + homePath + 'keys/' + user + '/' + user + 'SeedPhrase.txt'
    seed = subprocess.check_output(seed,shell=True)

    #1 Generate the ROOT private key from the recovery phrase
    seed = 'cat ' + homePath + 'keys/' + user + '/' + user + 'SeedPhrase.txt | ' + homePath + 'cardano-wallet key from-recovery-phrase Shelley > ' + homePath + 'keys/' + user + '/' + user + '.root.prv'
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





def exportParams(homePath, mainTest, user, userAddress):
    #Export protocol parameters
    if exists(homePath + 'keys/' + user + '/protocol.json'):
        # print('exportParams exists, exiting function')
        return

    exportParams = homePath + 'cardano-cli query protocol-parameters ' + mainTest + ' --out-file ' + homePath + 'keys/' + user + '/protocol.json'
    subprocess.call(exportParams,shell=True)

def generatePolicy(homePath, mainTest, user, policyName):
    if exists(homePath + 'keys/' + user + '/' + policyName + '.script'): 
        # print('generatePolicy exists, exiting function')
        return
    #Generate policy keys
    generatePolicy = homePath + 'cardano-cli address key-gen --verification-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.vkey --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey'
    subprocess.call(generatePolicy,shell=True)

def currentSlotD(homePath, mainTest):
    #Get nows slot to timelock NFT
    query = homePath + 'cardano-cli query tip ' + mainTest + ' | jq .slot?'
    result = subprocess.check_output(query,shell=True)
    result = result.decode('utf-8')
    result = result.replace('\n', '')
    result = int(result)
    return result

def keyHashD(homePath, mainTest, user, policyName):
    #keyHash keyHash
    query = homePath + 'cardano-cli address key-hash --payment-verification-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.vkey'
    result = subprocess.check_output(query,shell=True)
    result = result.decode('utf-8')
    result = result.replace('\n', '')
    return result

def createNewPolicy(homePath, mainTest, user, policyName, timeLock):
    if exists(homePath + 'keys/' + user + '/' + policyName + '.script'):
        # print('createNewPolicy exists, exiting function')
        return
    currentSlot = currentSlotD(homePath, mainTest)
    keyHash = keyHashD(homePath, mainTest, user, policyName)
    
    policy = {
                "type": "all",
                "scripts":[{
                    "type": "before",
                    "slot": "slot"#$(expr $(cardano-cli query tip --mainnet | jq .slot?) + 10000)"
                    },
                    {
                    "type": "sig",
                    "keyHash": "insert keyHash here"
                    }]
                }
    policy['scripts'][0]['slot'] = int(currentSlot) + int(timeLock)
    policy['scripts'][1]['keyHash'] = str(keyHash)
    stringPolicy = str(policy)
    stringPolicy = stringPolicy.replace("'", '"')

    path = homePath + 'keys/' + user + '/' + policyName + '.script'
    with open(path, 'w') as variable_name:
        variable_name.write(stringPolicy)


def createPolicyID(homePath, mainTest, user, policyName):
    if exists(homePath + 'keys/' + user + '/' + policyName + '.txt'): 
        # print('createPolicyID exists, exiting function')
        return
    #PolicyID
    policyID = homePath + 'cardano-cli transaction policyid --script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script'
    policyID = subprocess.check_output(policyID,shell=True)
    policyID = policyID.decode('utf-8').replace('\n', '')
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    with open(path, 'w') as text:
        text.write(policyID)


def metadataCreation(homePath, mainTest, user, policyName, NFTDescription, NFTName, NFTID, NFTImageUrl, NFTRoyaltiesPercentage, NFTRoyaltiesAddress, NFTImageUrlThumbnail, artist):
    #Metadata Creation
    x=64
    if len(NFTImageUrl) > 64:
        NFTImageUrl=[NFTImageUrl[y-x:y] for y in range(x, len(NFTImageUrl)+x,x)]
    if len(NFTImageUrlThumbnail) > 64:
        NFTImageUrlThumbnail=[NFTImageUrlThumbnail[y-x:y] for y in range(x, len(NFTImageUrlThumbnail)+x,x)]
    NFTDescription = NFTDescription.replace("'", '*')
    if len(NFTDescription) > 64:
        NFTDescription=[NFTDescription[y-x:y] for y in range(x, len(NFTDescription)+x,x)]
    NFTRoyaltiesAddress=[NFTRoyaltiesAddress[y-x:y] for y in range(x, len(NFTRoyaltiesAddress)+x,x)]
    query = f'/home/yop/Downloads/cardano-node1.30.0/cardano-cli transaction policyid --script-file /home/yop/Downloads/cardano-node1.30.0/keys/{user}/{policyName}.script'
    policyID = subprocess.check_output(query,shell=True)
    policyID = policyID.decode('utf-8').replace('\n', '')
    artist = artist.replace('"', '')
    nft_name_no_space = NFTName
    nft_name_no_space = nft_name_no_space.replace(' ', '').replace('_', '')
    meta_nft_name = NFTName
    meta_nft_name = meta_nft_name.replace('_', ' ')
    metadata = {}


    # There are issues with capital letters as tags OR "Minting Plaform" instead of "mintingPlatform"
    metadata["777"] = {
                    "prc": "0.5",
                    "addr": "Testnet"
                    }
    metadata["721"] = {
                    policyID: {
                        nft_name_no_space: {
                            "name": "Cardano foundation NFT guide token",
                            "artist": "artist",
                            "image": "Url THUMBNAIL",
                            "mediaType": "image/png",
                            "description": "This is my first NFT thanks to the Cardano foundation",
                            "files": [{
                                "mediaType": "image/png",
                                "src": "Url NORMAL SIZE",
                                "name": "image name"
                                }],
                            "ID": 1,
                            "mintingPlatform": "https://adamagic.io",
                            }
                        },
                    "version": "1.0"
                    }
    
    metadata["721"][policyID][nft_name_no_space]["description"] = NFTDescription
    metadata["721"][policyID][nft_name_no_space]["name"] = meta_nft_name
    metadata["721"][policyID][nft_name_no_space]["ID"] = NFTID
    metadata["721"][policyID][nft_name_no_space]["image"] = NFTImageUrlThumbnail
    metadata["721"][policyID][nft_name_no_space]["files"][0]["src"] = NFTImageUrl
    metadata["721"][policyID][nft_name_no_space]["files"][0]["name"] = meta_nft_name
    metadata["721"][policyID][nft_name_no_space]["artist"] = artist
    metadata["777"]["prc"] = NFTRoyaltiesPercentage
    metadata["777"]["addr"] = NFTRoyaltiesAddress


    metadata = str(metadata)
    metadata = metadata.replace('\n', '')
    metadata = metadata.replace("'", '"')
    metadata = metadata.replace('*', "'")
    path = homePath + 'keys/' + user + '/' + policyID + NFTName + str(1) + 'metadata.json'
    with open(path, 'w') as text:
        text.write(metadata)

def metadataCreationWithOutRoyalties(homePath, mainTest, user, policyName, NFTDescription, NFTName, NFTID, NFTImageUrl, NFTImageUrlThumbnail, artist):
    #Metadata Creation
    x=64 
    if len(NFTImageUrl) > 64:
        NFTImageUrl=[NFTImageUrl[y-x:y] for y in range(x, len(NFTImageUrl)+x,x)]
    if len(NFTImageUrlThumbnail) > 64:
        NFTImageUrlThumbnail=[NFTImageUrlThumbnail[y-x:y] for y in range(x, len(NFTImageUrlThumbnail)+x,x)]
    NFTDescription = NFTDescription.replace("'", '*')
    if len(NFTDescription) > 64:
        NFTDescription=[NFTDescription[y-x:y] for y in range(x, len(NFTDescription)+x,x)]

    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    query = f'/home/yop/Downloads/cardano-node1.30.0/cardano-cli transaction policyid --script-file /home/yop/Downloads/cardano-node1.30.0/keys/{user}/{policyName}.script'
    policyID = subprocess.check_output(query,shell=True)
    policyID = policyID.decode('utf-8').replace('\n', '')
    artist = artist.replace('"', '')
    nft_name_no_space = NFTName
    nft_name_no_space = nft_name_no_space.replace(' ', '').replace('_', '')
    meta_nft_name = NFTName
    meta_nft_name = meta_nft_name.replace('_', ' ')
    metadata = {}
    metadata["721"] = {
                    policyID: {
                        nft_name_no_space: {
                            "name": "Cardano foundation NFT guide token",
                            "artist": "artist name",
                            "image": "Url THUMBNAIL",
                            "mediaType": "image/png",
                            "description": "This is my first NFT thanks to the Cardano foundation",
                            
                            "files": [{
                                "mediaType": "image/png",
                                "src": "Url NORMAL SIZE",
                                "name": "image name"
                                }],
                            "ID": 1,
                            "mintingPlatform": "https://adamagic.io",
                            }
                        },
                    "Version": "1.0"
                    }
    
    metadata["721"][policyID][nft_name_no_space]["description"] = NFTDescription
    metadata["721"][policyID][nft_name_no_space]["name"] = meta_nft_name
    metadata["721"][policyID][nft_name_no_space]["ID"] = NFTID
    metadata["721"][policyID][nft_name_no_space]["image"] = NFTImageUrlThumbnail
    metadata["721"][policyID][nft_name_no_space]["files"][0]["src"] = NFTImageUrl
    metadata["721"][policyID][nft_name_no_space]["files"][0]["name"] = meta_nft_name
    metadata["721"][policyID][nft_name_no_space]["artist"] = artist
    metadata = str(metadata)
    metadata = metadata.replace('\n', '')
    metadata = metadata.replace("'", '"')
    metadata = metadata.replace('*', "'")

    path = homePath + 'keys/' + user + '/' + policyID + NFTName + str(1) + 'metadata.json'
    with open(path, 'w') as text:
        text.write(metadata)

def mint(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, timeLock):
    #load policyID
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    with open(path, 'r') as text:
        policyID = text.read()
    #load currentSlot
    currentSlot = currentSlotD(homePath, mainTest)

    #Create Transaction
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)

    #Clean the info and get only what matters
    craftTx = cleanCraftTx(craftTx)
    txIn, funds = transactionGatherer(craftTx, 1500000)
    # print(craftTx)

    #This has to be fixed, gotta meke a def gathering all balance, which is some time
    NFTFlag = False
    try:
        #You want all the data starting at craftTx[5] y acabando en craftTx[-2]
        hiddenNFTs = []
        for x, data in enumerate(craftTx):
            if x >= 5:
                hiddenNFTs.append(data)
        hiddenNFTs.pop(-1)
        hiddenNFTs.pop(-1)
        oldNFTs = ''
        for x, data in enumerate(hiddenNFTs):
            if len(data) > 20:
                oldNFTs = oldNFTs + ' ' + data
            if data == '+':
                oldNFTs = oldNFTs + ' + '
            try:
                oldNFTs = oldNFTs + data + ' '
            except:
                pass


        amountPreviosNFT = craftTx[5]
        NFTHashAndName = craftTx[6]
        NFTFlag = True
        # print(NFTFlag, 'NFTFlag')

    except:
        pass


    fee = 30000
    output = str(int(funds) - fee)

    if NFTFlag == False:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)
    else:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + oldNFTs + \
        ' + ' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)


    # #2.2 Calculate fee
    fee = homePath + 'cardano-cli transaction calculate-min-fee --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 2 ' + mainTest + ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    fee = str(fee.decode('utf-8'))
    output = str(int(funds) - int(fee))
    # time.sleep(0.1)

    if NFTFlag == False:
        # #Make raw Transaction with real fee
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)
    else:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + oldNFTs + \
        ' + ' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)

    # #2.3 Sign the Transaction
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + \
    mainTest + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = subprocess.check_output(signTx,shell=True)

    # #Send the REAL Transaction
    sendRealTx = homePath + 'cardano-cli transaction submit' + \
    ' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest

    sendRealTx = subprocess.check_output(sendRealTx,shell=True)























def mintWithPlatformFee(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, timeLock):
    #We will allow you to mint and during the same transaction we will charge you 1 ADA
    #load policyID
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    with open(path, 'r') as text:
        policyID = text.read()
    #load currentSlot
    currentSlot = currentSlotD(homePath, mainTest)

    #Create Transaction
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)

    #Clean the info and get only what matters
    craftTx = cleanCraftTx(craftTx)
    txIn, funds = transactionGatherer(craftTx, 1500000)
    # print(craftTx)

    #This has to be fixed, gotta meke a def gathering all balance, which is some time
    TxHash = craftTx[0]
    TxIx = craftTx[1]
    funds = craftTx[2]
    NFTFlag = False
    try:
        #You want all the data starting at craftTx[5] y acabando en craftTx[-2]
        hiddenNFTs = []
        for x, data in enumerate(craftTx):
            if x >= 5:
                hiddenNFTs.append(data)
        hiddenNFTs.pop(-1)
        hiddenNFTs.pop(-1)
        oldNFTs = ''
        for x, data in enumerate(hiddenNFTs):
            if len(data) > 20:
                oldNFTs = oldNFTs + ' ' + data
            if data == '+':
                oldNFTs = oldNFTs + ' + '
            try:
                oldNFTs = oldNFTs + data + ' '
            except:
                pass


        amountPreviosNFT = craftTx[5]
        NFTHashAndName = craftTx[6]
        NFTFlag = True
        # print(NFTFlag, 'NFTFlag')

    except:
        pass


    fee = 30000
    output = str(int(funds) - fee)

    if NFTFlag == False:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --tx-out ' + walletRoyalty + '+' + str(toRoyaltyWallet) + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)
    else:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + walletRoyalty + '+' + str(toRoyaltyWallet) + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + oldNFTs + \
        ' + ' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)


    # #2.2 Calculate fee
    fee = homePath + 'cardano-cli transaction calculate-min-fee --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 2 ' + mainTest + ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    fee = str(fee.decode('utf-8'))
    output = str(int(funds) - int(fee))
    # time.sleep(0.1)

    if NFTFlag == False:
        # #Make raw Transaction with real fee
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + walletRoyalty + '+' + str(toRoyaltyWallet) + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)
    else:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + walletRoyalty + '+' + str(toRoyaltyWallet) + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + oldNFTs + \
        ' + ' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)

    # #2.3 Sign the Transaction
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + \
    mainTest + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = subprocess.check_output(signTx,shell=True)

    # #Send the REAL Transaction
    sendRealTx = homePath + 'cardano-cli transaction submit' + \
    ' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest

    sendRealTx = subprocess.check_output(sendRealTx,shell=True)

def transactionGatherer(craftTx, amountToSend):
    #Decode and clean Transactions
    craftTx = craftTx.decode('utf-8').replace('\n', ' ')
    craftTx = craftTx.split(' ')
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)

    #Order Transactions  
    txs = []
    temp = []
    for data in craftTx:
        if len(data) == 64:
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)#The last portion of data to append is outside of the loop and therefore needs an extra append by the end
    txs.pop(0)#First portion of data is garbage
    
    #Append all transactions until the target money to send is been reached
    availableTxs = []
    currentADA = 0
    for tx in txs:
        if currentADA >= int(amountToSend): continue
        try:#Prevents any tx with already minted NFTs in it
            tx[6]
            continue
        except:
            pass
        currentADA += int(tx[2])
        availableTxs.append(tx)

    transactionComplete = ''
    for singleTx in availableTxs:
        transactionComplete += ' --tx-in ' + singleTx[0] + '#' + singleTx[1]
    print(currentADA)
    return transactionComplete, currentADA

def transactionGatherer1(craftTx, amountToSend):
    #Decode and clean Transactions
    
    #Append all transactions until the target money to send is been reached
    availableTxs = []
    currentADA = 0
    for tx in craftTx:
        # print(tx)
        if currentADA >= int(amountToSend): continue
        try:#Prevents any tx with already minted NFTs in it
            tx[6]
            continue
        except:
            currentADA += int(tx[2])
            availableTxs.append(tx)
        # if int(tx[2]) >= int(amountToSend):
            
    transactionComplete = ''
    for singleTx in availableTxs:
        transactionComplete += ' --tx-in ' + singleTx[0] + '#' + singleTx[1]

    return transactionComplete, currentADA

def transactionGatherer2(craftTx, amountToSend):
    #Decode and clean Transactions
    craftTx = craftTx.decode('utf-8').replace('\n', ' ')
    craftTx = craftTx.split(' ')
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)

    #Order Transactions  
    txs = []
    temp = []
    for data in craftTx:
        if ((len(data) == 64) and ('.' not in data)):
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)#The last portion of data to append is outside of the loop and therefore needs an extra append by the end
    txs.pop(0)#First portion of data is garbage

    #Append all transactions until the target money to send is been reached
    availableTxs = []
    currentADA = 0
    
    for tx in txs:
        if currentADA >= int(amountToSend): continue
        try:#Prevents any tx with already minted NFTs in it
            tx[6]
            continue
        except:#make sure all txs are without minted
            try:
                int(tx[2])
            except:
                pass
            currentADA += int(tx[2])
            availableTxs.append(tx)

    transactionComplete = ''
    for singleTx in availableTxs:
        transactionComplete += ' --tx-in ' + singleTx[0] + '#' + singleTx[1]

    return transactionComplete, currentADA

def transactionGathererForMintingTokens(craftTx, amountToSend, tokenHash):
    #Decode and clean Transactions
    craftTx = craftTx.decode('utf-8').replace('\n', ' ')
    craftTx = craftTx.split(' ')
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)

    #Order Transactions  
    txs = []
    temp = []
    for data in craftTx:
        if len(data) == 64:
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)#The last portion of data to append is outside of the loop and therefore needs an extra append by the end
    txs.pop(0)#First portion of data is garbage
    
    #Append one transactions until the target money to send is been reached
    availableTxs = []
    currentADA = 0
    for tx in txs:
        if currentADA >= amountToSend: continue
        try:
            # print(tx[6], 'tx6')
            if tokenHash in tx[6]:
                currentADA += int(tx[2])
                # print(currentADA, 'currentADA')
                availableTxs.append(tx)
        except:
            pass


    transactionComplete = ''
    for singleTx in availableTxs:
        transactionComplete += ' --tx-in ' + singleTx[0] + '#' + singleTx[1]
        break

    return transactionComplete, currentADA

def transactionGathererForMintingTokens1(craftTx, amountToSend, tokenHash):
    #Decode and clean Transactions
    craftTx = craftTx.decode('utf-8').replace('\n', ' ')
    craftTx = craftTx.split(' ')
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)

    #Order Transactions  
    txs = []
    temp = []
    for data in craftTx:
        if len(data) == 64:
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)#The last portion of data to append is outside of the loop and therefore needs an extra append by the end
    txs.pop(0)#First portion of data is garbage
    
    #Append one transactions until the target money to send is been reached
    availableTxs = []
    currentADA = 0
    for tx in txs:
        if currentADA >= amountToSend: continue
        try:
            # print(tx[6], 'tx6')
            if tokenHash in tx[6]:
                currentADA += int(tx[2])
                # print(currentADA, 'currentADA')
                availableTxs.append(tx)
        except:
            pass

    transactionComplete = ''
    for singleTx in availableTxs:
        transactionComplete += ' --tx-in ' + singleTx[0] + '#' + singleTx[1]
        break

    return transactionComplete, currentADA


def transactionGathererToSendNFT(homePath, user, craftTx, NFTName, policyName, amountToSend):
    #Decode and clean Transactions
    craftTx = craftTx.decode('utf-8').replace('\n', ' ')
    craftTx = craftTx.split(' ')
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)

    #find policyID

    with open(homePath + 'keys/' + user + '/' + policyName + '.txt', 'r') as text:
        policyID = text.read()

    #Order Transactions  
    txs = []
    temp = []
    for data in craftTx:
        if ((len(data) == 64) and ('.' not in data)):
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)#The last portion of data to append is outside of the loop and therefore needs an extra append by the end
    txs.pop(0)#First portion of data is garbage
    
    NFTTx = []
    for tx in txs:
        try:
            if ((policyID in tx[6]) and (NFTName in tx[6])):
                NFTTx = tx
        except:
            pass
    # #Append all transactions until the target money to send is been reached
    availableTxs = []
    currentADA = 0
    for tx in txs:
        if currentADA >= int(amountToSend): continue
        try:#Prevents any tx with already minted NFTs in it
            tx[6]
        except:
            currentADA += int(tx[2])
            availableTxs.append(tx)

    transactionComplete = ''
    transactionComplete += ' --tx-in ' + NFTTx[0] + '#' + NFTTx[1]
    for singleTx in availableTxs:
        transactionComplete += ' --tx-in ' + singleTx[0] + '#' + singleTx[1]

    return transactionComplete, int(currentADA) + int(NFTTx[2]), policyID


def sendSimpleTransaction(homePath, mainTest, user, userAddress, amountToSend, walletReveiver):
    #Gather basic info
    # print(userAddress, 'userAddress')
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)
    txIn, funds = transactionGatherer(craftTx, amountToSend)
    NumberOfTxIn = len(txIn.split('--'))-1
    fee = 30000
    currentSlot = currentSlotD(homePath, mainTest)
    ttl = str(int(currentSlot) + 2000)
    output = str(int(funds) - int(amountToSend) - int(fee))
    
    #Create draft
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(amountToSend) + \
    ' --tx-out ' + userAddress + '+' + output + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)

    #calculate fee
    feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/tx.draft' + \
    ' --tx-in-count ' + str(NumberOfTxIn) + \
    ' --tx-out-count 2' + \
    ' --witness-count ' + str(NumberOfTxIn) + \
    ' --byron-witness-count 0 ' + \
    mainTest + \
    ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json'
    feeCalculation = subprocess.check_output(feeCalculation,shell=True)
    feeCalculation = feeCalculation.decode('utf-8')
    fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')
    
    output = str(int(funds) - int(amountToSend) - int(fee))

    #Create draft with real fee
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(amountToSend) + \
    ' --tx-out ' + userAddress + '+' + output + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)


    #sign the motherfucker
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey ' + \
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


def send_ada_for_platform_users(homePath, mainTest, user, userAddress, amountToSend, walletReveiver):
    #Gather basic info
    # print(userAddress, 'userAddress')
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)
    txIn, funds = transactionGatherer(craftTx, amountToSend)
    NumberOfTxIn = len(txIn.split('--'))-1
    fee = 30000
    currentSlot = currentSlotD(homePath, mainTest)
    ttl = str(int(currentSlot) + 2000)
    output = str(int(funds) - int(amountToSend) - int(fee))
    output = str(int(amountToSend) - int(fee))
    
    #Create draft
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(output) + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)

    #calculate fee
    feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/tx.draft' + \
    ' --tx-in-count ' + str(NumberOfTxIn) + \
    ' --tx-out-count 2' + \
    ' --witness-count ' + str(NumberOfTxIn) + \
    ' --byron-witness-count 0 ' + \
    mainTest + \
    ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json'
    feeCalculation = subprocess.check_output(feeCalculation,shell=True)
    feeCalculation = feeCalculation.decode('utf-8')
    fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')
    
    output = str(int(funds) - int(amountToSend) - int(fee))
    output = str(int(amountToSend) - int(fee))

    #Create draft with real fee
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(output) + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)


    #sign the motherfucker
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey ' + \
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


def send_ada_penalized_transaction_vending_machine(homePath, mainTest, user, userAddress, amountToSend, walletReveiver, tx_hash, tx_in):
    
    #Gather basic info
    fee = 30000
    currentSlot = currentSlotD(homePath, mainTest)
    ttl = str(int(currentSlot) + 2000)
    receive_back =  str(int(amountToSend) - int(fee))
    
    #Create draft
    draft = homePath + 'cardano-cli transaction build-raw ' + \
    f'--tx-in {tx_hash}#{tx_in}' + \
    ' --tx-out ' + walletReveiver + '+' + str(receive_back) + \
    ' --tx-out ' + userAddress + '+' + '0' + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    f' --out-file /home/yop/Downloads/cardano/vending_machine/{project_name}/tx.draft'
    draft = subprocess.check_output(draft,shell=True)

    #calculate fee
    feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/tx.draft' + \
    ' --tx-in-count ' + str(1) + \
    ' --tx-out-count 2' + \
    ' --witness-count ' + str(1) + \
    ' --byron-witness-count 0 ' + \
    mainTest + \
    f' --protocol-params-file /home/yop/Downloads/cardano/vending_machine/{project_name}/protocol.json'
    feeCalculation = subprocess.check_output(feeCalculation,shell=True)
    feeCalculation = feeCalculation.decode('utf-8')
    fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')
    
    receive_back =  str(int(amountToSend) - int(fee))

    #Create draft with real fee
    draft = homePath + 'cardano-cli transaction build-raw ' + \
    f'--tx-in {tx_hash}#{tx_in}' + \
    ' --tx-out ' + walletReveiver + '+' + str(receive_back) + \
    ' --tx-out ' + userAddress + '+' + '0' + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    f' --out-file /home/yop/Downloads/cardano/vending_machine/{project_name}/tx.draft'
    draft = subprocess.check_output(draft,shell=True)


    #sign the motherfucker
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey ' + \
    mainTest + \
    f' --tx-body-file /home/yop/Downloads/cardano/vending_machine/{project_name}/tx.draft' + \
    f' --out-file /home/yop/Downloads/cardano/vending_machine/{project_name}/matx.signed'
    signTx = signTx.replace('\n', '')
    signTx = subprocess.check_output(signTx,shell=True)

    #Send the REAL Transaction
    sendRealTx = homePath + 'cardano-cli transaction submit' + \
    ' --tx-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/matx.signed ' + mainTest
    sendRealTx = sendRealTx.replace('\n', '')
    sendRealTx = subprocess.check_output(sendRealTx,shell=True)
    print('TX done')


def send_ada_penalized_transaction_single_nft(homePath, mainTest, username, single_nft, amountToSend, walletReveiver, tx_hash, tx_in):
    try:
        #Gather basic info
        fee = str(30000)
        currentSlot = currentSlotD(homePath, mainTest)
        ttl = str(int(currentSlot) + 2000)
        receive_back = str(int(amountToSend) - int(fee))

        #Create draft
        draft = homePath + 'cardano-cli transaction build-raw ' + \
        f'--tx-in {tx_hash}#{tx_in}' + \
        ' --tx-out ' + walletReveiver + '+' + str(receive_back) + \
        ' --invalid-hereafter '+ ttl + \
        ' --fee ' + str(fee) + \
        f' --out-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/tx.draft'
        draft = subprocess.check_output(draft,shell=True)

        #calculate fee
        feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
        ' --tx-body-file ' + f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/tx.draft' + \
        ' --tx-in-count ' + str(1) + \
        ' --tx-out-count 2' + \
        ' --witness-count ' + str(1) + \
        ' --byron-witness-count 0 ' + \
        mainTest + \
        f' --protocol-params-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/protocol.json'
        feeCalculation = subprocess.check_output(feeCalculation,shell=True)
        feeCalculation = feeCalculation.decode('utf-8')
        fee = feeCalculation.replace(' Lovelace\n', '')
        
        receive_back = str(int(amountToSend) - int(fee))

        #Create draft with real fee
        draft = homePath + 'cardano-cli transaction build-raw ' + \
        f'--tx-in {tx_hash}#{tx_in}' + \
        ' --tx-out ' + walletReveiver + '+' + str(receive_back) + \
        ' --invalid-hereafter '+ ttl + \
        ' --fee ' + str(fee) + \
        f' --out-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/tx.draft'
        draft = subprocess.check_output(draft,shell=True)


        # Sign the motherfucker
        #' --signing-key-file ' + f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/{single_nft}.skey ' + \
        signTx = homePath + 'cardano-cli transaction sign' + \
        ' --signing-key-file ' + f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/{single_nft}.skey ' + \
        mainTest + \
        f' --tx-body-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/tx.draft' + \
        f' --out-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/matx.signed'
        signTx = signTx.replace('\n', '')
        signTx = subprocess.check_output(signTx,shell=True)

        # Send the REAL Transaction
        sendRealTx = homePath + 'cardano-cli transaction submit' + \
        ' --tx-file ' + f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/matx.signed ' + mainTest
        sendRealTx = sendRealTx.replace('\n', '')
        sendRealTx = subprocess.check_output(sendRealTx,shell=True)

        return True

    except Exception as e:
        return e


def send_extra_ada_penalized_transaction_single_nft(homePath, mainTest, username, single_nft, amountToSend, walletReveiver, tx_hash, tx_in, buyer_address, price):
    try:
        #Gather basic info
        fee = str(30000)
        currentSlot = currentSlotD(homePath, mainTest)
        ttl = str(int(currentSlot) + 2000)
        receive_back = str(int(amountToSend) - int(fee) - int(price))
        output = str(int(amountToSend) - int(receive_back) - int(fee))
        
        # print(f'''
        #     out {output}
        #     receive_back {receive_back}
        #     amountToSend {amountToSend}
        #     fee {fee}
        #     ''')

        #Create draft
        draft = homePath + 'cardano-cli transaction build-raw ' + \
        f'--tx-in {tx_hash}#{tx_in}' + \
        ' --tx-out ' + walletReveiver + '+' + str(output) + \
        ' --tx-out ' + buyer_address + '+' + str(receive_back) + \
        ' --invalid-hereafter '+ ttl + \
        ' --fee ' + str(fee) + \
        f' --out-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/tx.draft'
        draft = subprocess.check_output(draft,shell=True)

        #calculate fee
        feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
        ' --tx-body-file ' + f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/tx.draft' + \
        ' --tx-in-count ' + str(1) + \
        ' --tx-out-count 2' + \
        ' --witness-count ' + str(1) + \
        ' --byron-witness-count 0 ' + \
        mainTest + \
        f' --protocol-params-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/protocol.json'
        feeCalculation = subprocess.check_output(feeCalculation,shell=True)
        feeCalculation = feeCalculation.decode('utf-8')
        fee = feeCalculation.replace(' Lovelace\n', '')
        
        receive_back = str(int(amountToSend) - int(fee) - int(price))
        output = str(int(amountToSend) - int(receive_back) - int(fee))
        
        #Create draft
        draft = homePath + 'cardano-cli transaction build-raw ' + \
        f'--tx-in {tx_hash}#{tx_in}' + \
        ' --tx-out ' + walletReveiver + '+' + str(output) + \
        ' --tx-out ' + buyer_address + '+' + str(receive_back) + \
        ' --invalid-hereafter '+ ttl + \
        ' --fee ' + str(fee) + \
        f' --out-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/tx.draft'
        draft = subprocess.check_output(draft,shell=True)


        # Sign the motherfucker
        #' --signing-key-file ' + f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/{single_nft}.skey ' + \
        signTx = homePath + 'cardano-cli transaction sign' + \
        ' --signing-key-file ' + f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/{single_nft}.skey ' + \
        mainTest + \
        f' --tx-body-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/tx.draft' + \
        f' --out-file /home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/matx.signed'
        signTx = signTx.replace('\n', '')
        signTx = subprocess.check_output(signTx,shell=True)

        # Send the REAL Transaction
        sendRealTx = homePath + 'cardano-cli transaction submit' + \
        ' --tx-file ' + f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/matx.signed ' + mainTest
        sendRealTx = sendRealTx.replace('\n', '')
        sendRealTx = subprocess.check_output(sendRealTx,shell=True)

        return True

    except Exception as e:
        return e


def sendNFT(homePath, mainTest, user, walletReveiver, NFTName, policyName):
    userAddress = loadAddress(homePath, user)

    #Gather basic info
    craftTx                 = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx                 = subprocess.check_output(craftTx,shell=True)
    fee                     = 300000
    amountToSend            = 1500000 + fee
    dummy                   = amountToSend + fee

    #Get the NFT tx
    txIn, funds, policyID   = transactionGathererToSendNFT(homePath, user, craftTx, NFTName, policyName)
    NumberOfTxIn            = len(txIn.split('--'))-1
    currentSlot             = currentSlotD(homePath, mainTest)
    ttl                     = str(int(currentSlot) + 200)
    output                  = str(int(funds) - int(amountToSend) - int(fee))
    
    #Create draft
    draft                   = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(amountToSend) + '+"1 ' + policyID + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + output + '+"0 ' + policyID + '.' + NFTName + '"' +  \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)

    #calculate fee
    feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/tx.draft' + \
    ' --tx-in-count ' + str(NumberOfTxIn) + \
    ' --tx-out-count 2' + \
    ' --witness-count ' + str(NumberOfTxIn) + \
    ' --byron-witness-count 0 ' + \
    mainTest + \
    ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json'
    feeCalculation = subprocess.check_output(feeCalculation,shell=True)
    feeCalculation = feeCalculation.decode('utf-8')
    fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')
    
    output = str(int(funds) - int(amountToSend) - int(fee))
    #TO DO
    #for some reason the amount to send to the walletReceiver is the sum of the amount to send and fee

    #Create draft with real fee
    raft                    = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(amountToSend) + '+"1 ' + policyID + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + output + '+"0 ' + policyID + '.' + NFTName + '"' +  \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)


    #sign the motherfucker
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey ' + \
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


def send_single_nft(homePath, mainTest, user, walletReveiver, NFTName, policyName, ADAMagic_fee, money_reminder, ADAMagic_wallet, nft_price, nft_utxo, nft_txin, ada_sent, nft_address, policy_id, tx_in, tx_hash):
    userAddress = loadAddress(homePath, user)

    #Gather basic info
    craftTx                 = homePath + 'cardano-cli query utxo --address ' + nft_address + ' ' + mainTest
    craftTx                 = subprocess.check_output(craftTx,shell=True)
    ADAMagic_fee            = int(ADAMagic_fee)

    nft_price               = int(nft_price)
    fee                     = 300000
    buyer_back              = int(money_reminder)
    amountToSend            = int(buyer_back) + int(fee) + int(ADAMagic_fee) + nft_price

    #Get the NFT tx
    txIn, funds, policyID   = nft_txin, ada_sent, policy_id
    policyID = policyID.replace('\n', '')
    NumberOfTxIn            = len(txIn.split('--'))  # There used to be a -1 at the end because the original did not include the external utx in from the NFT
    currentSlot             = currentSlotD(homePath, mainTest)
    ttl                     = str(int(currentSlot) + 200)
    output                  = str(int(funds) - int(buyer_back) - int(fee) - int(ADAMagic_fee))
    constant_nft_price      = 1500000
    
    buyer_back = str(int(funds) - int(nft_price))
    
    if int(money_reminder) >= 1000000:
        tx_out = f' --tx-out {walletReveiver}+{money_reminder} '
    else:
        tx_out = ''
    output = str(int(funds) - int(buyer_back) - int(fee) - int(ADAMagic_fee) - constant_nft_price)

    #Create draft
    draft                   = homePath + 'cardano-cli transaction build-raw' + \
    f' --tx-in {tx_hash}#{tx_in}' + \
    ' --tx-out ' + walletReveiver + '+' + str(constant_nft_price + int(buyer_back)) + '+"1 ' + policyID + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + output + '+"0 ' + policyID + '.' + NFTName + '"' +  \
    ' --tx-out ' + ADAMagic_wallet + '+' + str(ADAMagic_fee) + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)

    #calculate fee
    feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/tx.draft' + \
    ' --tx-in-count ' + str(NumberOfTxIn) + \
    ' --tx-out-count 2' + \
    ' --witness-count ' + str(NumberOfTxIn) + \
    ' --byron-witness-count 0 ' + \
    mainTest + \
    ' --protocol-params-file ' + f'/home/yop/Downloads/cardano/single_nfts/{user}/{NFTName}/protocol.json'
    feeCalculation = subprocess.check_output(feeCalculation,shell=True)
    feeCalculation = feeCalculation.decode('utf-8')
    fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')
    
    output = str(int(funds) - int(buyer_back) - int(fee) - int(ADAMagic_fee) - constant_nft_price)

    print(f'''
    Output2:
    funds {funds}
    nft_price {nft_price}
    buyer_back {int(buyer_back)}
    ADAMagic_fee {ADAMagic_fee}
    fee {fee}
    output {output}
    constant_nft {constant_nft_price}
    ''')


    #Create draft with real ADA
    draft                   = homePath + 'cardano-cli transaction build-raw' + \
    f' --tx-in {tx_hash}#{tx_in}' + \
    ' --tx-out ' + walletReveiver + '+' + str(constant_nft_price + int(buyer_back)) + '+"1 ' + policyID + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + output + '+"0 ' + policyID + '.' + NFTName + '"' +  \
    ' --tx-out ' + ADAMagic_wallet + '+' + str(ADAMagic_fee) + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'

    draft = subprocess.check_output(draft,shell=True)


    #sign the motherfucker
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + f'/home/yop/Downloads/cardano/single_nfts/{user}/{NFTName}/{NFTName}.skey ' + \
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


def sendSimpleTransactionWithRoyalties(homePath, mainTest, user, userAddress, amountToSend, walletReveiver, walletRoyalty, amountToSendRoyalty, platformAddress, platformFee):
    #Gather basic info
    # print(userAddress, 'userAddress')
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)
    txIn, funds = transactionGatherer(craftTx, amountToSend)
    NumberOfTxIn = len(txIn.split('--'))-1
    fee = 30000
    currentSlot = currentSlotD(homePath, mainTest)
    ttl = str(int(currentSlot) + 200)
    output = str(int(funds) - int(amountToSend) - int(fee) - int(platformFee) - str(amountToSendRoyalty))
    
    #Create draft
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(amountToSend) + \
    ' --tx-out ' + userAddress + '+' + output + \
    ' --tx-out ' + walletRoyalty + '+' + str(amountToSendRoyalty) + \
    ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)

    #calculate fee
    feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/tx.draft' + \
    ' --tx-in-count ' + str(NumberOfTxIn) + \
    ' --tx-out-count 4' + \
    ' --witness-count ' + str(NumberOfTxIn) + \
    ' --byron-witness-count 0 ' + \
    mainTest + \
    ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json'
    feeCalculation = subprocess.check_output(feeCalculation,shell=True)
    feeCalculation = feeCalculation.decode('utf-8')
    fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')
    
    output = str(int(funds) - int(amountToSend) - int(fee))

    #Create draft with real fee
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(amountToSend) + \
    ' --tx-out ' + userAddress + '+' + output + \
    ' --tx-out ' + walletRoyalty + '+' + str(amountToSendRoyalty) + \
    ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)


    #sign the motherfucker
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey ' + \
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

def sendSimpleTransactionWithOutRoyalties(homePath, mainTest, user, userAddress, amountToSend, walletReveiver, platformAddress, platformFee):
    #Gather basic info
    # print(userAddress, 'userAddress')
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)
    txIn, funds = transactionGatherer(craftTx, amountToSend)
    NumberOfTxIn = len(txIn.split('--'))-1
    fee = 30000
    currentSlot = currentSlotD(homePath, mainTest)
    ttl = str(int(currentSlot) + 200)
    output = str(int(funds) - int(amountToSend) - int(fee) - int(platformFee))
    #Create draft
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(amountToSend) + \
    ' --tx-out ' + userAddress + '+' + output + \
    ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)

    #calculate fee
    feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/tx.draft' + \
    ' --tx-in-count ' + str(NumberOfTxIn) + \
    ' --tx-out-count 3' + \
    ' --witness-count ' + str(NumberOfTxIn) + \
    ' --byron-witness-count 0 ' + \
    mainTest + \
    ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json'
    feeCalculation = subprocess.check_output(feeCalculation,shell=True)
    feeCalculation = feeCalculation.decode('utf-8')
    fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')
    
    output = str(int(funds) - int(amountToSend) - int(fee) - int(platformFee))

    #Create draft with real fee
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(amountToSend) + \
    ' --tx-out ' + userAddress + '+' + output + \
    ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)


    #sign the motherfucker
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey ' + \
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

def sendRoyaltyTransaction(homePath, mainTest, user, userAddress, amountToSend, walletReveiver, walletRoyalty, royaltyPercentage):
    #Gather basic info
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)
    txIn, funds = transactionGatherer(craftTx, amountToSend)
    NumberOfTxIn = len(txIn.split('--'))-1
    fee = 30000
    currentSlot = currentSlotD(homePath, mainTest)
    ttl = str(int(currentSlot) + 200)
    toRoyaltyWallet = int(round((royaltyPercentage * int(amountToSend)),0))
    toReceiverWallet = int(int(amountToSend) - toRoyaltyWallet)

    output = str(int(funds) - int(amountToSend) - int(fee))
    
    #Create draft
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(toReceiverWallet) + \
    ' --tx-out ' + walletRoyalty + '+' + str(toRoyaltyWallet) + \
    ' --tx-out ' + userAddress + '+' + output + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)

    #calculate fee
    feeCalculation = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/tx.draft' + \
    ' --tx-in-count ' + str(NumberOfTxIn) + \
    ' --tx-out-count 2' + \
    ' --witness-count ' + str(NumberOfTxIn) + \
    ' --byron-witness-count 0 ' + \
    mainTest + \
    ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json'
    feeCalculation = subprocess.check_output(feeCalculation,shell=True)
    feeCalculation = feeCalculation.decode('utf-8')
    fee = feeCalculation.replace(' Lovelace\n', '')#.replace(' Lovelace', '').replace('\n', '')
    
    output = str(int(funds) - int(amountToSend) - int(fee))

    #Create draft with real fee
    draft = homePath + 'cardano-cli transaction build-raw' + \
    txIn + \
    ' --tx-out ' + walletReveiver + '+' + str(toReceiverWallet) + \
    ' --tx-out ' + walletRoyalty + '+' + str(toRoyaltyWallet) + \
    ' --tx-out ' + userAddress + '+' + output + \
    ' --invalid-hereafter '+ ttl + \
    ' --fee ' + str(fee) + \
    ' --out-file ' + homePath + 'keys/' + user + '/tx.draft'
    draft = subprocess.check_output(draft,shell=True)


    #sign the motherfucker
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey ' + \
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


def mintNFT(homePath, mainTest, user, policyName, ):

    #1 create wallet
    # createWallet(homePath, mainTest, user, passPhrase)

    #2 load user
    # userAddress = loadAddress(homePath, user)

    #3 export parameters
    exportParams(homePath, mainTest, user, userAddress)

    #4 generate policy Singing files (skey, vkey)
    generatePolicy(homePath, mainTest, user, policyName)

    #5 create new policy
    createNewPolicy(homePath, mainTest, user, policyName, timeLock)

    #6 create new policyID
    createPolicyID(homePath, mainTest, user, policyName)

    #7 create metadata
    metadataCreation(homePath, mainTest, user, policyName, NFTDescription, NFTName, NFTID, NFTImageUrl, NFTRoyaltiesPercentage, NFTRoyaltiesAddress)

    #8 mint that shit
    mint(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, timeLock)


def check_if_noname_token_is_half_minted(policy_id, wallet_address):
    query = f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_51_check_simple_balance.py {wallet_address}'
    query = subprocess.check_output(query,shell=True)
    query = query.decode('utf-8')
    query = query.split('\n')
    for elem in query:
        elem = elem.split(' ')
        for single_value in elem:
            # Check for no name token. It has the policy id in it and no '.nft_name'
            # Tokens have: policy_id.nft_name
            if ((policy_id in single_value) and ('.' not in single_value)):
                return True
    return False







user = "testo"
passPhrase = '1234567890'
policyName = "Fest-policy"#Policies CANNOT have spaces
timeLock = 10000
NFTDescription = "First in the class"
NFTName = "FirTstNFTminted"#NFTName cannot have spaces either???? 
NFTID = 12
NFTImageUrl = "QmY2J8wWT4xpK3qAHmurGoZRhZtiXu62EvNVHJe34WFfKn"
NFTRoyaltiesPercentage = "0.15"
NFTRoyaltiesAddress = "addr_test1vp4hl8hdksyl720g5v087jpja5u6jphs24eenhllhlalfkqnc9vz6"
NFTAmount = "1"
# userAddress = loadAddress(homePath, user)











#mintNFT()
walletReveiver = 'addr_test1qzhx2hj7lctz033fh7schveujs0y3c64q70wrlt763pxvt29thnazclfq274u9l74cjre46as2rpn3jwx7xw8vxy8haslasp6m'
walletRoyalty =  'addr_test1vp4hl8hdksyl720g5v087jpja5u6jphs24eenhllhlalfkqnc9vz6'
# print(balance(homePath, mainTest, walletReveiver), 'receiver')
# print(balance(homePath, mainTest, walletRoyalty), 'royalty')
# print(balance(homePath, mainTest, userAddress), 'user')
username = user
password = '1234'
# connectDBCreateNewUser('test1', password)
# sys.exit()
# sendRoyaltyTransaction(homePath, mainTest, user, userAddress, '5000000', walletReveiver, walletRoyalty, 0.2)











def sendTokens(homePath, mainTest, user, userAddress, policyName, walletReceiver):
    #3 SEND TOKENS
    fee = 30000
    receiver=walletReceiver
    receiver_output="1500000"

    #Gather basic info
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    with open(path, 'r') as text:
        policyID = text.read()
    # print('policyID:', policyID)
    # with open(homePath + 'keys/' + user + '/' + policyName + '.script', 'r') as read:
        # print('policy script:', read.read())
    # policyIDDoubleCheck = homePath + 'cardano-cli transaction policyid --script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script'
    # policyIDDoubleCheck = subprocess.check_output(policyIDDoubleCheck,shell=True)
    # policyIDDoubleCheck = policyIDDoubleCheck.decode('utf-8').replace('\n', '')
    # print('policyIDDoubleCheck', policyIDDoubleCheck)
    # currentSlot = currentSlotD(homePath, mainTest)
    # timeLock = 10000

    #2.1 Make raw Transaction with OUT real fee
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)
    # print(craftTx.decode('utf-8'))
    #Clean the info and get only what matters
    probableAmountToMintToken = fee + int(receiver_output)
    txIn, funds = transactionGathererForMintingTokens(craftTx, probableAmountToMintToken, policyID)
    # print('Sending Token')
    NumberOfTxIn = len(txIn.split('--'))-1
    output = str(int(funds) - fee)
    # print('funds:', funds)
    # print('output',output)

    totalTokens = "1"
    tokensToGive = "1"
    tokensLeft = str(int(totalTokens) - int(tokensToGive))
    output = str(int(funds) - int(receiver_output) - int(fee))

    #Check if policyID was created:
    try:
        path = homePath + 'keys/' + user + '/' + policyName + '.txt'
        with open(path, 'r') as text:
            policyID = text.read()
            policyID = str(policyID)
    except:
        policyID = None

    #3.1Build raw Transaction
    buildRaw = homePath + 'cardano-cli transaction build-raw --fee ' + str(fee) + txIn + \
    ' --tx-out ' + receiver + '+' + receiver_output + '+"' + tokensToGive + ' ' + policyID + '"' \
    ' --tx-out ' + userAddress + '+' + output + '+"' + tokensLeft + ' ' + policyID + '"' \
    ' --out-file ' + homePath + 'keys/' + user + '/rec_matx.raw'
    buildRaw = buildRaw.replace('\n', '')
    buildRaw = subprocess.check_output(buildRaw,shell=True)

    #3.2 Calculate fee
    fee = homePath + 'cardano-cli transaction calculate-min-fee --tx-body-file ' + homePath + 'keys/' + user + '/rec_matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 2 ' + mainTest + ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    fee = str(fee.decode('utf-8'))
    fee = fee.replace('\n', '')
    output = str(int(funds) - int(receiver_output) - int(fee))

    #3.3 Update Transaction, sign, send
    #Update
    buildRaw = homePath + 'cardano-cli transaction build-raw  --fee ' + str(fee) + txIn + \
    ' --tx-out ' + receiver + '+' + receiver_output + '+"' + tokensToGive + ' ' + policyID + '"' \
    ' --tx-out ' + userAddress + '+' + output + '+"' + tokensLeft + ' ' + policyID + '"' + \
    ' --out-file ' + homePath + 'keys/' + user + '/rec_matx.raw'
    buildRaw = buildRaw.replace('\n', '')
    buildRaw = subprocess.check_output(buildRaw,shell=True)

    #Sign
    signTx = homePath + 'cardano-cli transaction sign --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + mainTest + ' --tx-body-file ' + homePath + 'keys/' + user + '/rec_matx.raw --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = subprocess.check_output(signTx,shell=True)

    #Send
    sendRealTx = homePath + 'cardano-cli transaction submit --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest
    sendRealTx = subprocess.check_output(sendRealTx,shell=True)






#YOU HAVE TO SELECT THE HASHID AND TOKEN ID IN ORFER TO MAKE A GOOD TRANSACTION
#tHE PROGRAM FAILS BECAUSE IT TAKES THE LAST TX INSTEAD OF THE RIGHT ONE
#SHOULD FIX transactionGathererForMintingTokens



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
    # print(craftTx.decode('utf-8'))
    #Clean the info and get only what matters
    fee = 300000
    if amountToMint == 1:
        craftTx2 = craftTx.decode('utf-8')
        if policyID in craftTx2:
            print(f'Token already created, exiting function. Amount to mint: {amountToMint}')
            return
        txIn, funds = transactionGatherer2(craftTx, fee + 15000000)
        # print(txIn)
        # print('Creating Token')
    if amountToMint == -1:
        txIn, funds = transactionGathererForMintingTokens1(craftTx, fee, policyID)
        # print('Burning Token')
    NumberOfTxIn = len(txIn.split('--'))-1
    output = str(int(funds) - int(fee))
    # print('funds:', funds)
    # print('output',output)
    # print(txIn)




    # #create raw file
    getRawTx = homePath + 'cardano-cli transaction build-raw --fee ' + str(fee) + \
    txIn + \
    ' --tx-out ' + userAddress + '+' +  output + '+"' + str(totalTokenAmmount) + ' ' + policyID + '"' + \
    ' --mint="' + str(amountToMint) + ' ' + policyID + '"' + \
    ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
    ' --invalid-hereafter ' + str(herafter) + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
    getRawTx = getRawTx.replace('\n', '')
    # print(getRawTx)

    getRawTx = subprocess.check_output(getRawTx,shell=True)
    getRawTx1 = getRawTx.decode('utf-8')
    getRawTx1 = getRawTx1.split('--tx-in')


    # #2.2 Calculate fee
    txins1 = len(getRawTx1)
    fee = homePath + 'cardano-cli transaction calculate-min-fee' + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' +\
    ' --tx-in-count ' + str(txins1) + \
    ' --tx-out-count 1' + \
    ' --witness-count ' + str(txins1) + ' ' + \
    mainTest + \
    ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    
    fee = fee.decode('utf-8')
    fee = fee.replace('\n', ' ')
    output = str(int(funds) - int(fee))
    print(funds, fee, 'funds, fee')

    # #Make raw Transaction with real fee
    getRawTx = homePath + 'cardano-cli transaction build-raw --fee ' + str(fee) + \
    txIn + \
    ' --tx-out ' + userAddress + '+' +  output + '+"' + str(totalTokenAmmount) + ' ' + policyID + '"' + \
    ' --mint="' + str(amountToMint) + ' ' + policyID + '"' + \
    ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
    ' --invalid-hereafter ' + str(herafter) + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
    getRawTx = getRawTx.replace('\n', '')
    getRawTx = subprocess.check_output(getRawTx,shell=True)


    # #2.3 Sign the Transaction
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey' +\
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + \
    mainTest + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' +\
    ' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = subprocess.check_output(signTx,shell=True)

    # #Send the REAL Transaction
    sendRealTx = homePath + 'cardano-cli transaction submit' + \
    ' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest
    sendRealTx = subprocess.check_output(sendRealTx,shell=True)


def checkForCreatedDeletedNoNameToken(homePath, mainTest, user, userAddress, policyName, createBurn):
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    with open(path, 'r') as text:
        policyID = text.read()

    # Create token
    if createBurn == 0:
        while True:
            txs = balance(homePath, mainTest, userAddress)
            if policyID in txs:
                return
            time.sleep(1)

    # Burn token
    if createBurn == 1:
        while True:
            txs = balance(homePath, mainTest, userAddress)
            # print(txs)
            # txs = txs.decode('utf-8')
            if policyID not in txs:
                return
            time.sleep(1)




















































































####################################### 
############### CLEAN 0 ############### 
####################################### 


def mintSplit(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, timeLock):
    #load policyID
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    with open(path, 'r') as text:
        policyID = text.read()
    #load currentSlot
    currentSlot = currentSlotD(homePath, mainTest)
    fee = 30000
    mininum = 1500000

    #Create Transaction
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)

    #Clean the info and get only what matters
    # craftTx = cleanCraftTx(craftTx)
    # print(craftTx)
    txIn, funds = transactionGatherer(craftTx, fee + 1000000 + mininum)
    # print(craftTx)
    # print(funds, 'funds')
    #This has to be fixed, gotta meke a def gathering all balance, which is some time
    NFTFlag = False
    try:
        #You want all the data starting at craftTx[5] y acabando en craftTx[-2]
        hiddenNFTs = []
        for x, data in enumerate(craftTx):
            if x >= 5:
                hiddenNFTs.append(data)
        hiddenNFTs.pop(-1)
        hiddenNFTs.pop(-1)
        oldNFTs = ''
        for x, data in enumerate(hiddenNFTs):
            if len(data) > 20:
                oldNFTs = oldNFTs + ' ' + data
            if data == '+':
                oldNFTs = oldNFTs + ' + '
            try:
                oldNFTs = oldNFTs + data + ' '
            except:
                pass


        amountPreviosNFT = craftTx[5]
        NFTHashAndName = craftTx[6]
        NFTFlag = True
        # print(NFTFlag, 'NFTFlag')

    except:
        pass


    
    output = str(int(funds) - fee - 1000000 - mininum)

    if NFTFlag == False:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + userAddress + '+' +  str(mininum) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --tx-out ' + userAddress + '+' +  output + \
        ' --tx-out ' + 'addr_test1qzvplvlu0pqd0spm7ev5pp9vdsuydjgycdcr2qct8xcapgz9thnazclfq274u9l74cjre46as2rpn3jwx7xw8vxy8hass0kdpa' + '+' +  '1000000' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        # print(getRawTx)
        getRawTx = getRawTx.replace('\n', '')
        
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)
    else:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + oldNFTs + \
        ' + ' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)


    # #2.2 Calculate fee
    fee = homePath + 'cardano-cli transaction calculate-min-fee --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw --tx-in-count 1 --tx-out-count 3 --witness-count 3 ' + mainTest + ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    fee = str(fee.decode('utf-8'))
    fee = fee.replace('\n', '')
    output = str(int(funds) - int(fee) - 1000000 - mininum)
    # print(fee, 'fee')
    # time.sleep(0.1)

    if NFTFlag == False:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + userAddress + '+' +  str(mininum) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --tx-out ' + userAddress + '+' +  output + \
        ' --tx-out ' + 'addr_test1qzvplvlu0pqd0spm7ev5pp9vdsuydjgycdcr2qct8xcapgz9thnazclfq274u9l74cjre46as2rpn3jwx7xw8vxy8hass0kdpa' + '+' +  '1000000' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)
    else:
        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        txIn + \
        ' --tx-out ' + userAddress + '+' +  output + '+"' + oldNFTs + \
        ' + ' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
        ' --invalid-hereafter ' + str(currentSlot + timeLock) + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)

    # #2.3 Sign the Transaction
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + \
    mainTest + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = subprocess.check_output(signTx,shell=True)

    # #Send the REAL Transaction
    sendRealTx = homePath + 'cardano-cli transaction submit' + \
    ' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest

    sendRealTx = subprocess.check_output(sendRealTx,shell=True)










def transactionGathererForSplitNFT(craftTx, amountToSend, userAddress, fee):
    #Decode and clean Transactions
    craftTx = craftTx.decode('utf-8').replace('\n', ' ')
    craftTx = craftTx.split(' ')
    k = []
    for x,y in enumerate(craftTx):
        if y == '':
            k.append(x)
    for x in k[::-1]:
        craftTx.pop(x)

    #Order Transactions  
    txs = []
    temp = []
    for data in craftTx:
        if len(data) == 64:
            txs.append(temp)
            temp = []
            temp.append(data)
        else:
            temp.append(data)
    txs.append(temp)#The last portion of data to append is outside of the loop and therefore needs an extra append by the end
    txs.pop(0)#First portion of data is garbage
    # print(txs)
    sys.exit()
    #Append all transactions until the target money to send is been reached
    
     # = []
    availableTxsYESNFT = []
    currentADA = 0
    for tx in txs:
        if currentADA >= int(amountToSend): continue
        availableTxs.append(tx)
        currentADA += int(tx[2])
        
    transactionOUT = ''
    transactionIN = ''
    for singleTx in availableTxs:
        try:
            singleTx[6]
            transactionIN += ' --tx-in ' + singleTx[0] + '#' + singleTx[1]
            transactionOUT += ' --tx-out ' + userAddress + '+1500000+"' + singleTx[5] + ' ' + singleTx[6].split('.')[0] + '.' + singleTx[6].split('.')[1] + '" --tx-out ' + userAddress + '+' + output + '"0 ' + singleTx[6].split('.')[0] + '.' + singleTx[6].split('.')[1] + '"'
        except:
            pass
    # --tx-out $receiver+$receiver_output+"2 $policyid.$tokenname1"
    # --tx-out $address+$output+"9999998 $policyid.$tokenname1 + 10000000 $policyid.$tokenname2"  \
    # print(availableTxs)
    sys.exit()

    return transactionComplete, currentADA


# def selfSendTokensTransactionGatherer(craftTx, amountToSend):
#     #Built for deattaching, freing, the NFT to the amount of money related to it
#     #Decode and clean Transactions
#     craftTx = craftTx.decode('utf-8').replace('\n', ' ')
#     craftTx = craftTx.split(' ')
#     k = []
#     for x,y in enumerate(craftTx):
#         if y == '':
#             k.append(x)
#     for x in k[::-1]:
#         craftTx.pop(x)

#     #Order Transactions  
#     txs = []
#     temp = []
#     for data in craftTx:
#         if len(data) == 64:
#             txs.append(temp)
#             temp = []
#             temp.append(data)
#         else:
#             temp.append(data)
#     txs.append(temp)#The last portion of data to append is outside of the loop and therefore needs an extra append by the end
#     txs.pop(0)#First portion of data is garbage
    
#     #Append all transactions until the target money to send is been reached
#     availableTxs = []
#     currentADA = 0
#     for tx in txs:
#         try:
#             print(tx[6], 'tx6')
#             currentADA += int(tx[2])
#             print(currentADA, 'currentADA')
#             availableTxs.append(tx)
#         except:
#             pass
#     print(availableTxs)
#     sys.exit()
#     transactionComplete = ''
#     for singleTx in availableTxs:
#         transactionComplete += ' --tx-in ' + singleTx[0] + '#' + singleTx[1]

#     return transactionComplete, currentADA

def selfSendTokens(homePath, mainTest, user, userAddress):
    #3 SEND TOKENS
    fee = 300000
    receiver=userAddress
    receiver_output="1500000"

    #Gather basic info
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    with open(path, 'r') as text:
        policyID = text.read()

    #2.1 Make raw Transaction with OUT real fee
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)

    #Clean the info and get only what matters
    probableAmountToMintToken = fee + int(receiver_output)
    txIn, funds = transactionGathererForSplitNFT(craftTx, probableAmountToMintToken)

    NumberOfTxIn = len(txIn.split('--'))-1

    output = str(int(funds) - fee)
    # print('funds:', funds)
    # print('output',output)

    totalTokens = "1"
    tokensToGive = "1"
    tokensLeft = str(int(totalTokens) - int(tokensToGive))
    output = str(int(funds) - int(receiver_output) - int(fee))

    #Check if policyID was created:
    try:
        path = homePath + 'keys/' + user + '/' + policyName + '.txt'
        with open(path, 'r') as text:
            policyID = text.read()
            policyID = str(policyID)
    except:
        policyID = None

    #3.1Build raw Transaction
    buildRaw = homePath + 'cardano-cli transaction build-raw --fee ' + str(fee) + txIn + \
    ' --tx-out ' + receiver + '+' + receiver_output + '+"' + tokensToGive + ' ' + policyID + '"' \
    ' --tx-out ' + userAddress + '+' + output + '+"' + tokensLeft + ' ' + policyID + '"' \
    ' --out-file ' + homePath + 'keys/' + user + '/rec_matx.raw'
    buildRaw = buildRaw.replace('\n', '')
    buildRaw = subprocess.check_output(buildRaw,shell=True)

    #3.2 Calculate fee
    fee = homePath + 'cardano-cli transaction calculate-min-fee --tx-body-file ' + homePath + 'keys/' + user + '/rec_matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 2 ' + mainTest + ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    fee = str(fee.decode('utf-8'))
    fee = fee.replace('\n', '')
    output = str(int(funds) - int(receiver_output) - int(fee))

    #3.3 Update Transaction, sign, send
    #Update
    buildRaw = homePath + 'cardano-cli transaction build-raw  --fee ' + str(fee) + txIn + \
    ' --tx-out ' + receiver + '+' + receiver_output + '+"' + tokensToGive + ' ' + policyID + '"' \
    ' --tx-out ' + userAddress + '+' + output + '+"' + tokensLeft + ' ' + policyID + '"' + \
    ' --out-file ' + homePath + 'keys/' + user + '/rec_matx.raw'
    buildRaw = buildRaw.replace('\n', '')
    buildRaw = subprocess.check_output(buildRaw,shell=True)

    #Sign
    signTx = homePath + 'cardano-cli transaction sign --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + mainTest + ' --tx-body-file ' + homePath + 'keys/' + user + '/rec_matx.raw --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = subprocess.check_output(signTx,shell=True)

    #Send
    sendRealTx = homePath + 'cardano-cli transaction submit --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest
    sendRealTx = subprocess.check_output(sendRealTx,shell=True)


def buildTransactionWithTokens(homePath, mainTest, user, userAddress, fee, txIn, receiver, receiver_output, tokensToGive, policyID, tokensLeft):
    buildRaw = homePath + 'cardano-cli transaction build-raw --fee ' + str(fee) + txIn + \
    ' --tx-out ' + receiver + '+' + receiver_output + '+"' + tokensToGive + ' ' + policyID + '"' \
    ' --tx-out ' + userAddress + '+' + output + '+"' + tokensLeft + ' ' + policyID + '"' \
    ' --out-file ' + homePath + 'keys/' + user + '/rec_matx.raw'
    buildRaw = buildRaw.replace('\n', '')
    buildRaw = subprocess.check_output(buildRaw,shell=True)











































































#############################################
################ CLEAN 1 ####################
#############################################

def mint1(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, timeLock, platformAddress, platformFee):
    #load policyID
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    with open(path, 'r') as text:
        policyID = text.read()
    #load hereafter
    path = homePath + 'keys/' + user + '/' + policyName + '.script'
    with open(path, 'r') as text:
        policyString = text.read()
        policyJSON = json.loads(policyString)
        herafter = str(policyJSON["scripts"][0]["slot"])

    #Create Transaction
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)

    #Clean the info and get only what matters
    craftTx = cleanCraftTx1(craftTx)
    fee = 300000
    minAmountLocked = 1500000
    amountToSend = str(int(fee) + minAmountLocked + int(platformFee))
    # amountToSend = str(int(platformFee) + int(minAmountLocked) + int(fee))
    txIn, funds = transactionGatherer1(craftTx, amountToSend)

    output = str(int(funds) - int(fee) - int(platformFee) - int(minAmountLocked))

    #create raw file
    getRawTx = homePath + 'cardano-cli transaction build-raw' + \
    ' --fee ' + str(fee) + \
    txIn + \
    ' --tx-out ' + userAddress + '+' +  str(minAmountLocked) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + str(output) + \
    ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
    ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
    ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
    ' --invalid-hereafter ' + herafter + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
    getRawTx = getRawTx.replace('\n', '')
    getRawTx = subprocess.check_output(getRawTx,shell=True)
    time.sleep(0.1)


    # #2.2 Calculate fee
    fee = homePath + 'cardano-cli transaction calculate-min-fee --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw --tx-in-count 1 --tx-out-count 3 --witness-count 3 ' + mainTest + ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    fee = fee.decode('utf-8')
    fee = fee.replace('\n', '')
    output = str(int(funds) - int(fee) - int(platformFee) - int(minAmountLocked))

    # #Make raw Transaction with real fee
    getRawTx = homePath + 'cardano-cli transaction build-raw' + \
    ' --fee ' + str(fee) + \
    txIn + \
    ' --tx-out ' + userAddress + '+' +  str(minAmountLocked) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + str(output) + \
    ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
    ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
    ' --metadata-json-file ' + homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json' + \
    ' --invalid-hereafter ' + herafter + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
    getRawTx = getRawTx.replace('\n', '')
    getRawTx = subprocess.check_output(getRawTx,shell=True)
    time.sleep(0.1)

    # #2.3 Sign the Transaction
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + \
    mainTest + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = subprocess.check_output(signTx,shell=True)

    # #Send the REAL Transaction
    sendRealTx = homePath + 'cardano-cli transaction submit' + \
    ' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest

    sendRealTx = subprocess.check_output(sendRealTx,shell=True)
    # print('MINTED')


def mint_on_another_address_no_royalties(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, timeLock, platformAddress, platformFee, address_where_mint, utxs_in, money, tx_in):
    #load policyID
    path = homePath + 'keys/' + user + '/' + policyName + '.txt'
    with open(path, 'r') as text:
        policyID = text.read()
    #load hereafter
    path = homePath + 'keys/' + user + '/' + policyName + '.script'
    with open(path, 'r') as text:
        policyString = text.read()
        policyJSON = json.loads(policyString)
        herafter = str(policyJSON["scripts"][0]["slot"])

    #Create Transaction
    craftTx = homePath + 'cardano-cli query utxo --address ' + userAddress + ' ' + mainTest
    craftTx = subprocess.check_output(craftTx,shell=True)

    #Clean the info and get only what matters
    craftTx = cleanCraftTx1(craftTx)
    fee = 300000
    minAmountLocked = 1500000
    # amountToSend = str(int(fee) + minAmountLocked + int(platformFee))
    # amountToSend = str(int(platformFee) + int(minAmountLocked) + int(fee))
    # txIn, funds = transactionGatherer1(craftTx, amountToSend)
    output = str(int(money) - int(fee) - int(platformFee) - minAmountLocked)

    
    #create raw file
    getRawTx = homePath + 'cardano-cli transaction build-raw' + \
    ' --fee ' + str(fee) + \
    f' --tx-in {tx_in}' + \
    ' --tx-out ' + address_where_mint + '+' +  str(minAmountLocked) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + str(output) + \
    ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
    ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
    ' --metadata-json-file ' + f'/home/yop/Downloads/cardano/single_nfts/{user}/{NFTName}/metadata.json' + \
    ' --invalid-hereafter ' + herafter + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
    getRawTx = getRawTx.replace('\n', '')
    getRawTx = subprocess.check_output(getRawTx,shell=True)
    time.sleep(0.1)


    # #2.2 Calculate fee
    fee = homePath + 'cardano-cli transaction calculate-min-fee --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw --tx-in-count '+ str(utxs_in) + ' --tx-out-count 3 --witness-count 3 ' + mainTest + ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    fee = fee.decode('utf-8')
    fee = fee.replace('\n', '')
    output = str(int(money) - int(fee) - int(platformFee) - minAmountLocked)
    print(output, 'output')

    # #Make raw Transaction with real fee
    getRawTx = homePath + 'cardano-cli transaction build-raw' + \
    ' --fee ' + str(fee) + \
    f' --tx-in {tx_in}' + \
    ' --tx-out ' + address_where_mint + '+' +  str(minAmountLocked) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --tx-out ' + userAddress + '+' + str(output) + \
    ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
    ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
    ' --metadata-json-file ' + f'/home/yop/Downloads/cardano/single_nfts/{user}/{NFTName}/metadata.json' + \
    ' --invalid-hereafter ' + herafter + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
    getRawTx = getRawTx.replace('\n', '')
    getRawTx = subprocess.check_output(getRawTx,shell=True)
    time.sleep(0.1)

    # #2.3 Sign the Transaction
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + \
    mainTest + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = subprocess.check_output(signTx,shell=True)

    # #Send the REAL Transaction
    sendRealTx = homePath + 'cardano-cli transaction submit' + \
    ' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest

    sendRealTx = subprocess.check_output(sendRealTx,shell=True)
    # print('MINTED')


def mint_on_another_address_single_nft(homePath, mainTest, user, userAddress, policyName, NFTName, NFTAmount, NFTID, platformAddress, platformFee, address_where_mint, money, tx_hash ,tx_in, original_nft_name):
    try:
        
        nft_metadata = NFTName
        nft_metadata = nft_metadata.replace('_', '')
        nft_name_no_space = NFTName.replace(' ', '').replace('_', '')
        original_nft_name = NFTName
        original_nft_name = original_nft_name.replace(' ', '_')

        #load policyID
        path = homePath + 'keys/' + user + '/' + policyName + '.txt'
        query = f'/home/yop/Downloads/cardano-node1.30.0/cardano-cli transaction policyid --script-file /home/yop/Downloads/cardano-node1.30.0/keys/{user}/{policyName}.script'
        policyID = subprocess.check_output(query,shell=True)
        policyID = policyID.decode('utf-8').replace('\n', '')

        # Create no name token in case it is the first time creating a policy
        # if os.exists(f'{homePath} keys/{user}/{policyName}LOADED.txt'):
        #     query = 
        #     result = subprocess.check_output(query,shell=True)

        #load hereafter
        path = homePath + 'keys/' + user + '/' + policyName + '.script'
        with open(path, 'r') as text:
            policyString = text.read()
            policyJSON = json.loads(policyString)
            herafter = str(policyJSON["scripts"][0]["slot"])

        #Create Transaction
        fee = 300000
        minAmountLocked = 1500000
        output = str(int(money) - int(fee) - int(platformFee) - minAmountLocked)
        # print(f'output: {output}, money: {money}, fee: {fee}, platformFee: {platformFee}, minAmountLocked: {minAmountLocked}')
        # sys.exit()

        # print(f'''
        #     money {money}
        #     fee: {fee}
        #     minAmountLocked: {minAmountLocked}
        #     output: {output}
        #     platformFee: {platformFee}
        #     ''')

        #create raw file
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        f' --tx-in {tx_hash}#{tx_in}' + \
        ' --tx-out ' + address_where_mint + '+' +  str(minAmountLocked) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + nft_name_no_space + '"' + \
        ' --tx-out ' + userAddress + '+' + str(output) + \
        ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + nft_name_no_space + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + f'/home/yop/Downloads/cardano/single_nfts/{user}/{original_nft_name}/metadata.json' + \
        ' --invalid-hereafter ' + herafter + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)

        # #2.2 Calculate fee
        fee = homePath + 'cardano-cli transaction calculate-min-fee --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw --tx-in-count '+ str(1) + ' --tx-out-count 3 --witness-count 3 ' + mainTest + ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
        fee = subprocess.check_output(fee,shell=True)
        fee = fee.decode('utf-8')
        fee = fee.replace('\n', '')
        output = str(int(money) - int(fee) - int(platformFee) - minAmountLocked)
        # print(output, 'output')
        
        # print(f'''
        #     fee: {fee}
        #     minAmountLocked: {minAmountLocked}
        #     output: {output}
        #     platformFee: {platformFee}
        #     ''')

        # #Make raw Transaction with real fee
        getRawTx = homePath + 'cardano-cli transaction build-raw' + \
        ' --fee ' + str(fee) + \
        f' --tx-in {tx_hash}#{tx_in}' + \
        ' --tx-out ' + address_where_mint + '+' +  str(minAmountLocked) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + nft_name_no_space + '"' + \
        ' --tx-out ' + userAddress + '+' + str(output) + \
        ' --tx-out ' + platformAddress + '+' + str(platformFee) + \
        ' --mint="' + str(NFTAmount) + ' ' + policyID + '.' + nft_name_no_space + '"' + \
        ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
        ' --metadata-json-file ' + f'/home/yop/Downloads/cardano/single_nfts/{user}/{original_nft_name}/metadata.json' + \
        ' --invalid-hereafter ' + herafter + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
        getRawTx = getRawTx.replace('\n', '')
        getRawTx = subprocess.check_output(getRawTx,shell=True)
        time.sleep(0.1)

        # #2.3 Sign the Transaction
        signTx = homePath + 'cardano-cli transaction sign' + \
        ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey' + \
        ' --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + \
        mainTest + \
        ' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' + \
        ' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
        signTx = subprocess.check_output(signTx,shell=True)
        # print('Almost done')
        # sys.exit()
        # #Send the REAL Transaction
        sendRealTx = homePath + 'cardano-cli transaction submit' + \
        ' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest
        sendRealTx = subprocess.check_output(sendRealTx,shell=True)

        
        with open(f'/home/yop/Downloads/cardano/single_nfts/{user}/{original_nft_name}/flags.txt', 'w') as text:
            text.write('1, 1, 0')
        print(f'{nft_name_no_space} minted successfully')
        return True

    except Exception as e:
        return e


def vending_machine_mint_multiple_nfts(mainTest, info):
    '''
    1 info is 1 NFT to mint, not a transaction
    info = [[
    nft_name, 
    nft_id, 
    nft_price,
    project_name,
    tx_hash,
    tx_in,
    funds,
    charging_fees,
    buyer_address,
    project_address,
    money_reminder
    ],

    [nft_name,
    ...],
    ...]

    1. Fetch all to be transfered
    2. Create metadata for each and everyone of the NFTs to be minted
    3. Gather the neccessary amount for minting, sending to the creator of the proyect and fees for my website
    4. Create one macro transaction
    '''

    # Load all common data
    home_path = '/home/yop/Downloads/cardano-node1.30.0/'
    min_locked_amount = 1500000
    tx_hash = info[0][1]
    tx_in = info[0][2]
    funds = info[0][3]
    buyer_address = info[0][4]
    charging_fees = info[0][5]
    project_address = info[0][6]
    nft_id = info[0][7]
    project_name = info[0][8]
    money_reminder = info[0][9]

    tx_out_amount = len(info)  # Amount of NFTs to mint

    # Cardano Magic wallet address
    cardano_magic_wallet = loadAddress(home_path, 'cardano_magic')

    # Load policy_id
    path = f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.txt'
    with open(path, 'r') as text:
        policy_id = text.read()

    # Load hereafter
    path = f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.script'
    with open(path, 'r') as text:
        policy_string = text.read()
        policy_json = json.loads(policy_string)
        herafter = str(policy_json["scripts"][0]["slot"])

    # CREATE --tx-in
    tx_in = f' --tx-in {tx_hash}#{tx_in}'

    # CREATE --tx-out
    platform_fee = 0
    proyect_creator = 0
    tx_outs = ''
    fee = 30000
    mint_tx = ' --mint='

    # --tx-out and --mint for the buyer
    for number_of_field, data in enumerate(info):
        data[8] = data[8].replace('_', '')
        platform_fee += int(charging_fees)  # in the end will be one single tx with all the fees to my website
        proyect_creator += min_locked_amount
        tx_outs += f' --tx-out {buyer_address}+1500000+"1 {policy_id}.{data[8]}{data[7]}"'
        mint_tx += f'"1 {policy_id}.{data[8]}{data[7]}"+'
    mint_tx = mint_tx[:-1]  # Delete last "+" since there are no more transactions
    
    # The buyer did not send the right amount and there is a left over
    if money_reminder != 0:
        tx_outs += f' --tx-out {buyer_address}+{money_reminder}'


    # --tx-out for the project creator
    project_earnings = int(funds) - int(fee) - int(proyect_creator) - int(platform_fee)
    tx_outs += f' --tx-out {project_address}+{project_earnings}'

    # --tx-out for Cardano Magic
    tx_outs += f' --tx-out {cardano_magic_wallet}+{platform_fee}'

    # CREATE raw file
    get_raw_tx = home_path + 'cardano-cli transaction build-raw' + \
    ' --fee ' + str(fee) + \
    tx_in + \
    tx_outs + \
    mint_tx + \
    ' --minting-script-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.script' + \
    ' --metadata-json-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/metadata.json' + \
    ' --invalid-hereafter ' + herafter + \
    ' --out-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/matx.raw'
    get_raw_tx = get_raw_tx.replace('\n', '')
    get_raw_tx = subprocess.check_output(get_raw_tx,shell=True)
    time.sleep(0.1)


    # #2.2 Calculate fee
    fee = f'{home_path}cardano-cli transaction calculate-min-fee --tx-body-file /home/yop/Downloads/cardano/vending_machine/{project_name}/matx.raw --tx-in-count 1 --tx-out-count {tx_out_amount} --witness-count 1 {mainTest} --protocol-params-file /home/yop/Downloads/cardano/vending_machine/{project_name}/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    fee = fee.decode('utf-8')
    fee = fee.replace('\n', '')


    # REDO
    # --tx-out and --mint for the buyer
    platform_fee = 0
    proyect_creator = 0
    tx_outs = ''
    mint_tx = ' --mint='
    for number_of_field, data in enumerate(info):
        platform_fee += int(charging_fees)  # in the end will be one single tx with all the fees to my website
        proyect_creator += min_locked_amount
        tx_outs += f' --tx-out {buyer_address}+1500000+"1 {policy_id}.{data[0]}"'
        mint_tx += f'"1 {policy_id}.{data[0]}"+'
    mint_tx = mint_tx[:-1]  # Delete last "+" since there are no more transactions


    # --tx-out for the project creator
    project_earnings = int(funds) - int(fee) - int(proyect_creator) - int(platform_fee)
    tx_outs += f' --tx-out {project_address}+{project_earnings}'

    # --tx-out for my website
    tx_outs += f' --tx-out {cardano_magic_wallet}+{platform_fee}'



    # CREATE REAL raw file
    get_raw_tx = home_path + 'cardano-cli transaction build-raw' + \
    ' --fee ' + str(fee) + \
    tx_in + \
    tx_outs + \
    mint_tx + \
    ' --minting-script-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.script' + \
    ' --metadata-json-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/metadata.json' + \
    ' --invalid-hereafter ' + herafter + \
    ' --out-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/matx.raw'
    get_raw_tx = get_raw_tx.replace('\n', '')
    get_raw_tx = subprocess.check_output(get_raw_tx,shell=True)
    time.sleep(0.1)

    # #2.3 Sign the Transaction
    sign_tx = home_path + 'cardano-cli transaction sign' + \
    f' --signing-key-file /home/yop/Downloads/cardano/vending_machine/{project_name}/{project_name}.skey' + \
    f' --signing-key-file /home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.skey ' + \
    mainTest + \
    ' --tx-body-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/matx.raw' + \
    ' --out-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/matx.signed'
    sign_tx = subprocess.check_output(sign_tx,shell=True)

    # #Send the REAL Transaction
    send_real_tx = home_path + 'cardano-cli transaction submit' + \
    ' --tx-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/matx.signed ' + mainTest

    send_real_tx = subprocess.check_output(send_real_tx,shell=True)

