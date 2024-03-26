import os
import sys
import json
import subprocess
import time
import requests
from os.path import exists
from orderedCommands import currentSlotD
import logging

logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

# Search folder for projects
# Call cardano-cli to search new transactions
# Load transactions to be double checked and not mint twice nor send twice to the same buyers wallet
# If a new transaction is been found store it and get the ADAs sent
# Call the explorer once we are sure we are ready to mint and send NFT
# Check on Cardano transaction explorer Dandalion if the transaction arrived to the destiny
# Delete transaction

time_now = int(time.time())
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet
home_path = '/home/yop/Downloads/cardano-node1.30.0/'


def subtract_minted_nfts(lists_of_nfts, willing_to_mint, project_name, json_lists_of_nfts):
    # Delete minted NFTs from random array
    for elem in range(willing_to_mint):
        lists_of_nfts = lists_of_nfts[1:]

    new_json_list_of_nfts = {}
    for number in lists_of_nfts:
        new_json_list_of_nfts[number] = json_lists_of_nfts[number]

    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/randomized_nfts.json', 'w') as text:
        text.write(json.dumps(new_json_list_of_nfts))
    sys.exit()

def load_random_nfts(project_name):
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/randomized_nfts.json') as f:
        json_lists_of_nfts = json.loads(f.read())
        lists_of_nfts = list(iter(json_lists_of_nfts))

    return lists_of_nfts, json_lists_of_nfts


def clear_tx(home_path, mainTest, project_address):
    craft_tx = f'{home_path}cardano-cli query utxo --address {project_address} {mainTest}'
    craft_tx = subprocess.check_output(craft_tx,shell=True)
    
    # Clean results
    craft_tx = craft_tx.decode('utf-8')
    craft_tx = craft_tx.split('\n')
    craft_tx = craft_tx[2:]

    return craft_tx


def get_tx_info(craft_tx):
    utxo_lovelace = []
    for x, utxo in enumerate(craft_tx):
        utxo = utxo.split(' ')

        # More than 17 is a token or NFT
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


def load_wallet(project_name):
    try:
        project_address = f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{project_name}.addr'
        with open(project_address, 'r') as text:
            project_address = text.read()
            project_address = project_address.replace('\n', '')
    except:
        pass

    return project_address



# # Search folders projects
# for subdir, dirs, files in os.walk('/home/yop/Downloads/cardano/vending_machine/'):
#     for project in dirs:
#         # print(project)
#         pass
#     for file in files:
#         pass

def load_info(project_name):
    # Randomized list of NFTs to mint and NFTs left
    lists_of_nfts, json_lists_of_nfts = load_random_nfts(project_name)

    # Load the price of each NFT
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/price.txt', 'r') as f:
        price = int(f.read())

    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/artist.txt', 'r') as f:
        artist = f.read()

    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/minting_date.txt', 'r') as f:
        minting_date = int(f.read())

    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/profit_wallet_address.txt', 'r') as f:
        profit_wallet_address = f.read()
    

    return lists_of_nfts, price, artist, json_lists_of_nfts, minting_date, profit_wallet_address


# Fetch the entire wallet transactions but just once per wallet!
def fetch_blockchain_data(project_address):
    result = requests.get('https://explorer-api.testnet.dandelion.link/api/addresses/summary/' + project_address)
    json_data = json.loads(result.text)

    return json_data


def fetch_ada_sent_from_wallet(json_data, tx_hash, project_address):
    for tx_number, history in enumerate(json_data["Right"]["caTxList"]):
        if json_data["Right"]["caTxList"][tx_number]["ctbId"] == tx_hash:
            
            # Sender wallet
            sender_address = json_data["Right"]["caTxList"][tx_number]["ctbInputs"][0]["ctaAddress"]

            # Amount received
            for elem, output in enumerate(json_data["Right"]["caTxList"][tx_number]["ctbOutputs"]):
                if json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][elem]["ctaAddress"] == project_address:
                    received_ada = int(json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][elem]["ctaAmount"]["getCoin"])

            return sender_address, received_ada


def delete_verified_tx(tx_hash, sender_address, stored_hashes):
    result = requests.get(f'https://explorer-api.testnet.dandelion.link/api/txs/summary/{tx_hash}')
    if sender_address in result.text:
        stored_hashes = stored_hashes.replace(f'{tx_hash}\n', '')
        with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/hashes.txt', 'w') as text:
            text.write(stored_hashes)

