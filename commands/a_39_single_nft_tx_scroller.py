import os
import sys
import json
import subprocess
import time
import requests
from os.path import exists
from orderedCommands import currentSlotD
from orderedCommands import balance
from orderedCommands import check_if_noname_token_is_half_minted
from orderedCommands import createNoNameTokens
from orderedCommands import checkForCreatedDeletedNoNameToken

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


def load_wallet(project_name):
    try:
        project_address = f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{project_name}.addr'
        with open(project_address, 'r') as text:
            project_address = text.read()
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
    ADAMagic_wallet = ''

    return price, buyer_pay_fees, royalty_percentage, royalty_wallet, description, nft_id, policy_name, artist, ADAMagic_fee, ADAMagic_wallet


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


def nft_tx_info(username, policy_name, single_nft, craft_tx):
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.txt') as text:
        policy_id = text.read()
    for utx in craft_tx:
        if ((policy_id in utx) and (single_nft in utx)):
            utx = utx.split(' ')
            nft_utxo = utx[0]
            nft_txin = utx[5]

            return nft_utxo, nft_txin
    return '0', '0'


def fetch_utxs(username):
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{username}.addr', 'r') as text:
        user_address = text.read()
    query = f'/home/yop/Downloads/cardano-node1.30.0/cardano-cli query utxo {mainTest} --address {user_address}'
    query = subprocess.check_output(query,shell=True)
    query = query.decode('utf-8')
    txs = query.split('\n')
    tx_out = '--tx-out '
    tx_in = ''
    money = 0
    utxs_in = 0
    for utxo in txs:
        utxo = utxo.split(' ')
        if len(utxo) == 17:  # It is not an NFT
            tx_in += f'{utxo[0]}#{utxo[5]} '
            utxs_in += 1
            money += int(utxo[13])

    return utxs_in, money, tx_in




def browse_nfts():
    # Load pending addresses:
    with open(f'/home/yop/Downloads/cardano/single_nfts/pending_nfts.txt', 'r') as text:
        pending_nfts = text.read()

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


def check_new_income():
    with open('/home/yop/Downloads/cardano/single_nfts/pending_addresses.txt', 'r') as text:
        pending = text.read()
        pending = pending.replace('\n', '')
    if pending == '':
        return ''
    list_of_addresses = []
    pending = pending.split('|')
    if pending[-1] == '':
        pending.pop(-1)
    for addresses in pending:
        if addresses[-1:] == '':
            addresses = addresses[:-1]
        info = addresses.split(',')
        username = info[0]
        nft_name = info[1]
        address = info[2]
        how_much = info[3]
        policy_name = info[4]
        policy_duration = info[5]
        list_of_addresses.append([username, nft_name, address, how_much, policy_name, policy_duration])

    return list_of_addresses


def mint_it(home_path, username, nft_name, address, how_much, policy_name, policy_duration, ADAMagic_wallet, platform_fee):
    # Check balance
    # If money, mint it
    # Send to website the address of the minted NFT
    print('mint_it')
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{username}.addr') as text:
        user_address = text.read()
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.txt') as text:
        policy_id = text.read()

    # Check for previous unfinished minted noname tokens:
    flag_to_skip = check_if_noname_token_is_half_minted(policy_id, user_address)
    if flag_to_skip:
        print('unfinished noname token')
        createNoNameTokens(home_path, mainTest, username, user_address, policy_name, 0, -1)
        checkForCreatedDeletedNoNameToken(home_path, mainTest, username, user_address, policy_name, 1)
        path = f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}LOADED.txt'
        with open(path, 'w') as text:
            text.write('policy LOADED')

    # Check balance
    money = balance(home_path, mainTest, address)
    query = f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/1current_balance.py {username}'
    query = subprocess.check_output(query,shell=True)
    query = query.decode('utf-8')
    utxs_in, money, tx_in = fetch_utxs(username)
    money = query.replace(' ', '')
    money, money_locked = money.split(',')
    if int(money) >= int(how_much):
        print('About to create NFT')

        # Fetch hash of the transaction
        # utxo_hash = 
        # The user sent the money
        # print(f'Mint_IT: {username} {nft_name} {ADAMagic_wallet} {platform_fee} {utxs_in} {money} {tx_in}')
        query = f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_38_create_nft_to_another_wallet.py {username} {nft_name} {ADAMagic_wallet} {platform_fee} {utxs_in} {money} {tx_in}'
        query = subprocess.check_output(query,shell=True)
        query = query.decode('utf-8')
        print(f'Query: {query}')
        if 'success' in query:
            return True
        else:
            return False

    else:
        return False


