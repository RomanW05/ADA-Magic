import os
import sys
from os.path import exists
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

homePath = '/home/yop/Downloads/cardano-node1.30.0/'
user = sys.argv[1]

with open(homePath + 'keys/' + user + '/' + user + 'SeedPhrase.txt', 'r') as text:
	seed = text.read()
print(f'keyword555{seed}keyword555')
sys.exit()
