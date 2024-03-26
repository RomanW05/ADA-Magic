import random
import sys
import time
import os
import json
from os.path import exists
import subprocess
from orderedCommands import currentSlotD
import requests
import base64
from PIL import Image
from time import strftime, localtime


def fetch_data_from_website():
    password = ''
    results = requests.get(f'https://adamagic.io/compose_single_nft/{password}')
    results = json.loads(results.text)

    return results


def create_folders(username, temp_name):
    try:
        os.mkdir(f'/home/yop/Downloads/cardano/single_nfts/{username}/')
    except Exception as e:
        pass
    try:
        os.mkdir(f'/home/yop/Downloads/cardano/single_nfts/{username}/{temp_name}/')
    except Exception as e:
        pass
    try:
        os.mkdir(f'/home/yop/Downloads/cardano/temp_keys/{temp_name}/')
    except Exception as e:
        pass


def create_policy(username, policy_name, timelock):
    if exists(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.script'): 
        # print('generatePolicy exists, exiting function')
        return
    try:
        # Generate policy keys
        generate_policy = f'/home/yop/Downloads/cardano/cardano-node-1.33.0-linux/cardano-cli address key-gen --verification-key-file /home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.vkey --signing-key-file /home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.skey'
        subprocess.call(generate_policy,shell=True)
        time.sleep(0.1)
        
        # CREATE new policy
        # Need a limit when to mint: Current slot + time added
        current_slot = currentSlotD(homePath, mainTest)

        #Need keyhash
        query = homePath + 'cardano-cli address key-hash --payment-verification-key-file ' + f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.vkey'
        result = subprocess.check_output(query,shell=True)
        time.sleep(0.1)
        result = result.decode('utf-8')
        key_hash = result.replace('\n', '')

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
        policy['scripts'][0]['slot'] = int(current_slot) + int(timelock)
        policy['scripts'][1]['keyHash'] = str(key_hash)
        string_policy = str(policy)
        string_policy = string_policy.replace("'", '"')

        path = f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.script'
        with open(path, 'w') as f:
            f.write(string_policy)
        time.sleep(0.1)

        #PolicyID
        policy_id = homePath + 'cardano-cli transaction policyid --script-file ' + f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.script'
        policy_id = subprocess.check_output(policy_id,shell=True)
        time.sleep(0.1)
        policy_id = policy_id.decode('utf-8').replace('\n', '')
        path = f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.txt'
        with open(path, 'w') as text:
            text.write(str(policy_id))
        path = f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_id.txt'
        with open(path, 'w') as text:
            text.write(str(policy_id))



    except Exception as e:
        print(f'Error while creating NFT: {e}')
        with open('/home/yop/Downloads/cardano/error_log.txt', 'a') as text:
            text.write(f'\n{e}, Error while creating policy id. a_35_create_single_nft.py\n')


def reconvert_base64_image(img64, username, nft_name):
    img64 = bytes(img64,'UTF-8')
    png_recovered = base64.decodebytes(img64)

    path = f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/{nft_name}.png'
    with open(path, 'wb') as f:
        f.write(png_recovered)
    im = Image.open(path)
    # im.save(path, 'webp')

    new_path = f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/{nft_name}_thumbnail.png'
    im = Image.open(path)
    im.thumbnail([200, 200])
    im.save(new_path, 'webp')


def update_db(username, internal_id, policy_id, policy_name, nft_wallet, nft_name):
    password = ''
    results = requests.get(f'https://adamagic.io/resync_single_nft_db/{password}/{nft_wallet}/{internal_id}/{policy_id}/{username}/{policy_name}/{nft_name}')
    if 'page not found' in results.text:
        print(f'Updated results: page not found | {nft_name} {username}')
    else:
        print(f'Updated results: {results.text} | {nft_name} {username}')


def create_project(elem):
    # return
    # try:
        # Load data
        # username = 'nasartz'
        # policy_name = 'Standard'
        # timelock = 3650 * 24*60*60
        # using_old_policy = False
    # print(f'\n\
    #     {elem["username"]}\n \
    #     {elem["nft_name"]}\n \
    #     {elem["using_old_policy"]}\n \
    #     {elem["policy_name"]}\n \
    #     {elem["royalty_percentage"]}\n \
    #     {elem["royalty_wallet"]}\n \
    #     {elem["timelock"]}\n \
    #     {elem["description"]}\n \
    #     {elem["nft_id"]}\n \
    #     {elem["price"]}\n \
    #     {elem["artist"]}\n \
    #     {elem["selling_fees"]}\n \
    #     {elem["beneficiary_address"]}')

    username = elem["username"]  # username
    nft_name = elem["nft_name"]  # nft_name
    # using_old_policy = elem["using_old_policy"] # Using old policy ID
    policy_name = elem["policy_name"]  # policy
    if policy_name == '':
        policy_name = 'Standard'
    royalty_percentage = elem["royalty_percentage"]  # royalty_percentage
    royalty_wallet = elem["royalty_wallet"]  # royalty_wallet
    try:
        timelock = int(elem["timelock"]) * 60 * 60 * 24  # policy_duration
    except:
        timelock = 3650 * 60 * 60 * 24
    description = elem["description"]  # description
    nft_id = 1
    price = elem["price"]
    buyer_pay_fees = '0'
    artist = elem["artist"]
    try:
        selling_fees = int(elem["selling_fees"])
    except:
        selling_fees = int((int(price)/100)) + 2
    price = int(price) * 1000000
    beneficiary_address = elem["beneficiary_address"]
    full_size_image = elem["full_size_image"]
    thumbnail_img = elem["thumbnail_img"]
    internal_id = elem["internal_id"]

    print(username, nft_name)

    nft_name = nft_name.replace(' ', '_')
    create_folders(username, nft_name)
    reconvert_base64_image(full_size_image, username, nft_name)

    query = 'export CARDANO_NODE_SOCKET_PATH=/home/yop/Downloads/cardano/db1.33.0/node.socket'
    subprocess.check_output(query,shell=True)

    # Check if policy exists
    if exists(homePath + 'keys/' + username + '/' + policy_name + '.script'):
        with open(homePath + 'keys/' + username + '/' + policy_name + '.txt') as text:
            policy_id = text.read()

        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_id.txt', 'w') as text:
            text.write(policy_id)
    else:
        create_policy(username, policy_name, timelock)
    # Make sure folders are been created
    # sys.exit()
    

    # try:
    query = 'export CARDANO_NODE_SOCKET_PATH=/home/yop/Downloads/cardano/db1.33.0/node.socket'
    subprocess.check_output(query,shell=True)

    # Create seed phrase
    seed = '/home/yop/Downloads/cardano-node1.30.0/cardano-wallet recovery-phrase generate > ' + f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/SeedPhrase.txt'
    subprocess.call(seed, shell=True)
    time.sleep(0.1)

    # Create wallet
    os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_36_create_wallet_testnet.py {nft_name}')
    time.sleep(0.1)
    
    # Migrate files from one folder to another
    if not os.path.exists(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/{nft_name}.addr'):
        for subdir, dirs, files in os.walk(f'/home/yop/Downloads/cardano/temp_keys/{nft_name}'):
            for file in files:
                os.rename(f'/home/yop/Downloads/cardano/temp_keys/{nft_name}/{file}', f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/{file}')
    time.sleep(0.1)

    # Export parameters
    exportParams = f'/home/yop/Downloads/cardano/cardano-node-1.33.0-linux/cardano-cli query protocol-parameters {mainTest} --out-file /home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/protocol.json'
    subprocess.call(exportParams,shell=True)
    time.sleep(0.1)

    # Store NFT
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/price.txt', 'w') as text:
        text.write(f'{price}')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/buyer_pay_fees.txt', 'w') as text:
        text.write(buyer_pay_fees)
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_percentage.txt', 'w') as text:
        text.write(royalty_percentage)
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_wallet.txt', 'w') as text:
        text.write(royalty_wallet)
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/description.txt', 'w') as text:
        text.write(description)
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/nft_id.txt', 'w') as text:
        text.write(f'{nft_id}')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_name.txt', 'w') as text:
        text.write(policy_name)
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/artist.txt', 'w') as text:
        artist = artist.replace('_', ' ')
        text.write(artist)
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/hashes.txt', 'w') as text:
        text.write('')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/selling_fees.txt', 'w') as text:
        text.write(f'{selling_fees}')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/ADAMagic_fee.txt', 'w') as text:
        text.write(f'{selling_fees}')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/flags.txt', 'w') as text:
        text.write('0, 0, 0')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/beneficiary_address.txt', 'w') as text:
        text.write(beneficiary_address)
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/internal_id.txt', 'w') as text:
        text.write(f'{internal_id}')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/buyer_address.txt', 'w') as text:
        text.write(f'')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/{nft_name}.addr', 'r') as text:
        nft_wallet = text.read()
    query = f'/home/yop/Downloads/cardano-node1.30.0/cardano-cli transaction policyid --script-file /home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.script'
    policy_id = subprocess.check_output(query,shell=True)
    policy_id = policy_id.decode('utf-8').replace('\n', '')

    # print(f'Policy ID: {policy_id}')
    update_db(username, internal_id, policy_id, policy_name, nft_wallet, nft_name)





testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet
homePath = '/home/yop/Downloads/cardano-node1.30.0/'

main_start = int(time.time())
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
while True:
    try:
        results = fetch_data_from_website()
        if len(results) != 0:
            print(f'Project to be imported: {len(results)}')
        for elem in results:
            create_project(results[elem])
    except Exception as e:
        print(f'{e}')

    time.sleep(120)
    if int(time.time()) > (main_start + 3600):
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        main_start = int(time.time())

    # sys.exit()
