import os
import sys
import json
import subprocess
import time
import random
from os.path import exists
from orderedCommands import currentSlotD
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet
homePath = '/home/yop/Downloads/cardano-node1.30.0/'

project_name = sys.argv[1]
timelock = int(sys.argv[2])
nfts_total = sys.argv[3]
price = sys.argv[4]
theoretical_maximum = sys.argv[5]
artist = sys.argv[6]
minting_date = sys.argv[7]
number_of_layers = int(sys.argv[8])
profit_wallet_address = sys.argv[9]

# Delete all files and folders of a project
try:
    folders = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}')
    for folder in folders:
        if os.path.isdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{folder}'):
            files = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{folder}')
            for file in files:
                os.remove(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{folder}/{file}')
            os.rmdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{folder}')
    os.rmdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}')
except Exception as e:
    logging.exception(f'a_34_create_vending_machine_project_redo.py|\nProject name:{project_name}')



try:
    try:
        os.mkdir(f'{homePath}keys/{project_name}')
        time.sleep(0.1)
    except Exception as e:
        time.sleep(0.1)
        print(f"Error creating folder: {homePath}keys/{project_name}")

    try:
        os.mkdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}')
        time.sleep(0.1)
    except:
        time.sleep(0.1)
        print(f"Error creating folder: /home/yop/Downloads/cardano/vending_machine/{project_name}")

    try:
        os.mkdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/to_upload')
        time.sleep(0.1)
    except:
        time.sleep(0.1)
        print(f"Error creating folder: /home/yop/Downloads/cardano/vending_machine/{project_name}/to_upload')")

    for layer_number in range(number_of_layers):
        layer_number += 1
        try:
            os.mkdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/layer{layer_number}')
            time.sleep(0.1)
        except:
            time.sleep(0.1)
            print(f"/home/yop/Downloads/cardano/vending_machine/{project_name}/layer{layer_number}")


    query = 'export CARDANO_NODE_SOCKET_PATH=/home/yop/Downloads/cardano/db1.33.0/node.socket'
    subprocess.check_output(query,shell=True)

    # Create seed phrase
    seed = homePath + 'cardano-wallet recovery-phrase generate > ' + homePath + 'keys/' + project_name + '/' + project_name + 'SeedPhrase.txt'
    subprocess.call(seed, shell=True)
    time.sleep(0.1)

    # Create wallet
    os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/2createNewWallet.py {project_name}')
    time.sleep(0.1)

    # Migrate files from one folder to another
    for subdir, dirs, files in os.walk(homePath + 'keys/' + project_name):
        for file in files:
            os.rename(f'{homePath}keys/{project_name}/{file}', f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{file}')
    time.sleep(0.1)

    # Export parameters
    exportParams = f'/home/yop/Downloads/cardano/cardano-node-1.33.0-linux/cardano-cli query protocol-parameters {mainTest} --out-file /home/yop/Downloads/cardano/vending_machine/{project_name}/protocol.json'
    subprocess.call(exportParams,shell=True)
    time.sleep(0.1)

    # Generate policy keys
    generate_policy = f'/home/yop/Downloads/cardano/cardano-node-1.33.0-linux/cardano-cli address key-gen --verification-key-file /home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.vkey --signing-key-file /home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.skey'
    subprocess.call(generate_policy,shell=True)
    time.sleep(0.1)

    # CREATE new policy
    # Need a limit when to mint: Current slot + time added
    current_slot = currentSlotD(homePath, mainTest)

    #Need keyhash
    query = homePath + 'cardano-cli address key-hash --payment-verification-key-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.vkey'
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

    path = f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.script'
    with open(path, 'w') as f:
        f.write(string_policy)
    time.sleep(0.1)

    #PolicyID
    policy_id = homePath + 'cardano-cli transaction policyid --script-file ' + f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.script'
    policy_id = subprocess.check_output(policy_id,shell=True)
    time.sleep(0.1)
    policy_id = policy_id.decode('utf-8').replace('\n', '')
    path = f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.txt'
    with open(path, 'w') as text:
        text.write(policy_id)
    time.sleep(0.1)

    # Store transaction hash for storing
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/hashes.txt', 'w') as text:
        text.write('')
    time.sleep(0.1)

    # Store the valuable
    # Include the artist in the project
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/artist.txt', 'w') as text:
        text.write(artist)

    # Set the price
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/price.txt', 'w') as text:
        text.write(price)

    # Set minting date
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/minting_date.txt', 'w') as text:
        text.write(minting_date)

    # Create images file structure
    path_files = []
    projects_name = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}')

    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{project_name}.addr', 'r') as text:
        address = text.read()
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/policy_id.txt', 'r') as text:
        policy_id = text.read()
    # Set wallet address for profits
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/profit_wallet_address.txt', 'w') as text:
        text.write(profit_wallet_address)


    print(f'key555word{address},{policy_id}key555word')

    sys.exit()

except Exception as e:
    print(f'FAILED creating project. Linux system 22create_vending_machine_project.py {e}')
    logging.exception('Got exception on main handler')
    raise
    