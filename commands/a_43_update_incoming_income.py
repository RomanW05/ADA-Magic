from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageSequence
from PIL import ImageFilter
from PIL import ImageEnhance
import os
import sys
from werkzeug.utils import secure_filename
import io
import random
import requests
import json
from PIL import Image
from base64 import b16encode
import logging
import time
import random
import a_27_upload_im_ipfs
import numpy as np
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)

username = sys.argv[1]
nft_name = sys.argv[2]
wallet_address = sys.argv[3]
how_much = sys.argv[4]
policy = sys.argv[5]
policy_duration = sys.argv[6]


with open('/home/yop/Downloads/cardano/single_nfts/pending_addresses.txt', 'a') as text:
    text.write(f'{username},{nft_name},{wallet_address},{how_much},{policy},{policy_duration}|')