def scroll(username, single_nft, project_address):
    # LOADING SECTION!!!
    # Clean transaction
    craft_tx = clear_tx(home_path, mainTest, project_address)
    # if craft_tx == ['']:
    #     return

    # Get tx_hash, tx_in, lovelaces in an array for this wallet [tx_hash, tx_in, lovelaces]
    utxo_lovelace = get_tx_info(craft_tx)
    print('utxo_lovelace', utxo_lovelace)

    # Load all transaction history from project wallet before taking action
    json_data = fetch_blockchain_data(project_address)

    # Load information
    price, buyer_pay_fees, royalty_percentage, royalty_wallet, description, nft_id, policy_name, artist, ADAMagic_fee, ADAMagic_wallet = load_info(username, single_nft)

    # Fetch NFT utxo and utxin info
    nft_utxo, nft_txin = nft_tx_info(username, policy_name, single_nft, craft_tx)

    # Update pending transaction status
    # Load all pending transactions from project wallet
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/hashes.txt', 'r') as text:
        stored_hashes_whole_string = text.read()

    # Compare hashes
    new_transactions = []
    for single_hash in utxo_lovelace:

        # Single hash was sent but not received yet
        if single_hash[0] in stored_hashes_whole_string:
            print('no single_hash[0]')
            return
        new_transactions.append(single_hash)

    # In case there are no new transactions continue to the next wallet
    if len(new_transactions) == 0:
        print('no tx')
        return

    # LODING IS FINISHED
    # TAKE ACTION

    # In case someone already minted the NFT return all transactions
    if len(stored_hashes_whole_string) > 2:
        for tx in new_transactions:

            # Rename tx variables
            tx_hash = tx[0]
            tx_in = tx[1]
            ada_sent1 = tx[2]

            #Load sender address and Lovelaces sent
            sender_address, ada_sent = fetch_ada_sent_from_wallet(json_data, tx_hash, project_address)

            # ASSERT
            if int(ada_sent) != int(ada_sent1):
                print('assert2')
                sys.exit()
                return 'YOU ARE SENDING DIFFERENT AMOUNTS TO PROBABLY DIFFERENT ADDRESSES'

            # In case there is enough money to return the tx
            if ada_sent >= 1500000:
                os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_40_send_ada_penalzed_single_nft.py {username} {project_address} {ada_sent} {sender_address} {tx_hash} {tx_in} {single_nft}')

        # The NFT has been sold already 
        return

    # SELL
    for tx in new_transactions:
        print(f'One seller on {username} for NFT: {single_nft}')
        sys.exit()

        # Rename tx variables
        tx_hash = tx[0]
        tx_in = tx[1]
        ada_sent1 = tx[2]
        #Load sender address and Lovelaces sent
        sender_address, ada_sent = fetch_ada_sent_from_wallet(json_data, tx_hash, project_address)

        # ASSERT
        if int(ada_sent) != int(ada_sent1):
            print('YOU ARE SENDING DIFFERENT AMOUNTS TO PROBABLY DIFFERENT ADDRESSES')
            sys.exit()

        # Info about the misunderstanding of the buyer
        money_reminder = int(ada_sent) - int(price)

        # In case Not enough money to send back < 1000000 + fee
        if ada_sent <= 1500000:
            continue

        # In case Not enough money for one nft
        if ((int(ada_sent) > 1500000) and (int(ada_sent) < int(price))):
            os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_40_send_ada_penalzed_single_nft.py {username} {project_address} {ada_sent} {sender_address} {tx_hash} {tx_in} {single_nft}')
            print('Not enough money')
            continue

        # FINALLY, SEND THE NFTS
        os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_41_send_single_nft.py {username} {sender_address} {single_nft} {policy_name} {ADAMagic_fee} {money_reminder} {ADAMagic_wallet} {price} {nft_utxo} {nft_txin} {ada_sent} {project_address} {tx_in} {tx_hash}')
        # Store hash in unverified hashes
        # with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{single_nft}/hashes.txt', 'w') as text:
        #     text.write(f'{tx_hash}')

        return

        

def check_address_policy_minted(address):
    results = requests.get(f"https://explorer-api.testnet.dandelion.link/testnet/utxos/{address}/")
    json_data = json.loads(results.text)
    income = json_data[0]["caBalance"]

    # Money is received, time to mint
    if int(income) >= 2500000:
        os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_38_create_nft_to_another_wallet.py {username} {nft_name} {platform_address} {platform_fee}')


def gather_info():
    # Gather information to be done from the website
    password = ''
    results = requests.get(f'https://adamagic.io/check_for_money_inflow/{password}')
    addresses_to_check = results.text.split('|')
    for nft in addresses_to_check:
        username = nft[0]
        using_old_policy = nft[1]
        nft_name = nft[2]
        nft_address = nft[3]
        policy_id = nft[4]
        nft_policy_name = nft[5]

    return results


def main():

    new_list = ''
    list_of_addresses = check_new_income()
    addr = ''
    claro = ''
    platform_fee = 1000000
    if list_of_addresses != '':
        for info in list_of_addresses:
            username = info[0]
            nft_name = info[1]
            address = info[2]
            how_much = info[3]
            policy_name = info[4]
            policy_duration = info[5]
            price, buyer_pay_fees, royalty_percentage, royalty_wallet, description, nft_id, policy_name, artist, ADAMagic_fee, ADAMagic_wallet = load_info(username, nft_name)
            response = mint_it(home_path, username, nft_name, address, how_much, policy_name, policy_duration, ADAMagic_wallet, platform_fee)

            # Delete NFT. mint_it returns True, False. True for success, False for not
            print('response', response)
            if not response:
                for elem in info:
                    new_list += f'{elem},'
                new_list = new_list[:-1] + '|'
        with open('/home/yop/Downloads/cardano/single_nfts/pending_addresses.txt', 'w') as text:
            text.write(f'{new_list}')



    list_of_addresses = browse_nfts()
    for single_nfts in list_of_addresses:
        username = single_nfts[0]
        single_nft = single_nfts[1]
        nft_address = single_nfts[2]

        scroll(username, single_nft, nft_address)

main()
