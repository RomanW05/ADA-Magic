import os
import subprocess
import time
def protocol(path_protocol):
    mainTest = '--mainnet'
    exportParams = f'/home/yop/Downloads/cardano/cardano-node-1.33.0-linux/cardano-cli query protocol-parameters {mainTest} --out-file {path_protocol}'
    subprocess.call(exportParams,shell=True)
    time.sleep(0.1)


def mk_protocol(path):
    usernames = os.listdir(path)
    for username in usernames:
        path_user = f'{path}{username}/'
        if os.path.isdir(path_user):
            path_protocol = f'{path_user}protocol.json'
            if os.path.exists(path_protocol):
                continue
            else:
                protocol(path_protocol)


path1 = '/home/yop/Downloads/cardano-node1.30.0/keys/'
path2 = '/home/yop/Downloads/cardano/single_nfts/'

mk_protocol(path1)
mk_protocol(path2)