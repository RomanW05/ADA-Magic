import requests
import json
import sys
import os
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

'''
This is the following workflow:

-Create a wallet for the project
-Listen to txs
-One or more txs found with cardano-cli
-Mint the NFTs and send them
-Store those tx hashes
-Delete those hashed txs if they arrived
-
'''



price_per_nft = 8300000

# New income tx found after cardano-cli query website wallet!
tx_hash = ""

# Search website wallet for that tx
with open('C:/Users/yop/Desktop/proyects/marketplace/history.json', 'r') as text:
	json_data = text.read()
	json_data = json.loads(json_data)
# result = requests.get('https://explorer-api.testnet.dandelion.link/api/addresses/summary/addr_test1qppsljw6p08t7nxmhfc3u5exrq8x80mf9znzzzcgd3kmvveqt6xjsuz4kndsrtpw2wscjpafe453297l38pqercjpv6q7ay77q')
# json_data = json.loads(result.text)


def fetch_blockchain_data(wallet_address):
	result = requests.get('https://explorer-api.testnet.dandelion.link/api/addresses/summary/' + wallet_address)
	json_data = json.loads(result.text)

	return json_data


def fetch_ada_sent_from_wallet(json_data, tx_hash):
	for tx_number, history in enumerate(json_data["Right"]["caTxList"]):
		if json_data["Right"]["caTxList"][tx_number]["ctbId"] == fetch_tx:
			
			# Sender wallet
			sender_address = json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][0]["ctaAddress"]

			# Amount received
			received_ada = int(json_data["Right"]["caTxList"][tx_number]["ctbOutputs"][1]["ctaAmount"]["getCoin"])
			
			return sender_address, received_ada


def cases(price_per_nft, project_name, json_data, mint_limit, tx_hash):
	'''
	CASES:
	X1. Not enough money to send back < 1000000 + fee
	X2. Not enough money for one nft
	3. More than one NFT, rounded amount
	4. Exceeded minting limit
	5. More than one NFT, not rounded amount
	X6. No more NFTs to mint
	7. Tx did not go through
	'''


	# Retreive wallet sender and ADAs sent
	sender_address, received_ada = fetch_ada_sent_from_wallet(json_data, tx_hash)

	# Info about the willingness of the buyer:
	willing_to_mint = received_ada // price_per_nft  # Modulus
	money_reminder = received_ada - (willing_to_mint * price_per_nft)

	# How many NFTs are left?
	nfts_left = 0
	with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/nfts_left.txt', 'r') as text:
		nfts_left = int(text.read())


	# Case 6:
	if nfts_left == 0:
		return

	# Case 1
	# Sender looses the money because is stupid. Say that on disclaimer website
	if received_ada < int(1300000):
		return


	# Case 2
	# Send the money back minus the fees of tx
	if ((willing_to_mint == 0) and (received_ada > int(1300000))):
		os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/18send_ada_penalzed.py {project_name} {received_ada} {sender_address}')


	# Case3
	if money_reminder == 0:
		os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/19mint_multiple_nfts.py {project_name} {received_ada} {sender_address} {willing_to_mint}')
		





# Make request to website just once
json_data = fetch_blockchain_data(wallet_address)

# Start the main
main(price_per_nft, project_name, json_data, tx_hash)











willing_to_mint = received_ada // price_per_nft  # Modulus


if willing_to_mint == 0:
	query = 'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/18send_ada_penalzed.py admin received_ada sender_address'
	return

send_back_leftover = received_ada - (price_per_nft * int(willing_to_mint))  # int() always rounds down
print(f'willing_to_mint {willing_to_mint}')
print(f'Mint the NFT to {sender_address}')
print(f'Send send_back_leftover {send_back_leftover}')




