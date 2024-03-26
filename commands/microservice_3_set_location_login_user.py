import requests
import time
from time import strftime, localtime


main_start = int(time.time())
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
while True:
    password = ''
    results = requests.get(f'https://adamagic.io/stablish_location/{password}')
    if results.text != '':
        print(results.text)

    if int(time.time()) > (main_start + 3600):
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        main_start = int(time.time())

    time.sleep(300)
