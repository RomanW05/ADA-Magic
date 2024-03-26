import os
import sys
import json
import subprocess
import time

from orderedCommands import balance

homePath = '/home/yop/Downloads/cardano-node1.30.0/'
testnet = '--testnet-magic 1097911063'
mainnet = '--mainnet'
mainTest = mainnet

address = sys.argv[1]
balanceResult = balance(homePath, mainTest, address)
print(balanceResult)
sys.exit()
