import os
import sys
import json
import subprocess
import time
import requests
from multiprocessing import Process, Queue
from os.path import exists
from orderedCommands import currentSlotD
from orderedCommands import balance
from orderedCommands import check_if_noname_token_is_half_minted
from orderedCommands import createNoNameTokens
from orderedCommands import checkForCreatedDeletedNoNameToken
from orderedCommands import mint_on_another_address_single_nft
from orderedCommands import send_ada_penalized_transaction_single_nft
from orderedCommands import send_extra_ada_penalized_transaction_single_nft
from orderedCommands import metadataCreationWithOutRoyalties
from orderedCommands import metadataCreation
from bs4 import BeautifulSoup

import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

# Search folder for projects
# Call cardano-cli to search new transactions
# Load transactions to be double checked and not mint twice nor send twice to the same buyers wallet
# If a new transaction is found store it and get the ADAs sent
# Call the explorer once we are sure we are ready to mint and send NFT
# Check on Cardano transaction explorer Dandalion if the transaction arrived to the destiny
# Delete transaction

time_now = int(time.time())
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet
home_path = '/home/yop/Downloads/cardano-node1.30.0/'

Q = Queue()
def cardano_scan(project_address):
    sender_address = ''
    money_received = 0
    tx_hash = ''
    money_flag = False
    tx_flag = False
    fetched_index = None
    results = requests.get(f'https://cardanoscan.io/address/{project_address}')
    results = results.text
    soup = BeautifulSoup(results, 'html.parser')
    for link in soup.find_all('span'):
        if 'h4 adaAmount text-success font-weight-bold' in str(link):
            try:
                if int(link.text) == 0:
                    continue
                else:
                    print('NEW TX FOUND!!!')
            except:
                continue

    # Fetch sender address and money sent
    for link in soup.find_all('table'):
        if 'table class="table table-striped"' not in str(link):
            continue
        for index, tr in enumerate(link.tbody):
            if (('Outputs' in str(tr)) and (f'{project_address}' in str(tr))):
                for td in tr:
                    if len(td) > 1:
                        for elem in td:
                            for info in elem:
                                if len(info.text) == 0:
                                    continue
                                if money_flag:
                                    money_received = info.text
                                    money_received = money_received.replace(' ₳', '')
                                    money_flag = False
                                if f'{project_address}' in info.text:
                                    money_flag = True
                                if len(info.text) > 30:
                                    sender_address = info.text
                                    fetched_index = index - 2
                                    tx_flag = True
    # # Fetch tx_hash
    # if fetched_index != None:
    #     for link in soup.find_all('table'):
    #         if 'table class="table table-striped"' not in str(link):
    #             continue
    #         for x, elem in enumerate(link.tbody):
    #             if x != fetched_index:
    #                 continue
    #             for a in elem.find_all('a'):
    #                 if len(a.text) >= 64:
    #                     tx_hash = a.text
    Q.put([project_address, tx_flag, sender_address, money_received])
    # print(f'Sender address: {sender_address}. Money sent: {money_received}. Tx hash: {tx_hash}')



def clear_tx(home_path, mainTest, project_address):
    craft_tx = f'{home_path}cardano-cli query utxo {mainTest} --address {project_address}'
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

        # sys.exit()
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


def load_info(username, nft_name):

    # Load data of NFT
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/price.txt', 'r') as text:
        price = text.read()
        price = price.replace('\n', '')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/buyer_pay_fees.txt', 'r') as text:
        buyer_pay_fees = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_percentage.txt', 'r') as text:
        royalty_percentage = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_wallet.txt', 'r') as text:
        royalty_wallet = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/description.txt', 'r') as text:
        description = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/nft_id.txt', 'r') as text:
        nft_id = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_name.txt', 'r') as text:
        policy_name = text.read()
        policy_name = policy_name.replace('\n', '')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/artist.txt', 'r') as text:
        artist = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/ADAMagic_fee.txt', 'r') as text:
        ADAMagic_fee = text.read()
        ADAMagic_fee = ADAMagic_fee.replace('\n', '')
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/ADA_Magic_io/ADA_Magic_io.addr', 'r') as text:
        ADAMagic_wallet = text.read()
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{username}.addr', 'r') as text:
        username_wallet = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/flags.txt', 'r') as text:
        flags = text.read()
        flags = flags.split(',')
        for x, y in enumerate(flags):
            try:
                flags[x] = int(y)
            except:
                pass
    try:
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/buyer_address.txt', 'r') as text:
            buyer_address = text.read()
    except:
        buyer_address = ''
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/beneficiary_address.txt', 'r') as text:
            beneficiary_address = text.read()
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.txt', 'r') as text:
        policy_id = text.read()

    return price, buyer_pay_fees, royalty_percentage, royalty_wallet, description, nft_id, policy_name, artist, ADAMagic_fee, ADAMagic_wallet, username_wallet, flags, buyer_address, beneficiary_address, policy_id


