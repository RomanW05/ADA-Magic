import requests
import json
import io
from PIL import Image
import sys
import time
import logging
import time
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)


def upload_ipfs(url, project_id, project_secret, img_path):
    files = encode_img(img_path)
    results = requests.post(url, auth=(project_id, project_secret), files=files)

    return results


def get_img_url(results):
    # Clean results and extract the full img url and its hash
    p = results.json()
    img_hash = p['Hash']

    return img_hash


def encode_img(img_path):
    # Encode needed to upload a file to infura, return a dict
    img = Image.open(img_path)
    buf = io.BytesIO()
    img.save(buf, format='webp')
    byte_im = buf.getvalue()
    files = {'files': byte_im}

    return files


def pin(img_hash, project_id, project_secret):
    # Endpoint to pin a hash without files
    url = "https://ipfs.infura.io:5001/api/v0/pin/add"
    params = (('arg',img_hash),)
    results = requests.post(url, params=params, auth=(project_id, project_secret))

    return results


def main(img_path):
    # Upload image to server
    project_id = ""
    project_secret = ""
    url = 'https://ipfs.infura.io:5001/api/v0/add'
    results = upload_ipfs(url, project_id, project_secret, img_path)
    img_hash = get_img_url(results)

    # Pin image in ipfs
    results = pin(img_hash, project_id, project_secret)
    print(f' IPFS results: {results.text}')

    # Make sure it is all good and use the img url in the metadata
    if str(results) == '<Response [200]>':
        print(f'{img_path}')
        with open(f'{img_path[:-4]}_hash.txt', 'w') as text:
            text.write(f'{img_hash}')


def upload_im(img_path):
    img_thumb_path = f'{img_path[:-4]}_thumbnail.png'
    main(img_path)
    main(img_thumb_path)

upload_im(sys.argv[1])
