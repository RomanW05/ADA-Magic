import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
import paramiko
from orderedCommands import send_single_nft
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

collection_name = sys.argv[1]

folders = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/')
for file in folders:
    if os.path.isdir(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/{file}'):
        os.rmdir(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/{file}')
    else:
        os.remove(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/{file}')
os.rmdir(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/')
print('Success')