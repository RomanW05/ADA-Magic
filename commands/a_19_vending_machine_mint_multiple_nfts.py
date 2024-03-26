import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
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
from orderedCommands import vending_machine_mint_multiple_nfts

import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet
project_name = 'testo'
policyName = 'Try8'
timeLock = 315360000#315360000=10years
NFTDescription = 'Testing the code for NFT minting functionality continuity'
NFTName = 'NFTTest'
NFTAmount = 1
NFTID = 2
NFTImageUrl = 'not yet'
NFTRoyaltiesPercentage = "0.2"


'''
The structure of what is expected from ending_machine_mint_multiple_nfts()
Use double array because it still works regardless of one or multiple minted NFTs
info = [[]]
 info = [[
    nft_name, 
    nft_id, 
    nft_price,
    project_name,
    tx_hash,
    funds,
    charging_fees,
    buyer_address,
    website_address,
    admin_username
    ],

    [nft_name,
    ...],
    ...]

    receive transactions array: # [tx_hash, tx_in, lovelaces]

    -Receive the number of NFTs to mint
    -Receive the hashes of the txs
    -Call the generator to create the NFT image, thumbnail and metadata
    -Send the transaction
'''
try:
    # Receive number of NFTs to mint, the tx_hash and the tx_in
    project_name = sys.argv[1] 
    project_address = sys.argv[2] 
    ada_sent = sys.argv[3] 
    sender_address = sys.argv[4] 
    tx_hash = sys.argv[5] 
    tx_in = sys.argv[6]
    willing_to_mint = sys.argv[7]
    artist = sys.argv[8]
    price = sys.argv[9]
    money_reminder = sys.argv[10]
    platform_fees = '0'

    info = []  # Array to throw at vending_machine_mint_multiple_nfts()
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/platform_fees.txt', 'r') as text:
        platform_fees = text.read()
        platform_fees = platform_fees.replace('\n', '').replace(' ', '')


    # Iterate through the NFTs to be minted
    for nft_to_mint in range(int(willing_to_mint)):

        # Load random number to mint NFT
        with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/randomized_nfts.json') as text:
            lists_of_nfts = json.loads(text.read())
            lists_of_nfts = list(iter(lists_of_nfts))
            nft_id = lists_of_nfts[nft_to_mint]  # Number loaded

        fields = []
        fields.append(f'{project_name}{nft_id}')  # Need to encode nft_name base 16
        fields.append(f'{tx_hash}')
        fields.append(f'{tx_in}')
        fields.append(f'{ada_sent}')
        fields.append(f'{sender_address}')
        fields.append(f'{platform_fees}')
        fields.append(f'{project_address}')
        fields.append(f'{nft_id}')
        fields.append(f'{project_name}')
        fields.append(f'{money_reminder}')

        info.append(fields)
        os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_32_generative_art_with_rarities.py {project_name}')

    # CREATE metadata
    metadata = {}

    # Load policy_id
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.txt', 'r') as text:
        policy_id = text.read()

    # Load standard template
    metadata['721'] = {
                        policy_id: {
                            },
                        "version": "1.0"
                        }

    # Iterate over the metadata in json and add it to the final metadata file
    for nft in info:
        with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/to_upload/{nft[0]}.json', 'r') as text:
            file_metadata = json.load(text)
            metadata['721'][policy_id][nft[0]] = file_metadata

    # list_of_im_metadata = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/to_upload')
    # for file in list_of_im_metadata:
    #     if file.endswith('json', -4):
    #         # Read metadata of each file
    #         with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/to_upload{file}', 'r') as text:
    #             file_metadata = json.load(text.read())
            
    #         nft_name = file.replace('.json', '')

    #         metadata['721'][policy_id][nft_name] = file_metadata

    # Curate the metadata file
    # metadata = json.dumps(metadata)

    # Store the metadata file
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/metadata.json', 'w') as text:
        json.dump(metadata, text)

    # MINT THE GOD DAMN NFT
    vending_machine_mint_multiple_nfts(mainTest, info)

    # Store pending hash hash
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/hashes.txt', 'a') as text:
        temp = '\n'
        for nft in info:
            temp += f'{nft[1]}\n'
        temp = temp[:-1]
        text.write(temp)
except:
    logging.exception('Got exception on main handler')
    raise
    