def scroll():
    projects_name = os.listdir('/home/yop/Downloads/cardano/vending_machine/')
    # Scroll through every project
    for project_name in projects_name:
        if os.path.isdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}'):
            # LOADING SECTION!!!
            # Load wallet
            project_address = load_wallet(project_name)

            # Clean transaction
            craft_tx = clear_tx(home_path, mainTest, project_address)

            # Get tx_hash, tx_in, lovelaces in an array for this wallet [tx_hash, tx_in, lovelaces]
            utxo_lovelace = get_tx_info(craft_tx)

            # Load information before taking action
            lists_of_nfts, price, artist, json_lists_of_nfts, minting_date, profit_wallet_address = load_info(project_name)

            # Load all transaction history from project wallet
            json_data = fetch_blockchain_data(project_address)

            # Update pending transaction status
            # Load all pending transactions from project wallet
            with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/hashes.txt', 'r') as text:
                stored_hashes = text.read()
                stored_hashes_whole_string = stored_hashes.replace('\n','')
            
            # Delete received transactions
            for tx in utxo_lovelace:
                tx_hash = tx[0]
                sender_address, ada_sent = fetch_ada_sent_from_wallet(json_data, tx_hash, project_address)
                delete_verified_tx(tx_hash, sender_address, stored_hashes)

            # Reload hashes in case some were deleted
            with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/hashes.txt', 'r') as text:
                stored_hashes = text.read()
                stored_hashes_whole_string = stored_hashes.replace('\n','')

            # Compare hashes
            new_transactions = []
            for single_hash in utxo_lovelace:

                # Single hash was sent but not received yet
                if single_hash[0] in stored_hashes_whole_string:
                    print('no single_hash[0]')
                    # continue
                new_transactions.append(single_hash)

            # In case there are no new transactions continue to the next wallet
            if len(new_transactions) == 0:
                print(f'no tx on {project_name}')
                continue

            # Before storing new transactions make sure nfts_left is not 0
            # Check how many NFTs you can actually mint
            # Cut all the new coming transactions that don't fit the bucket
            number_of_nfts_to_mint = len(lists_of_nfts) - len(new_transactions)
            if number_of_nfts_to_mint < 0:
                #absolute value and remove latest new_transactions
                number_of_nfts_to_mint = abs(number_of_nfts_to_mint)
                for x in number_of_nfts_to_mint:
                    new_transactions.pop(-1)

            # LODING IS FINISHED
            # TAKE ACTION

            # In case nfts_left is 0 doesn't make sense to continue so return all transactions
            if len(lists_of_nfts) == 0:
                for tx in new_transactions:

                    # Rename tx variables
                    tx_hash = tx[0]
                    tx_in = tx[1]
                    ada_sent1 = tx[2]

                    #Load sender address and Lovelaces sent
                    sender_address, ada_sent = fetch_ada_sent_from_wallet(json_data, tx_hash, project_address)

                    # ASSERT
                    if int(ada_sent) != int(ada_sent1):
                        return 'YOU ARE SENDING DIFFERENT AMOUNTS TO PROBABLY DIFFERENT ADDRESSES'

                    # In case Not enough money to send back < 1000000 + fee
                    if ada_sent <= 1500000:
                        continue

                    # In case Not enough money for one nft
                    if ((ada_sent > 1500000) and (ada_sent < price)):
                        os.system(f'{home_path}commands/spltCommands/18send_ada_penalzed.py {project_name} {project_address} {ada_sent} {sender_address} {tx_hash} {tx_in}')

            # Mint
            for tx in new_transactions:

                # Rename tx variables
                tx_hash = tx[0]
                tx_in = tx[1]
                ada_sent1 = tx[2]
                #Load sender address and Lovelaces sent
                sender_address, ada_sent = fetch_ada_sent_from_wallet(json_data, tx_hash, project_address)

                # ASSERT
                if int(ada_sent) != int(ada_sent1):
                    print('assert')
                    return 'YOU ARE SENDING DIFFERENT AMOUNTS TO PROBABLY DIFFERENT ADDRESSES'

                # Info about the willingness of the buyer:
                willing_to_mint = ada_sent // price  # Modulus
                willing_to_mint = int(willing_to_mint)
                money_reminder = ada_sent - (willing_to_mint * price)

                # In case Not enough money to send back < 1000000 + fee
                if ada_sent <= 1500000:
                    continue

                # In case Not enough money for one nft
                if ((ada_sent > 1500000) and (ada_sent < price)):
                    os.system(f'{home_path}commands/spltCommands/18send_ada_penalzed.py {project_name} {project_address} {ada_sent} {sender_address} {tx_hash} {tx_in}')

                # FINALLY, MINT AND SEND THE NFTS
                os.system(f'python3 {home_path}commands/spltCommands/a_19_vending_machine_mint_multiple_nfts.py {project_name} {profit_wallet_address} {ada_sent} {sender_address} {tx_hash} {tx_in} {willing_to_mint} {artist} {price} {money_reminder}')

                # Store hash in unverified hashes
                # with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/hashes.txt', 'a') as text:
                #     text.write(f'{tx_hash}\n')

                subtract_minted_nfts(lists_of_nfts, willing_to_mint, project_name)







scroll()


        










