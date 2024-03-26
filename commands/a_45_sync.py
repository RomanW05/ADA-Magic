import os
import sys
import json
import subprocess
import requests
import time
from os.path import exists
import mysql.connector
import paramiko
from orderedCommands import loadAddress
from orderedCommands import sendSimpleTransaction
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)


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


def request_data():
    results = requests.get('https://adamagic.io/resync_single_nft/')
    print(results.text)
    results = json.loads(results.text)

    return results


def update_db(data):
    nft_wallet = data[0]
    policy_id = data[1]
    internal_id = data[2]
    username = data[3]
    policy_name = data[4]
    nft_name = data[5]
    
    results = requests.get(f'https://adamagic.io/resync_single_nft_db//{nft_wallet}/{policy_id}/{internal_id}/{username}/{policy_name}/{nft_name}')
    print(f'Updated results: {results.text}')



def create_project(data):
    x = 0
    while True:
        try:
            username = data[str(x)]["username"]  # username
        except Exception as e:
            print(f'Done creating projects {e}')
            break

        username = data[str(x)]["username"]  # username
        nft_name = data[str(x)]["nft_name"]  # nft_name
        using_old_policy = data[str(x)]["using_old_policy"] # Using old policy ID
        policy_name = f'{data[str(x)]["policy"]}'  # policy
        royalty_percentage = data[str(x)]["royalty_perc"]  # royalty_percentage
        royalty_wallet = data[str(x)]["royal_wallet"]  # royalty_wallet
        timelock = int(data[str(x)]["policy_duration"]) * 60 * 60 * 24  # policy_duration
        description = f'{data[str(x)]["desc"]}'  # description
        nft_id = data[str(x)]["nftid"]  # NFT ID
        price = data[str(x)]["price"]
        buyer_pay_fees = data[str(x)]["buyer_pay_fees"]
        artist = f'{data[str(x)]["artist"]}'
        selling_fees = data[str(x)]["selling_fees"]
        beneficiary_address = data[str(x)]["beneficiary_address"]
        internal_id = data[str(x)]["internal_id"]


        temp_name = nft_name
        temp_name = temp_name.replace(' ', '_')
        create_folders(username, temp_name)

        query = f'export CARDANO_NODE_SOCKET_PATH=/home/yop/Downloads/cardano-node1.30.0/dbMainnet/node.socket; python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_35_create_single_nft.py {username} {nft_name} {using_old_policy} {policy_name} {royalty_percentage} {royalty_wallet} {timelock} "{description}" {nft_id} {price} {buyer_pay_fees} "{artist}" {selling_fees} {beneficiary_address}'
        result = subprocess.call(query,shell=True)
        print(f'\n --{username}\n --{nft_name}\n --{using_old_policy}\n --{policy_name}\n --{royalty_percentage}\n --{royalty_wallet}\n --{timelock}\n --{description}\n --{nft_id}\n --{price}\n --{buyer_pay_fees}\n --{artist}\n --{selling_fees}\n --{beneficiary_address} \nwith code: {result}')

        # Success
        if result == 0:
            with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_id.txt', 'r') as text:
                policy_id = text.read()
            with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/{nft_name}.addr', 'r') as text:
                nft_address = text.read()

            print('NFTS to update:', nft_address, policy_id, internal_id)
            update_db([nft_address, policy_id, internal_id, username, policy_name, nft_name])

        x += 1




data = request_data()
create_project(data)
# print()