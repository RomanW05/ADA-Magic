import os
import sys
import subprocess
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

file = sys.argv[1]
command = 'ipfs add ' + file
result = subprocess.check_output(command,shell=True)
result = result.decode('utf-8')
result = result.split(' ')[-2]
print(result)
command = 'ipfs swarm peers'
subprocess.check_output(command,shell=True)