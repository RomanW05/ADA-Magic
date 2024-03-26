import sys

username = sys.argv[1]
nft_name = sys.argv[2]
address = sys.argv[3]
how_much = sys.argv[4]
policy_name = sys.argv[5]
policy_duration = sys.argv[6]

with open('/home/yop/Downloads/cardano/single_nfts/pending_addresses.txt', 'a') as text:
    text.write(f'{username},{nft_name},{address},{how_much},{policy_name},{policy_duration}|)