import os
import sys
import json
import subprocess
import time
import requests
# from multiprocessing import Process, Queue
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
from m_7_manually_send_ada_no_fee_multiples_website import transfer_funds
from bs4 import BeautifulSoup
from threading import Thread
from time import strftime, localtime
import logging
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import smtplib, ssl
from email.message import EmailMessage
import email.utils
from email.mime.text import MIMEText
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



def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding





def cardano_scan(project_address, info, username, nft_name, nft_price, internal_id):
    # print(project_address, info, username, nft_name, 'project_address, info, username, nft_name')
    sender_address = ''
    money_received = 0
    tx_hash = ''
    money_flag = False
    tx_flag = False
    fetched_index = None
    tx_flag2 = False

    #RESTORE THIS BLOCK
    try:
        results = requests.get(f'https://cardanoscan.io/address/{project_address}')
        results = results.text
    except Exception as e:
        return
    soup = BeautifulSoup(results, 'html.parser')
    for link in soup.find_all('span'):
        if 'h4 adaAmount text-success font-weight-bold' in str(link):
            try:
                if int(link.text) == 0:
                    continue
                else:
                    print(f'NEW TX FOUND!!!\n{nft_name} {project_address} {link.text}')
                    tx_flag2 = True

            except:
                continue

    
    #RESTORE THIS BLOCK
    if tx_flag2 == False:
        # print(project_address, tx_flag, sender_address, money_received)
        info.append([project_address, tx_flag2, sender_address, money_received, username, nft_name, tx_hash])
        return

    # Fetch sender address and money sent
    txs = []
    info_temp = []
    for link in soup.find_all('table'):
        if 'table class="table table-striped"' not in str(link):
            continue
        # print(link.tbody)
        trs = []
        temp = []
        for tr in link.tbody.find_all('tr'):
            if "onclick" in str(tr):
                trs.append(temp)
                temp = []
                temp.append(tr)
            temp.append(tr)
        trs.append(tr)
        trs = str(link.tbody)
        trs_list = trs.split('onclick')[1:]
        # print(trs_list)
        # print(trs_list)
        if len(trs_list) > 0:
            txs.append(trs_list)
    # print(f'TXS: {txs}')
    if txs == []:
        return

    try:

        for elem in txs[0]:
            soup = BeautifulSoup(elem, 'html.parser')
    except Exception as e:
        info.append([project_address, tx_flag2, sender_address, money_received, username, nft_name, tx_hash])
        return

    for elem in txs[0]:
        soup = BeautifulSoup(elem, 'html.parser')
        for link in soup.find_all('a'):
            if 'href="/transaction/' in str(link):
                if len(link.text) == 64:
                    tx_hash = link.text
                    print('tx_hash: ', tx_hash)



        for link in soup.find_all('div'):
            if (("transactions-container" in str(link)) and (project_address in str(link))):
                temp = str(link)
                temp = temp.split('adaAmount')[1]
                temp = temp.split('span')[0]
                temp = temp.split('>')[1]
                money_received = temp.split('<')[0]

                temp = str(link)
                temp = temp.split('href="/address/')
                temp = temp[0]

                for link2 in link.find_all('a'):
                    if 'addr' in link2.text:
                        sender_address = link2.text

        info_temp = [project_address, tx_flag2, sender_address, money_received, username, nft_name, tx_hash]
    if info_temp != []:
        info.append(info_temp)
        if int(money_received) == int(nft_price):
            password = ''
            results = requests.get(f'https://adamagic.io/single_nft_sold/{password}/{internal_id}')
            print(f'Updated db sold nft for: {internal_id} {results.text}')
    return



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
    print('loading info')
    try:

        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/internal_id.txt', 'r') as text:
            internal_id = text.read()
        internal_id = internal_id.replace('\n', '')
        password = ''
        results = requests.get(f'https://adamagic.io/fetch_nft_data/{password}/{internal_id}')
        nft = json.loads(results.text)

        # Load data of NFT
        buyer_pay_fees = 0
        nft_id = 1
        artist = nft["artist"]
        description = nft["description"]
        policy_id = nft["policy_id"]
        price = nft["price"]
        price = str(int(price) * 1000000)
        ADAMagic_fee = nft["selling_fees"]
        ADAMagic_fee = str(int(ADAMagic_fee) * 1000000)
        royalty_percentage = nft["royalty_percentage"]
        royalty_wallet = nft["royalty_wallet"]
        policy_name = nft["policy_name"]
        email = nft["email"]
        if policy_name == '':
            policy_name = 'Standard'
    except Exception as e:
        print(f'Exception while loading from website def load_info: {e}')

    try:
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_name.txt', 'r') as text:
            policy_name = text.read()
            policy_name = policy_name.replace('\n', '')
        with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/ADA_Magic_io/ADA_Magic_io.addr', 'r') as text:
            ADAMagic_wallet = text.read()
        with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{username}.addr', 'r') as text:
            username_wallet = text.read()
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/flags.txt', 'r') as text:
            flags = text.read()
            flags = flags.replace('\n', '')
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
        beneficiary_address = username_wallet
        royalty_wallet = username_wallet
    except Exception as e:
        print(f'Exception while loading from local server def load_info: {e}')
    print('info loaded')

    return price, buyer_pay_fees, royalty_percentage, royalty_wallet, description, nft_id, policy_name, artist, ADAMagic_fee, ADAMagic_wallet, username_wallet, flags, buyer_address, beneficiary_address, policy_id, internal_id, nft, email


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
    original_nft_name = results["original_nft_name"]
    original_nft_name = original_nft_name.replace(' ', '_')
    original_nft_name = original_nft_name.replace('\n', '')
    # if os.path.exists(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/metadata.json'):
    #     print('metadata already created')
    #     return
    price = results["price"]
    price = price.replace('\n', '')
    price = int(price) * 1000000
    description = results["description"]
    if description[0] == '"':
        description = description[1:]
    if description[-1] == '"':
        description = description[:-1]
    royalty_percentage = results["royalty_percentage"]
    royalty_wallet = results["royalty_wallet"]
    if len(royalty_wallet) < 10:
        with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{username}.addr') as text:
            royalty_wallet = text.read()
            royalty_wallet = royalty_wallet.replace('\n', '')
            royalty_wallet = royalty_wallet.replace(' ', '')
    artist = results["artist"]
    artist = artist.replace('\n', '')
    nft_name = results["nft_name"] # Variable change, if any


    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/buyer_pay_fees.txt', 'r') as text:
        buyer_pay_fees = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/nft_id.txt', 'r') as text:
        nft_id = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/policy_name.txt', 'r') as text:
        policy_name = text.read()
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

    query = f'/home/yop/Downloads/cardano-node1.30.0/cardano-cli transaction policyid --script-file /home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.script'
    policy_id = subprocess.check_output(query,shell=True)
    policy_id = policy_id.decode('utf-8').replace('\n', '')

    # Upload images to the IPFS
    print('Uploading file to ipfs')
    query = f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_27_upload_im_ipfs.py /home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/{original_nft_name}.png'
    result = subprocess.check_output(query,shell=True)
    print(f'File uploaded to the ipfs with results: {result}')
    
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/{original_nft_name}_hash.txt') as text:
        NFTImageUrl = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/{original_nft_name}_thumbnail_hash.txt') as text:
        NFTImageUrlThumbnail = text.read()


    if royalty_percentage == '0':
        print('Creating metadata withOUT royalties')
        metadataCreationWithOutRoyalties(home_path, mainTest, username, policy_name, description, original_nft_name, "1", NFTImageUrl, NFTImageUrlThumbnail, artist)
    else:
        royalty_percentage = '0.' + royalty_percentage
        print('Creating metadata WITH royalties')
        metadataCreation(home_path, mainTest, username, policy_name, description, original_nft_name, "1", NFTImageUrl, royalty_percentage, royalty_wallet, NFTImageUrlThumbnail, artist)


    # old = home_path + 'keys/' + username + '/' + policy_id + original_nft_name + str(1) + 'metadata.json'
    old = f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_id}{original_nft_name}{1}metadata.json'
    new = f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/metadata.json'
    try:
        os.rename(old, new)
    except:
        try:
            old = f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_id}{original_nft_name}metadata.json'
            new = f'/home/yop/Downloads/cardano/single_nfts/{username}/{original_nft_name}/metadata.json'
            os.rename(old, new)
        except:
            print(f'File: {old} not found')

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
                        with open(f'{path}/price.txt', 'r') as text:
                            nft_price = text.read()
                            nft_price = nft_price.replace('\n', '')
                        with open(f'{path}/internal_id.txt', 'r') as text:
                            internal_id = text.read()
                            internal_id = internal_id.replace('\n', '')

                        list_of_addresses.append([username, single_nft, project_address, nft_price, internal_id])
                    except Exception as e:
                        continue

    return list_of_addresses