# Fetch the entire wallet transactions but just once per wallet!
def fetch_blockchain_data(project_address):
    result = requests.get('https://explorer-api.mainnet.dandelion.link/api/addresses/summary/' + project_address)
    print(f'\n\n{result.text}\n\n')
    json_data = json.loads(result.text)

    return json_data


def fetch_ada_sent_from_wallet(json_data, tx_hash, project_address):
    try:
        for tx_number, history in enumerate(json_data["Right"]["caTxList"]):
            if json_data["Right"]["caTxList"][tx_number]["ctbId"] == tx_hash:
                
                # Sender wallet
                sender_address = json_data["Right"]["caTxList"][tx_number]["ctbInputs"][0]["ctaAddress"]

                # Amount received
                for elem, output in enumerate(json_data["Right"]["caTxList"][tx_number]["ctbOutputs"]):
                    if json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][elem]["ctaAddress"] == project_address:
                        received_ada = int(json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][elem]["ctaAmount"]["getCoin"])

                return sender_address, received_ada

    except Exception as e:
        print(f'ERROR {e}\n{json_data}')

def fetch_ada_sent_from_wallet2(json_data, tx_hash, project_address):
    try:
        for tx_number, history in enumerate(json_data["Right"]["caTxList"]):
            for number, elem in enumerate(json_data["Right"]["caTxList"][tx_number]["ctbOutputs"]):
                # if json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][number]["ctaAddress"] == project_address:

                if json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][number]["ctaTxHash"] == tx_hash:
                    sender_address = json_data["Right"]["caTxList"][tx_number]["ctbInputs"][0]["ctaAddress"]
                    received_ada = json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][number]["ctaAmount"]["getCoin"]
                    new_hash = json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][number]["ctaTxHash"]

                    return sender_address, received_ada, new_hash
    
    except Exception as e:
        pass



def browse_nfts(pending_nfts):

    list_of_addresses = []
    projects_name = os.listdir('/home/yop/Downloads/cardano/single_nfts')
    # Scroll through every project
    for username in projects_name:
        if os.path.isdir(f'/home/yop/Downloads/cardano/single_nfts/{username}'):
            list_of_nfts = os.listdir(f'/home/yop/Downloads/cardano/single_nfts/{username}')
            for single_nft in list_of_nfts:
                if os.path.isdir(f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}'):

                    # Read NFT wallet address
                    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/{single_nft}.addr', 'r') as text:
                        nft_address = text.read()
                        if nft_address not in pending_nfts:
                            list_of_addresses.append([username, single_nft, nft_address])

    return list_of_addresses


def save_current_flag_status(username, nft_name, array_status, tx_hash, buyer_address):
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/flags.txt', 'w') as text:
        text.write(f'{array_status}')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/sent_hash.txt', 'w') as text:
        text.write(tx_hash)
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/buyer_address.txt', 'w') as text:
        text.write(buyer_address)



