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

time_now = int(time.time())
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet
home_path = '/home/yop/Downloads/cardano-node1.30.0/'
username = ''
policy_name = 'Standard'
description = ''
original_nft_name = ''
NFTImageUrl = ''
royalty_percentage = '0'
royalty_wallet = ''
NFTImageUrlThumbnail = ''
artist = ''



# query = f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/a_27_upload_im_ipfs.py /home/yop/Downloads/cardano-node1.30.0/keys/{username}/{original_nft_name}.jpg'
# result = subprocess.check_output(query,shell=True)
# print(f'File uploaded to the ipfs with results: {result}')
metadataCreationWithOutRoyalties(home_path, mainTest, username, policy_name, description, original_nft_name, 1, NFTImageUrl, NFTImageUrlThumbnail, artist)