def create_no_name_token(homePath, mainTest, username, policy_name):
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{username}.addr') as text:
        userAddress = text.read()
        userAddress = userAddress.replace('\n', '')
        userAddress = userAddress.replace(' ', '')
    try:
        createNoNameTokens(homePath, mainTest, username, userAddress, policy_name, '1', '1')
        checkForCreatedDeletedNoNameToken(homePath, mainTest, username, userAddress, policy_name, '0')
        createNoNameTokens(homePath, mainTest, username, userAddress, policy_name, '0', '-1')
        checkForCreatedDeletedNoNameToken(homePath, mainTest, username, userAddress, policy_name, '1')
        with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}LOADED.txt' ,'w') as text:
            text.write('Loaded')
    except Exception as e:
        sys.exit(1)


def fetch_updated_data(username, internal_id):
    print('retrieving data from adamagic')
    try:
        password = ''
        results = requests.get(f'https://adamagic.io/fetch_nft_data/{password}/{internal_id}')
        # results = requests.get(f'https://adamagic.io/fetch_for_metadata_single_nft/{password}/{username}/{original_nft_name}')
        results = json.loads(results.text)
    except Exception as e:
        print(f'{e}')
    print('done retrieving')
    return results


def fetch_for_tx(addr, username_wallet):
    results = requests.get(f'https://cardanoscan.io/address/{addr}')
    results = results.text
    if username_wallet in results:
        return True
    else:
        return False


