import subprocess
import sys
import time
import json


def simple_mint(user, userAddress, txhash, txin, funds, policyID, policyName, NFTName, NFTAmount, NFTMint, metadata_path, invalid_herafter):
    mainTest = '--mainnet'
    fee = 300000
    output = str(int(funds) - fee)
    NFTName = NFTName.replace('_', '')
    #create raw file
    homePath = '/home/yop/Downloads/cardano-node1.30.0/'
    getRawTx = homePath + 'cardano-cli transaction build-raw' + \
    ' --fee ' + str(fee) + \
    ' --tx-in ' + txhash + '#' + txin + \
    ' --tx-out ' + userAddress + '+' +  str(output) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --mint="' + str(NFTMint) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
    ' --metadata-json-file ' + metadata_path + \
    ' --invalid-hereafter ' + str(invalid_herafter) + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
    getRawTx = getRawTx.replace('\n', '')
    # print(getRawTx)
    # sys.exit()
    getRawTx = subprocess.check_output(getRawTx,shell=True)
    time.sleep(0.1)


    # #2.2 Calculate fee
    fee = homePath + 'cardano-cli transaction calculate-min-fee --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 1 ' + mainTest + ' --protocol-params-file ' + homePath + 'keys/' + user + '/protocol.json | cut -d " " -f1'
    fee = subprocess.check_output(fee,shell=True)
    fee = fee.decode('utf-8')
    fee = fee.replace('\n', '')
    output = str(int(funds) - int(fee))

    # #Make raw Transaction with real fee
    getRawTx = homePath + 'cardano-cli transaction build-raw' + \
    ' --fee ' + str(fee) + \
    ' --tx-in ' + txhash + '#' + txin + \
    ' --tx-out ' + userAddress + '+' +  str(output) + '+"' + str(NFTAmount) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --mint="' + str(NFTMint) + ' ' + policyID + '.' + NFTName + '"' + \
    ' --minting-script-file ' + homePath + 'keys/' + user + '/' + policyName + '.script' + \
    ' --metadata-json-file ' + metadata_path + \
    ' --invalid-hereafter ' + str(invalid_herafter) + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.raw'
    getRawTx = getRawTx.replace('\n', '')
    getRawTx = subprocess.check_output(getRawTx,shell=True)
    time.sleep(0.1)


    # #2.3 Sign the Transaction
    signTx = homePath + 'cardano-cli transaction sign' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + user + '.skey' + \
    ' --signing-key-file ' + homePath + 'keys/' + user + '/' + policyName + '.skey ' + \
    mainTest + \
    ' --tx-body-file ' + homePath + 'keys/' + user + '/matx.raw' + \
    ' --out-file ' + homePath + 'keys/' + user + '/matx.signed'
    signTx = subprocess.check_output(signTx,shell=True)

    # #Send the REAL Transaction
    sendRealTx = homePath + 'cardano-cli transaction submit' + \
    ' --tx-file ' + homePath + 'keys/' + user + '/matx.signed ' + mainTest

    sendRealTx = subprocess.check_output(sendRealTx,shell=True)
    print('MINTED')


user = 'JoseCatala'
policyName = 'Standard'
txhash = ''
txin = '0'
funds = '67925869'

NFTName = 'Vampirella_1_d'
NFTAmount = '0'
NFTMint = '-1'


with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{user}/{policyName}.script') as text:
    invalid_herafter = json.loads(text.read())
    invalid_herafter = int(invalid_herafter["scripts"][0]["slot"])
with open(f'/home/yop/Downloads/cardano-node1.30.0/keys/{user}/{user}.addr') as text:
    userAddress = text.read()
query = f'/home/yop/Downloads/cardano-node1.30.0/cardano-cli transaction policyid --script-file /home/yop/Downloads/cardano-node1.30.0/keys/{user}/{policyName}.script'
policyID = subprocess.check_output(query,shell=True)
policyID = policyID.decode('utf-8').replace('\n', '')
metadata_path = f'/home/yop/Downloads/cardano/single_nfts/{user}/{NFTName}/metadata.json'

print(f'''invalid_herafter {invalid_herafter}
userAddress {userAddress}
policyID {policyID}''')



simple_mint(user, userAddress, txhash, txin, funds, policyID, policyName, NFTName, NFTAmount, NFTMint, metadata_path, invalid_herafter)
