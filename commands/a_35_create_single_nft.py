import random
import sys
import time
import os
import json
from os.path import exists
import subprocess
from orderedCommands import currentSlotD
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)
with open('/home/yop/Downloads/cardano/error_log3.txt', 'w') as text:
    text.write(f'{time.time()}')


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


def metadata_creation(homePath, mainTest, user, policy_name, NFTDescription, NFTName, NFTID, NFTImageUrl, NFTRoyaltiesPercentage, NFTRoyaltiesAddress, NFTImageUrlThumbnail):
    #Metadata Creation
    x=64
    NFTImageUrl=[NFTImageUrl[y-x:y] for y in range(x, len(NFTImageUrl)+x,x)]
    NFTImageUrlThumbnail=[NFTImageUrlThumbnail[y-x:y] for y in range(x, len(NFTImageUrlThumbnail)+x,x)]
    NFTRoyaltiesAddress=[NFTRoyaltiesAddress[y-x:y] for y in range(x, len(NFTRoyaltiesAddress)+x,x)]
    NFTDescription=[NFTDescription[y-x:y] for y in range(x, len(NFTDescription)+x,x)]
    path = f'/home/yop/Downloads/cardano/single_nfts/{user}/{NFTName}/{policy_name}.txt'
    with open(path, 'r') as text:
        policyID = text.read()
    metadata = {}
    metadata["777"] = {
                    "prc": "0.5",
                    "addr": "Testnet"
                    }
    metadata["721"] = {
                    policyID: {
                        policy_name: {
                            "name": "Cardano foundation NFT guide token",
                            "image": "Url THUMBNAIL",
                            "mediaType": "image/png",
                            "description": "This is my first NFT thanks to the Cardano foundation",
                            
                            "files": [{
                                "mediaType": "image/png",
                                "src": "Url NORMAL SIZE",
                                "name": "image name"
                                }],
                            "ID": 1,
                            }
                        },
                    "version": "1.0"
                    }
    metadata["721"][policyID][policy_name]["description"] = description
    metadata["721"][policyID][policy_name]["name"] = NFTName
    metadata["721"][policyID][policy_name]["ID"] = NFTID
    metadata["721"][policyID][policy_name]["image"] = NFTImageUrlThumbnail
    metadata["721"][policyID][policy_name]["files"][0]["src"] = NFTImageUrl
    metadata["721"][policyID][policy_name]["files"][0]["name"] = NFTName
    metadata["777"]["prc"] = NFTRoyaltiesPercentage
    metadata["777"]["addr"] = NFTRoyaltiesAddress

    metadata = str(metadata)
    metadata = metadata.replace('\n', '').replace("'", '"')
    path = homePath + 'keys/' + user + '/' + policyID + NFTName + str(NFTID) + 'metadata.json'
    with open(path, 'w') as text:
        text.write(metadata)


def metadataCreationWithOutRoyalties(homePath, mainTest, user, policy_name, NFTDescription, NFTName, NFTID, NFTImageUrl, NFTImageUrlThumbnail):
    #Metadata Creation
    x=64
    if len(NFTImageUrl) > 64:
        NFTImageUrl=[NFTImageUrl[y-x:y] for y in range(x, len(NFTImageUrl)+x,x)]
    if len(NFTImageUrlThumbnail) > 64:
        NFTImageUrlThumbnail=[NFTImageUrlThumbnail[y-x:y] for y in range(x, len(NFTImageUrlThumbnail)+x,x)]
    if len(NFTDescription) > 64:
        NFTDescription=[NFTDescription[y-x:y] for y in range(x, len(NFTDescription)+x,x)]
    path = homePath + 'keys/' + user + '/' + policy_name + '.txt'
    with open(path, 'r') as text:
        policyID = text.read()
    metadata = {}
    metadata["721"] = {
                    policyID: {
                        policy_name: {
                            "name": "Cardano foundation NFT guide token",
                            "image": "Url THUMBNAIL",
                            "mediaType": "image/png",
                            "description": "This is my first NFT thanks to the Cardano foundation",
                            
                            "files": [{
                                "mediaType": "image/png",
                                "src": "Url NORMAL SIZE",
                                "name": "image name"
                                }],
                            "ID": 1,
                            }
                        },
                    "version": "1.0"
                    }
    
    metadata["721"][policyID][policy_name]["description"] = description
    metadata["721"][policyID][policy_name]["name"] = NFTName
    metadata["721"][policyID][policy_name]["ID"] = NFTID
    metadata["721"][policyID][policy_name]["image"] = NFTImageUrlThumbnail
    metadata["721"][policyID][policy_name]["files"][0]["src"] = NFTImageUrl
    metadata["721"][policyID][policy_name]["files"][0]["name"] = NFTName
    metadata = str(metadata)
    metadata = metadata.replace('\n', '').replace("'", '"')
    path = f'/home/yop/Downloads/cardano/single_nfts/{user}/{NFTName}/metadata.json'
    with open(path, 'w') as text:
        text.write(metadata)


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
            text.write(policy_id)
        path = f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_id.txt'
        with open(path, 'w') as text:
            text.write(policy_id)

    except Exception as e:
        with open('/home/yop/Downloads/cardano/error_log.txt', 'a') as text:
            text.write(f'\n{e}, Error while creating policy id. a_35_create_single_nft.py\n')





























testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet
homePath = '/home/yop/Downloads/cardano-node1.30.0/'


try:
    # Load data
    # username = 'nasartz'
    # policy_name = 'Standard'
    # timelock = 3650 * 24*60*60
    # using_old_policy = False
    
    username = sys.argv[1]  # username
    nft_name = sys.argv[2]  # nft_name
    using_old_policy = sys.argv[3] # Using old policy ID
    policy_name = sys.argv[4]  # policy
    royalty_percentage = sys.argv[5]  # royalty_percentage
    royalty_wallet = sys.argv[6]  # royalty_wallet
    timelock = int(sys.argv[7]) * 60 * 60 * 24  # policy_duration
    description = f"{sys.argv[8]}"  # description
    nft_id = sys.argv[9]  # NFT ID
    price = sys.argv[10]
    buyer_pay_fees = sys.argv[11]
    artist = f'{sys.argv[12]}'
    selling_fees = sys.argv[13]
    beneficiary_address = sys.argv[14]
    with open('/home/yop/Downloads/cardano/error_log2.txt', 'w') as text:
        text.write(f'Data Loaded in a_35_create_single_nft: {username}\n{nft_name}\n{using_old_policy}\n{policy_name}\n{royalty_percentage}\n{royalty_wallet}\n{timelock}\n{description}\n{nft_id}\n{price}\n{buyer_pay_fees}\n{artist}\n{selling_fees}\n{beneficiary_address}\n')
    
    policy_creation_date = 0
    # Check if policy exists
    if exists(homePath + 'keys/' + username + '/' + policy_name + '.script'): 
        with open(homePath + 'keys/' + username + '/' + policy_name + '.script') as text:
            policy_id = json.loads(text.read())
            policy_id = policy_id["scripts"][1]["keyHash"]
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_id.txt', 'w') as text:
            text.write(policy_id)
    elif ((using_old_policy == 'True') or (using_old_policy == True)):
        policy_creation_date = 0
    else:
        create_policy(username, policy_name, timelock)
        policy_creation_date = int(time.time())
    # Make sure folders are been created
    # sys.exit()
    temp_name = nft_name
    temp_name = temp_name.replace(' ', '_')
    create_folders(username, temp_name)

    try:
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
            text.write(price)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/buyer_pay_fees.txt', 'w') as text:
            text.write(buyer_pay_fees)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_percentage.txt', 'w') as text:
            text.write(royalty_percentage)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_wallet.txt', 'w') as text:
            text.write(royalty_wallet)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/description.txt', 'w') as text:
            text.write(description)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/nft_id.txt', 'w') as text:
            text.write(str(nft_id))
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_name.txt', 'w') as text:
            text.write(policy_name)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/artist.txt', 'w') as text:
            artist = artist.replace('_', ' ')
            text.write(artist)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/hashes.txt', 'w') as text:
            text.write('')
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/selling_fees.txt', 'w') as text:
            text.write(selling_fees)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/ADAMagic_fee.txt', 'w') as text:
            text.write(selling_fees)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/flags.txt', 'w') as text:
            text.write('0, 0, 0')
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/beneficiary_address.txt', 'w') as text:
            text.write(beneficiary_address)
        with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/{nft_name}.addr', 'r') as text:
            address = text.read()
        with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.txt', 'r') as text:
            policy_id = text.read()

        print(f'key555word{address},{policy_id},{policy_creation_date}key555word')



    except Exception as e:
        with open('/home/yop/Downloads/cardano/error_log.txt', 'a') as text:
            text.write(f'{e}, Error while creating wallet address. a_35_create_single_nft.py\n')
        print(f'FAILED creating project. Linux system a_35_create_single_nft.py {e}')
        raise

except Exception as e:
    with open('/home/yop/Downloads/cardano/error_log.txt', 'a') as text:
        text.write(f'a_35_create_single_nft Error, {e}\n')
    print(f'FAILED Overall creating project. Linux system a_35_create_single_nft.py | {e}')
    raise