def create_metadata(username, results):
    # Load data of NFT from website

    price = results["price"]
    price = price.replace('\n', '')
    price = int(price)
    price = price * 1000000
    description = results["description"]
    royalty_percentage = results["royalty_percentage"]
    royalty_wallet = results["royalty_wallet"]
    artist = results["artist"]
    artist = artist.replace('\n', '')
    nft_name = results["nft_name"] # Variable change, if any
    original_nft_name = results["original_nft_name"]
    original_nft_name = original_nft_name.replace(' ', '_')


    # with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/price.txt', 'r') as text:
    #     price = text.read()
    #     price = price.replace('\n', '')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/buyer_pay_fees.txt', 'r') as text:
        buyer_pay_fees = text.read()
    # with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_percentage.txt', 'r') as text:
    #     royalty_percentage = text.read()
    # with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_wallet.txt', 'r') as text:
    #     royalty_wallet = text.read()
    # with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/description.txt', 'r') as text:
    #     description = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/nft_id.txt', 'r') as text:
        nft_id = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/policy_name.txt', 'r') as text:
        policy_name = text.read()
        policy_name = policy_name.replace('\n', '')
    # with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/artist.txt', 'r') as text:
    #     artist = text.read()
    #     artist = artist.replace('\n', '')
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{username}.addr', 'r') as text:
        username_wallet = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/flags.txt', 'r') as text:
        flags = text.read()
        flags = flags.split(',')
        for x, y in enumerate(flags):
            try:
                flags[x] = int(y)
            except:
                pass
    try:
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/buyer_address.txt', 'r') as text:
            buyer_address = text.read()
    except:
        buyer_address = ''
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/beneficiary_address.txt', 'r') as text:
            beneficiary_address = text.read()
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.txt', 'r') as text:
        policy_id = text.read()

    # Upload images to the IPFS
    print('Uploading file to ipfs')
    query = f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_27_upload_im_ipfs.py /home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/{original_nft_name}.png'
    result = subprocess.check_output(query,shell=True)
    print(f'File uploaded to the ipfs')
    
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/{original_nft_name}_hash.txt') as text:
        NFTImageUrl = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/{original_nft_name}_thumbnail_hash.txt') as text:
        NFTImageUrlThumbnail = text.read()

    
    if royalty_percentage == '0':
        metadataCreationWithOutRoyalties(home_path, mainTest, username, policy_name, description, original_nft_name, "1", NFTImageUrl, NFTImageUrlThumbnail, artist)
    else:
        royalty_percentage = '0.' + royalty_percentage
        metadataCreation(home_path, mainTest, username, policy_name, description, original_nft_name, "1", NFTImageUrl, royalty_percentage, royalty_wallet, NFTImageUrlThumbnail, artist)


    old = home_path + 'keys/' + username + '/' + policy_id + original_nft_name + str(1) + 'metadata.json'
    old = f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_id}{original_nft_name}{1}metadata.json'
    new = f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/metadata.json'
    os.rename(old, new)


def import_projects():
    list_of_addresses = []
    usernames = os.listdir('/home/yop/Downloads/cardano/single_nfts')
    for username in usernames:
        path = f'/home/yop/Downloads/cardano/single_nfts/{username}'
        if os.path.isdir(path):
            single_nfts = os.listdir(f'/home/yop/Downloads/cardano/single_nfts/{username}')
            for single_nft in single_nfts:
                path = f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}'
                if os.path.isdir(path):

                    # Read data
                    try:
                        with open(f'{path}/{single_nft}.addr', 'r') as text:
                            project_address = text.read()

                        list_of_addresses.append([username, single_nft, project_address])
                    except Exception as e:
                        continue

    return list_of_addresses


def create_no_name_token():
    try:
        createNoNameTokens(homePath, mainTest, user, userAddress, policyName, '1', '1')
        checkForCreatedDeletedNoNameToken(homePath, mainTest, user, userAddress, policyName, '0')
        createNoNameTokens(homePath, mainTest, user, userAddress, policyName, '0', '-1')
        checkForCreatedDeletedNoNameToken(homePath, mainTest, user, userAddress, policyName, '1')
        with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}LOADED.txt' ,'w') as text:
            text.write('Loaded')
    except Exception as e:
        sys.exit(1)


def fetch_updated_data(username, original_nft_name):
    password = ''
    results = requests.get(f'https://adamagic.io/fetch_for_metadata_single_nft/{password}/{username}/{original_nft_name}')
    # print(results.text)
    results = json.loads(results.text)
    return results


















