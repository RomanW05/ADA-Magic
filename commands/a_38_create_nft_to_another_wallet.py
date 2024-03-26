import os
import sys
from os.path import exists
import json
import subprocess
from orderedCommands import mint_on_another_address_single_nft
from orderedCommands import createNoNameTokens
from orderedCommands import checkForCreatedDeletedNoNameToken
from orderedCommands import metadataCreationWithOutRoyalties
from orderedCommands import metadataCreation
from orderedCommands import check_if_noname_token_is_half_minted
from a_27_upload_im_ipfs import upload_im

testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = testnet
home_path = '/home/yop/Downloads/cardano-node1.30.0/'
username = sys.argv[1]
nft_name = sys.argv[2]
platform_address = sys.argv[3]
platform_fee = sys.argv[4]
money = sys.argv[5]
tx_in = sys.argv[6]
buyer_address = sys.argv[7]

try:
    # Load project
    nft_amount = 1
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{username}.addr', 'r') as text:
        user_address = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/policy_name.txt', 'r') as text:
        policy_name = text.read()
        policy_name = policy_name.replace('\n', '')
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/price.txt', 'r') as text:
        price = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_percentage.txt', 'r') as text:
        royalty_percentage = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/royalty_wallet.txt', 'r') as text:
        royalty_wallet = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/description.txt', 'r') as text:
        description = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/nft_id.txt', 'r') as text:
        nft_id = text.read()
    with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.txt', 'r') as text:
        policy_id = text.read()
    with open(f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/benefit_address.txt', 'r') as text:
        benefit_address = text.read()
        benefit_address = benefit_address.replace('\n', '')


    policy_name = policy_name.replace('\n', '')


    # If the policy is brand new you have to create a new empty token and burn it
    path = f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}LOADED.txt'

    if exists(path):
        print('No name token already exists')
    else:

        # Check if there was a problem during the noname token creating and if it were, delete the token and all good
        flag_to_skip = check_if_noname_token_is_half_minted(policy_id, user_address)
        if flag_to_skip:
            createNoNameTokens(home_path, mainTest, username, user_address, policy_name, 0, -1)
            checkForCreatedDeletedNoNameToken(home_path, mainTest, username, user_address, policy_name, 1)
        else:
            createNoNameTokens(home_path, mainTest, username, user_address, policy_name, 1, 1)
            checkForCreatedDeletedNoNameToken(home_path, mainTest, username, user_address, policy_name, 0)
            createNoNameTokens(home_path, mainTest, username, user_address, policy_name, 0, -1)
            checkForCreatedDeletedNoNameToken(home_path, mainTest, username, user_address, policy_name, 1)

        with open(path, 'w') as text:
            text.write('policy LOADED')
        print('No name token created')

    path = f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{policy_name}.script'
    path = path.replace('\n', '')
    with open(path, 'r') as text:
        policyString = text.read()
        policyJSON = json.loads(policyString)
        timeLock = str(policyJSON["scripts"][0]["slot"])

    # Create metadata
    img_path = f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/{nft_name}.png'
    upload_im(img_path)
    with open(f'{img_path[:-4]}_hash.txt', 'r') as text:
        img_url = text.read()
    with open(f'{img_path[:-4]}_thumbnail_hash.txt', 'r') as text:
        img_thumb_url = text.read()

    if royalty_percentage == '0':
        metadataCreationWithOutRoyalties(home_path, mainTest, username, policy_name, description, nft_name, nft_id, img_url, img_thumb_url)
    else:
        metadataCreation(home_path, mainTest, username, policy_name, description, nft_name, nft_id, img_url, royalty_percentage, royalty_wallet, img_thumb_url)

    path = home_path + 'keys/' + username + '/' + policy_id + nft_name + str(nft_id) + 'metadata.json'
    new_path = f'/home/yop/Downloads/cardano/single_nfts/{username}/{nft_name}/metadata.json'
    os.rename(path, new_path)

    mint_on_another_address_single_nft(home_path, mainTest, username, benefit_address, policy_name, nft_name, nft_amount, nft_id, timeLock, platform_address, platform_fee, buyer_address, '1', money, tx_in)
    print('success')

except Exception as e:
    print(f'a_38 {e} NFT could not be minted')