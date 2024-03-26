import time
import requests
import json
from time import strftime, localtime
import subprocess
import os

# Really???
# def encrypt(key, source, encode=True):
#     key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
#     IV = Random.new().read(AES.block_size)  # generate IV
#     encryptor = AES.new(key, AES.MODE_CBC, IV)
#     padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
#     source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
#     data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
#     return base64.b64encode(data).decode("latin-1") if encode else data

# def decrypt(key, source, decode=True):
#     if decode:
#         source = base64.b64decode(source.encode("latin-1"))
#     key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
#     IV = source[:AES.block_size]  # extract the IV from the beginning
#     decryptor = AES.new(key, AES.MODE_CBC, IV)
#     data = decryptor.decrypt(source[AES.block_size:])  # decrypt
#     padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
#     if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
#         raise ValueError("Invalid padding...")
#     return data[:-padding]  # remove the padding

def new_user():
    password = ''
    results = requests.get(f'https://adamagic.io/async_new_users/{password}/get')
    usernames = json.loads(results.text)
    if len(usernames) == 0:
        # print('0 new users found\n')
        return
    seed_key = b''
    print(f'New users to be imported: {len(usernames)}')
    for username in usernames:
        try:
            os.mkdir(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}')
        except Exception as e:
            print(f'Folder could not be created. Error: {e}')
        try:
            # Create seed phrase
            seed = '/home/yop/Downloads/cardano-node1.30.0/cardano-wallet recovery-phrase generate > ' + f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/SeedPhrase.txt'
            subprocess.call(seed, shell=True)
            time.sleep(0.1)

            # Create new wallet
            query = f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/2createNewWallet.py {username}'
            query = subprocess.check_output(query,shell=True)
        
        except Exception as e:
            print(f'{e}')
            continue


        with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/{username}.addr') as text:
            address = text.read()
            address = address.replace('\n', '')
        with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/SeedPhrase.txt') as text:
            seedphrase = text.read()
            seedphrase = seedphrase.replace('\n', '')
        if not os.path.exists(f'/home/yop/Downloads/cardano-node1.30.0/keys/{username}/protocol.json'):
            return


        # seedphrase = seedphrase.encode()
        # encrypted = encrypt(seed_key, seedphrase)


        payload = {'internal_id': usernames[username]['internal_id'], 'address': f'{address}'}
        results = requests.get(f'https://adamagic.io/async_new_users/{password}/update', params=payload)
        # results = requests.get(f'https://adamagic.io/async_new_users/{password}/{status}/{internal_id}/{seedphrase}/{address}')
        print(f'New user found!: {username} with internal_id: {results.text}')

print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
main_start = int(time.time())
while True:
    try:
        new_user()
    except Exception as e:
        print(f'{e}')
    time.sleep(120)
    if int(time.time()) > (main_start + 3600):
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        main_start = int(time.time())