def user_wants_their_money():
    results = requests.get(f'https://adamagic.io/withdraw_balance/check')
    results = results.text.replace('\n', '')
    if results == '{}':
        return
    users = json.loads(results)
    for user in users.items():
        username = user[0]
        address = user[1]

        # Check everything is ok before sending the funds
        if unsolved_projects_check(username):  # if True
            continue


        result = transfer_funds(username, address)

        payload = {
                'password': '',
                'username': f'{username}'
                }

        if result:
            status = requests.get(f'https://adamagic.io/withdraw_balance/update', params=payload)
            print(f'{username} {status.text}')
        else:
            status = requests.get(f'https://adamagic.io/withdraw_balance/inform', params=payload)
            print(f'{username} {status.text}')

    return


def unsolved_projects_check(username):
    if username == 'Smilesgfx':
        return True
    path = f'/home/yop/Downloads/cardano/single_nfts/{username}'
    try:
        single_nfts = os.listdir(path)
    except:
        return True
    for nft in single_nfts:
        if os.path.isdir(f'{path}/{nft}'):  # now you are inside a single nft folder, check flags
            with open(f'{path}/{nft}/flags.txt') as text:
                flags = text.read()
                flags = flags.replace('\n', '')
            if ((flags == '1, 0, 0') or (flags == '1, 1, 0')):
                return True

    return False


def send_congratulations_email(username, to_email, nft_name, price):
    try:
        print(f'sending email to: {username}. With email: {to_email}')
        server='server105.web-hosting.com'
        from_email='info@adamagic.io'
        password = ''
        # body = f"Congratulations, {username}\n\nYour artwork {nft_name} has been sold for {price} ADA.\nYou can claim it by logging in, going to your profile https://adamagic.io/profile/{username}, select a correct Cardano wallet address and double check it is correct, hit send.\nPlease, make sure it is the right one because once we send the money, we will no longer be able to recover it\nThank you for using our platform and have a great day.\n\nKind Regards,\nRoman,\nADA Magic Marketplace"
        body = f"Congratulations, {username}!\n\nYour artwork {nft_name} has been sold for {price} ADA. You can claim it by logging in, going to your profile https://adamagic.io/profile/{username}, select a correct Cardano wallet address and double check it is correct, hit send.\nThank you for using our platform and have a great day.\n\nKind Regards,\nRoman\nADA Magic Marketplace"
        subject = f"Congratulations, you sold on ADA Magic {nft_name} for {price} ADA"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        s = smtplib.SMTP_SSL(server)
        s.login(from_email, password)
        s.sendmail(from_email, [to_email], msg.as_string())
        s.quit()
    except Exception as e:
        print(f'{e}')
    print('Congrats email sent')





































