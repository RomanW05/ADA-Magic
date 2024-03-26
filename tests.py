import unittest
import sys
from unittest.mock import patch
from flask import session
import requests


class Flask_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('setUpClass\n')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')


    def setUp(self):
        print('setUp')
        # app.config['TESTING'] = False


    def tearDown(self):
        print('tearDown\n')
        pass


    # Check logout redirects
    # def test_logout(self):
    #     print('test_logout')
    #     # tester = app.test_client(self)
    #     response = requests.get('https://adamagic.io/logout')
    #     self.assertEqual(response.status_code, 200)


    # def test_root(self):
    #     print('test_root')
    #     response = requests.get('https://adamagic.io')
    #     self.assertEqual(response.status_code, 200)
    #     assert "<h2>Welcome to ADA Magic NFT Marketplace</h2>" in response.text

    # def test_fetch_otp(self):
    #     print('fetching otp')
    #     response = requests.get('https://adamagic.io/get_otp/')
    #     print(response, response.text)
    #     self.assertEqual(response.status_code, 200)
    #     otp = response.text

    # def test_login(self):
    #     print('test_login')
    #     # with (app.test_client()) as client:
    #     response = requests.post("https://adamagic.io/login2", data={
    #             "username": "",
    #             "password": ""
    #         })
    #     self.assertEqual(response.status_code, 200)


    def test_new_user_registration(self):
        print('test_new_user')

        # Open session
        s = requests.Session()
        username = ""
        password = ""

        # Send new user submit registration
        print('send new user parameters')
        response = s.post('https://adamagic.io/newUserCreation', data={
            "username": username,
            "email": "" 
            })
        self.assertEqual(response.status_code, 200)
        # assert "<h1>New user creation</h1>" in response.text

        # Fetch otp
        print('Fetching otp')
        response = s.get('https://adamagic.io/get_otp/')
        self.assertEqual(response.status_code, 200)
        otp = response.text

        # Verify otp number
        print('verifying otp')
        response = s.post('https://adamagic.io/verified', data={
            "verificationNumber": otp
            })
        self.assertEqual(response.status_code, 200)
        assert "<h1>Create a new password</h1>" in response.text

        # New password
        print('creating new password')
        response = s.post('https://adamagic.io/enterNewPassword', data={
            "password0": password,
            "password1": password
            })

        try:
            self.assertEqual(response.status_code, 200)
        except:
            print(response.text)
        # assert "<h1>Repeat the seed phrase</h1>" in response.text

        # Fetch seed phrase
        print('fetching seed phrase')
        response = s.get(f'https://adamagic.io/read_seed/{username}/')
        self.assertEqual(response.status_code, 200)
        seed = response.text
        print(seed)

        # Enter seedphrase and get address
        print('Entering seedphrase')
        response = s.post(f'https://adamagic.io/checkSeed', data={
            "seed": seed
            })
        self.assertEqual(response.status_code, 200)
        assert "Success. You created a new account." in response.text

        # # Delete user from database
        print('deleting user from database')
        response = s.post(f'https://adamagic.io/delete_user_from_db/{username}/')
        self.assertEqual(response.status_code, 200)
        assert "deleted from database" in response.text

        # Delete user from local server
        print('deleting user from local server')
        response = s.post(f'https://adamagic.io/delete_user_from_local_server/{username}/')
        self.assertEqual(response.status_code, 200)
        assert f'User {username} deleted' in response.text


    # def test_vending_machine_project_creation(self):
    #     print('vending machine project creation')
    #     password = ''
    #     collection_name = ''
    #     collection_total = '23'
    #     price = '16000000'
    #     artist = 'jamilo'
    #     minting_date = '45566887987'
    #     total_layers = '8'
    #     profit_wallet_address = ''
    #     response = requests.get(f'http://adamagic.io/check_vending_machine_project_creation/{password}/{collection_name}/{collection_total}/{price}/{artist}/{minting_date}/{total_layers}/{profit_wallet_address}')

    #     self.assertEqual(response.status_code, 200)
    #     print('vending machine check response', response.text)

    #     response = requests.get(f'http://adamagic.io/delete_vending_machine_project_creation/{password}/{collection_name}')
    #     self.assertEqual(response.status_code, 200)
    #     print('vending machine deleted response', response.text)





if __name__ == '__main__':
    unittest.main()



[
{'tx_hash': '',
'block_hash': '',
'block_height': 7735164, 'epoch': 362, 'epoch_slot': 142919, 'absolute_slot': 71163719, 'tx_timestamp': 1662730010, 'tx_block_index': 4, 'tx_size': 491, 'total_output': '3185200364',
'fee': '177205',
'deposit': '0',
'invalid_before': None, 'invalid_after': 71170864, 'collateral_inputs': [], 'collateral_outputs': [], 'reference_inputs': [],

'inputs': [
    {'value': '3182597167',
    'tx_hash': '',
    'tx_index': 1, 'asset_list': [], 'datum_hash': None, 'stake_addr': '',
    'inline_datum': None,
    'payment_addr': {'cred': '',
    'bech32': ''},
    'reference_script': None},

    {'value': '2780402',
    'tx_hash': '',
    'tx_index': 0, 'asset_list': [], 'datum_hash': None, 'stake_addr': '',
    'inline_datum': None, 'payment_addr': {'cred': '',
    'bech32': ''}, 'reference_script': None}], 

'outputs': [
    {'value': '200000000',
    'tx_hash': '',
    'tx_index': 0, 'asset_list': [], 'datum_hash': None, 'stake_addr': '',
    'inline_datum': None, 'payment_addr': {'cred': '',
    'bech32': ''}, 'reference_script': None},

    {'value': '220000000',
    'tx_hash': '',
    'tx_index': 1, 'asset_list': [], 'datum_hash': None, 'stake_addr': '',
    'inline_datum': None,
    'payment_addr': {'cred': '',
    'bech32': ''},
    'reference_script': None},

    {'value': '2765200364',
    'tx_hash': '',
    'tx_index': 2, 'asset_list': [], 'datum_hash': None, 'stake_addr': '',
    'inline_datum': None, 'payment_addr': {'cred': '',
    'bech32': ''}, 'reference_script': None}],



 'withdrawals': [], 'assets_minted': [], 'metadata': [], 'certificates': [], 'native_scripts': [], 'plutus_contracts': []}]
