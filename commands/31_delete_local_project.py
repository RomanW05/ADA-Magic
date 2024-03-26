import os
import sys
import json
import subprocess
import time
from os.path import exists
import mysql.connector
import paramiko
from orderedCommands import createWallet
from orderedCommands import loadAddress
from orderedCommands import sendSimpleTransaction
import logging

def delete_project_website(collection_name):
    # First iterate inside all the folders within the collection
    folders = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/')
    for folder in folders:
        if os.path.isdir(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/{folder}'):
            files = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/{folder}')

            # Delete files within one subfolder
            for file in files:
                os.remove(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/{folder}/{file}')
            os.rmdir(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/{folder}')
    files = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/')

    # Delete single files on the main folder project
    for file in files:
        os.remove(f'/home/yop/Downloads/cardano/vending_machine/{collection_name}/{file}')
    os.rmdir('tmp/' + collection_name + '/')