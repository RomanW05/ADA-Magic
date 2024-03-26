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
policyName = ''
# policyName = 'Try8'
timeLock = 315360000#315360000=10years
NFTDescription = 'Testing the code for NFT minting functionality continuity'
NFTName = ''
NFTAmount = 1
NFTID = 2
NFTImageUrl = 'not yet'
NFTRoyaltiesPercentage = "0.2"
userAddress = loadAddress(homePath, user)
print(userAddress)
# NFTRoyaltiesAddress = userAddress
platformAddress = ''




'''
3. Receive info from website.
	-Total number of NFTs
	-Name of the project
	-Address to deposit the ADAs
	-Royalties?
	-Images
	-Attributes
4. Create db for vending machine
	New table: proyect_name_#of_total_NFTs (Ethereal_5555)
	Fields:
		minted_number
3. Use generative art generator to randomly create the images
4. Upload images to the ipfs
3. Check balance every 1 min
4. Check TxHash and isolate the hash and the balance
5. Check if the balance is the money that is supposed to be
6. Mint random NFT
7. Check on the explorer which wallet is that TxHash comming from
8. Send NFT to the wallet that sent the money
'''
'''
setup groups to arrange  
section for grouping policy ids!!!!!
'''

def upload_to_ipfs()
                                                buf = io.BytesIO()
                                                newImage.save(buf, format='PNG')
                                                byte_im = buf.getvalue()
                                                files = {
                                                  'files': byte_im
                                                }
                                                url = 'https://ipfs.infura.io:5001/api/v0/add'
                                                results = requests.post(url, files=files)
                                                p = results.json()
                                                hash = p['Hash']
                                                imageUrl = "https://ipfs.infura.io/ipfs/" + hash
                                                imageUrl = '"' + imageUrl[1:-1] + '"'