def scroll(username, nft_name, project_address, tx_flag, sender_address, money_received, tx_hash_seller, nft_flags):

    # LOADING SECTION!!!

    # Load information
    print('inside scroll')
    print(f'\n    Displaying data for:\n    project_address: {project_address}\n    tx_flag: {tx_flag}\n    sender_address: {sender_address}\n    money_received: {money_received}\n    username: {username}\n    nft_name: {nft_name}\n    tx_hash: {tx_hash_seller}\n    nft_flags {nft_flags}\n')
    price, buyer_pay_fees, royalty_percentage, royalty_wallet, description, nft_id, policy_name, artist, ADAMagic_fee, ADAMagic_wallet, username_wallet, flags, buyer_address_stored, beneficiary_address, policy_id, internal_id, results, email = load_info(username, nft_name)
    print('info fetched')
    # print('tx_flag, nft_name, money_received, sender_address', tx_flag, nft_name, money_received, sender_address)


    # Increases scalability
    if ((flags[0] == 0) and (tx_flag == False)):
        # print(f'Case 0, No txs      User: {username},       NFT: {nft_name},        ')
        return

    if ((flags[2] == 1) and (tx_flag == False)):
        # print(f'Case 3, No txs      User: {username},       NFT: {nft_name},        ')
        return


    # Clean transaction
    craft_tx = clear_tx(home_path, mainTest, project_address)

    # Get tx_hash, tx_in, lovelaces in an array for this wallet [tx_hash, tx_in, lovelaces]
    utxo_lovelace = get_tx_info(craft_tx)

    # CASES:
    # Case 0: 0, 0, 0
    # No txs and nothing to look for, exit
    if ((flags[0] == 0) and (tx_flag == False)):
        print(f'Case 0, No txs      User: {username},       NFT: {nft_name},        ')
        return

    elif ((flags[0] == 0) and (tx_flag)):
        print(f'Case 0, 1 tx        User:       {username},     NFT: {nft_name},        ')
        # Load all transaction history from project wallet before taking action
        # json_data = fetch_blockchain_data(project_address)
        # Check for valid transactions sent
        if utxo_lovelace == []:
            print('Node not synchronized!')
        for transaction_number, tx in enumerate(utxo_lovelace):
            print(f'transaction_number: {transaction_number} with tx:{tx}')

            # Rename tx variables
            tx_hash = tx[0]
            tx_in = tx[1]
            ada_sent1 = tx[2]
            print(f'ada_sent1: {ada_sent1} price: {price}')

            if tx_hash != tx_hash_seller:
                print('tx_hash not maching the tx_hash_seller')
                continue
            print('price equality cases start')
            try:
                if ada_sent1 < price:
                    print(f'ada_sent1 < price ada_sent1:{ada_sent1} price:{price}')
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
                    # Transaction is correct

                    print('correct adas sent from buyer')
                    response = send_ada_penalized_transaction_single_nft(home_path, mainTest, username, nft_name, ada_sent1, username_wallet, tx_hash, tx_in)
                    if response == True:
                        # Update status
                        print('updating status')
                        save_current_flag_status(username, nft_name, '1, 0, 0', tx_hash_seller, sender_address)
                        print('saved 1, 0, 0')
                    else:
                        print('error sending transaction')

                elif ada_sent1 > price:
                    print('ada_sent1 > price')
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
                else:
                    print('there is a weird case that does not match any of the previous, take a look')
                    print(f'ada_sent1: {ada_sent1} price: {price}')
            except Exception as e:
                print(f'{e}')

        return

    # Case 1: 1, 0, 0
    if flags[1] == 0:
        print(f'Case 1      User:       {username},     NFT: {nft_name},        ')
        # results = fetch_updated_data(username, internal_id)
        # sys.exit()
        price = results["price"]
        price = int(price) * 1000000

        print('cleaning transaction')
        # Clean transaction
        craft_tx = clear_tx(home_path, mainTest, username_wallet)
        utxo_lovelace_username = get_tx_info(craft_tx)

        print('Start looking for txs')
        # Check if the tx was received and mint along
        for txs in utxo_lovelace_username:
            tx_hash = txs[0].replace('\n', '')
            tx_in = txs[1]
            ada_sent = txs[2]
            print(f'price: {price} ada sent: {ada_sent}')
            # if ((int(ada_sent) > int(price)-300000) and (int(ada_sent) < int(price)+300000)):
                # json_data = fetch_blockchain_data(project_address)
                # json_data = json.dumps(json_data)
                # if tx_hash in json_data:

                    # Tx was received and you can start minting
            try:
                if os.path.exists(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}LOADED.txt'):
                    pass
                else:
                    create_no_name_token(home_path, mainTest, username, policy_name)
                print('creating metadata')
                create_metadata(username, results)
                mint_response = mint_on_another_address_single_nft(home_path, mainTest, username, beneficiary_address, policy_name, results["nft_name"], '1', '1', ADAMagic_wallet, ADAMagic_fee , buyer_address_stored, ada_sent, tx_hash, tx_in, results["original_nft_name"])

            except Exception as e:
                print(f'{e}')
                print('fuck!')
                return
            if mint_response == True:
                # password = ''
                # response = requests.get(f'https://adamagic.io/sinfle_nft_sold/{password}/{internal_id}')
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
        if fetch_for_tx(buyer_address_stored, username_wallet):
        # json_data = fetch_blockchain_data(buyer_address_stored)
        # if project_address in json.dumps(json_data):
            # Buyer received the NFT
            save_current_flag_status(username, nft_name, '1, 1, 1', '', buyer_address_stored)
            print('saved 1, 1, 1')

            # Update database from website
            response = requests.get(f'https://adamagic.io/single_nft_sold//{internal_id}/')
            password = ''

            requests.get(f'https://adamagic.io/user_can_request_money/{password}/{username}')
            email = requests.get(f'https://adamagic.io/request_email//{username}')
            email = email.text
            email = email.replace(' ', '')
            email = email.replace('\n', '')
            send_congratulations_email(username, email, nft_name, price)


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

