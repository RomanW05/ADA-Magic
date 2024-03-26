import os
import sys
import json
import subprocess
import time
import logging
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

user = sys.argv[1]

try:
    with open(f'/home/yop/Downloads/cardano/vending_machine/{user}/{user}.addr', 'r') as text:
        address = text.read()
    with open(f'/home/yop/Downloads/cardano/vending_machine/{user}/policy_id.txt', 'r') as text:
        policy_id = text.read()

    print(f'key555word{address},{policy_id}key555word')
except Exception as e:
    print(f'FAILED {e}')
    logging.exception('Got exception on main handler')
    raise