def scroll(username, nft_name, project_address):
    # LOADING SECTION!!!

    # Load information
    price, buyer_pay_fees, royalty_percentage, royalty_wallet, description, nft_id, policy_name, artist, ADAMagic_fee, ADAMagic_wallet, username_wallet, flags, buyer_address_stored, beneficiary_address, policy_id = load_info(username, nft_name)

    # Clean transaction
    craft_tx = clear_tx(home_path, mainTest, project_address)

    # Get tx_hash, tx_in, lovelaces in an array for this wallet [tx_hash, tx_in, lovelaces]
    utxo_lovelace = get_tx_info(craft_tx)

    # CASES:
    # Case 0: 0, 0, 0
    # No txs and nothing to look for, exit
    if ((flags[0] == 0) and (utxo_lovelace == [])):
        print(f'Case 0, No txs      User: {username},       NFT: {nft_name},        ')
        return

    elif ((flags[0] == 0) and (utxo_lovelace != [])):
        print(f'Case 0, 1 tx        User:       {username},     NFT: {nft_name},        ')
        # Load all transaction history from project wallet before taking action
        json_data = fetch_blockchain_data(project_address)
        # Check for valid transactions sent
        for tx in utxo_lovelace:

            # Rename tx variables
            tx_hash = tx[0]
            tx_in = tx[1]
            ada_sent1 = tx[2]
            
            if ada_sent1 < price:
                print('ada_sent1 < price')
                continue
                # return tx
                #Load sender address and Lovelaces sent
                buyer_address, ada_sent, new_hash = fetch_ada_sent_from_wallet2(json_data, tx_hash, project_address)
                try:
                    response = send_ada_penalized_transaction_single_nft(home_path, mainTest, username, nft_name, ada_sent1, buyer_address, tx_hash, tx_in)
                    if response == True:
                        # save_current_flag_status(username, nft_name, '0, 0, 0', new_hash, buyer_address)
                        print('returned tx')
                except:
                    # Transaction is probably less than 1 ADA and it gets stacked
                    print(f'Tx problem, ada_sent: {ada_sent}')
                    continue

            elif ada_sent1 == price:
                # Transaction is correct,
                #Load sender address and Lovelaces sent
                buyer_address, ada_sent, new_hash  = fetch_ada_sent_from_wallet2(json_data, tx_hash, project_address)
                response = send_ada_penalized_transaction_single_nft(home_path, mainTest, username, nft_name, ada_sent1, username_wallet, tx_hash, tx_in)
                if response == True:
                    # Update status
                    save_current_flag_status(username, nft_name, '1, 0, 0', new_hash, buyer_address)
                    requests.get(f'https://adamagic.io/sinfle_nft_sold//{username}/{nft_name}')
                    print('saved 1, 0, 0')
            else:
                # Transaction is correct but the buyer sent more ada
                # Option 1: Money back is less than minimum 1000000 lovelaces
                #Load sender address and Lovelaces sent
                buyer_address, ada_sent, new_hash = fetch_ada_sent_from_wallet2(json_data, tx_hash, project_address)
                if int(ada_sent1) - int(price) <= 1250000:
                    response = send_ada_penalized_transaction_single_nft(home_path, mainTest, username, nft_name, ada_sent1, username_wallet, tx_hash, tx_in)
                    if response == True:
                        # Update status
                        save_current_flag_status(username, nft_name, '1, 0, 0', new_hash, buyer_address)
                        print('saved 1, 0, 0')
                # Option 2: Money is returned
                else:
                    print(f'ADA SEND: {ada_sent1}')
                    response = send_extra_ada_penalized_transaction_single_nft(home_path, mainTest, username, nft_name, ada_sent1, username_wallet, tx_hash, tx_in, buyer_address, price)
                    if response == True:
                        # Update status
                        save_current_flag_status(username, nft_name, '1, 0, 0', new_hash, buyer_address)
                        print('saved 1, 0, 0')

        return

    # Case 1: 1, 0, 0
    if flags[1] == 0:
        print(f'Case 1      User:       {username},     NFT: {nft_name},        ')
        results = fetch_updated_data(username, nft_name)
        price = results["price"]
        price = int(price) * 1000000

        # Clean transaction
        craft_tx = clear_tx(home_path, mainTest, username_wallet)
        utxo_lovelace_username = get_tx_info(craft_tx)

        # Check if the tx was received and mint along
        for txs in utxo_lovelace_username:
            tx_hash = txs[0].replace('\n', '')
            tx_in = txs[1]
            ada_sent = txs[2]
            if ((int(ada_sent) > int(price)-300000) and (int(ada_sent) < int(price)+300000)):
                # json_data = fetch_blockchain_data(project_address)
                # json_data = json.dumps(json_data)
                # if tx_hash in json_data:

                    # Tx was received and you can start minting
                try:
                    create_metadata(username, results)
                    mint_response = mint_on_another_address_single_nft(home_path, mainTest, username, beneficiary_address, policy_name, results["nft_name"], '1', '1', ADAMagic_wallet, ADAMagic_fee , buyer_address_stored, ada_sent, tx_hash, tx_in, results["original_nft_name"])
                except Exception as e:
                    print(f'{e}')
                    print('fuck!')
                    return
                if mint_response == True:
                    password = ''
                    response = requests.get(f'https://adamagic.io/sinfle_nft_sold/{password}{username}/{results["nft_name"]}')
                    original_nft_name = results["original_nft_name"]
                    original_nft_name = original_nft_name.replace(' ', '_')
                    save_current_flag_status(username, original_nft_name, '1, 1, 0', '', buyer_address_stored)
                    print('saved 1, 1, 0')
                    return
                else:
                    print(f'Transaction did not go through | {mint_response}')
        return

    # Case 2: 1, 1, 0
    if flags[2] == 0:
        print(f'Case 2      User:       {username},     NFT: {nft_name},        ')
        json_data = fetch_blockchain_data(buyer_address_stored)
        if project_address in json.dumps(json_data):
            # Buyer received the NFT
            save_current_flag_status(username, nft_name, '1, 1, 1', '', buyer_address_stored)
            print('saved 1, 1, 1')

            # Update database from website
            response = requests.get(f'https://adamagic.io/sinfle_nft_sold/{username}/{nft_name}/')

        return

    # Case 3: 1, 1, 1
    # Send back all txs

    if utxo_lovelace != []:
        print(f'Case 3      User: {username}, NFT: {nft_name}, ')
        json_data = fetch_blockchain_data(project_address)
        for tx in utxo_lovelace:
            tx_hash = tx[0]
            tx_in = tx[1]
            ada_sent = tx[2]
            tx_hash = tx_hash.replace('\n', '')

            if ada_sent > 1250000:
                buyer_address, ada_sent, new_hash = fetch_ada_sent_from_wallet2(json_data, tx_hash, project_address)
                response = send_ada_penalized_transaction_single_nft(home_path, mainTest, username, nft_name, ada_sent, buyer_address, tx_hash, tx_in)


def main():
    query = 'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_35_create_single_nft_extended.py'
    query = subprocess.call(query, shell=True)
    list_of_addresses = import_projects()
    print(f'Number of projects to check their status: {len(list_of_addresses)}')
    list_of_addresses = list_of_addresses[:]
    # print(list_of_addresses)
    # cardano_scan('')
    # sys.exit()
    start = time.time()
    status = []
    for single_nfts in list_of_addresses:
        username = single_nfts[0]
        nft_name = single_nfts[1]
        nft_address = single_nfts[2]
        scroll(username, nft_name, nft_address)
        # cardano_scan(project_address)
        # p = Process(target=cardano_scan, args=([nft_address]))
        # p = Process(target=scroll, args=(username, nft_name, nft_address))
        # p.start()
        # cardano_scan(nft_address)
        # sys.exit()
        # status.append(Q.get())
    # p.join()

    print(f'{time.time() - start} Seconds took the whole thing to scrape')
    # print(status)

    # start = time.time()
    # for single_nfts in list_of_addresses:
    #     username = single_nfts[0]
    #     nft_name = single_nfts[1]
    #     nft_address = single_nfts[2]
    #     scroll(username, nft_name, nft_address)
    # print(time.time() - start)

main()