def remove_old_minted_from_scanner(projects):
    x = len(projects)
    new = []
    for project in projects:
        username = project[0]
        nft_name = project[1]
        # print('a')
        if os.path.exists(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/buyer_address.txt'):
            pass
        else:
            with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/buyer_address.txt', 'w') as text:
                text.write(f'')
            pass
        modified_time = os.path.getmtime(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/buyer_address.txt')
        # print('ba')
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/flags.txt') as text:
            flags = text.read()
            flags = flags.replace('\n', '')
            if ((flags == '1, 1, 1') and (int(time.time()) > (modified_time + 172800) )):  # 172800 2 days in seconds
                continue
            else:
                new.append(project)
    # print(f'Projects before: {len(projects)}, after: {len(new)}')
    return new

def main():
    # query = 'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_35_create_single_nft_extended.py'
    # query = subprocess.call(query, shell=True)
    list_of_addresses = import_projects()

    # print(f'Number of projects to check their status: {len(list_of_addresses)}')
    # list_of_addresses = list_of_addresses[:]
    # list_of_addresses = list_of_addresses[-2:-1]

    # Remove projects that were minted and sold after 2 days
    list_of_addresses = remove_old_minted_from_scanner(list_of_addresses)
    # print(f'Number of projects to search from: {len(list_of_addresses)} \n')

    start = time.time()
    threads = []
    info = []
    for number, single_nfts in enumerate(list_of_addresses):

        username = single_nfts[0]
        nft_name = single_nfts[1]
        nft_address = single_nfts[2]
        nft_price = single_nfts[3]
        internal_id = single_nfts[4]
        time.sleep(1)
        # scroll(username, nft_name, nft_address)
        process = Thread(target=cardano_scan, args=[nft_address, info, username, nft_name, nft_price, internal_id])
        process.start()
        threads.append(process)


    for process in threads:
        process.join()


    # Info:
    # project_address, tx_flag2, sender_address, money_received, username, nft_name
    for x, elem in enumerate(info):
        project_address = elem[0]
        tx_flag = elem[1]
        sender_address = elem[2]
        money_received = elem[3]
        username = elem[4]
        nft_name = elem[5]
        tx_hash = elem[6]
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/flags.txt') as text:
            nft_flags = text.read()
            nft_flags = nft_flags.replace('\n', '')

        if ((nft_flags == '0, 0, 0') and (tx_flag == False)):
            continue
        if ((nft_flags == '1, 1, 1') and (tx_flag == False)):
            continue
        print('Entering scroll')
        scroll(username, nft_name, project_address, tx_flag, sender_address, money_received, tx_hash, nft_flags)
    # print(f'{int(time.time() - start)} Seconds')

main_start = int(time.time())
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
while True:
    try:
        main()
    except Exception as e:
        print(f'Error at main(): {e}')
    
    user_wants_their_money()

    if int(time.time()) > (main_start + 3600):
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        main_start = int(time.time())
    time.sleep(120)
    
