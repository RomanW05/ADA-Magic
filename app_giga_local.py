from ast import expr_context
from distutils.command.clean import clean
from unicodedata import category
import flask
from flask import *
from flask import Flask, request, send_from_directory, session
from flask_session import Session
import json
import hashlib
from werkzeug.utils import secure_filename
from werkzeug.exceptions import InternalServerError
import os
import sys
from PIL import Image
import shutil
import io
import time
import mysql.connector
import random
from flask_mail import *
import bcrypt
from os.path import exists
from PIL import Image

from time import strftime,localtime
import datetime
import qrcode
from contextlib import closing
import base64
from logging import FileHandler,WARNING

import sys
import traceback
from flask import jsonify
import string

import geocoder
from geopy.geocoders import Nominatim

import filetype
import re

import random 
from flask_seasurf import SeaSurf

from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}


#App start
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_mapping(config)
cache = Cache(app)
csrf = SeaSurf(app)
csrf.init_app(app)
if f':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
    file_handler = FileHandler("C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\my_error.log")
    app.config["IMAGES"] = 'C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\'
    app.config['UPLOAD_FOLDER'] = 'C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\'
else:
    file_handler = FileHandler('/home//ada_magic/error_handler.txt')
    app.config["IMAGES"] = '/static/images'
    app.config["UPLOAD_FOLDER"] = '/tmp'
file_handler.setLevel(WARNING)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True,
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = 'Lax'
# app.config["PERMANENT_SESSION_LIFETIME"]=36000
app.config['PROPAGATE_EXCEPTIONS'] = True


#for the email
app.config["MAIL_SERVER"]=''  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = ''
app.config['MAIL_PASSWORD'] = ''  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True 
mail = Mail(app)
app.jinja_env.autoescape = True

if f':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
    Session(app)
    app.config['SECRET_KEY'] = 'key'
else:
    #key for safety during the session. It changes with every new login
    key = ''
    for x in range(10):
        keyInsert = random.randint(1, 1000000)
        insertInto = random.randint(0, len(key))
        key = key[:insertInto] + str(keyInsert) + key[insertInto:]
    encoded = key.encode()
    result = hashlib.sha256(encoded)
    key = result.hexdigest()
    app.secret_key = key

    # csrf = CSRFProtect()
    # csrf.init_app(app)
    Session(app)
    app.config['SECRET_KEY'] = key


@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["HTTP-HEADER"] = "VALUE"
    return response


# @app.after_request
# def add_security_headers(response):
#     response.headers['Content-Security-Policy']='default-src \'self\''
#     return response




# Error handling
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('/gigatheme/404.html')


@app.errorhandler(Exception)          
def basic_error(e):
    date_local  = strftime("%H:%M | %A,%d,%b,%Y", localtime())

    save_log_error(f'{date_local} {e}', 'errorhandler\n')
    # except Exception as e:
    # save_log_error(f'{date_local} {e}', 'errorhandler exception trigered\n')
    return render_template('/gigatheme/404.html', error=f'It is not you, it is us. We are working under the hood to bring you the best service. We will be back as soon as possible')












'''
███╗░░░███╗███████╗████████╗██╗░░██╗░█████╗░██████╗░░██████╗
████╗░████║██╔════╝╚══██╔══╝██║░░██║██╔══██╗██╔══██╗██╔════╝
██╔████╔██║█████╗░░░░░██║░░░███████║██║░░██║██║░░██║╚█████╗░
██║╚██╔╝██║██╔══╝░░░░░██║░░░██╔══██║██║░░██║██║░░██║░╚═══██╗
██║░╚═╝░██║███████╗░░░██║░░░██║░░██║╚█████╔╝██████╔╝██████╔╝
╚═╝░░░░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═════╝░╚═════╝░
'''

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




def db_params(database):
    if f':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
        db_conn_info = {
        "user": "1234",
        "password": "1234",
        "host": "localhost",
        "database": f"{database}"
        }
    else:

        db_conn_info = {
        "user": "",
        "password": "",
        "host": "",
        "database": f"{database}"
        }

    return db_conn_info


def downsize_image(img_path, img_type):
    try:
        # Cou create a thumbnail image to reduce costs since it is going to be the cover of the 5mb file
        im = Image.open(img_path)
        width, height = im.size  # resize to 300*300

        if img_type == 'thumbnail':
            if width > height:
                ratio = ((300.0 * 100.0) / width) / 100.0
            else:
                ratio = ((300.0 * 100.0) / height) / 100.0
            x = int(width * ratio)
            y = int(height * ratio)
            im = im.resize((x,y),Image.ANTIALIAS)
            im.save(f'{img_path[:-4]}_thumbnail.png', optimize=True, quality=70)
        if img_type == 'main':
            if width > height:
                ratio = ((600.0 * 100.0) / width) / 100.0
            else:
                ratio = ((600.0 * 100.0) / height) / 100.0
            x = int(width * ratio)
            y = int(height * ratio)
            im = im.resize((x,y),Image.ANTIALIAS)
            im.save(f'{img_path}', optimize=True, quality=100)

    except Exception as e:
        save_log_error(f'{e}', f'could not downsize image, {img_type}')


# def downsize_image_mint(img_path):
#     og_size = os.path.getsize(img_path)
    
#     try:
#         im = Image.open(img_path)
#     except Exception as e:
#         save_log_error(f'{e}', f'def downsize_image_mint Could not open the image in path: {img_path}')
#         return

#     # get the ratio betwee the target and the actual size of the image
#     # if the ratio is > 1 means the image is already bigger than the target, pass
#     # save the image under 1 or 5 mb
#     def ratios(name, path, target, og_size):
#         image_path = f'{path[:-4]}_{name}{path[-4:]}'
#         ratio = target / og_size
#         if ratio > 1.0:
#             shutil.copyfile(path, image_path)
#             return
#         else:
#             im = Image.open(path)
#             im.save(f'{image_path}', optimize=True, quality=int(ratio*100))

#     ratios('thumbnail', img_path, 500000, og_size)
#     ratios('main', img_path, 2500000, og_size)


def resize_blob(img_path):
    # get the ratio betwee the target and the actual size of the image
    # if the ratio is > 1 means the image is already bigger than the target, pass
    # save the image under 1 or 5 mb

    # image_path = f'{img_path[:-4]}_main{img_path[-4:]}'
    image_path = f'{img_path[:-4]}_main{img_path[-4:]}'
    im = Image.open(img_path)
    im.thumbnail([600, 600])
    im.save(f'{image_path}', 'webp', quality=95, subsampling=0, optimize=True)


def create_image_thumbnail(old_path, new_path):
    # get the ratio betwee the target and the actual size of the image
    # if the ratio is > 1 means the image is already bigger than the target, pass
    # save the image under 1 or 5 mb
    # image_path = f'{img_path[:-4]}_thumbnail{img_path[-4:]}'
    # print(f'Save at:{image_path}, Take pic from:{img_path}')
    im = Image.open(old_path)
    im.thumbnail([265, 265])
    im.save(f'{new_path}', 'webp', quality=95, subsampling=0, optimize=True)


def create_image_devices(image_path, internal_id):
    
    if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
        path = f'C:/Users//Desktop/proyects/ada_magic/website/single_nfts/{internal_id}/'
    else:
        path = f"/home//ada_magic/single_nfts/{internal_id}/"
    
    desktop = f'{path}thumbnail.png'
    mobile_thumb = f'{path}mobile_thumbnail.png'
    mobile_main = f'{path}mobile.png'
    try:
        # print(f'opening:{image_path}')
        # Thumbnail desktop view
        im = Image.open(image_path)
        # print('opened')
        im.thumbnail([265, 265])
        # print(f'resizing, saving in desktop: {desktop}')
        im.save(f'{desktop}', 'webp', quality=95, subsampling=0, optimize=True)
        # print(f'saved: {desktop}')
    except Exception as e:
        print(f'{e}')

    # Thumbnail mobile view
    im = Image.open(image_path)
    im.thumbnail([220, 220])
    im.save(f'{mobile_thumb}', 'webp', quality=95, subsampling=0, optimize=True)

    # Show nft mobile view
    im = Image.open(image_path)
    im.thumbnail([400, 400])
    im.save(f'{mobile_main}', 'webp', quality=95, subsampling=0, optimize=True)


# depricated
def store_project(collection_name, artist, collection_total, price, description, website, minting_date, total_layers, profit_wallet_address, username, royalties_wallet, royalties_perc, alternatives):
    with open('/home//ada_magic/vending_machine_projects_to_be_uploaded_to_server.txt', 'a') as text:
        text.write(f'\n{collection_name}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/artist.txt", 'w') as text:
        text.write(f'{artist}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/collection_total.txt", 'w') as text:
        text.write(f'{collection_total}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/price.txt", 'w') as text:
        text.write(f'{price}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/description.txt", 'w') as text:
        text.write(f'{description}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/website.txt", 'w') as text:
        text.write(f'{website}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/minting_date.txt", 'w') as text:
        text.write(f'{minting_date}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/total_layers.txt", 'w') as text:
        text.write(f'{total_layers}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/username.txt", 'w') as text:
        text.write(f'{username}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/profit_wallet_address.txt", 'w') as text:
        text.write(f'{profit_wallet_address}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/royalties_wallet.txt", 'w') as text:
        text.write(f'{royalties_wallet}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/royalties_perc.txt", 'w') as text:
        text.write(f'{royalties_perc}')
    with open(f"/home//ada_magic/vending_machine/{username}/{collection_name}/alternatives.txt", 'w') as text:
        text.write(f'{alternatives}')


# depricated
def store_single_nft(username, nft_name, description, using_old_policy, policy, royalty_percentage, royalty_wallet, policy_duration, NFTID, price, buyer_pay_fees, artist, selling_fees, how_much, beneficiary_address):
    # selling_fees = int(selling_fees) * 1000000
    price = int(price) * 1000000
    how_much = int(how_much) * 1000000
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/nft_name.txt', 'w') as text:
        text.write(nft_name)
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/description.txt', 'w') as text:
        text.write(description)
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/using_old_policy.txt', 'w') as text:
        text.write(using_old_policy)
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/policy.txt', 'w') as text:
        text.write(policy)
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/royalty_percentage.txt', 'w') as text:
        text.write(f'{royalty_percentage}')
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/royalty_wallet.txt', 'w') as text:
        text.write(royalty_wallet)
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/policy_duration.txt', 'w') as text:
        text.write(f'{policy_duration}')
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/datetime.txt', 'w') as text:
        text.write(f'{time.time()}')
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/NFTID.txt', 'w') as text:
        text.write(f'{NFTID}')
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/price.txt', 'w') as text:
        text.write(f'{int(price)}')
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/buyer_pay_fees.txt', 'w') as text:
        text.write(f'{buyer_pay_fees}')
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/artist.txt', 'w') as text:
        text.write(f'{artist}')
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/selling_fees.txt', 'w') as text:
        text.write(f'{selling_fees}')
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/how_much.txt', 'w') as text:
        text.write(f'{how_much}')
    with open(f'/home//ada_magic/single_nfts/{username}/{nft_name}/beneficiary_address.txt', 'w') as text:
        text.write(f'{beneficiary_address}')


# depricated


# depricated


def save_log_error(error, message):
    # exc_type, exc_obj, tb = sys.exc_info()
    # f = tb.tb_frame
    # lineno = tb.tb_lineno
    # filename = f.f_code.co_filename
    # linecache.checkcache(filename)
    # line = linecache.getline(filename, lineno, f.f_globals)
    # error_data = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    error_data = traceback.format_exc()
    if f':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
        with open("C:/Users//Desktop/proyects/ada_magic/website/my_error.log", 'a') as text:
            to_write = f'{datetime.datetime.utcnow()} | {error} | {message} | {error_data}\n'
            text.write(to_write)
    else:
        with open('/home//ada_magic/my_error.log', 'a') as text:
            to_write = f'Time: {datetime.datetime.utcnow()}\nTicket: {error}\nDefinition where happened: {message}\nError message: {error_data}\n\n'
            text.write(to_write)


# depricated


# depricated


def qr_code(address, username, nft_name, type_flag, internal_id):
    try:
        try:
            path = "/home//ada_magic/static/image/ADAMagic_logo.png"
            logo = Image.open(path)
        except Exception as e:
            save_log_error(f'', f'{path}, is not usable')

        basewidth = 100
        # adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        QRcode.add_data(address)
        QRimg = QRcode.make_image(
            back_color='white', fill_color='black').convert('RGB')

        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)
         
        # save the QR code generated
        if type_flag == 'generative':
            path = f"/home//ada_magic/vending_machine/{username}/{nft_name}/qr_code.png"
            QRimg.save(path)
            with open(path, "rb") as img_file:
                img2 = base64.b64encode(img_file.read()).decode('utf-8')
        if type_flag == 'single':
            try:
                os.mkdir(f"/home//ada_magic/single_nfts/{internal_id}")
            except:
                pass
            try:
                path = f"/home//ada_magic/single_nfts/{internal_id}/qr_code.png"
                QRimg.save(path)
            except Exception as e:
                save_log_error('Error saving qr_code', f'{e}')
            # with open(path, "rb") as img_file:
            #     img2 = base64.b64encode(img_file.read()).decode('utf-8')

    except Exception as e:
        save_log_error(f'{e}', 'qr_code')



def display_market_data(data):
    total_volume = 0 # Total volume to be sold:
    total_sales = 0 # Total sold 
    for x, elem in enumerate(data):
        try:
            if int(elem[17]) == 1:
                total_sales =+ int(elem[10])
        except Exception as e:
            pass
        try:
            if int(elem[17]) != 1:
                total_volume_in_sale += int(elem[10])
                total_volume_sold += int(elem[10])
        except Exception as e:
            pass


def top_artist(artist_list):
    # username, price
    artists = {}
    for elem in artist_list:
        try:
            artists[elem[0]]["price"] += int(elem[1])
        except:
            artists[elem[0]] = {"price": int(elem[1]), "username": elem[0]}

    top_sellers = []
    for elem in artists.items():
        top_sellers.append([elem[1]["username"], elem[1]["price"]])

    for row in top_sellers:
        top_sellers.sort(key = lambda row: row[1])
    top_sellers.reverse()
    top_sellers = top_sellers[:8]

    return top_sellers



    # artists = {}
    # for elem in artist_list:
    #     try:
    #         artists[elem[0]]["price"] += int(elem[1])
    #     except:
    #         artists[elem[0]] = {"price": int(elem[1]), "username": elem[0]}

    # new_list = list(artists.items())
    # top_sellers = new_list[-8:]
    # db_conn_info = db_params('_NFT')
    # top_sellers_json = {}
    # top_sellers_array = []
    # with closing(mysql.connector.connect(**db_conn_info)) as conn:
    #     cursor = conn.cursor()
    #     for x, artist in enumerate(top_sellers):
    #         temp = {}
    #         cursor.execute('''SELECT picture, alias FROM user_profile WHERE username = %s''', (artist[1]["username"],))
    #         results = cursor.fetchone()
    #         temp = {"price": artist[1]["price"], "profile_image": results[0], "username": artist[1]["username"], "artist": results[1]}
    #         top_sellers_json[x] = temp
    #         top_sellers_array.append([artist[1]["price"], results[0], artist[1]["username"], results[1]])

    # # Sort from lowest to highest
    # for row in top_sellers_array:
    #     top_sellers_array.sort(key = lambda row: row[0])
    # # Reverse list
    # top_sellers_array.reverse()

    return top_sellers_json, top_sellers_array


def load_projects_to_display_db():
    try:
        latest_json = {}
        single_nfts_json = {}
        vending_machine_json = {}
        issold = {}
        remembered_hearts = {}

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM single_nfts WHERE deleted = "" ORDER BY internal_id DESC''')
            latest = cursor.fetchall()
            info = cursor.fetchall()
            latest = latest[:8]

            cursor.execute('''SELECT internal_id, nft_name, nft_image, price, policy_id, artist, issold, username, deposit_wallet, hearts FROM single_nfts WHERE featured = "1"''')
            single_nfts = cursor.fetchall()
            conn.commit()
            cursor.execute('''SELECT internal_id, name, thumbnail, price, policy_id, number_of_mints, minted_so_far, artist, username, wallet_address, hearts FROM vending_machine_projects WHERE featured = "1"''')
            vending_machine = cursor.fetchall()
            cursor.execute('''SELECT username, price FROM single_nfts WHERE issold = "1"''')
            issold = cursor.fetchall()
            conn.commit()

            if session.get('username'):
                remembered_hearts = []
                cursor.execute('''SELECT nft_liked FROM user_likes_nft WHERE username = %s''', (session['username'],))
                results = cursor.fetchall()
                conn.commit()
                for x in results:
                    remembered_hearts.append(x[0])

    except Exception as e:
        save_log_error(f'{e}', 'could not load db')
        latest = {}
        single_nfts = {}
        vending_machine = {}
        top_sellers = {}
        issold = {}
        remembered_hearts = {}

        return latest, single_nfts, vending_machine, issold, remembered_hearts

    return latest, single_nfts, vending_machine, issold, remembered_hearts


def load_all_single_nfts():
    try:
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM single_nfts WHERE deleted = ""''')
            single_nfts = cursor.fetchall()
        return single_nfts

    except:
        return ''


def load_all_single_nfts_search(items_per_page, current_page, query, category, ordered_by):
    # how info is going to be presented
    # if ((order != 'DESC') or order!= 'ASC'):
    #     order = 'DESC'


    # True = DESC
    # False = ASC

    # cases:
    if ordered_by == 'Newest':
        ordered_by = 'internal_id'
        order = 'DESC'
    elif ordered_by == 'Oldest':
        ordered_by = 'internal_id'
        order = 'ASC'
    elif ordered_by == 'Cheapest':
        ordered_by = 'price'
        order = 'ASC'
    elif ordered_by == 'Most expensive':
        ordered_by = 'price'
        order = 'DESC'
    else:
        ordered_by = 'internal_id'
        order = 'DESC'
    


    remembered_hearts = []

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        flag = False

        if ((query == '') and (category == '')):
            cursor.execute(f"SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts, verified_status FROM single_nfts WHERE deleted = '' ORDER BY {ordered_by} {order}")
            results1 = cursor.fetchall()
            flag = True
        
        elif ((query == '') and (category != '')):
            cursor.execute("SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts, verified_status FROM single_nfts WHERE category = %s AND deleted = '' ORDER BY %s %s", (category, ordered_by, order))
            results1 = cursor.fetchall()
            flag = True
        
        if flag == True:
            if order == 'DESC':
                order = True
            else:
                order = False
            if ordered_by == 'internal_id':
                lamda_x = 0
            else:
                lamda_x = 2

            new_list = sorted(results1, key=lambda x: int(x[lamda_x]), reverse=order)

            total_pages = int(len(new_list) / items_per_page)
            start = current_page * items_per_page
            finish = current_page * items_per_page + items_per_page
            new_list = new_list[start:finish]

            single_nfts = search_results_single_nft_json_search(new_list)

            return single_nfts, remembered_hearts, total_pages


        if category!= '':
            cursor.execute(f"SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts FROM single_nfts WHERE description LIKE '{query}%' AND ('category' = '{category}' AND deleted = '') ORDER BY {ordered_by} {order}")
        else:
            cursor.execute(f"SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts FROM single_nfts WHERE description LIKE '{query}%' AND (deleted = '') ORDER BY {ordered_by} {order}")
        results1 = cursor.fetchall()

        if category!= '':
            cursor.execute(f"SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts FROM single_nfts WHERE nft_name LIKE '{query}%' AND ('category' = '{category}' AND deleted = '') ORDER BY {ordered_by} {order}")
        else:
            cursor.execute(f"SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts FROM single_nfts WHERE nft_name LIKE '{query}%' AND (deleted = '') ORDER BY {ordered_by} {order}")
        results2 = cursor.fetchall()

        if category!= '':
            cursor.execute(f"SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts FROM single_nfts WHERE artist LIKE '{query}%' AND ('category' = '{category}' AND deleted = '') ORDER BY {ordered_by} {order}")    
        else:
            cursor.execute(f"SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts FROM single_nfts WHERE artist LIKE '{query}%' AND (deleted = '') ORDER BY {ordered_by} {order}")
        results3 = cursor.fetchall()

        hashtags = query.split(' ')
        results4 = []
        if len(query) == 1:
            pass
        else:
            for hashtag in hashtags:
                if category!= '':
                    cursor.execute(f"SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts FROM single_nfts WHERE hashtags LIKE '{hashtag}%' AND ('category' = '{category}') ORDER BY {ordered_by} {order}")    
                else:
                    cursor.execute(f"SELECT internal_id, nft_name, price, artist, issold, username, deposit_wallet, hearts FROM single_nfts WHERE hashtags LIKE '{hashtag}%' ORDER BY {ordered_by} {order}")
                temp = cursor.fetchall()
                if len(temp) < 5:  # probably empty
                    continue
                else:
                    results4.append(temp)

        if session.get('username'):
            cursor.execute('''SELECT nft_liked FROM user_likes_nft WHERE username = %s''', (session['username'],))
            results = cursor.fetchall()
            conn.commit()
            for x in results:
                remembered_hearts.append(x[0])
        
        # Store search for later analysis
        cursor.execute('''INSERT INTO searches (query, category, ordered_by, asc_desc, ip, time_now) VALUES (%s,%s,%s,%s,%s,%s)''', (query[:124], category, ordered_by, order, f'{request.remote_addr}', f'{datetime.datetime.utcnow()}'))
        conn.commit()
    
    internal_ids = []
    new_list = []
    def unique_ids(results, new_list, internal_ids):
        for elem in results:
            if elem[0] not in internal_ids:
                internal_ids.append(elem[0])
                new_list.append(elem)

    unique_ids(results1, new_list, internal_ids)
    unique_ids(results2, new_list, internal_ids)
    unique_ids(results3, new_list, internal_ids)
    unique_ids(results4, new_list, internal_ids)
    
    if order == 'DESC':
        order = True
    else:
        order = False
    if ordered_by == 'internal_id':
        lamda_x = 0
    else:
        lamda_x = 2

    new_list = sorted(new_list, key=lambda x: int(x[lamda_x]), reverse=order)

    total_pages = int(len(new_list) / items_per_page)
    start = current_page * items_per_page
    finish = current_page * items_per_page + items_per_page
    new_list = new_list[start:finish]

    single_nfts = search_results_single_nft_json_search(new_list)

    return single_nfts, remembered_hearts, total_pages







def load_all_single_nfts_explore(items_per_page, current_page):
    try:
        single_nfts_json = {}
        vending_machine_json = {}
        remembered_hearts = []

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT internal_id, username, nft_name, artist, internal_id, price, qr_code, hearts, deposit_wallet, issold, verified_status FROM single_nfts WHERE deleted = "" ORDER BY internal_id DESC''')
            results_single_nfts = cursor.fetchall()
            # conn.commit()
            # cursor.execute('''SELECT internal_id, name, thumbnail, price, policy_id, number_of_mints, minted_so_far, artist, username, wallet_address, hearts FROM vending_machine_projects WHERE featured = "1"''')
            # vending_machine = cursor.fetchall()


            if session.get('username'):
                remembered_hearts = []
                cursor.execute('''SELECT nft_liked FROM user_likes_nft WHERE username = %s''', (session['username'],))
                remembered_hearts = cursor.fetchall()


        
        total_pages = int(len(results_single_nfts) / items_per_page)
        start = current_page * items_per_page
        finish = current_page * items_per_page + items_per_page
        results_single_nfts1 = results_single_nfts[start:finish]
        # for elem in vending_machine:
        #     if elem[7] not in artists:
        #         artists.append(elem[7])
        # save_log_error('delete', f'{results_single_nfts}')

    except Exception as e:
        save_log_error(f'{e}', 'def load_all_single_nfts_explore()')
        single_nfts = {}
        remembered_hearts = {}

        return single_nfts, remembered_hearts, total_pages

    elements = ["internal_id", "username","nft_name","artist","image","price","qr_code","hearts","address", "issold", "verified"]
    single_nfts = {}
    for x, elem in enumerate(results_single_nfts1):
        single_nfts[x] = dict(zip(elements, elem))
    

    return single_nfts, remembered_hearts, total_pages



def load_all_single_nfts_index():
    collections = ''
    try:
        remembered_hearts = {}

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT internal_id, nft_name, internal_id, price, policy_id, artist, issold, username, deposit_wallet, hearts, qr_code, description, verified_status FROM single_nfts WHERE deleted = "" ORDER BY internal_id DESC LIMIT 8''')
            results1 = cursor.fetchall()

            cursor.execute('''SELECT internal_id, nft_name, internal_id, price, policy_id, artist, issold, username, deposit_wallet, hearts, qr_code, description, verified_status FROM single_nfts WHERE featured = "1"''')
            results2 = cursor.fetchall()
            conn.commit()
            cursor.execute('''SELECT internal_id, name, thumbnail, price, policy_id, number_of_mints, minted_so_far, artist, username, wallet_address, hearts, qr_code, description FROM vending_machine_projects WHERE featured = "1"''')
            results3 = cursor.fetchall()

            cursor.execute('''SELECT total_volume FROM total_volume WHERE internal_id = "1"''')
            total_volume = cursor.fetchone()
            total_volume = total_volume[0]

            cursor.execute('''SELECT username, ROUND(SUM(price), 0) FROM single_nfts WHERE issold = '1' GROUP BY username HAVING ROUND(SUM(price)) ORDER BY ROUND(SUM(price)) DESC LIMIT 8''')
            top_sellers_array = cursor.fetchall()

            cursor.execute(f"SELECT username, collection_name, MIN(price), COUNT(collection_name), COUNT(issold), verified_status FROM single_nfts WHERE deleted = '' AND collection_name != '' GROUP BY collection_name ORDER BY creation_time LIMIT 8")
            collections = cursor.fetchall()

            cursor.execute("SELECT COUNT(internal_id) FROM single_nfts WHERE deleted='' AND issold=''")
            total_artwork = cursor.fetchone()
            total_artwork = total_artwork[0]

            collection_list = ['username', 'collection_name', 'floor', 'collection_total', 'collection_sold', 'verified_status']
            collections_nft = {}
            for x, elem in enumerate(collections):
                collections_nft[x] = dict(zip(collection_list, elem))

            if session.get('username'):
                remembered_hearts = []
                cursor.execute('''SELECT nft_liked FROM user_likes_nft WHERE username = %s''', (session['username'],))
                results = cursor.fetchall()
                conn.commit()
                for x in results:
                    remembered_hearts.append(str(x[0]))

    except Exception as e:
        save_log_error(f'{e}', 'could not load db')
        latest = {}
        single_nfts = {}
        vending_machine = {}
        remembered_hearts = {}
        top_sellers_array = []
        total_artwork = 0
        collections_nft = {}

        return latest, single_nfts, vending_machine, remembered_hearts, total_volume, top_sellers_array, collections_nft, total_artwork

    latest = {}
    single_nfts = {}
    vending_machine = {}


    for elem in results3:
        temp = {
            "internal_id": str(elem[0]),
            "nft_name": elem[1],
            "image": f'/single_nfts/{elem[0]}/single_nft.png',
            "price": elem[3],
            "policy_id": elem[4],
            "number_of_mints": elem[5],
            "minted_so_far": elem[6],
            "artist": elem[7],
            "username": elem[8],
            "address": elem[9],
            "hearts": elem[10],
            "qr_code": elem[11],
            "description": elem[12]
            }
        vending_machine[elem[0]] = temp

    latest = search_results_single_nft_json(results1)
    single_nfts = search_results_single_nft_json(results2)

 
    # artists = []
    # for elem in latest:
    #     if latest[elem]["username"] not in artists: 
    #         artists.append(latest[elem]["username"])
    # for elem in single_nfts:
    #     if single_nfts[elem]["username"] not in artists:
    #         artists.append(single_nfts[elem]["username"])
    # for elem in vending_machine:
    #     if vending_machine[elem]["username"] not in artists:
    #         artists.append(vending_machine[elem]["username"])

    # profile_pictures = get_profile_pictures(artists)

    return latest, single_nfts, vending_machine, remembered_hearts, total_volume, top_sellers_array, collections_nft, total_artwork




def update_profile_img_db(file_type, img):
    if file_type == 'file':
        try:
            if f':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
                path200 = f"C:/Users//Desktop/proyects/ada_magic/website/users/{session['username']}/profile_picture.png"
                path50 = f"C:/Users//Desktop/proyects/ada_magic/website/users/{session['username']}/profile_picture_thumb.png"
            else:
                path200 = f"/home//ada_magic/users/{session['username']}/profile_picture.png"
                path50 = f"/home//ada_magic/users/{session['username']}/profile_picture_thumb.png"
            img.save(path200)
            im = Image.open(path200)
            img1 = im.resize((200,200))
            img1.save(path200, 'webp')
            img2 = im.resize((50, 50))
            img2.save(path50, 'webp')
        except Exception as e:
            save_log_error('error storing profile picture at def update_profile_img_db', f'{e}')
    if file_type == 'file_banner':

        if f':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
            path = f"C:/Users//Desktop/proyects/ada_magic/website/users/{session['username']}/banner.png"
        else:
            path = f"/home//ada_magic/users/{session['username']}/banner.png"

        try:
            img.save(path)
        except Exception as e:
            save_log_error('error saving banner image at def update_profile_img_db', f'{e}')
        try:
            im = Image.open(path)
        except Exception as e:
            save_log_error('error opening banner image at def update_profile_img_db', f'{e}')

        try:
            im.save(path, 'webp')
        except Exception as e:
            save_log_error('error storing webp banner at def update_profile_img_db', f'{e}')



def base64_single_nft(path):

    with open(path, "rb") as img_file:
        img = base64.b64encode(img_file.read()).decode('utf-8')
    os.remove(path)

    return img


def store_single_nft_project(
                    username, nft_name, description, policy_name, using_old_policy,
                    royalty_percentage, royalty_wallet, policy_duration, NFTID, price,
                    artist, selling_fees, beneficiary_wallet, nft_image, nft_image_thumbnail, full_size_image
                    ):
    if policy_name == '':
        policy_name = 'Standard'
    db_conn_info = db_params('_NFT')
    try:
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO single_nfts (username, nft_name, artist, beneficiary_wallet, nft_image, nft_image_thumbnail, description, price, royalty_percentage, royalty_wallet, policy_id, policy_name, using_old_policy, policy_duration, NFTID, full_size_image, selling_fees, original_nft_name, views) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (username, nft_name, artist, beneficiary_wallet, nft_image, nft_image_thumbnail, description, f'{int(int(price)/1000000)}', royalty_percentage, royalty_wallet, 'synchronizing', policy_name, using_old_policy, policy_duration, NFTID, full_size_image, selling_fees, nft_name, '0'))
            conn.commit()
            cursor.execute('''SELECT internal_id FROM single_nfts WHERE username = %s AND nft_name = %s''', (username, nft_name))
            internal_id = cursor.fetchone()
            internal_id = internal_id[0]
    except Exception as e:
        save_log_error(f'{e}', 'async problem')
        internal_id = -1
    return f'https://adamagic.io/show_single_nft/{internal_id}'


def get_profile_pictures(artists):
    artists_pfp = {}
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        for x, artist in enumerate(artists):
            cursor = conn.cursor()
            cursor.execute('''SELECT picture FROM user_profile WHERE username = %s''', (artist,))
            pfp = cursor.fetchone()
            artists_pfp[artist] = pfp

    return artists_pfp


def mint_check():
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT address, external_wallet, inform_user FROM users WHERE username = %s''',(session['username'],))
        results = cursor.fetchone()
    if results[2] == '1':
        return False
    if results[0] == 'Placeholder':  # New wallet or external wallet needed
        if ((results[1] == '') or (results[1] == None)):
            return True
        else:
            return False
    return False


def email_checks(email):
    if (('@' not in email) or ('.' not in email) or ("'" in email) or ('"' in email) or ('(' in email) or
        ('(' in email) or (',' in email) or ('=' in email) or ('+' in email) or (':' in email) or (';' in email) or
        ('/' in email) or ('*' in email) or (' from ' in email) or (' FROM ' in email)):
        return True
    else:
        return False


def sanity_check_login(query):
    if (("'" in query) or ('"' in query) or ('(' in query) or
        ('(' in query) or (',' in query) or ('=' in query) or ('+' in query) or (':' in query) or (';' in query) or
        ('/' in query) or ('*' in query) or (' from ' in query) or (' FROM ' in query)):
        return True
    else:
        return False

def sanity_check(query):
    if (('@' in query) or ('.' in query) or ("'" in query) or ('"' in query) or ('(' in query) or
        ('(' in query) or (',' in query) or ('=' in query) or ('+' in query) or (':' in query) or (';' in query) or
        ('/' in query) or ('*' in query) or (' from ' in query) or (' FROM ' in query)):
        return True
    else:
        return False


def description_check(query):
    #/@#;*=+"()
    if (('@' in query) or ('#' in query) or ('(' in query) or (')' in query) or 
        ('/' in query) or (' FROM ' in query) or ('*' in query)):
        return True
    else:
        return False

def website_check(query):
    if (('@' in query) or ("'" in query) or ('"' in query) or ('(' in query) or
        ('(' in query) or (',' in query) or ('=' in query) or ('+' in query) or (';' in query) or
        ('*' in query) or (' from ' in query) or (' FROM ' in query)):
        return True
    else:
        return False


def sanity_check_minting_date(query):
    if (('@' in query) or ('.' in query) or ("'" in query) or ('"' in query) or ('(' in query) or
        ('(' in query) or (',' in query) or ('=' in query) or ('+' in query) or (';' in query) or
        ('/' in query) or ('*' in query) or (' from ' in query) or (' FROM ' in query)):
        return True
    else:
        return False


def search_results_single_nft_json(results):
    
    final = {}
    element = ['internal_id', 'nft_name', 'internal_id', 'price', 'policy_id', 'artist', 'issold', 'username', 'address', 'hearts', 'qr_code', 'description', 'verified']
    for x, elem in enumerate(results):
        final[x] = dict(zip(element, elem))
        # temp = {
        #     "internal_id": str(elem[0]),
        #     "username": elem[7],
        #     "nft_name": elem[1],
        #     "artist": elem[5],
        #     "image": f'/single_nfts/{elem[0]}/single_nft.png',
        #     "price": elem[3],
        #     "hearts": elem[9],
        #     "address": elem[8],
        #     "issold": elem[6],
        #     "description": elem[11]
        # }
        # final[elem[0]] = temp
    return final


def search_results_single_nft_json_search(results):
    try:
        final = {}
        collection_list = ['internal_id', 'nft_name', 'price', 'artist', 'issold', 'username', 'address', 'hearts', 'verified_status']
        for elem in results:
            for x, elem in enumerate(results):
                final[x] = dict(zip(collection_list, elem))
    except Exception as e:
        save_log_error('search_results_single_nft_json_search', f'{e}')
        return {}
    return final


def check_ownership_vm(internal_id):
    # Check the ownership of the project
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM vending_machine_projects WHERE internal_id = %s", (internal_id,))
        owenership = cursor.fetchone()
        save_log_error('check owenership', f'owenership: {owenership[0]}, username: {session["username"]}')
    if owenership[0] == session['username']:
        return True
    else:
        return False
















'''
███╗░░██╗███████╗░██╗░░░░░░░██╗             ██╗░░░██╗░██████╗███████╗██████╗░
████╗░██║██╔════╝░██║░░██╗░░██║             ██║░░░██║██╔════╝██╔════╝██╔══██╗
██╔██╗██║█████╗░░░╚██╗████╗██╔╝             ██║░░░██║╚█████╗░█████╗░░██████╔╝
██║╚████║██╔══╝░░░░████╔═████║░             ██║░░░██║░╚═══██╗██╔══╝░░██╔══██╗
██║░╚███║███████╗░░╚██╔╝░╚██╔╝░             ╚██████╔╝██████╔╝███████╗██║░░██║
╚═╝░░╚══╝╚══════╝░░░╚═╝░░░╚═╝░░             ░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝

░█████╗░██████╗░███████╗░█████╗░████████╗██╗░█████╗░███╗░░██╗
██╔══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║
██║░░╚═╝██████╔╝█████╗░░███████║░░░██║░░░██║██║░░██║██╔██╗██║
██║░░██╗██╔══██╗██╔══╝░░██╔══██║░░░██║░░░██║██║░░██║██║╚████║
╚█████╔╝██║░░██║███████╗██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║
░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝
'''

# @app.route('/newUserForm', methods=['GET', 'POST'])
# def newUserForm():
#     return render_template('/NFT/createNewUser.html')

# @app.route('/newUserCreation', methods=['GET', 'POST'])
# def newUserCreation():
#     if request.method == "POST":
#         username = request.form['username']
#         email = request.form['email']
#         checked = request.form['check']

#         db_conn_info = db_params('_NFT')
#         with closing(mysql.connector.connect(**db_conn_info)) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''SELECT * FROM users WHERE username = %s''', (username,))
#             username_result = cursor.fetchone()
#             try:
#                 cursor.fetchall()
#             except:
#                 pass
#             cursor.execute('''SELECT * FROM users WHERE email = %s''', (email,))
#             email_result = cursor.fetchone()
#             try:
#                 cursor.fetchall()
#             except:
#                 pass

#             if username_result != None:
#                 return render_template('/NFT/createNewUser.html', username='Username already exists')
#             if email_result != None:
#                 return render_template('NFT/createNewUser.html', email='Email already exists')

#             date_local  = strftime("%H:%M | %A, %d %b %Y", localtime())

#             if 'on' in checked:
#                 cursor.execute('''INSERT INTO users (username, email, emailVerification, verified, creationDate) VALUES (%s,%s,%s,%s,%s)''', (username, email, 0, 1, date_local))
#                 conn.commit()
#             else:
#                 cursor.execute('''INSERT INTO users (username, email, emailVerification, verified, creationDate) VALUES (%s,%s,%s,%s,%s)''', (username, email, 0, 0, date_local))
#                 conn.commit()

#         session['username'] = username
#         session['email']    = email

#         return redirect("verifyEmailAddress")

#     return render_template('/NFT/createNewUser.html')

#Validation number
# otp = random.randint(000000,999999)
# @app.route('/verifyEmailAddress', methods=['GET', 'POST'])
# def verifyEmailAddress():
#     try:
#         email = session['email']

#         response = requests.get("https://isitarealemail.com/api/email/validate",
#          params = {'email': email})
#         status = response.json()['status']
#         if status == "invalid":
#             return render_template('/NFT/createNewUser.html', email='Please enter a valid email')

#         msg = Message('ADA Magic Marketplace. Verification code', sender='', recipients=[email])
#         msg.body = f'Welcome to ADA Magic Marketplace.\n\n Your verification code is: {str(otp)}\n\n It is great to see you here, in case you do need something let us know via email () or Twitter @ada_magic_io\n Happy minting'
#         mail.send(msg)
        
#         return render_template('/NFT/verification.html')

#     except:
#         return render_template('/NFT/login.html', error='Something went wrong. Please, login with your username and a random password in order to verify your account')

# @app.route('/verified', methods=['GET', 'POST'])
# def verified():
#     session['verification'] = False
#     if request.method == "POST":
#         try:
#             userOPT = request.form['verificationNumber']
#             if int(otp) == int(userOPT):
#                 session['verification'] = True

#                 #email is verified, add to database and wait for new password
#                 return render_template('/NFT/newPassword.html')
#         except:
#             return render_template('/NFT/success.html', email='UNSUCCESSFUL')
#     else:
#         return render_template('/NFT/success.html', email='UNSUCCESSFUL')


# @app.route('/enterNewPassword', methods=['GET', 'POST'])
# def enterNewPassword():
#     if session['verification'] == False:
#         return redirect('verifyEmailAddress')
#     if request.method == "POST":

#         #Get password, hash it and store it in the database
#         password0 = request.form['password0']
#         password1 = request.form['password1']
#         if password0 != password1:
#             return render_template('NFT/newPassword.html', result='Passwords did not match, please try again')
#         password0 = password0.encode()
#         hashed = bcrypt.hashpw(password0, bcrypt.gensalt(rounds=16))
#         hashed = hashed.decode('utf-8')

#         db_conn_info = db_params('_NFT')
#         with closing(mysql.connector.connect(**db_conn_info)) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''UPDATE users set password = %s, emailVerification = %s, address = "Placeholder", need_new_wallet = "1", inform_user = "0" WHERE username = %s''', (hashed, 1, session['username']))
#             conn.commit()
#             cursor.execute('''INSERT INTO password_recovery (email, is_valid, email_opt, time_now) VALUES (%s,%s,%s,%s)''', (session['email'], "False", "0", "0"))
#             conn.commit()

#         session['wallet_address'] = 'Placeholder'
#         latest, single_nfts, vending_machine, issold, remembered_hearts = load_projects_to_display_db()
#         return render_template('/NFT/login.html', username=session['username'], address=session['wallet_address'],
#             latest=latest, single_nfts=single_nfts, vending_machine=vending_machine)

#     return render_template('NFT/newPassword.html', result='No password entered, please try again')










# Check seed (depricated)
# @app.route('/checkSeed', methods=['GET', 'POST'])
# def checkSeed():
#     if not session.get('username'): return redirect('login')
#     if request.method == "POST":
#         userSeedInput   = request.form['seed']

#         # There is an error and a space at the end of the seedphrase is been sent. Correct that
#         if userSeedInput[-1:] == ' ':
#             userSeedInput = userSeedInput[:-1]
#         userSeedInput = userSeedInput.replace('\n', '')
#         userSeedInput = userSeedInput.split(' ')
#         user = session['username']
#         home_path = '/home//Downloads/cardano-node1.30.0/'
#         commands = [
#                     f'python3 /home//Downloads/cardano-node1.30.0/commands/spltCommands/readSeed.py {user}'
#                     ]
#         try:
#             outdata, errdata = connect_paramiko(commands)
#         except:
#             return render_template('/NFT/verification.html', error='We are experiencing delays from the server. Please, try again later')

#         try:
#             seed = outdata.split('keyword555')
#             seed = seed[1]
#             seed = seed.replace('keyword555', '')
#             seed = seed.replace('\n', '')
#             if seed[-1:] == ' ':
#                 seed = seed[:-1]
#             if seed[-1:] == '\n':
#                 seed = seed[:-1]
#             seed = seed.split(' ')

#         except:
#             save_log_error('Error parsing seed to check with users input', [session['username'], outdata, ['user input:', userSeedInput], 'seed', seed])
#             seed = 'Seed will be sent by email'

#         flag = True
#         try:
#             for x, word in enumerate(seed):
#                 if seed[x] != userSeedInput[x]:
#                     flag = False
#         except:
#             flag = False
            
#         if flag:
#             address = ''
#             try:
#                 #The user has the seed phrase, create wallet and delete the seed
#                 commands = [
#                         f'python3 /home//Downloads/cardano-node1.30.0/commands/spltCommands/2createNewWallet.py {user}',
#                         f'python3 /home//Downloads/cardano-node1.30.0/commands/spltCommands/3deleteSeed.py {user}',
#                         f'python3 /home//Downloads/cardano-node1.30.0/commands/spltCommands/4readAddress.py {user}'
#                         ]

#                 try:
#                     outdata, errdata = connect_paramiko(commands)
#                 except:
#                     return render_template('/NFT/seedPhrase.html', address='See address once logged in', username=session['username'])

#                 address = outdata.split('keyword555')
#                 address = address[1]

#             except Exception as e:
#                 save_log_error(f'{e}', f'error creating address{outdata}, {address}')
#                 date_local  = strftime("%M, %H, %A, %d %b %Y", localtime())
#                 conn        = mysql.connector.connect(host='localhost', 
#                             user='', 
#                             password='BvhR8i1redKd', 
#                             database='_NFT')
#                 cursor      = conn.cursor()
#                 cursor.execute("UPDATE users set creationDate = %s WHERE username = %s", (date_local, session['username']))
#                 conn.commit()
#                 conn.close()
#                 return render_template('/NFT/seedPhrase.html', address='See address once logged in', username=session['username'])


#             date_local  = strftime("%M, %H, %A, %d %b %Y", localtime())
#             conn        = mysql.connector.connect(host='localhost', 
#                         user='', 
#                         password='BvhR8i1redKd', 
#                         database='_NFT')
#             cursor      = conn.cursor()

#             cursor.execute("UPDATE users set address = %s, creationDate = %s WHERE username = %s", (address, date_local, session['username']))
#             conn.commit()
#             cursor.execute('''INSERT INTO user_profile (picture, description, title, alias, username) VALUES (%s,%s,%s,%s,%s)''', ('', 'No description', 'No title', session['username'], session['username']))
#             conn.commit()
#             conn.close()

#             try:
#                 # Create folders
#                 os.mkdir(f"/home//ada_magic/vending_machine/{session['username']}")
#                 os.mkdir(f"/home//ada_magic/single_nfts/{session['username']}")
#                 os.mkdir(f"/home//ada_magic/users/{session['username']}")
#             except Exception as e:
#                 save_log_error(f'{e}', 'could not create user folders at user creation')

#             username = session['username']
#             session['username'] = None
#             return render_template('/NFT/seedPhrase.html', address=address, user=username)
#         else:
#             return render_template('/NFT/repeatSeed.html', seed=seed, error=f'{userSeedInput}')
#     return render_template('/NFT/login.html')

'''
CACHE
'''

@csrf.include
@app.route('/withdraw_balance/<action>', methods=['GET', 'POST'])
def withdraw_balance(action):

    if sanity_check(action):
        return ''

    if action == 'withdraw':
        if not session.get('username'): return redirect('/login')

        address = request.form['address']
        if sanity_check(address):
            return redirect('/login')

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT can_request FROM users WHERE username = %s ", (session['username'],))
            can_request = cursor.fetchone()
            if can_request[0] != '1':
                return redirect(f'/profile/{session["username"]}')
            if address == 'Cancel':
                cursor.execute("UPDATE users set wants_money = '0' WHERE username = %s", (session['username'],))
            else:
                cursor.execute("UPDATE users set wants_money = '1', withdraw_to = %s WHERE username = %s", (address, session['username']))
            conn.commit()
        
        return redirect(f'/profile/{session["username"]}')

    elif action == 'update':
        password = request.args.get('password')
        username = request.args.get('username')

        if password != '':
            return ''
        
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users set wants_money = '0', can_request = '0' WHERE username = %s", (username,))
            conn.commit()
        
        return 'updated'

    elif action == 'check':
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, withdraw_to FROM users WHERE wants_money = '1' AND can_request = '1'")
            results = cursor.fetchall()
            conn.commit()

        users_dic = {}
        if results == []:
            return {}

        for elem in results:
            users_dic[elem[0]] = elem[1]

        return jsonify(users_dic)

    elif action == 'inform':
        password = request.args.get('password')
        username = request.args.get('username')

        if sanity_check(username):
            return ''

        if password != '':
            return ''
        
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users set wants_money = '2' WHERE username = %s", (username,))
            conn.commit()
        
        return 'notified'

    elif action == 'update_wallet':
        if not session.get('username'): return redirect('/login')
        try:

            beneficiary_address = request.form['beneficiary_address']
            if sanity_check(beneficiary_address):
                return redirect('/profile/session["username"]')
            if 'addr' not in beneficiary_address:
                return redirect('/profile/session["username"]')
            if beneficiary_address.isalnum() and len(beneficiary_address) > 64:
                db_conn_info = db_params('_NFT')
                with closing(mysql.connector.connect(**db_conn_info)) as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_profile set beneficiary_address = %s WHERE username = %s", (beneficiary_address, session['username']))
                    conn.commit()
        except Exception as e:
            save_log_error('Error updating user wants money withdraw wallet addr', f'{e}')

        return redirect(f'profile/{session["username"]}')

    else:
        return 'nothing'


def modify_total_sold_volume(issold):
    total_volume = 0
    for elem in issold:
        try:
            total_volume += int(elem[1])
        except:
            continue
    
    return total_volume


def modify_top_sellers():
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username, price FROM single_nfts WHERE issold = "1"''')
        issold = cursor.fetchall()
        # conn.commit()

        # artists = {}
        # for elem in issold:
        #     try:
        #         price = int(elem[1])
        #     except:
        #         continue
        #     try:
        #         artists[elem[0]]["price"] += price
        #     except:
        #         artists[elem[0]] = {"price": price, "username": elem[0]}

        # top_sellers = []
        # for elem in artists.items():
        #     top_sellers.append([elem[1]["username"], elem[1]["price"]])

        # for row in top_sellers:
        #     top_sellers.sort(key = lambda row: row[1])
        # top_sellers.reverse()
        # top_sellers = top_sellers[:8]

        # for internal_id, seller in enumerate(top_sellers):
        #     cursor.execute('''UPDATE top_sellers set username=%s, price=%s WHERE internal_id=%s''', (seller[0], int(seller[1]), internal_id+1))
        #     conn.commit()
        total_volume = modify_total_sold_volume(issold)
        # cursor.execute('''UPDATE top_sellers set username=%s, price=%s WHERE internal_id=%s''', (seller[0], int(seller[1]), internal_id+1))
        # conn.commit()
        cursor.execute('''UPDATE total_volume set total_volume=%s WHERE internal_id=1''', (total_volume,))
        conn.commit()

    return 'done'

def load_top_sellers():
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username, price FROM top_sellers ORDER BY price DESC LIMIT 8''')
        top_sellers = cursor.fetchall()

    return top_sellers




def load_index_current_state():
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT nft_internal_id, username, artist, hearts, nft_name, issold, price, address FROM cache_index_featured''')
        featured1 = cursor.fetchall()
        conn.commit()
        cursor.execute('''SELECT nft_internal_id, username, artist, hearts, nft_name, issold, price, address FROM cache_index_latest''')
        latest1 = cursor.fetchall()
        conn.commit()
        cursor.execute('''SELECT username, amount_sold FROM cache_index_top_sellers''')
        top_sellers = cursor.fetchall()
        conn.commit()

    featured = {}
    for elem in featured1:
        if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
            image = f"C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\users\\{elem[1]}\\profile_picture.png"
        else:
            image = f'/users/{elem[1]}/profile_picture.png'

        temp = {
            "nft_internal_id": elem[0],
            "username": elem[1],
            "nft_name": elem[4],
            "artist": elem[2],
            "image": image,
            "price": elem[6],
            "hearts": elem[3],
            "address": elem[7],
            "issold": elem[5]
        }
        featured[elem[0]] = temp

    latest = {}
    for elem in latest1:
        if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
            image = f"C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\users\\{elem[1]}\\profile_picture.png"
        else:
            image = f'/users/{elem[1]}/profile_picture.png'

        temp = {
            "nft_internal_id": elem[0],
            "username": elem[1],
            "nft_name": elem[4],
            "artist": elem[2],
            "image": image,
            "price": elem[6],
            "hearts": elem[3],
            "address": elem[7],
            "issold": elem[5]
        }
        latest[elem[0]] = temp

    # featured =      [internal_id, username, artist, hearts, nft_name, issold, price, address]
    # latest =        [internal_id, username, artist, hearts, nft_name, issold, price, address]
    # top_sellers =   [username, amount_sold]

    return featured, latest, top_sellers












'''
██████╗░░█████╗░░██████╗░██████╗░██╗░░░░░░░██╗░█████╗░██████╗░██████╗░
██╔══██╗██╔══██╗██╔════╝██╔════╝░██║░░██╗░░██║██╔══██╗██╔══██╗██╔══██╗
██████╔╝███████║╚█████╗░╚█████╗░░╚██╗████╗██╔╝██║░░██║██████╔╝██║░░██║
██╔═══╝░██╔══██║░╚═══██╗░╚═══██╗░░████╔═████║░██║░░██║██╔══██╗██║░░██║
██║░░░░░██║░░██║██████╔╝██████╔╝░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██████╔╝
╚═╝░░░░░╚═╝░░╚═╝╚═════╝░╚═════╝░░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═════╝░

██████╗░███████╗░█████╗░░█████╗░██╗░░░██╗███████╗██████╗░██╗░░░██╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██║░░░██║██╔════╝██╔══██╗╚██╗░██╔╝
██████╔╝█████╗░░██║░░╚═╝██║░░██║╚██╗░██╔╝█████╗░░██████╔╝░╚████╔╝░
██╔══██╗██╔══╝░░██║░░██╗██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗░░╚██╔╝░░
██║░░██║███████╗╚█████╔╝╚█████╔╝░░╚██╔╝░░███████╗██║░░██║░░░██║░░░
╚═╝░░╚═╝╚══════╝░╚════╝░░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░
'''

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template("/gigatheme/1_password_recovery_email.html")


@app.route('/forgot_recovery', methods=['GET', 'POST'])
def forgot_recovery():

    if request.method == "POST":
        # Generate random key to secure the link to be sent to the user as an email
        email_opt = random.randint(000000, 999999)
        key = ''
        for number in range(100):
            key += random.choice(string.ascii_letters)

        email_opt = str(email_opt) + key
        email = request.form['email']
        
        if email_checks(email):
            
            return render_template('/gigatheme/1_password_recovery_email.html', msg='Wrong email. Please, enter the email you used to create your account')

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT username FROM users WHERE email = %s''', (email,))
            results = cursor.fetchone()
            try:
                username = results[0]
            except:
                return render_template('/gigatheme/1_password_recovery_email.html', msg='Wrong email. Please, enter the email you used to create your account')
            # Flush buffer
            try:
                cursor.fetchall()
            except:
                pass

            if results == None:  # The email is not in the database
                return render_template('/gigatheme/1_password_recovery_email.html', msg='Wrong email. Please, enter the email you used to create your account')
            cursor.execute('''UPDATE password_recovery set is_valid = %s, email_opt = %s, time_now = %s WHERE email = %s''', ("True", email_opt, str(int(time.time())), email))
            conn.commit()
            composed = email + email_opt
            composed = bytes(composed, 'utf-8')
            sha_obj = hashlib.sha256()
            sha_obj.update(composed)
            hexadecimal = sha_obj.hexdigest()
            link = f'http://adamagic.io/new_password_recover/{username}/{hexadecimal}'

            server=''
            from_email=''
            password = ''
            body = f"""
                This email is sent to you because you requested a password recovery. If is wasn't you, please ignore this email.\n\n
                Click on this link to create a new password.\n
                Please, verify that the link redirects to the original website: https://adamagic.io\n
                {link}
                """
            subject = f"ADA Magic account recovery"

            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = email

            s = smtplib.SMTP_SSL(server)
            s.login(from_email, password)
            s.sendmail(from_email, [email], msg.as_string())
            s.quit()





            # msg = Message('ADA Magic Marketplace. Password recovery', sender='', recipients=[email])
            # msg.body = 
            # mail.send(msg)

            return render_template("/gigatheme/1_password_recovery_email_followup.html", email=email)

    return render_template("/gigatheme/1_password_recovery_email.html", msg='No email was sent. Please, enter an email')


@app.route('/new_password_recover/<username>/<composed>', methods=['GET', 'POST'])
def new_password_recover(username, composed):

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''SELECT email FROM users WHERE username = %s''', (username,))
            results0 = cursor.fetchone()
            email = results0[0]
            # Flush buffer
            try:
                cursor.fetchall()
            except:
                pass
        except:
            return render_template('/gigatheme/1_password_recovery_email.html', msg='Wrong email. Please, enter the email you used to create your account')
        cursor.execute('''SELECT email, email_opt, is_valid, time_now FROM password_recovery WHERE email = %s''', (email,))
        results1 = cursor.fetchone()
    try:
        email = results1[0]
        email_opt = results1[1]
        is_valid = results1[2]
        old_time = int(results1[3])
    except:
        return render_template("/gigatheme/1_password_recovery_email.html", msg='Email not found')

    if is_valid == "False":
        cursor.execute('''UPDATE password_recovery set is_valid = %s, email_opt = %s, time_now = %s WHERE email = %s''', ("False", "0", "0", email))
        conn.commit()
        conn.close()
        return render_template("/gigatheme/1_password_recovery_email.html", msg='Time expired. Please, try again')

    time_now = int(time.time())
    if time_now - old_time > 900:
        cursor.execute('''UPDATE password_recovery set is_valid = %s, email_opt = %s, time_now = %s WHERE email = %s''', ("False", "0", "0", email))
        conn.commit()
        conn.close()
        return render_template("/gigatheme/1_password_recovery_email.html", message='Time expired. Please, try again')


    composed_check = email + str(email_opt)
    composed_check = bytes(composed_check, 'utf-8')
    sha_obj = hashlib.sha256()
    sha_obj.update(composed_check)
    hexadecimal = sha_obj.hexdigest()

    if hexadecimal == composed:
        session['username'] = username
        conn.close()
        return render_template("/gigatheme/1_password_recovery_password.html", hexadecimal=hexadecimal)
    conn.close()
    return render_template("/gigatheme/password_recovery.html")


@app.route('/new_password_recover_continue/', methods=['GET', 'POST'])
def new_password_recover_continue():
    if not session.get('username'):
        return render_template('/gigatheme/1_login.html')
    try:
        if request.method == "POST":
            password0 = request.form['password0']
            password1 = request.form['password1']
            hexadecimal = request.form['hexadecimal']
            if password0 != password1:
                return render_template("/gigatheme/1_type_new_password.html", hexadecimal=hexadecimal, message='Passwords are not the same')
            username = session['username']

            db_conn_info = db_params('_NFT')
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''SELECT email FROM users WHERE username = %s''', (username,))
                    results = cursor.fetchone()
                    email = results[0]
                    
                    # Flush buffer
                    try:
                        cursor.fetchall()
                    except:
                        pass
                except:
                    return render_template("/gigatheme/1_type_new_password.html", msg='The email does not correspond to any of our users')

                cursor.execute('''SELECT email_opt FROM password_recovery WHERE email = %s''', (email,))
                results = cursor.fetchone()
                email_opt = results[0]
                composed_check = email + str(email_opt)
                composed_check = bytes(composed_check, 'utf-8')
                sha_obj = hashlib.sha256()
                sha_obj.update(composed_check)
                hexadecimal_to_check = sha_obj.hexdigest()
                if hexadecimal == hexadecimal_to_check:
                    password0 = password0.encode()
                    hashed = bcrypt.hashpw(password0, bcrypt.gensalt(rounds=16))
                    hashed = hashed.decode('utf-8')
                    cursor.execute('''UPDATE users set password = %s WHERE username = %s''', (hashed, session['username']))
                    conn.commit()
                    session.clear()
                    return render_template("/gigatheme/1_success.html", msg='You have successfully changed your password. You can now login using your new password')
                return render_template('/gigatheme/1_login.html')
    except Exception as e:
        save_log_error('Error while recovering password at def new_password_recover_continue', f'{e}')
        return render_template("/gigatheme/1_password_recovery.html")






'''
██╗░░░██╗███████╗██████╗░██╗███████╗██╗░░░██╗               ░██████╗███████╗███████╗██████╗░
██║░░░██║██╔════╝██╔══██╗██║██╔════╝╚██╗░██╔╝               ██╔════╝██╔════╝██╔════╝██╔══██╗
╚██╗░██╔╝█████╗░░██████╔╝██║█████╗░░░╚████╔╝░               ╚█████╗░█████╗░░█████╗░░██║░░██║
░╚████╔╝░██╔══╝░░██╔══██╗██║██╔══╝░░░░╚██╔╝░░               ░╚═══██╗██╔══╝░░██╔══╝░░██║░░██║
░░╚██╔╝░░███████╗██║░░██║██║██║░░░░░░░░██║░░░               ██████╔╝███████╗███████╗██████╔╝
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝╚═╝░░░░░░░░╚═╝░░░               ╚═════╝░╚══════╝╚══════╝╚═════╝░
'''

@app.route('/wallets/<option>', methods=['GET', 'POST'])
def wallets(option):
    if option == 'create_new':
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE users set inform_user = "1" WHERE username = %s''', (session['username'],))
            conn.commit()
        return render_template('/NFT/success.html', success=' Your wallet address is being created. You will receive a message with your wallet address and your seedphrase. While the message is being displayed, copy the 25 ramdonly generated words (seedphrase) in order on a sheet of paper. Your seedphrase is the key to your wallet and access your funds, we do not hold your seedphrase so make sure you do write them down in a secure place.')
    
    elif option == 'use_existing':
        return render_template('/NFT/use_external_wallet.html')

    elif option == 'update_external':
        if request.method == "POST":
            external_wallet = request.form['external_wallet']
            # Check wallet address is not harmfull
            if (("'" in external_wallet) or ('\\' in external_wallet) or (' ' in external_wallet)):
                return redirect('mint')

            db_conn_info = db_params('_NFT')
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE users set external_wallet = %s WHERE username = %s''', (external_wallet, session['username']))
                conn.commit()
                


    else:
        return redirect('mint')






























'''
░█████╗░░██████╗██╗░░░██╗███╗░░██╗░█████╗░              ░██╗░░░░░░░██╗██╗████████╗██╗░░██╗
██╔══██╗██╔════╝╚██╗░██╔╝████╗░██║██╔══██╗              ░██║░░██╗░░██║██║╚══██╔══╝██║░░██║
███████║╚█████╗░░╚████╔╝░██╔██╗██║██║░░╚═╝              ░╚██╗████╗██╔╝██║░░░██║░░░███████║
██╔══██║░╚═══██╗░░╚██╔╝░░██║╚████║██║░░██╗              ░░████╔═████║░██║░░░██║░░░██╔══██║
██║░░██║██████╔╝░░░██║░░░██║░╚███║╚█████╔╝              ░░╚██╔╝░╚██╔╝░██║░░░██║░░░██║░░██║
╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝░╚════╝░              ░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝

██╗░░░░░░█████╗░░█████╗░░█████╗░██╗░░░░░                ░██████╗███████╗██████╗░██╗░░░██╗███████╗██████╗░
██║░░░░░██╔══██╗██╔══██╗██╔══██╗██║░░░░░                ██╔════╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗
██║░░░░░██║░░██║██║░░╚═╝███████║██║░░░░░                ╚█████╗░█████╗░░██████╔╝╚██╗░██╔╝█████╗░░██████╔╝
██║░░░░░██║░░██║██║░░██╗██╔══██║██║░░░░░                ░╚═══██╗██╔══╝░░██╔══██╗░╚████╔╝░██╔══╝░░██╔══██╗
███████╗╚█████╔╝╚█████╔╝██║░░██║███████╗                ██████╔╝███████╗██║░░██║░░╚██╔╝░░███████╗██║░░██║
╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝                ╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
'''

@app.route('/fetch_for_metadata_single_nft/<password>/<username>/<original_nft_name>')
def fetch_for_metadata_single_nft(password, username, original_nft_name):
    if password != '':
        return 'OK'

    original_nft_name = original_nft_name.replace('_', ' ')
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM single_nfts WHERE original_nft_name = %s AND deleted = %s ''',(original_nft_name, ''))
        results = cursor.fetchone()
    data = {}
    data["artist"] = results[3]
    data["original_nft_name"] = results[21]
    data["price"] = results[10]
    data["description"] = results[8]
    data["nft_name"] = results[2]
    data["royalty_percentage"] = results[13]
    data["royalty_wallet"] = results[14]

    return jsonify(data)


@app.route('/fetch_nft_data/<password>/<internal_id>')
def fetch_nft_data(password, internal_id):
    if password != '':
        return ''

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT artist, description, policy_id, price, royalty_percentage, royalty_wallet, policy_name, selling_fees, nft_name, username FROM single_nfts WHERE internal_id = %s''', (internal_id,))
        nft = cursor.fetchone()
        cursor.execute('''SELECT email FROM users WHERE username = %s''', (nft[9],))
        email = cursor.fetchone()

    single_nft = {
        "artist": nft[0],
        "description": nft[1],
        "policy_id": nft[2],
        "price": nft[3],
        "royalty_percentage": nft[4],
        "royalty_wallet": nft[5],
        "policy_name": nft[6],
        "selling_fees": nft[7],
        "original_nft_name": nft[8],
        "nft_name": nft[8],
        "email": email[0]
        }

    return jsonify(single_nft)


@app.route('/resync_single_nft/<password>')
def resync_single_nft(password):

    # Send data to local server
    if password == '':

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM single_nfts WHERE policy_id = %s AND deleted = %s ''',('synchronizing', ''))
            results = cursor.fetchall()

        # Load data
        data = {}
        i = 0
        for x, elem in enumerate(results):
            try:
                internal_id = elem[0]
                username = elem[1]
                nft_name = elem[2]
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/description.txt", 'r') as text:
                    description = f'''{text.read()}'''
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/policy.txt", 'r') as text:
                    policy = text.read()
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/using_old_policy.txt", 'r') as text:
                    using_old_policy = text.read()
                    if using_old_policy == 'False':
                        using_old_policy = False
                    elif using_old_policy == 'True':
                        using_old_policy = True
                    else:
                        return render_template('/NFT/error_page.html', error='We found an error and are working to fix it')
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/royalty_percentage.txt", 'r') as text:
                    royalty_percentage  = text.read()
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/royalty_wallet.txt", 'r') as text:
                    royalty_wallet = text.read()
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/policy_duration.txt", 'r') as text:
                    policy_duration = text.read()
                    if policy_duration == '':
                        policy_duration = '0'
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/NFTID.txt", 'r') as text:
                    NFTID = text.read()
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/price.txt", 'r') as text:
                    price = text.read()
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/buyer_pay_fees.txt", 'r') as text:
                    buyer_pay_fees = text.read()
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/artist.txt", 'r') as text:
                    artist = text.read()
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/selling_fees.txt", 'r') as text:
                    selling_fees = text.read()
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/how_much.txt", 'r') as text:
                    how_much = text.read()
                with open(f"/home//ada_magic/single_nfts/{username}/{nft_name}/beneficiary_address.txt", 'r') as text:
                    beneficiary_address = text.read()
            except Exception as e:
                save_log_error(f'{e}', 'error loading data at sync nft')
                continue
                return f'{e} | loading data'

            try:
                # Create NFT project
                temp_name = nft_name
                temp_name = temp_name.replace(' ', '_')

                new_entry = {
                        "username": f'{username}',
                        "nft_name": f'{temp_name}',
                        "using_old_policy": f'{using_old_policy}',
                        "policy": f'{policy}',
                        "royalty_perc": f'{royalty_percentage}',
                        "royal_wallet": f'{royalty_wallet}',
                        "policy_duration": f'{policy_duration}',
                        "desc": f'{description}',
                        "nftid": f'{NFTID}',
                        "price": f'{price}',
                        "buyer_pay_fees": f'{buyer_pay_fees}',
                        "artist": f'{artist}',
                        "selling_fees": f'{selling_fees}',
                        "beneficiary_address": f'{beneficiary_address}',
                        "internal_id": f'{internal_id}'
                        }
            except Exception as e:
                return f'{e}'
            data[i] = new_entry
            i += 1

        try:
            return jsonify(data)
        except Exception as e:
            return f'{e}'


@app.route('/compose_single_nft/<password>')
def compose_single_nft(password):
    if password != '':
        return 'OK'

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username, nft_name, using_old_policy, policy_name, policy_duration, NFTID, price, selling_fees, beneficiary_wallet, full_size_image, nft_image_thumbnail, artist, description, royalty_percentage, royalty_wallet, internal_id, metadata_fields, file_type, collection_name FROM single_nfts WHERE policy_id = %s AND deleted = %s ''',('synchronizing', ''))
        results = cursor.fetchall()

    data = {}
    elements = [
        "username", "nft_name", "using_old_policy", "policy_name", "timelock",
        "nft_id", "price", "selling_fees", "beneficiary_address", "full_size_image",
        "thumbnail_img", "artist", "description", "royalty_percentage", "royalty_wallet",
        "internal_id", "metadata_fields", "file_type", "collection_name"]
    for x, elem in enumerate(results):
        data[x] = dict(zip(elements, elem))
    
    # data = data['']

    return jsonify(data)


@app.route('/resync_single_nft_db/<password>/<nft_wallet>/<internal_id>/<policy_id>/<username>/<policy_name>/<nft_name>', methods=['GET', 'POST'])
def resync_single_nft_db(password, nft_wallet, internal_id, policy_id, username, policy_name, nft_name):
    if password != '':
        return 'OK'
    try:
        # Update db from local server
        nft_name_temp = nft_name.replace('_', ' ')
        # try:
        #     os.mkdir(f'/home//ada_magic/single_nfts/{username}/{nft_name_temp}')
        # except:
        #     pass
        try:
            qr_code(nft_wallet, username, nft_name_temp, 'single', internal_id)
        except Exception as e:
            save_log_error(f'{qr_code}', 'resync')
        try:
            db_conn_info = db_params('_NFT')
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE single_nfts set deposit_wallet = %s, policy_id = %s, policy_name = %s, original_nft_name = %s, nft_image = %s, nft_image_thumbnail = %s, full_size_image = %s WHERE internal_id = %s''', (nft_wallet, policy_id, policy_name, nft_name_temp, '', '', '', internal_id))
                conn.commit()
        except Exception as e:
            return f'Error in database while updating: {e}'

        db_conn_info = db_params('_NFTsTracker')
        try:
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT * FROM policies WHERE policyID = %s''',(policy_id,))
                results = cursor.fetchall()
                if len(results) == 0:
                    cursor.execute('''INSERT INTO policies (policyName, policyID, username) VALUES(%s,%s,%s)''', (policy_name, policy_id, username))
                    conn.commit()
        except Exception as e:
            save_log_error(f'{e}', 'resync insert into policies')

        return f'NFT with internal_id: {internal_id}, was updated successfully. OK'
    except Exception as e:
        return f'{e}'


# Update sold single NFT
@app.route('/single_nft_sold/<password>/<internal_id>', methods=['GET', 'POST'])
def single_nft_sold(password, internal_id):
    if password == '':
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT username FROM single_nfts WHERE internal_id = %s''', (internal_id,))
            username = cursor.fetchone()
            cursor.execute("UPDATE users set can_request = '1' WHERE username = %s", (username[0],))
            conn.commit()
            cursor.execute('''UPDATE single_nfts set issold = '1' WHERE internal_id = %s''', (internal_id,))
            conn.commit()
            cursor.execute("SELECT SUM(price) FROM single_nfts WHERE issold = '1'")
            total_volume = cursor.fetchone()
            total_volume = total_volume[0]
            cursor.execute('''UPDATE total_volume set total_volume = %s WHERE internal_id = "1"''', (total_volume,))
            conn.commit()
        
        return 'updated'
    else:
        return 'Not updated'


@app.route('/request_email/<password>/<username>', methods=['GET', 'POST'])
def request_email(password, username):
    if password == '':
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT email FROM users WHERE username = %s''', (username,))
            username = cursor.fetchone()
        
        return username[0]

    return 'nope'



@app.route('/async_new_users/<password>/<status>', methods=['GET', 'POST'])
def async_new_users(password, status):
    if password != '':
        return jsonify({"Status": "OK"})


    if status == 'get':
        try:
            users = {}
            db_conn_info = db_params('_NFT')
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT username, external_wallet, inform_user, need_new_wallet, internal_id FROM users WHERE address = "Placeholder"''')
                results = cursor.fetchall()
            for elem in results:
                users[elem[0]] = {"internal_id": elem[4], "external_wallet": elem[1], "inform_user": elem[2], "need_new_wallet": elem[3]}

            return jsonify(users)
        except Exception as e:
            save_log_error(f'{e}', 'error async_new_users')
            return f'{e}'

    elif status == 'update':
        try:
            internal_id = request.args.get('internal_id')
            address = request.args.get('address')
            # seedphrase = request.args.get('seedphrase')
            
        except Exception as e:
            return f'{e}'

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE users set address = %s, inform_user = "2", need_new_wallet = "0" WHERE internal_id = %s''', (address, internal_id))
            conn.commit()
        return 'updated'


@app.route('/stablish_location/<password>', methods=['GET', 'POST'])
def stablish_location(password):
    if password != '':
        return 'no'
    
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT internal_id, ip, username FROM session_log WHERE location = ""''')
        logins = cursor.fetchall()
        cursor.execute('''SELECT internal_id, ip, username FROM single_nfts WHERE location = "" AND ip != ""''')
        nfts = cursor.fetchall()
        cursor.execute('''SELECT internal_id, ip, username FROM users WHERE location = "" AND ip != ""''')
        new_users = cursor.fetchall()
         

        def get_location(data_array, db_table):
            for elem in data_array:
                g = geocoder.ip(elem[1])
                geolocator = Nominatim(user_agent="")
                location = geolocator.reverse(f"{g.latlng[0]}, {g.latlng[1]}")
                physical_address = location.address

                cursor.execute(f"UPDATE {db_table} set location = %s WHERE internal_id = %s", (physical_address, elem[0]))
                conn.commit()
                time.sleep(2)
        
        get_location(logins, 'session_log')
        get_location(nfts, 'single_nfts')
        get_location(new_users, 'users')


      
    return 'ok'           


@app.route('/purge_deleted_nfts/<password>/', methods=['GET', 'POST'])
def purge_deleted_nfts(password):
    if password != '':
        return jsonify({"Status": "OK"})
    status = request.args.get('status')

    if status == 'get':
        try:
            users = {}
            elements = ['internal_id', 'username', 'nft_name', 'deposit_wallet']
            db_conn_info = db_params('_NFT')
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT internal_id, username, nft_name, deposit_wallet FROM single_nfts''')
                results = cursor.fetchall()
            for x, elem in enumerate(results):
                users[x] = dict(zip(elements, elem))
            
            return jsonify(users)

        except Exception as e:
            return f'{e}'

    if status == 'delete':
        internal_id = request.args.get('internal_id')
        # os.remove()
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM single_nfts WHERE internal_id=%s''', (internal_id,))
            conn.commit()

        return f'{internal_id} deleted'































































# Mailing list

# Resubscribe / Unsubscribe
@app.route('/subscription/<username>/<provided_hash>', methods=['GET', 'POST'])
def subscription(username, provided_hash):
    if ((sanity_check(username)) or (sanity_check(provided_hash))):
        return ''

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT email FROM users WHERE username = %s''', (username,))
        email = cursor.fetchone()
        email = email[0]
        checked_hash = encode_url(username, email, 'unsubscribe')
        if checked_hash == provided_hash:
            cursor.execute('''UPDATE users set subscribed = 0 WHERE username = %s''', (username,))
            conn.commit()

            # In case of user mistakenly unsubscribed:
            resubscribe = encode_url(username, email, 'subscribe')
            return render_template('/gigatheme/subscription.html', msg=f'{username}, you have been successfully unsubscribed from our mailing list', action=['unsubscribe', resubscribe])
    
# Resubscribe

# Encode url
def encode_url(username, email, action):
    salt = ''
    text = f'{username}{email}{salt}{action}'
    hashObject = hashlib.sha512(text.encode('utf-8'))
    digest = hashObject.hexdigest()

    return digest
# Sanity check

'''
███╗░░░███╗███████╗██████╗░██╗░█████╗░
████╗░████║██╔════╝██╔══██╗██║██╔══██╗
██╔████╔██║█████╗░░██║░░██║██║███████║
██║╚██╔╝██║██╔══╝░░██║░░██║██║██╔══██║
██║░╚═╝░██║███████╗██████╔╝██║██║░░██║
╚═╝░░░░░╚═╝╚══════╝╚═════╝░╚═╝╚═╝░░╚═╝
'''

@app.route('/media', methods=['GET', 'POST'])
def media():

    # Load Media
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT internal_id, name, description, thumbnail, code FROM audio''')
        audio = cursor.fetchall()
        conn.commit()

    return render_template('/NFT/media.html', audio=audio, video=['','','','',''])


@app.route('/play_media/<media_type>/<internal_id>', methods=['GET', 'POST'])
def play_media(media_type, internal_id):

    # Load Media
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        query = f'SELECT name, description, thumbnail, code FROM {media_type} WHERE internal_id = {internal_id}'
        cursor.execute(query)
        audio = cursor.fetchone()
        conn.commit()

    audio = audio.decode()
    return render_template('/NFT/play_media.html', media_type=f'{media_type}', audio=audio)


@app.route('/insert_media/', methods=['GET', 'POST'])
def insert_audio():
    return render_template('/NFT/insert_media.html')



@app.route('/insert_media_files/', methods=['GET', 'POST'])
def insert_media_files():
    try:
        try:
            file = request.files['audio']
            name = request.form['name']
            description = request.form['description']
            thumbnail = request.files['thumbnail']
            media_type = 'audio'
        except:
            pass
        try:
            file = request.files['video']
            name = request.form['name']
            description = request.form['description']
            thumbnail = request.files['thumbnail']
            media_type = 'video'
        except:
            pass
        try:
            file = request.files['blog']
            name = request.form['name']
            description = request.form['description']
            thumbnail = request.files['thumbnail']
            media_type = 'blog'
        except:
            pass


        file.save('/home//ada_magic/tmp/temp.mp3')
    except Exception as e:
        return f'{e}, previous saving stage'
    try:

        with open('/home//ada_magic/tmp/temp.mp3' ,'rb') as text:
            code = base64.b64encode(text.read())
            code = str(code,'ascii', 'ignore')
            # f2.write("data:audio/mp3;base64,")
            # code = str(code,'ascii', 'ignore')
    except Exception as e:
        return f'{e}, saving stage'
    try:

        db_conn_info = db_params('_NFT')
        if media_type == 'audio':

            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cursor = conn.cursor()
                if media_type == 'audio':
                    cursor.execute('''INSERT INTO audio (name, description, thumbnail, code) VALUES (%s,%s,%s,%s)''',(name, description, '', f'{code}'))
                audio = cursor.fetchall()
                conn.commit()

    except Exception as e:
        return f'{e}, database phase, {code}'

    return 'success'
















'''
██████╗░██████╗░░█████╗░███████╗██╗██╗░░░░░███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██║██║░░░░░██╔════╝
██████╔╝██████╔╝██║░░██║█████╗░░██║██║░░░░░█████╗░░
██╔═══╝░██╔══██╗██║░░██║██╔══╝░░██║██║░░░░░██╔══╝░░
██║░░░░░██║░░██║╚█████╔╝██║░░░░░██║███████╗███████╗
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░░░░╚═╝╚══════╝╚══════╝
'''




'''
██████╗░███████╗░██████╗████████╗               ░█████╗░███████╗            ████████╗██╗░░██╗███████╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝               ██╔══██╗██╔════╝            ╚══██╔══╝██║░░██║██╔════╝
██████╔╝█████╗░░╚█████╗░░░░██║░░░               ██║░░██║█████╗░░            ░░░██║░░░███████║█████╗░░
██╔══██╗██╔══╝░░░╚═══██╗░░░██║░░░               ██║░░██║██╔══╝░░            ░░░██║░░░██╔══██║██╔══╝░░
██║░░██║███████╗██████╔╝░░░██║░░░               ╚█████╔╝██║░░░░░            ░░░██║░░░██║░░██║███████╗
╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░               ░╚════╝░╚═╝░░░░░            ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝

███╗░░░███╗███████╗███╗░░██╗██╗░░░██╗
████╗░████║██╔════╝████╗░██║██║░░░██║
██╔████╔██║█████╗░░██╔██╗██║██║░░░██║
██║╚██╔╝██║██╔══╝░░██║╚████║██║░░░██║
██║░╚═╝░██║███████╗██║░╚███║╚██████╔╝
╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░╚═════╝░
'''






'''
███╗░░░███╗░█████╗░███╗░░██╗██╗░░░██╗░█████╗░██╗░░░░░               ░█████╗░░█████╗░████████╗██╗░█████╗░███╗░░██╗░██████╗
████╗░████║██╔══██╗████╗░██║██║░░░██║██╔══██╗██║░░░░░               ██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║██╔════╝
██╔████╔██║███████║██╔██╗██║██║░░░██║███████║██║░░░░░               ███████║██║░░╚═╝░░░██║░░░██║██║░░██║██╔██╗██║╚█████╗░
██║╚██╔╝██║██╔══██║██║╚████║██║░░░██║██╔══██║██║░░░░░               ██╔══██║██║░░██╗░░░██║░░░██║██║░░██║██║╚████║░╚═══██╗
██║░╚═╝░██║██║░░██║██║░╚███║╚██████╔╝██║░░██║███████╗               ██║░░██║╚█████╔╝░░░██║░░░██║╚█████╔╝██║░╚███║██████╔╝
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚══════╝               ╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░
'''

@app.route('/delete_user_from_db_manually/<password1>', methods=['GET', 'POST'])
def delete_user_from_db2(password1):
    if password1 != '':
        return ''

    users = []
    conn = mysql.connector.connect(host='', 
                    user='', 
                    password='', 
                    database='')
    cursor = conn.cursor()
    for username in users:
        sql = "DELETE FROM users WHERE username = %s"
        adr = (f"{username}", )
        cursor.execute(sql, adr)
        conn.commit()
    conn.close()

    return f'{username} deleted from database'


@app.route('/delete_user_from_db/<username>/<password2>', methods=['GET', 'POST'])
def delete_user_from_db(username, password2):
    if password2 == '':
        conn = mysql.connector.connect(host='', 
                        user='', 
                        password='', 
                        database='')
        cursor = conn.cursor()
        sql = "DELETE FROM users WHERE username = %s"
        adr = (f"{username}", )
        cursor.execute(sql, adr)
        conn.commit()
        conn.close()
        return f'{username} deleted from database'
    else:
        return ''


@app.route('/delete_user_profile_from_db/<internal_id>/<password2>', methods=['GET', 'POST'])
def delete_user_profile_from_db(internal_id, password2):
    if password2 == '':
        conn = mysql.connector.connect(host='',
                        user='',
                        password='',
                        database='')
        cursor = conn.cursor()
        sql = "DELETE FROM user_profile WHERE internal_id = %s"
        adr = (f"{internal_id}", )
        cursor.execute(sql, adr)
        conn.commit()
        conn.close()
        return f'{internal_id} deleted from database'
    else:
        return ''



# Only do this when phpmyadmin does not allow manual change
@app.route('/manually_feature_art/<action>/<password>/<internal_id>', methods=['GET', 'POST'])
def manually_feature_art(action, password, internal_id):
    if password != '':
        return ''
    try:
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            if action == 'feature':
                cursor.execute("UPDATE single_nfts set featured = '1' WHERE internal_id = %s", (internal_id,))
                conn.commit()

            if action == 'unfeature':
                cursor.execute('''UPDATE single_nfts set featured = '' WHERE internal_id = %s''', (internal_id,))
                conn.commit()
    except Exception as e:
        return f'{e}'

    return ''


# Only do this when phpmyadmin does not allow manual change
@app.route('/change_policy_id/<policy_id>/<internal_id>', methods=['GET', 'POST'])
def change_policy_id(policy_id, internal_id):
    try:
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE single_nfts set policy_id = %s WHERE internal_id = %s''', (policy_id, internal_id))
            conn.commit()
    except Exception as e:
        return 'yeah'

    return 'no'


# Set fees correctly
@app.route('/set_fees', methods=['GET', 'POST'])
def set_fees():

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT price, internal_id FROM single_nfts''')
        results = cursor.fetchall()
        for elem in results:
            price = int(elem[0])
            fees = int(price / 100) + 2
            cursor.execute('''UPDATE single_nfts set selling_fees = %s WHERE internal_id = %s''', (str(fees), elem[1]))
            conn.commit()


    return 'ok'


def load_single_collection(collection_name, username):
    data = {}
    collection_name = collection_name.replace('_', ' ')
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT internal_id, nft_name, price, artist, issold, deposit_wallet, hearts, policy_id, verified_status FROM single_nfts WHERE collection_name=%s AND deleted = "" AND username=%s''', (collection_name, username))
        results = cursor.fetchall()
        if results == []:
            return None, None, None
        
        data['policy_id'] = results[0][7]
        cursor.execute('''SELECT MIN(price), MAX(price), COUNT(internal_id) FROM single_nfts WHERE collection_name=%s AND deleted = "" AND username=%s''', (collection_name, username))
        collection_data = cursor.fetchone()
        data['floor'] = collection_data[0]
        data['ceil'] = collection_data[1]
        data['total'] = str(collection_data[2])
        cursor.execute('''SELECT COUNT(internal_id) FROM single_nfts WHERE collection_name=%s AND issold = "1" AND username=%s''', (collection_name, username))
        sold = cursor.fetchone()
        sold = str(sold[0])
        data['sold'] = sold
        cursor.execute('''SELECT description FROM collections WHERE collection_name=%s AND username=%s''', (collection_name, username))
        description = cursor.fetchone()
        data['description'] = description[0]
        data['collection_name'] = collection_name
        data['username'] = username

    nft = search_results_single_nft_json_search(results)
    if session.get('username'):
        remembered_hearts = []
        cursor.execute('''SELECT nft_liked FROM user_likes_nft WHERE username = %s''', (session['username'],))
        results = cursor.fetchall()
        conn.commit()
        for x in results:
            remembered_hearts.append(str(x[0]))
    else:
        remembered_hearts = []
    
    
    return nft, remembered_hearts, data
    
        
















'''
████████╗███████╗░██████╗████████╗░██████╗
╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝
░░░██║░░░█████╗░░╚█████╗░░░░██║░░░╚█████╗░
░░░██║░░░██╔══╝░░░╚═══██╗░░░██║░░░░╚═══██╗
░░░██║░░░███████╗██████╔╝░░░██║░░░██████╔╝
░░░╚═╝░░░╚══════╝╚═════╝░░░░╚═╝░░░╚═════╝░
'''

# Unit testing

# Restore projects (depricated)



# Keep ssh alive (depricated)



@app.route('/get_otp/<password>', methods=['GET', 'POST'])
def get_otp(password):
    if password == '':
        return str(otp)
    else:
        return ''


# Read seed (depricated)



@app.route('/test/<password>', methods=['GET', 'POST'])
def test(password):
    if password == '':
        try:
            conn = mysql.connector.connect(host='', 
                    user='', 
                    password='', 
                    database='')
            cursor = conn.cursor()
            email = ''
            cursor.execute('''INSERT INTO password_recovery (email, email_opt, is_valid, time_now) VALUES (%s,%s,%s,%s)''',(email, "0", "False", "0"))
            conn.commit()
            conn.close()
            return "Added"
        except Exception as e:
            return render_template("/NFT/test.html", error=e)




@app.route('/error', methods=['GET', 'POST'])
def error():
    ds = ds
    return 'success'



@app.route('/test1', methods=['GET', 'POST'])
def test1():
    return render_template('/NFT/test.html')



@app.route('/image_card/<internal_id>.png', methods=['GET', 'POST'])
def image_card(internal_id):
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT nft_image_thumbnail FROM single_nfts WHERE internal_id = %s''',(internal_id,))
        result = cursor.fetchone()

    return render_template('/NFT/image_card.html', image=result[0]) 
        
@app.route('/test5')
def test5():
    return render_template('/NFT/login_test.html')


@app.route('/css/<file>')
def css(file):
    return render_template(f'/gigatheme/css/{file}')


@app.route('/test6')
def test6():
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM user_profile''')
        profile_data = cursor.fetchall()
        for elem in profile_data:
            if 'user' in elem[0]:
                try:
                    with open(f'/home//ada_magic/{elem[0]}', "rb") as img_file:
                        img = base64.b64encode(img_file.read()).decode('utf-8')
                        cursor.execute('''UPDATE user_profile set picture = %s WHERE internal_id = %s''', (elem[7],))
                        conn.commit()
                except Exception as e:
                    save_log_error('test6', f'{e}')
                    pass
            if elem[0] == '':
                try:
                    with open(f'/home//ada_magic/users/{elem[5]}/profile_picture.png', "rb") as img_file:
                        img = base64.b64encode(img_file.read()).decode('utf-8')
                        cursor.execute('''UPDATE user_profile set picture = %s WHERE internal_id = %s''', (elem[7],))
                        conn.commit()
                except Exception as e:
                    save_log_error('test6a', f'{e}')

    return 'pl'


@app.route('/test9')
def test9():
    
    return render_template('/NFT/login_test.html')


@app.route('/test10')
def test10():
    
    return render_template('/gigatheme/1_verify_seed.html', seedphrase=['', '', ''])


@app.route('/test11', methods=['GET', 'POST'])
def test11():
    if request.method == "POST":

        try:
            seed = request.form['hidden']
            save_log_error('seed1', f'{seed}')
            return f'<h1>seed:|{seed}|</h1>'
        except Exception as e:
            save_log_error('seed error', f'{e}')
            return f'<h1>seed error:|{e}|</h1>'
    return 'none'







'''
░█████╗░██████╗░██╗
██╔══██╗██╔══██╗██║
███████║██████╔╝██║
██╔══██║██╔═══╝░██║
██║░░██║██║░░░░░██║
╚═╝░░╚═╝╚═╝░░░░░╚═╝
'''




@app.route('/api/<route>/<heart_id>', methods=['GET', 'POST'])
def api(route, heart_id):
    if route == 'landing_page':
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM single_nfts WHERE deleted = ""''')
            latest = cursor.fetchall()
            info = cursor.fetchall()
            latest = latest[-8:]
            cursor.execute('''SELECT internal_id, nft_name, nft_image_thumbnail, price, policy_id, artist, issold FROM single_nfts WHERE featured = "1"''')
            single_nfts = cursor.fetchall()
            conn.commit()
            cursor.execute('''SELECT internal_id, name, thumbnail, price, policy_id, number_of_mints, minted_so_far, artist FROM vending_machine_projects WHERE featured = "1"''')
            vending_machine = cursor.fetchall()
            cursor.execute('''SELECT price, username FROM single_nfts WHERE issold = "1"''')
            issold = cursor.fetchall()
            conn.commit()

        latest = list(reversed(latest))
        top_sellers, top_sellers_array = top_artist(issold)

        return jsonify({"latest": latest, "single_nfts": single_nfts, "vending_machine": vending_machine, "top_sellers": top_sellers})

    if route == 'hearts':
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor.execute('''SELECT hearts FROM single_nfts WHERE internal_id = %s''', (heart_id))
            results = cursor.fetchone()
            results = int(results[0]) + 1
            cursor.execute('''UPDATE single_nfts set hearts = %s WHERE internal_id = %s''', (heart_id,))
            conn.commit()

        return jsonify({"Success": f'{heart_id}'})

    return jsonify({"Error": f"Route: {route}, not found"})






















@app.route('/newsletter_send/<username>', methods=['GET', 'POST'])
def blabla(username):
    pass
















'''
░██████╗░██╗░██████╗░░█████╗░██╗░░░░░░█████╗░███╗░░██╗██████╗░
██╔════╝░██║██╔════╝░██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔══██╗
██║░░██╗░██║██║░░██╗░███████║██║░░░░░███████║██╔██╗██║██║░░██║
██║░░╚██╗██║██║░░╚██╗██╔══██║██║░░░░░██╔══██║██║╚████║██║░░██║
╚██████╔╝██║╚██████╔╝██║░░██║███████╗██║░░██║██║░╚███║██████╔╝
░╚═════╝░╚═╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
'''

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    if sanity_check(username):
        return redirect('giga_index')

    
    try:
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT picture, title, alias, username, banner, website, twitter, discord_invite, instagram, description, beneficiary_address FROM user_profile WHERE username = %s''', (username,))
            profile_data = cursor.fetchone()
            cursor.fetchall()

            cursor.execute('''SELECT * FROM vending_machine_projects WHERE username = %s''', (username,))
            vending_machine_projects = cursor.fetchall()
            
            cursor.execute('''SELECT internal_id, nft_name, internal_id, price, policy_id, hearts, issold, views, artist, deposit_wallet, qr_code, username FROM single_nfts WHERE username = %s AND deleted = ""''', (username,))
            single_nfts = cursor.fetchall()

            cursor.execute('''SELECT price FROM single_nfts WHERE username = %s AND deleted = "" ORDER BY price ASC LIMIT 1''', (username,))
            floor = cursor.fetchall()
            if len(floor) == 0:
                floor = 0
            else:
                floor = floor[0][0]

            cursor.execute('''SELECT nft_liked, action FROM user_likes_nft''')
            remembered_hearts = cursor.fetchall()


            cursor.execute('''SELECT wants_money, withdraw_to FROM users WHERE username = %s''', (username,))
            user = cursor.fetchone()
            balance = None
            try:
                wants_money = user[0]
            except:
                wants_money = False
            error = False
            if wants_money == '1':
                wants_money = True
            elif wants_money == '2':
                wants_money = True
                error = True
            else:
                wants_money == False
            try:
                withdraw_to = user[1]
            except:
                withdraw_to = ''


    except Exception as e:
        save_log_error(f'{e}', 'error loading profile info')
        return render_template('/gigatheme/404.html', msg='User not found')
    
    try:

        if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
            profile_pic = f"C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\users\\{username}\\profile_picture.png"
            profile_pic = f"C:/Users//Desktop/proyects/ada_magic/website/users/{username}/profile_picture.png"
            banner_pic = f"C:/Users//Desktop/proyects/ada_magic/website/users/{username}/banner.png"

            


            
        else:
            profile_pic = f"/home//ada_magic/users/{username}/profile_picture.png"
            banner_pic = f"/home//ada_magic/users/{username}/banner.png"
        
        try:
            with open(banner_pic, 'rb') as text:
                banner_pic = str(base64.b64encode(text.read()).decode('utf-8'))
                # banner_pic = text.read()
                # banner_pic = base64.encodestring(banner_pic)
        except:
            banner_pic = ''

        try:
            with open(profile_pic, 'rb') as text:
                profile_pic = str(base64.b64encode(text.read()).decode('utf-8'))
        except:
            profile_pic = ''

        try:
            user_profile = {
                "username": username,
                "profile_pic": profile_pic,
                "title": profile_data[1],
                "alias": profile_data[2],
                "banner": banner_pic,
                "website": profile_data[5],
                "twitter": profile_data[6],
                "discord_invite": profile_data[7],
                "instagram": profile_data[8],
                "description": profile_data[9],
                "beneficiary_address": profile_data[10],
                "floor": floor
                
                }
        except Exception as e:
            save_log_error('Could not mount user_profile at /profile. Maybe user not found', f'{e}')
            return render_template('/gigatheme/1_msg.html', msg='User not found')
        single = {}#internal_id, nft_name, internal_id, price, policy_id, hearts, issold, views, artist, deposit_wallet, qr_code, username
        elements = ["internal_id","nft_name","image","price","policy_id","hearts","issold","views","artist","deposit_wallet","qr_code","username"]
        for x, nft in enumerate(single_nfts):
            single[x] = dict(zip(elements, nft))


        vending = []
        for nft in vending_machine_projects:
            temp = {
                "internal_id": nft[13],
                "name": nft[0],
                "image": nft[15],
                "price": nft[5],
                "policy_id": nft[7],
                "minted_so_far": nft[14],
                "number_of_mints": nft[1]
            }
            vending.append(temp)
        user_profile["vending_machine"] = vending
    except Exception as e:
        save_log_error(f'{e}', 'Error at user_profile')
        return render_template('/gigatheme/404.html', msg=f'Something went wrong while looking for the user: {username}')

    if not session.get('username'):
        if ((profile_data == None) or (profile_data == '')):
            return render_template('/gigatheme/404.html', msg='User not found')

        resp = make_response(render_template('/gigatheme/1_profile.html', profile_data=profile_data,
                vending_machine_projects=vending_machine_projects,
                single_nfts=single, updatable=False, user=username,
                address='', user_profile_view=user_profile, remembered_hearts=remembered_hearts))
        resp.cache_control.max_age = 0
        return resp

    if ((profile_data == None) or (profile_data == '')):
        return render_template('/gigatheme/404.html', error='User not found', username=session['username'],
            user_profile=session['user_profile'])

    if session['username'] == username:
        resp = make_response(render_template('/gigatheme/1_profile.html', profile_data=profile_data,
            vending_machine_projects=vending_machine_projects,
            single_nfts=single, updatable=True, username=session['username'],
            user=username, user_profile=session['user_profile'], address=session['wallet_address'],
            user_profile_view=user_profile, remembered_hearts=remembered_hearts, balance=balance,
            wants_money=wants_money, withdraw_to=withdraw_to, error=error))
        resp.cache_control.max_age = 0
        return resp
    else:
        resp = make_response(render_template('/gigatheme/1_profile.html', profile_data=profile_data,
            vending_machine_projects=vending_machine_projects,
            single_nfts=single, updatable=False, username=session['username'],
            user=username, user_profile=session['user_profile'], user_profile_view=user_profile,
            remembered_hearts=remembered_hearts, address=''))
        resp.cache_control.max_age = 0
        return resp


@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    if not session.get('username'):
        return render_template('/gigatheme/1_login.html')

    if username != session['username']:
        return redirect(f'profile/{username}')
    else:
        return render_template('/gigatheme/1_edit_profile.html', username=session['username'],
            user_profile=session['user_profile'], updatable=True)


@csrf.include
@app.route('/update_user_profile', methods=['GET', 'POST'])
def update_user_profile():
    if not session.get('username'):
        return redirect('login')

    if request.method == "POST":
        username = request.form['username_modify']

        if sanity_check(username):
            return username

        if username == session['username']:
            alias = request.form['alias']
            title = request.form['title']
            description = request.form.get("description")
            website = request.form['website']
            twitter = request.form['twitter']
            discord_invite = request.form['discord_invite']
            instagram = request.form['instagram']

            if ((sanity_check(alias)) or (sanity_check(title)) or (sanity_check(twitter)) or 
                (sanity_check(instagram)) or (website_check(website)) or 
                (description_check(description)) or (website_check(discord_invite))):
                return redirect(f'profile/{session["username"]}')



            if request.files:
                try:
                    img = request.files['file']
                    if img.filename != '':
                        update_profile_img_db('file', img)
                except Exception as e:
                    save_log_error('resizing images f""', f'{img}')
                    pass
                try:
                    img = request.files['file_banner']
                    if img.filename != '':
                        update_profile_img_db('file_banner', img)
                except Exception as e:
                    pass

            try:
                # Store values
                db_conn_info = db_params('_NFT')
                with closing(mysql.connector.connect(**db_conn_info)) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''UPDATE user_profile set description = %s, title = %s, alias = %s, website = %s, twitter = %s, discord_invite = %s, instagram = %s WHERE username = %s''', (description, title, alias, website, twitter, discord_invite, instagram, f"{session['username']}"))
                    conn.commit()
                    cursor.execute('''SELECT internal_id, alias, username, title, description, internal_id, twitter, instagram, discord_invite FROM user_profile WHERE username = %s''', (session['username'],))
                    results = cursor.fetchone()
                    cursor.execute('''SELECT * FROM vending_machine_projects WHERE username = %s''', (username,))
                    vending_machine_projects = cursor.fetchall()
                    conn.commit()
                    cursor.execute('''SELECT internal_id, nft_name, nft_image_thumbnail, price, policy_id FROM single_nfts WHERE username = %s''', (session['username'],))
                    single_nfts = cursor.fetchall()
                    conn.commit()
            except Exception as e:
                save_log_error(f'{e}', 'error updating db profile')
                return render_template('/gigatheme/1_login.html/', msg='Your profile could not be updated',
                    username=session['username'], user_profile=session['user_profile'])

            profile_pic = f"/home//ada_magic/users/{session['username']}/profile_picture.png"
            with open(profile_pic, 'rb') as text:
                profile_pic = str(base64.b64encode(text.read()).decode('utf-8'))

            user_profile = {
                "alias": results[1],
                "description": results[4],
                "username": results[2],
                "profile_pic": profile_pic,
                "title": results[3],
                "twitter": results[6], 
                "instagram": results[7], 
                "discord_invite": results[8], 
            }

            session['user_profile'] = user_profile

            return redirect(f'profile/{session["username"]}')
        else:
            return render_template('/gigatheme/1_login.html', username=session['username'], user_profile=session['user_profile'],
                msg=f'You are not the user you are trying to modify. The user is: {username}' )
    else:
        return render_template('/gigatheme/1_login.html', username=session['username'], user_profile=session['user_profile'],
            msg='Incorrect method' )



@app.route('/explore/<current_page>', methods=['GET', 'POST'])
@cache.cached()
def explore(current_page: int):

    # Purge bad actors
    try:
        current_page = int(current_page)
    except:
        if not session.get('username'):
            return render_template('/gigatheme/404.html', error='Page not found')
        else:
            return render_template('/gigatheme/404.html', error='Page not found', username=session['username'],
                user_profile=session['user_profile'])

    items_per_page = 24
    single_nfts, remembered_hearts, total_pages = load_all_single_nfts_explore(items_per_page, current_page)    

    # Paginations
    pagination_start = current_page - 3
    if pagination_start < 0:
        pagination_start = 0

    pagination_end = current_page + 3
    if pagination_end > total_pages:
        pagination_end = total_pages
    


    # Case 2: There are NFTs available
    if not session.get('username'):
        return render_template('/gigatheme/1_explore.html', total_pages=total_pages,
                current_page=current_page, single_nfts=single_nfts, pagination_start=pagination_start,
                pagination_end=pagination_end, remembered_hearts=[])
    else:
        return render_template('/gigatheme/1_explore.html', total_pages=total_pages,
                current_page=current_page, single_nfts=single_nfts, pagination_start=pagination_start,
                pagination_end=pagination_end, username=session['username'], remembered_hearts=remembered_hearts,
                user_profile=session['user_profile'])


@app.route('/login', methods=['GET', 'POST'])
@cache.cached()
def giga_login():

    if not session.get('username'):
        response = make_response(render_template('/gigatheme/1_login.html'))
        return response
    else:
        response = make_response(render_template('/gigatheme/1_login.html', username=session['username'], user_profile=session['user_profile']))
        return response


@csrf.include
@app.route('/verify_login', methods=['GET', 'POST'])
def verify_login():
    try:
        username = request.form['username']
        username = username.replace(' ', '_')
        if sanity_check_login(username):
            return render_template('/gigatheme/1_login.html', msg='Invalid username or email')
    except:
        pass

    if request.method == "POST":
        password = request.form['password'].encode()

        if '@' in username:  # User is trying to login with email instead of username
            option = 'email'
        else:
            option = 'username'


        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()

            #Check if user has validated the email. Fetch the email and resend the OTP
            cursor.execute(f"SELECT username, password, email, emailVerification, address, external_wallet, inform_user, blocked FROM users WHERE {option} = %s", (username,))
            results = cursor.fetchone()
            if results == None:
                conn.close()
                return render_template('/gigatheme/1_login.html', msg='Invalid username')

            # Flush buffer
            try:
                cursor.fetchall()
            except:
                pass

            if results[7] == 1:
                return render_template('/gigatheme/1_inform_message.html', msg='This user is temporarly blocked due to copyright infringment. If you think this is an error, please, contact us.')

        session.clear()

        try:
            if int(results[3]) == 0: #Email is not verified verifyEmailAddress
                email = results[2]
                msg = Message('OTP', sender = '', recipients = [email])  
                msg.body = f'Welcome to ADA Magic Marketplace.\n\n Your verification code is: {str(otp)}\n\n It is great to see you here, in case you do need something let us know via email () or Twitter @ada_magic_io\n Happy minting'  
                mail.send(msg)
                session['username'] = results[0]
                return ('verify_email')

        except:
            try:
                if results[3] == None: #Email is not verified verifyEmailAddress
                    email = results[2]
                    msg = Message('ADA Magic Marketplace verification code',sender = '', recipients = [email])  
                    msg.body = f'Welcome to ADA Magic Marketplace.\n\n Your verification code is: {str(otp)}\n\n It is great to see you here, in case you do need something let us know via email () or Twitter @ada_magic_io\n Happy minting'  
                    mail.send(msg)
                    session['username'] = results[0]
                    return ('verify_email')
            except:
                return redirect('verify_email')
        
        #check password
        storedPassword = results[1].encode()
        if bcrypt.checkpw(password, storedPassword):
            if ((results[4] == '') or (results[4] == None)):  # User has no wallet address
                session['wallet_address'] = 'Placeholder'

            # elif len(results[5]) > 5:  # User has external wallet
            #     session['wallet_address'] = results[db_external_wallet]
            else:
                results[4].replace('\n', '')
                session['wallet_address'] = results[4]
            session['username'] = results[0]

            if results[6] == "10":  # Inform user
                # Fetch seedphrase
                return redirect('inform_user')
            
            # try:
            #     remember_me = request.form['remember_me']
            #     app.config["SESSION_PERMANENT"] = True
            # except:
            #     app.config["SESSION_PERMANENT"] = False

            db_conn_info = db_params('_NFT')
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT picture, alias, username, title, description, banner, twitter, instagram, discord_invite, discord_name FROM user_profile WHERE username = %s''', (session['username'],))
                results = cursor.fetchone()
                cursor.execute('''INSERT INTO session_log (username, ip, login_time) VALUES (%s, %s, %s)''', (session['username'], f'{request.remote_addr}', f'{datetime.datetime.utcnow()}'))
                conn.commit()
            
            profile_pic = f"/home//ada_magic/users/{session['username']}/profile_picture.png"
            try:
                with open(profile_pic, 'rb') as text:
                    profile_pic = str(base64.b64encode(text.read()).decode('utf-8'))
            except:
                profile_pic = ''
            user_profile = {
                "alias": results[1],
                "description": results[4],
                "username": results[2],
                "profile_pic": profile_pic,
                "title": results[3],
                "twitter": results[6], 
                "instagram": results[7], 
                "discord_invite": results[8], 
                "discord_name": results[9]
            }
            session['user_profile'] = user_profile
            latest, single_nfts, vending_machine, remembered_hearts, total_volume, top_sellers_array, collections, total_artwork = load_all_single_nfts_index()
            # top_sellers_array = load_top_sellers()

            return render_template('/gigatheme/1_index.html', single_nfts=single_nfts, vending_machine=vending_machine,
            latest=latest, username=session['username'], top_sellers=top_sellers_array, remembered_hearts=remembered_hearts,
            user_profile=session['user_profile'], total_volume=total_volume, collections=collections, total_artwork=total_artwork)
        else:
            return render_template('/gigatheme/1_login.html', msg="Login and or password don't match, please try again")


    return render_template('/gigatheme/1_login.html')


@app.route('/', methods=['GET', 'POST'])
@cache.cached()
def giga_index():

    latest, featured, vending_machine, remembered_hearts, total_volume, top_sellers_array, collections, total_artwork = load_all_single_nfts_index()
    if not session.get('username'):
        return render_template('/gigatheme/1_index.html', single_nfts=featured, vending_machine=vending_machine,
            latest=latest, top_sellers=top_sellers_array, remembered_hearts='', total_volume=total_volume,
            collections=collections, total_artwork=total_artwork)
    else:
        return render_template('/gigatheme/1_index.html', single_nfts=featured, vending_machine=vending_machine,
            latest=latest, collections=collections, username=session['username'], top_sellers=top_sellers_array,
            remembered_hearts=remembered_hearts, user_profile=session['user_profile'], total_volume=total_volume,
            total_artwork=total_artwork)


@app.route('/show_single_nft/<internal_id>', methods=['GET', 'POST'])
@cache.cached()
def show_single_nft_giga(internal_id):
    try:
        int(internal_id)
    except:
        return redirect('index')
    try:
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT internal_id, username, nft_name, artist, deposit_wallet, internal_id, description, policy_id, price, qr_code, metadata, royalty_percentage, hearts, views, issold, category, metadata_fields FROM single_nfts WHERE internal_id = %s''', (internal_id,))
            results = cursor.fetchone()
            cursor.execute('''SELECT twitter, instagram, discord_invite, website FROM user_profile WHERE username = %s''', (results[1],))
            social_media_links = cursor.fetchone()
            views = int(results[13])
            views += 1
            cursor.execute('''UPDATE single_nfts set views = %s WHERE internal_id = %s''', (str(views), internal_id))
            conn.commit()
            cursor.execute("INSERT INTO views2 (ip_address, time_now, nft_internal_id) VALUES(%s, %s, %s)", (f'{request.remote_addr}', f'{datetime.datetime.utcnow()}', internal_id))
            conn.commit()
            if not session.get('username'):
                pass
            else:
                cursor.execute('''SELECT * FROM user_likes_nft WHERE nft_liked = %s and username = %s ORDER BY timestamped DESC''', (internal_id, session['username']))
                liked = cursor.fetchall()
    except Exception as e:
        return render_template('/gigatheme/404.html', error='NFT not found')

    # Show the heart be active or not?
    if not session.get('username'):
        liked = False
    else:
        # not liked ever
        if liked == []:
            liked = False
        elif len(liked[0]) == 0:
            liked = False
        else:
            if liked[0][4] == 'plus':
                liked = True
            else:
                liked = False



    

    if results[16] == None or results[16] == '' or results[16] == '{}':
        metadata = ''
    else:
        metadata = json.dumps(results[16])
        metadata = json.loads(metadata)

    single_nft = {
        "internal_id": results[0],
        "username": results[1],
        "nft_name": results[2],
        "artist": results[3],
        "deposit_wallet": results[4],
        "nft_image": f'/single_nfts/{results[0]}/single_nft.png',
        "description": results[6],
        "policy_id": results[7],
        "price": results[8],
        "qr_code": results[9],
        "metadata": results[10],
        "royalty_percentage": results[11],
        "hearts": results[12],
        "views": results[13],
        "issold": results[14],
        "liked": liked,
        "category": results[15],
        "metadata": metadata
        }

    social_media = {}
    try:
        social_media["twitter"] = social_media_links[social_media_links[0]]
    except:
        pass
    try:
        social_media["instagram"] = social_media_links[social_media_links[1]]
    except:
        pass
    try:
        social_media["discord_invite"] = social_media_links[social_media_links[2]]
    except:
        pass
    try:
        social_media["website"] = social_media_links[social_media_links[3]]
    except:
        pass

    if not session.get('username'):
        return render_template('/gigatheme/1_show_nft.html', nft=single_nft, social_media=social_media)
    else:
        if single_nft["username"] == session['username']:
            return render_template('/gigatheme/1_show_nft.html', nft=single_nft, username=session['username'],
                updatable=True, user_profile=session['user_profile'], social_media=social_media)
        else:
            return render_template('/gigatheme/1_show_nft.html', nft=single_nft, username=session['username'],
                user_profile=session['user_profile'], social_media=social_media)


@app.route('/mint', methods=['GET', 'POST'])
def mint():
    if not session.get('username'):
        return render_template('/gigatheme/1_mint.html', policies='', username='', collections='', user_profile='{}')
    
        # return redirect('login')
    

    db_conn_info = db_params('_NFTsTracker')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT policyName FROM policies WHERE username = %s''', (session['username'],))
        results = cursor.fetchall()
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT internal_id, collection_name FROM collections WHERE username = %s''', (session['username'],))
        collections = cursor.fetchall()
        conn.commit()


    return render_template('/gigatheme/1_mint.html', policies=results, username=session['username'], user_profile=session['user_profile'],
    collections=collections)


@csrf.include
@app.route('/create_item', methods=['GET', 'POST'])
def create_item():
    if not session.get('username'):
        return render_template('/gigatheme/1_login.html', msg='You need to be logged in before minting')


    if request.method == "POST":

        # Collection
        nft_type = request.form['nft_type']
        if nft_type == 'Collection':
            collection_raw = request.form['collection_id']
            if collection_raw == '':
                collection_name = request.form['collection_name']
                if sanity_check(collection_name):
                    return render_template('/gigatheme/1_mint.html', msg='Invalid collection name. Please, use only letters from a-z, numbers and spaces',
                        address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])
                collection_id = ''
            else:
                collection_raw = collection_raw.replace('(', '').replace(')', '')
                collection_raw = collection_raw.split(',')
                try:
                    int(collection_raw[0])
                    collection_id = int(collection_raw[0])
                except Exception as e:
                    save_log_error(f'Wrong collection IF. Username: {session["username"]}', f'{e}')
                    return render_template('/gigatheme/1_mint.html', msg='Incorrect collection id',
                        address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])

                # Clean collection name
                collection_name = collection_raw[1][2:-1]
                
                if description_check(collection_name):
                    session['user_profile']['msg'] = 'Incorrect collection name'
                    return render_template('/gigatheme/1_mint.html', msg='Invalid collection name. Please, use only letters from a-z, numbers and spaces',
                    address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])
        
            temp_collection_name = collection_name.replace(' ', '_')
            if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
                collection_path = f"C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\collections\\{session['username']}\\{temp_collection_name}\\single_nft.png"
                folder1 = f"C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\collections\\{session['username']}"
                folder2 = f'{folder1}\\{temp_collection_name}'
            else:
                collection_path = f"/home//ada_magic/collections/{session['username']}/{temp_collection_name}/single_nft.png"
                folder1 = f"/home//ada_magic/collections/{session['username']}"
                folder2 = f"{folder1}/{temp_collection_name}"
            try:
                file_collection = request.files['file_collection']
            except Exception as e:
                pass
            try:
                os.mkdir(folder1)
            except:
                pass
            try:
                os.mkdir(folder2)
            except:
                pass
            try:
                file_collection.save(collection_path)
                im = Image.open(collection_path)
                im.thumbnail([600, 600])
                im.save(collection_path, 'webp', quality=95, subsampling=0, optimize=True)
            except:
                pass
        else:
            collection_name = ''


        
        # Metadata
        raw_metadata = request.form.getlist('metadata')
        metadata_fields = ''
        if raw_metadata == ['', ''] or raw_metadata == ['', '', '', ''] or raw_metadata == ['', '', '', '', '', '']:
             metadata_fields = None
        else:
            for elem in raw_metadata:
                if sanity_check(elem):
                    return render_template('/gigatheme/1_mint.html', msg='Invalid metadata fields',
                        address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])
            x = 0
            if len(raw_metadata) % 2 != 0:
                return render_template('/gigatheme/1_mint.html', msg='We did not understand the metadata. Please, try again with correct values',
                    address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])

            for elem in raw_metadata:
                if elem == '':
                    continue
                metadata_fields += f'"{elem}"'
                x += 1
                if x % 2 == 0:
                    metadata_fields += ','
                else:
                    metadata_fields += ':'
            metadata_fields = metadata_fields[:-1]
            metadata_fields = "'{" + metadata_fields + "}'"





        # Artist
        try:
            artist = request.form['artist']
            if sanity_check(artist):
                return render_template('/gigatheme/1_mint.html', msg='Invalid artist name. Please, try again', artist='Artist name',
                    address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])
            if ((artist == '') or (artist == None)):
                return render_template('/gigatheme/1_mint.html', msg='Invalid artist name. Please, try again', artist='Artist name',
                    address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])
        except:
            return render_template('/gigatheme/1_mint.html', msg='Invalid artist name. Please, try again', artist='Artist name',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])

        # NFT name
        try:
            nft_name = request.form['name']
            if sanity_check(nft_name):
                return render_template('/gigatheme/1_mint.html', msg='Invalid nft name. Please, try again',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])
        except:
            return render_template('/gigatheme/1_mint.html', msg='Invalid nft name. Please, try again',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])
        while nft_name[-1] == ' ':
            nft_name = nft_name[:-1]

        # Check no minted art with the same name
        # UNCOMMENT!!!
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT internal_id, nft_name, username FROM single_nfts WHERE nft_name = %s AND username = %s AND deleted = %s", (nft_name, session['username'], ''))
            is_taken = cursor.fetchall()
        if len(is_taken) != 0:
            return render_template('/gigatheme/1_mint.html', msg='You do already have a project with the same name. Please, modify it or delete it to start over',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])

        category = request.form['category']
        hashtags = request.form['hashtags']
        if ((sanity_check(category)) or sanity_check(hashtags)):
            return redirect('/')
        
        # NFT ID, by default: 1
        NFTID = 1

        # Price
        try:
            price = request.form['price']
            price = int(price)
            if price < 3:
                return render_template('/gigatheme/1_mint.html', msg='The minimum price is 3 ADA',
                    address=session['wallet_address'], username=session['username'], user_profile=session['user_profile']) 
        except:
            return render_template('/gigatheme/1_mint.html', msg='Invalid price. Please, try again',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])

        # Description
        # >>> OnlyAscii = lambda s: re.match('^[\x00-\x7F]+$', s) != None
        # >>> OnlyAscii('string')
        # True
        try:
            description = request.form['description']
            if description_check(description):
                return render_template('/gigatheme/1_mint.html', msg='Invalid description. You used some characters that are not allowed. Please, try again',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])
        except:
            description = ''
        
        description = description.replace('\r', '')
        description = description.replace('\n', '')
        string_pattern = r"[^a-zA-Z0-9!+ =.,;:?(')\n -]"
        regex_pattern = re.compile(string_pattern)
        result = regex_pattern.search(description)

        if result != None:
            a = result.span()
            return render_template('/gigatheme/1_mint.html', msg=f'Description is not correct. Character not accepted: {description[a[0]:a[1]]}',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])

        if ((description == '') or (description == None)):
            description = ''

        try:
            royalty_percentage = int(request.form['royalties'])
        except:
            royalty_percentage = 0

        # Policy
        using_old_policy = True

        try:
            old_policy_name = request.form['oldPolicy']
        except Exception as e:
            old_policy_name = ''
        try:
            policy_name = request.form['policyName']
        except:
            policy_name = ''
        if sanity_check(policy_name):
            return render_template('/gigatheme/1_mint.html', msg=f'Incorrect policy ID',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])

        policy_name = policy_name.replace(' ', '_')
        if policy_name == session['username']:
            return render_template('/gigatheme/1_mint.html', msg='Invalid policy name. Please, use a different policy name than your username and try again',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])


        policy_duration = request.form['policyExpirationDate']
        if ((old_policy_name == '') or (old_policy_name == None)):
            using_old_policy = False
            actual_policy = policy_name
            if actual_policy == '':
                actual_policy = 'Standard'
            else:
                db_conn_info = db_params('_NFTsTracker')
                with closing(mysql.connector.connect(**db_conn_info)) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT policyName FROM policies WHERE username = %s", (session['username'],))
                    results = cursor.fetchall()
                    conn.commit()
                    if len(results) == 0:
                        cursor.execute("INSERT INTO policies (policyName, username) VALUES (%s,%s)", (policy_name ,session['username']))
                        conn.commit()
                    
        else:
            using_old_policy = True
            actual_policy = old_policy_name
            policy_duration = ''
        if actual_policy == '':
            actual_policy = 'Standard'

        # Store NFT
        try:
            file = request.files['file']
        except Exception as e:
            save_log_error(f'invalid file . Username: {session["username"]}', e)
            return render_template('/gigatheme/1_mint.html', msg=f'{e}Invalid file. Please, try again',
                user_profile=session['user_profile'], username=session['username']) 

        try:
            os.mkdir(f"/home//ada_magic/single_nfts/{session['username']}/")
        except:
            pass
        # try:
        #     os.mkdir(f"/home//ada_magic/single_nfts/{session['username']}/single_nft")
        # except Exception as e:
        #     save_log_error(f'{e}', 'could not make folder while minting')
        #     pass
        

        try:
            if f':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
                image_path = f"C:/Users//Desktop/proyects/ada_magic/website/single_nfts/{session['username']}/single_nft.png"
                try:
                    os.mkdir(f"C:/Users//Desktop/proyects/ada_magic/website/single_nfts/{session['username']}")
                except:
                    pass
            else:
                image_path = f"/home//ada_magic/single_nfts/{session['username']}/single_nft.png"

            try:
                file.save(image_path)
            except:
                os.remove(image_path)
                file.save(image_path)
            
            # File checks
            size = os.path.getsize(image_path)
            if size > 50000000:
                return render_template('/gigatheme/1_mint.html', msg=f'File size greater than 30mb. Please, make it smaller than 30',
                    address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])
            kind = filetype.guess(image_path)
            try:
                if kind.mime == 'image/png' or kind.mime == 'image/jpg' or kind.mime == 'image/jpeg':
                    resize_blob(image_path)
            except Exception as e:
                save_log_error(f"{session['username']} Error recognizing image type", f'{e}')
                return render_template('/gigatheme/1_msg.html', msg='The file you tried to upload is not correct. Please, make sure you only use .png, .jpg or .jpeg')
            
        except Exception as e:
            save_log_error(f'Error downsizing images giga mint. Username: {session["username"]}', f'{e}')
            return render_template('/gigatheme/1_mint.html', msg=f'Invalid image downsize action. Please, try again',
            address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])  # Picture is wrong, return to mint

        # Assert Image has the right properties
        try:
            with open(image_path, "rb") as img_file:
                base_64_img = base64.b64encode(img_file.read()).decode('utf-8')
            img64 = bytes(base_64_img,'UTF-8')
            png_recovered = base64.decodebytes(img64)
            with open(image_path, 'wb') as f:
                f.write(png_recovered)
            im = Image.open(image_path)
            im.close()
            
        except Exception as e:
            save_log_error(f'Error converting img to base64 . Username: {session["username"]}', f'{e}')
            return render_template('/gigatheme/1_mint.html', msg=f'The image file you tried to upload is not valid. Please, make sure the image format is correct and the image is not corrupted',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])

        kind_test = filetype.guess(image_path)
        if kind.mime != kind_test.mime:
            save_log_error(f'Error asserting mime types after image conversion. Username: {session["username"]}', f'{e}')
            return render_template('/gigatheme/1_mint.html', msg=f'Error finding out image type. Please, for the moment use only jpg or png',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])

        # Base64 images and delete them from web server
        try:
            main = f'{image_path[:-4]}_main{image_path[-4:]}'
            full = image_path
            def fast_convertion(path):
                with open(path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode('utf-8')
            nft_image = fast_convertion(main)
            full_size_image = fast_convertion(full)

        except Exception as e:
            save_log_error(f'Error base64 image convertion. Username: {session["username"]}', f'{e}')
            return render_template('/gigatheme/1_mint.html', msg=f'Invalid image type. Please, use only .jpg or .png files',
            address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])  # Picture is wrong, return to mint


        # Calculating fees
        minting_fees = 1
        selling_fees = int(price / 100) + 1
        binding = 1.5
        if using_old_policy:
            tx_fee = 0.5
        else:
            tx_fee = 1
        total_fees = float(minting_fees) + float(selling_fees) + binding + tx_fee
        ada_magic_fees = minting_fees + selling_fees
        # Store NFT in DB
        try:
            db_conn_info = db_params('_NFT')
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cursor = conn.cursor()
                # items = ['username', 'nft_name', 'artist', 'deposit_wallet', 'nft_image', 'description', 'policy_id', 'price', 'royalty_percentage', 'policy_name', 'original_nft_name', 'full_size_image', 'policy_duration', 'selling_fees', 'deleted', 'views', 'hearts', 'category', 'hashtags', 'ip', 'creation_time']
                # storing_items = [session['username'], nft_name, artist, 'synchronizing', nft_image, description, 'synchronizing', price, royalty_percentage, actual_policy, nft_name, full_size_image, policy_duration, selling_fees+1, '0', '0', 0, category, hashtags, f'{request.remote_addr}', f'{datetime.datetime.now()}']
                
                # Artist verified status
                cursor.execute('''SELECT verified_status FROM users WHERE username=%s''', (session['username'],))
                verified_status = cursor.fetchone()
                verified_status = verified_status[0]

                cursor.execute('''SELECT internal_id FROM single_nfts ORDER BY internal_id DESC LIMIT 1''')
                latest = cursor.fetchone()
                cursor.fetchall()
                latest = latest[0]
                internal_id = int(latest) + 1
                if nft_type == 'Collection':
                    temp_coll = collection_name
                    temp_coll = temp_coll.replace(' ', '_')
                    actual_policy = f'{temp_coll}_collection'
                cursor.execute('''INSERT INTO single_nfts (username, nft_name, artist, deposit_wallet, nft_image, description, policy_id, price, royalty_percentage, policy_name, original_nft_name, full_size_image, policy_duration, selling_fees, deleted, views, hearts, category, hashtags, ip, creation_time, internal_id, metadata_fields, file_type, verified_status)
                                VALUES (
                                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                    %s, %s, %s, %s, %s)''',
                                (session['username'], nft_name, artist, 'synchronizing', nft_image, description, 'synchronizing', price, royalty_percentage, actual_policy, nft_name, full_size_image, policy_duration, selling_fees+1, '0', '0', 0, category, hashtags, f'{request.remote_addr}', f'{datetime.datetime.now()}', internal_id, metadata_fields, kind.mime, verified_status))
                conn.commit()

                # New collection
                if nft_type == 'Collection' and collection_id == '':
                    try:
                        cursor.execute('''INSERT INTO collections (username, collection_name) VALUES (%s, %s)''', (session['username'], collection_name))
                        conn.commit()
                    except:
                        pass
                    cursor.execute('''SELECT internal_id FROM collections WHERE username = %s AND collection_name = %s''', (session['username'], collection_name))
                    collection_id = cursor.fetchone()
                    collection_id = collection_id[0]
                
                # Old and new collection, both apply
                if nft_type == 'Collection':
                    cursor.execute('''INSERT INTO collections_users (collection_id, username, single_nft_internal_id) VALUES (%s, %s, %s)''', (collection_id, session['username'], internal_id))
                    conn.commit()
                    cursor.execute("UPDATE single_nfts set collection_name = %s WHERE internal_id = %s", (collection_name, internal_id,))
                    conn.commit()


        except Exception as e:
            save_log_error(f'Storing collection NFT. Username {session["username"]}', f'{e}')
            return render_template('/gigatheme/1_mint.html', msg=f'Error saving new collection into database',
                address=session['wallet_address'], username=session['username'], user_profile=session['user_profile'])



        if f':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
            new_path = f"C:/Users//Desktop/proyects/ada_magic/website/single_nfts/{internal_id}/single_nft.png"
            # thumb_path = new_path[:-4] + 'thumbnail.png'
            try:
                try:
                    os.mkdir(f"C:/Users//Desktop/proyects/ada_magic/website/single_nfts/{internal_id}")
                except:
                    pass
                if kind.mime == 'image/png' or kind.mime == 'image/jpg' or kind.mime == 'image/jpeg':
                    create_image_devices(image_path, internal_id)
                shutil.copyfile(main, new_path)
            except Exception as e:
                save_log_error(f'mint shutil. Username: {session["username"]}', f'{e}')
        else:
            new_path = f"/home//ada_magic/single_nfts/{internal_id}/single_nft.png"
            # thumb_path = new_path[:-4] + 'thumbnail.png'
            try:
                try:
                    os.mkdir(f"/home//ada_magic/single_nfts/{internal_id}")
                except:
                    pass
                if kind.mime == 'image/png' or kind.mime == 'image/jpg' or kind.mime == 'image/jpeg':
                    create_image_devices(image_path, internal_id)
                shutil.copyfile(main, new_path)
            except Exception as e:
                save_log_error(f'mint shutil. Username: {session["username"]}', f'{e}')

        summary = {
            "image": full_size_image,
            "name": nft_name,
            "artist": artist,
            "price": price,
            "description": description,
            "royalties": royalty_percentage,
            "internal_id": internal_id,
            "policy_name": actual_policy,
            "policy_duration": policy_duration,
            "minting_fees": minting_fees,
            "selling_fees": selling_fees,
            "tx_fee": tx_fee,
            "total_fees": total_fees,
            "internal_id": internal_id,
            "category": category,
            "hashtags": hashtags,
            "nft_type": nft_type,
            "collection_name": collection_name,
            "metadata": metadata_fields
            }

        return render_template('/gigatheme/1_verify_single.html', nft=summary, username=session['username'], user_profile=session['user_profile'])

    else:
        return render_template('/gigatheme/1_mint.html', user_profile=session['user_profile'], username=session['username'],
            msg='Error, you did not upload your artwork correctly. Please, try again or contact us via Twitter at @ada_magic_io')


@app.route('/verify_nft/<internal_id>', methods=['GET', 'POST'])
def verify_nft(internal_id):
    if not session.get('username'):
        return render_template('/gigatheme/1_login.html')

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username, deleted FROM single_nfts WHERE internal_id = %s''', (internal_id,))
        results = cursor.fetchone()
        if ((results[0] == session['username']) and (results[1] == '0')):
            cursor.execute("UPDATE single_nfts set deleted = '' WHERE internal_id = %s", (internal_id,))
            conn.commit()

    return render_template('/gigatheme/1_success.html', msg='Congratulations, you have successfully uploaded one artwork.',
        username=session['username'], user_profile=session['user_profile'])


@app.route('/edit_nft/<internal_id>', methods=['GET', 'POST'])
def edit_nft(internal_id):
    if not session.get('username'):
        return render_template('/gigatheme/1_login.html')
    try:
        int(internal_id)
    except:
        return redirect('/')

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username, artist, nft_name, price, description, royalty_percentage, category, hashtags FROM single_nfts WHERE internal_id = %s''', (internal_id,))
        result = cursor.fetchone()
    if result[0] != session['username']:
        return redirect('/')
    try:
        hashtags = result[7].split(' ')
    except:
        hashtags = []
    hashtags1 = []
    for hashtag in hashtags:
        if hashtag != []:
            hashtags1.append(hashtag)
    nft = {
        "username": result[0],
        "artist": result[1],
        "nft_name": result[2],
        "price": result[3],
        "description": result[4],
        "royalties_perc": result[5],
        "category": result[6],
        "hashtags": hashtags1,
        "image": f"/single_nfts/{internal_id}/single_nft.png",
        "internal_id": internal_id
    }
    
    return render_template('/gigatheme/1_modify_single_nfts.html', nft=nft, username=session['username'], user_profile=session['user_profile'])


@app.route('/modify_single_nft/<internal_id>', methods=['GET', 'POST'])
def modify_single_nft(internal_id):
    try:
        internal_id = int(internal_id)
    except:
        return redirect('/')

    if not session.get('username'):
        return redirect('/')

    if request.method == "POST":
        artist = request.form['artist']
        royalties_perc = request.form['royalties']
        description = request.form['description']
        nft_name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        hashtags = request.form['hashtags']

        try:
            int(price)
            if royalties_perc != '':
                int(royalties_perc)
        except:
            return redirect('/')

        if ((sanity_check(artist)) or (sanity_check(nft_name)) or (sanity_check(category)) or (sanity_check(hashtags))
            or (description_check(description))):
            return redirect('/')

        file = request.files['file']
        if file.filename != '':
            if secure_filename(file.filename):
                path = f"/home//ada_magic/single_nfts/{internal_id}/single_nft.png"
                file.save(path)
                with open(path, 'rb') as text:
                    image_base64 = text.read()
                im = Image.open(path)
                im.thumbnail([600, 600])
                im.save(path, 'webp')
        else:
            image_base64 = ''

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT username FROM single_nfts WHERE internal_id = %s''',(internal_id,))
            results = cursor.fetchone()

            # EXTREAMLY IMPORTANT CHECK
            if session['username'] != results[0]:
                return redirect('/')

            if image_base64 == '':
                cursor.execute('''UPDATE single_nfts set artist = %s, royalty_percentage = %s, description = %s, nft_name = %s, price = %s, category = %s, hashtags = %s, nft_image = '' WHERE internal_id = %s''', (artist, royalties_perc, description, nft_name, price, category, hashtags, internal_id))
            else:
                cursor.execute("UPDATE single_nfts set artist = %s, royalty_percentage = %s, description = %s, nft_name = %s, price = %s, category = %s, hashtags = %s, full_size_image = %s  WHERE internal_id = %s", (artist, royalties_perc, description, nft_name, price, category, hashtags, image_base64, internal_id))
            conn.commit()

        return render_template('/gigatheme/1_success.html', msg=f'You have modified "{nft_name}"', username=session['username'], user_profile=session['user_profile'])
    

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username, artist, nft_name, price, description, royalty_percentage, category, hashtags FROM single_nfts WHERE internal_id = %s''', (internal_id,))
        result = cursor.fetchone()
    if result[0] != session['username']:
        return redirect('/')
    try:
        hashtags = result[7].split(' ')
    except:
        hashtags = []
    hashtags1 = []
    for hashtag in hashtags:
        if hashtag != []:
            hashtags1.append(hashtag)
    nft = {
        "username": result[0],
        "artist": result[1],
        "nft_name": result[2],
        "price": result[3],
        "description": result[4],
        "royalties_perc": result[5],
        "category": result[6],
        "hashtags": hashtags1,
        "image": f"/single_nfts/{internal_id}/single_nft.png",
        "internal_id": internal_id
    }
    return render_template('/gigatheme/1_modify_single_nfts.html', nft=nft, username=session['username'], user_profile=session['user_profile'], msg='Something went wrong. Please, modify again your NFT')


@app.route('/single_nft_delete/<internal_id>', methods=['GET', 'POST'])
def single_nft_delete(internal_id):
    try:
        internal_id = int(internal_id)
    except:
        return render_template('/gigatheme/1_inform_message.html', msg='It is not a valid NFT the item you are trying to delete')

    if not session.get('username'):
        return render_template('/gigatheme/1_login.html', msg='Login first in order to modify an NFT')

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username FROM single_nfts WHERE internal_id = %s''', (internal_id,))
        result = cursor.fetchone()
        # EXTREAMLY IMPORTANT CHECK
        if result[0] != session['username']:
            return redirect('login', msg='You need to be the author in order to delete this file')

        cursor.execute("UPDATE single_nfts set deleted = '1' WHERE internal_id = %s", (internal_id,))
        conn.commit()

    if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
        shutil.rmtree(f"C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\single_nfts\\{internal_id}")
    else:
        shutil.rmtree(f"/home//ada_magic/single_nfts/{internal_id}/")

    return render_template('/gigatheme/1_success.html', msg='Congratulations, you have successfully deleted one artwork.',
        username=session['username'], user_profile=session['user_profile'])


@app.route('/collections/<collection_name>/<username>', methods=['GET', 'POST'])
def collections(collection_name, username):

    collection, remembered_hearts, data = load_single_collection(collection_name, username)

    # Collection not found
    if collection == None:
        # No username
        if not session.get('username'):
            return render_template('/gigatheme/1_msg.html', msg='Collection not found')
        # Username found
        else:
            try:
                return render_template('/gigatheme/1_msg.html', msg='Collection not found', username=session['username'],
                user_profile=session['user_profile'])
            except:
                user_profile = {
                "username": username,
                "profile_pic": '',
                "title": '',
                "alias": '',
                "banner": '',
                "website": '',
                "twitter": '',
                "discord_invite": '',
                "instagram": '',
                "description": '',
                "beneficiary_address": '',
                "floor": ''
                }
                return render_template('/gigatheme/1_msg.html', msg='Collection not found', username=session['username'],
                user_profile=user_profile)

    # Collection found
    # No username
    if not session.get('username'):
        return render_template('/gigatheme/1_single_collection.html', collection=collection,remembered_hearts=remembered_hearts,
        data=data)

    # Username found
    else:    
        return render_template('/gigatheme/1_single_collection.html', collection=collection, username=session['username'],
        remembered_hearts=remembered_hearts, user_profile=session['user_profile'], data=data)


@app.route('/vending_m', methods=['GET', 'POST'])
def vending_m():
    if not session.get('username'):
        return render_template('/gigatheme/1_vending_machine.html')
    else:
        return render_template('/gigatheme/1_vending_machine.html', username=session['username'],
            user_profile=session['user_profile'])


@app.route('/vending_machine_load', methods=['GET', 'POST'])
def vending_machine_load():
    if not session.get('username'):
        return render_template('/gigatheme/1_vending_machine.html', msg='You need to be logged in in order to mint')

    if request.method == "POST":
        username = session['username']
        collection_name = request.form['collection_name']
        if sanity_check(collection_name):
            return redirect('vending_m')

        if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
            folder_name = f"C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\users\\{username}\\{collection_name}\\"
            user_folder = f"C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\users\\{username}"
        else:
            folder_name = f"/home//ada_magic/users/{username}/{collection_name}/"
            user_folder = f"/home//ada_magic/users/{username}/"
        try:
            os.mkdir(f"{user_folder}")
        except:
            pass
        try:
            os.mkdir(folder_name)
        except:
            pass

        # print(f'''
        #         collection name:{request.form['collection_name']}
        #         thumbnail: {request.files['thumbnail']}
        #         total: {request.form['collection_total']}
        #         price: {request.form['price']}
        #         description: {request.form['description']}
        #         ''')
        
        
        # Check the username is not taken
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM vending_machine_projects WHERE name = %s", (collection_name,))
            is_taken = cursor.fetchone()
            print(is_taken)
        # if is_taken != None:
        #     return render_template('/gigatheme/1_vending_machine.html', msg=f'project name is taken: {is_taken}',
        #         username=session['username'], wallet=session['wallet_address'], user_profile=session['user_profile'])

        # Artist name
        try:
            artist = request.form['artist']
            if sanity_check(artist):
                return redirect('vending_m')
        except:
            return render_template('/gigatheme/1_vending_machine.html', msg='There is no artist in this project, you MUST include the artist',
                username=username, wallet=session['wallet_address'], user_profile=session['user_profile'])

        # Total number of NFTs and folders
        try:
            collection_total = int(request.form['collection_total'])
        except:
            return render_template('/gigatheme/1_vending_machine.html', msg='You need to tell how many NFTs in total your collection has',
                username=username, wallet=session['wallet_address'], user_profile=session['user_profile'])

        # Price of each NFT
        try:
            price = int(request.form['price'])
        except:
            return render_template('/gigatheme/1_vending_machine.html', msg='You need to tell the price of each NFT',
                username=username, wallet=session['wallet_address'], user_profile=session['user_profile'])

        # Royalties percentage
        royalties_perc = request.form['royalties']
        if royalties_perc == '':
            pass
        else:
            try:
                royalties_perc = int(royalties_perc)
            except:
                return render_template('/gigatheme/1_vending_machine.html', msg='You need to tell the percentage of the royalties you want with one or two numbers',
                    username=username, wallet=session['wallet_address'], user_profile=session['user_profile'])

        # Description
        try:
            description = request.form['description']
            if description_check(description):
                return redirect('vending_m')
        except:
            description = 'No description'
        
        # Website
        try:
            website = request.form['website']
            if website_check(website):
                return redirect('vending_m')
        except:
            website = 'No website'

        # Minting date
        try:
            minting_date = request.form['date1']
            minting_date = int(minting_date)
            minting_date2 = request.form['date2']
            if sanity_check_minting_date(minting_date2):
                return redirect('vending_m')
        except:
            return render_template('/gigatheme/1_vending_machine.html', msg='You need to set a starting date for the project',
                username=username, wallet=session['wallet_address'], user_profile=session['user_profile'])

        # store images
        # Thumbnail image
        try:
            thumbnail_img = request.files['thumbnail']
            thumbnail_img.save(f"{folder_name}thumbnail.png")
        except Exception as e:
            save_log_error(f'{e}', 'Vending machine thumbnail could not be saved')

        # images_path = {}
        print('About to store images')
        # print(request.files)

        '''
        ImmutableMultiDict([
        ('thumbnail',
         <FileStorage: '' ('application/octet-stream')>),
         ('obj0',
         <FileStorage: 'background_1.PNG' ('image/png')>),
         ('obj0',
         <FileStorage: 'background_2.PNG' ('image/png')>),
         ('obj0',
         <FileStorage: 'background_3.PNG' ('image/png')>),
         ('obj1',
         <FileStorage: 'element_1.PNG' ('image/png')>),
         ('obj1',
         <FileStorage: 'element_2.PNG' ('image/png')>),
         ('obj2',
         <FileStorage: 'skin_1.PNG' ('image/png')>),
         ('obj2',
         <FileStorage: 'skin_2.PNG' ('image/png')>),
         ('obj2',
         <FileStorage: 'skin_3.PNG' ('image/png')>),
         ('obj3',
         <FileStorage: 'marking_1.PNG' ('image/png')>),
         ('obj3',
         <FileStorage: 'marking_2.PNG' ('image/png')>),
         ('obj3',
         <FileStorage: 'marking_3.PNG' ('image/png')>),
         ('obj4',
         <FileStorage: '' ('application/octet-stream')>),
         ('obj5',
         <FileStorage: '' ('application/octet-stream')>),
         ('obj6',
         <FileStorage: '' ('application/octet-stream')>),
         ('obj7',
         <FileStorage: '' ('application/octet-stream')>),
         ('obj8',
         <FileStorage: '' ('application/octet-stream')>),
         ('obj9',
          <FileStorage: '' ('application/octet-stream')>)])
        '''
        # print(request.files.getlist())
        

        for x in range(10):
            files = request.files.getlist(f'obj{x}')
            for file in files:
                if 'image' not in file.content_type:
                    break
                print(files)
                print(file.content_type)
                
        sys.exit()
        # for elem in request.files.items():
        #     print(elem)
        # print(request.files["obj0"], 'THUMBNAIL\n\n')

        # try:
        #     items = request.files.items()
        # except Exception as e:
        #     print(f'\nException, could not transform dic: {e}\n')
        # print(type(items))
        # print(f'lenght: {len(items)}')
        # print(f'lenght: {len(items)}, items0: {items[0]}, items1: {items[1]}')











        nft_theoretical_max = 1
        for layer_number in range(1, 9):
            layer_nft = 0
            files = request.files.getlist('obj_b' + str(layer_number))
            print(files, 'files')
            # paths = []
            for file_number, file in enumerate(files):
                if secure_filename(file.filename).endswith('.png', -4):
                    layer_nft += 1

                # meaning secure_file(file.filame) is not empty
                if f'{folder_name}{secure_filename(file.filename)}' != f'{folder_name}':

                    try:
                        os.mkdir(f'{folder_name}/layer{layer_number}/')
                    except:
                        pass

                    if secure_filename(file.filename).endswith('.png', -4):
                        file.save(f'{folder_name}/layer{layer_number}/{secure_filename(file.filename)}')
                        fixed_image = Image.open(f'{folder_name}/layer{layer_number}/{secure_filename(file.filename)}')
                        fixed_image = fixed_image.convert('RGBA')
                        fixed_image.save(f'{folder_name}/layer{layer_number}/{secure_filename(file.filename)}')
                        # paths.append(f'{folder_name}/layer{layer_number}/{secure_filename(file.filename)}')
            # images_path[layer_nft] = paths
            if layer_nft != 0:
                nft_theoretical_max *= layer_nft

        # Create an iterator with the number of layers
        all_files = os.listdir(f'{folder_name}')
        all_files.sort()
        total_layers = 0
        for elem in all_files:
            if os.path.isdir(f'{folder_name}/{elem}'):
                total_layers += 1

        # Store images path
        total_files = []
        stored_img = {"layer1":{0:{}}}
        for layer_number in range(total_layers):
            fields = []
            layer_number += 1
            files_in_layer = os.listdir(f'{folder_name}layer{layer_number}')
            files_in_layer.sort()
            print(files_in_layer, 'files_in_layer')

            layer = {}
            for file_number, filename in enumerate(files_in_layer):
                number = {}
                if '.png' in filename:
                    try:
                        with open(f'{folder_name}layer{layer_number}/{filename}', "rb") as img_file:
                            img = base64.b64encode(img_file.read()).decode('utf-8')
                        fields.append(filename)
                    except Exception as e:
                        save_log_error('vending machine giga searching imgs', f'{e}')
                        continue
                    try:
                        stored_img[f"layer{layer_number}"][file_number] = {"img": img}
                    except:
                        stored_img[f"layer{layer_number}"] = {}
                        stored_img[f"layer{layer_number}"][file_number] = {"img": img}

            total_files.append(fields)
        # save_log_error(f'Total files vending machine: {total_files}', f"{username}")
        
        # Create 9 images and display to the user in case he/she does not want it!
        images = []
        # try:
        #     os.mkdir(f'static/temp_images/{collection_name}/')
        # except:
        #     pass
        print(f'\n\n{total_files}')
        print(f'{len(total_files)}')
        for elem in total_files:
            assert len(elem) != 0
        for x in range(9):
            random_number1 = random.randint(0, len(total_files[0])-1)
            random_number2 = random.randint(0, len(total_files[1])-1)
            # f'{folder_name}/layer{layer_number}/{filename}'
            im1 = Image.open(f'{folder_name}layer1/{total_files[0][random_number1]}')
            im2 = Image.open(f'{folder_name}layer2/{total_files[1][random_number2]}')
            try:
                im1 = im1.convert('RGBA')
                im2 = im2.convert('RGBA')
            except:
                pass
            newImage = Image.alpha_composite(im1, im2)


            for layer, elem in enumerate(total_files[2:]):
                layer += 3
                random_number = random.randint(0, len(elem)-1)
                im2 = Image.open(f'{folder_name}layer{layer}/{total_files[layer-1][random_number]}')
                try:
                    im2 = im2.convert('RGBA')
                except:
                    pass
                newImage = Image.alpha_composite(newImage, im2)

            newImage.save(f'{folder_name}{collection_name}{x}.png')
            images.append(f'{folder_name}{collection_name}{x}.png')
            
            # newImage.save(f'static/temp_images/{collection_name}/{collection_name}{x}.png')
            # images.append(f'static/temp_images/{collection_name}/{collection_name}{x}.png')

        # Store project
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO vending_machine_projects (artist, description, name, number_of_mints, policy_id, price, website, minting_date, layers, hearts, views, username, deleted)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (artist, description, collection_name, str(collection_total), 'synchronizing', str(price), website, minting_date, json.dumps(stored_img), 0, '0', username, '0'))
            conn.commit()
            cursor.execute("SELECT internal_id FROM vending_machine_projects WHERE name = %s", (collection_name,))
            results = cursor.fetchone()

        summary = {
            "internal_id": results[0],
            "images": images,
            "collection_name": collection_name,
            "price": price,
            "royalties_perc": royalties_perc,
            "artist": artist,
            "total_nfts": collection_total,
            "description": description,
            "website": website,
            "minting_date2": minting_date2
            }
        return render_template('/gigatheme/1_verify_vm.html', username=session['username'],
            nft=summary, user_profile=session['user_profile'])

    return render_template('/gigatheme/1_vending_machine.html', error='No project could get generated. Please try again or contact us via Twitter at: @ada_magic_io',
        username=session['username'], user_profile=session['user_profile'])


@app.route('/verify_vm/<internal_id>', methods=['GET', 'POST'])
def verify_vm(internal_id):
    if not session.get('username'):
        return render_template('/gigatheme/1_vending_machine.html', msg='You need to be logged in in order to mint')

    # sanity check
    try:
        dummy_variable = int(internal_id)
    except:
        return redirect('vm_giga')
    
    # Check ownership
    if check_ownership_vm(internal_id):
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE vending_machine_projects set deleted = '' WHERE internal_id = %s", (internal_id,))
            conn.commit()
        return render_template('/gigatheme/1_success.html', msg='Congratulations, your project has been successfully uploaded. The policy ID and address will get synchronized soon',
            user_profile=session['user_profile'], username=session['username'])
    else:
        return render_template('/gigatheme/1_vending_machine.html', username=session['username'], user_profile=session['user_profile'])


@app.route('/delete_vm/<internal_id>', methods=['GET', 'POST'])
def delete_vm(internal_id):
    if not session.get('username'):
        return render_template('/gigatheme/1_vending_machine.html', msg='You need to be logged in in order to mint')

    # sanity check
    try:
        dummy_variable = int(internal_id)
    except:
        return redirect('vm_giga')

    # Check ownership
    if check_ownership_vm(internal_id):
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM vending_machine_projects WHERE internal_id = %s''', (internal_id,))
            conn.commit()
        return render_template('/gigatheme/1_success.html', msg='Project deleted successfully', username=session['username'], user_profile=session['user_profile'])
    else:
        return render_template('/gigatheme/1_vending_machine.html', username=session['username'], user_profile=session['user_profile'])


@csrf.include
@app.route('/search/<current_page>', methods=['POST'])
def search(current_page):
    if request.method == "POST":
        try:
            request.form['ordered_by']
        except:
            ordered_by = 'Order by'
        try:
            request.form['category']
        except:
            category = 'All categories'

        if ((request.form['query'] == '') and (request.form['ordered_by'] == 'Order by') and (request.form['category'] == 'All categories') and 
            session.get('search')):
            query = session['search'][0]
            category = session['search'][1]
            ordered_by = session['search'][2]
        else:
            query = request.form['query']
            try:
                category = request.form['category']
                if 'All categories' == category:
                    category = ''
            except:
                category = ''
            try:
                ordered_by = request.form['ordered_by']
                if 'Order by' == ordered_by:
                    ordered_by = 'Newest'
            except:
                ordered_by = 'Newest'
    else:
        try:
            session.get('search')
            query = session['search'][0]
            category = session['search'][1]
            ordered_by = session['search'][2]
        except:
            session['search'] = ['', '', '']



    if ((sanity_check(query)) or (sanity_check(ordered_by) or (sanity_check(category)))):
        return redirect('/')
    try:
        current_page = int(current_page)
    except:
        return redirect('/')

    
    query1, category1, ordered_by1 = query, category, ordered_by
    category1 = category1.replace(' ', '_')

    items_per_page = 24
    single_nfts, remembered_hearts, total_pages = load_all_single_nfts_search(items_per_page, current_page, query1, category1, ordered_by1)
    
    # Paginations
    pagination_start = current_page - 3
    if pagination_start < 0:
        pagination_start = 0

    pagination_end = current_page + 3
    if pagination_end > total_pages:
        pagination_end = total_pages
    session['search'] = [query, category, ordered_by]


    if not session.get('username'):
        return render_template('/gigatheme/1_search_explore.html', total_pages=total_pages,
                current_page=current_page, single_nfts=single_nfts, pagination_start=pagination_start,
                pagination_end=pagination_end, remembered_hearts=[], quote={"query": query, "category": category, "ordered_by":ordered_by})
    else:
        return render_template('/gigatheme/1_search_explore.html', total_pages=total_pages,
                current_page=current_page, single_nfts=single_nfts, pagination_start=pagination_start,
                pagination_end=pagination_end, username=session['username'], remembered_hearts=remembered_hearts,
                user_profile=session['user_profile'], quote={"query": query, "category": category, "ordered_by":ordered_by})


@app.route('/artists/', methods=['GET', 'POST'])
def artists():
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        # cursor.execute("SELECT DISTINCT user_profile.username, alias FROM user_profile INNER JOIN single_nfts ON user_profile.username = single_nfts.username WHERE deleted = ''")
        cursor.execute('''SELECT username, ROUND(SUM(price), 0) FROM single_nfts WHERE deleted = '' GROUP BY username HAVING ROUND(SUM(price)) ORDER BY username ASC''')
        results = cursor.fetchall()
    if not session.get('username'):
        return render_template('/gigatheme/1_artists.html', artists=results)
    return render_template('/gigatheme/1_artists.html', username=session['username'], user_profile=session['user_profile'], artists=results)

    

@app.route('/register', methods=['GET', 'POST'])
@cache.cached()
def register():
    return render_template('/gigatheme/1_register.html')


@csrf.include
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == "POST":
        username = request.form['username']
        while username[-1] == ' ':
            username = username[:-1]
        username = username.replace(' ', '_')
        email = request.form['email']
        checked = 'on'

        if email_checks(email):
            return render_template('/gigatheme/1_register.html', msg='Wrong email')
        if sanity_check(username):
            return render_template('/gigatheme/1_register.html', msg='Wrong username')

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM users WHERE username = %s''', (username,))
            username_result = cursor.fetchone()
            try:
                cursor.fetchall()
            except:
                pass
            cursor.execute('''SELECT * FROM users WHERE email = %s''', (email,))
            email_result = cursor.fetchone()
            try:
                cursor.fetchall()
            except:
                pass

            if username_result != None:
                return render_template('/gigatheme/1_register.html', msg='Username already exists')
            if email_result != None:
                return render_template('/gigatheme/1_register.html', msg='Email already exists')


            physical_address = ''
            # date_local  = strftime("%H:%M | %A, %d %b %Y", localtime())
            # g = geocoder.ip(f'{request.remote_addr}')
            # geolocator = Nominatim(user_agent="MpXY5Vz67y1M6LtG5nq5kMmc1dtv11nnGKyidmEN")
            # try:
            #     location = geolocator.reverse(f"{g.latlng[0]}, {g.latlng[1]}")
            #     physical_address = location.address
            # except:
            #     save_log_error('new user registration', 'location not fetched')
            #     physical_address = ''

            if 'on' in checked:
                cursor.execute('''INSERT INTO users (username, email, emailVerification, verified, creationDate, ip, location) VALUES (%s,%s,%s,%s,%s,%s,%s)''', (username, email, 0, 1, f'{datetime.datetime.now()}', f'{request.remote_addr}', physical_address))
                conn.commit()
            else:
                cursor.execute('''INSERT INTO users (username, email, emailVerification, verified, creationDate, ip, location) VALUES (%s,%s,%s,%s,%s,%s,%s)''', (username, email, 0, 0, f'{datetime.datetime.now()}', f'{request.remote_addr}', physical_address))
                conn.commit()

        session['username'] = username
        session['email']    = email
        user_profile = {
                "username": username,
                "profile_pic": '',
                "title": '',
                "alias": '',
                "banner": '',
                "website": '',
                "twitter": '',
                "discord_invite": '',
                "instagram": '',
                "description": '',
                "beneficiary_address": '',
                "floor": ''
                }
        session['user_profile'] = user_profile

        return redirect("send_email_validation")

    return render_template('/gigatheme/1_register.html', msg='You need a username and an email to get started')


#Validation number
otp = random.randint(000000,999999)
@app.route('/send_email_validation')
def send_email_validation():
    try:
        email = session['email']
        # response = requests.get("https://isitarealemail.com/api/email/validate",
        #  params = {'email': email})
        # print(response.text)
        # status = response.json()['status']
        # sanity
        # if status == "invalid":
        #     return render_template('/gigatheme/1_register.html', msg='Please enter a valid email')
        msg = Message('ADA Magic Marketplace. Verification code', sender='', recipients=[email])
        msg.body = f'Welcome to ADA Magic Marketplace.\n\n Your verification code is: {str(otp)}\n\n It is great to see you here, in case you do need something let us know via email () or Twitter @ada_magic_io\n Happy minting'
        mail.send(msg)
        return render_template('/gigatheme/1_email_verification.html')

    except Exception as e:
        session.clear()
        return render_template('/gigatheme/1_register.html', msg='We could not send an email to you. Please, try registering again with a different email account.')

@csrf.include
@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    session['verification'] = False
    if request.method == "POST":
        try:
            userOPT = request.form['verification_number']
            if int(otp) == int(userOPT):
                session['verification'] = True

                #email is verified, add to database and wait for new password
                return render_template('/gigatheme/1_password_type.html')
            else:
                return render_template('/gigatheme/1_register.html', msg='The verification number is not correct')
        except:
            return render_template('/gigatheme/1_register.html', msg='Something went wrong during the registration progress')
    else:
        return render_template('/gigatheme/1_success.html', msg='This is not the right way, try entering the verification number')


@app.route('/resend_otp')
def resend_otp():
    if session['verification'] == False:
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT emailVerification, email FROM users WHERE username = %s''', (session['username'],))
            results = cursor.fetchone()
        if results[0] == 0:
            msg = Message('ADA Magic Marketplace. Verification code', sender='', recipients=[results[1]])
            msg.body = f'Welcome to ADA Magic Marketplace.\n\n Your verification code is: {str(otp)}\n\n It is great to see you here, in case you do need something let us know via email () or Twitter @ada_magic_io\n Happy minting'
            mail.send(msg)

            return redirect("send_email_validation")

        else:
            return render_template('/gigatheme/1_success.html', msg='You are already registered')

    else:
        return render_template('/gigatheme/1_success.html', msg='You are already registered',
            username=session['username'], user_profile=session['user_profile'])

@csrf.include
@app.route('/new_user_password', methods=['GET', 'POST'])
def new_user_password():
    if session['verification'] == False:
        return redirect('send_email_validation')
    if request.method == "POST":

        #Get password, hash it and store it in the database
        password0 = request.form['password0']
        password1 = request.form['password1']
        if password0 != password1:
            return render_template('/gigatheme/1_password_type.html', msg='Passwords did not match, please try again',
                username=session['username'])
        password0 = password0.encode()
        hashed = bcrypt.hashpw(password0, bcrypt.gensalt(rounds=16))
        hashed = hashed.decode('utf-8')

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE users set password = %s, emailVerification = %s, address = "Placeholder", need_new_wallet = "1", inform_user = "0" WHERE username = %s''', (hashed, 1, session['username']))
            conn.commit()
            try:
                cursor.execute('''INSERT INTO password_recovery (email, is_valid, email_opt, time_now) VALUES (%s,%s,%s,%s)''', (session['email'], "False", "0", "0"))
                conn.commit()
            except:
                pass
            try:
                cursor.execute('''INSERT INTO user_profile (alias, username) VALUES (%s, %s)''', (session['username'], session['username']))
                conn.commit()
            except:
                pass

        session['wallet_address'] = 'Placeholder'
        session['user_profile'] = {
            "profile_pic": "",
            "alias": session['username'],
            "username": session['username'],
            "title": "",
            "description": ""
            }

        if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
            try:
                os.mkdir(f'C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\users\\{session["username"]}')
            except:
                pass
            shutil.copy('C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\users\\Untitled.png', f'C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\users\\{session["username"]}\\profile_picture.png')
        else:
            try:
                os.mkdir(f"/home//ada_magic/users/{session['username']}/")
            except:
                pass
            shutil.copy("/home//ada_magic/users/Untitled.png", f"/home//ada_magic/users/{session['username']}/profile_picture.png")

        return render_template('/gigatheme/1_edit_profile.html', username=session['username'],
            user_profile=session['user_profile'], updatable=True, msg='Congratulations! You created a new account. Please, fill in your profile before first')


    return redirect('send_email_validation')


@app.route('/inform_user', methods=['GET', 'POST'])
def inform_user():
    if not session.get('username'):
        return render_template('/gigatheme/1_login.html')

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT seedphrase, inform_user FROM users WHERE username = %s''', (session["username"],))
        results = cursor.fetchone()

    if results[1] == '2':
        my_password = b''
        seed = decrypt(my_password, results[0])

        seed = seed.decode()
        try:
            seed = seed.split(' ')
        except:
            pass
        return render_template('/gigatheme/1_verify_seed.html', seedphrase=seed,
            user_profile=session['user_profile'], username=session['username'])
    else:
        return redirect('giga_index')


@app.route('/verify_seed', methods=['GET', 'POST'])
def verify_seed():
    if not session.get('username'):
        return render_template('/gigatheme/1_login.html')

    if request.method == "POST":

        seed = request.form['hidden']

        if sanity_check(seed):
            return redirect('giga_login')

        while seed[-1] == ' ':
            seed = seed[:-1]

        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT seedphrase, inform_user, address FROM users WHERE username = %s''', (session["username"],))
            results = cursor.fetchone()

            my_password = b''
            decrypted = decrypt(my_password, results[0])
            decrypted = decrypted.decode()
            seed_array = decrypted
            decrypted1 = f'{decrypted}'

            if decrypted1 == seed:
                cursor.execute("UPDATE user set seedphrase = '', inform_user = '0' WHERE username = %s", (session['username'],))
                conn.commit()

                return render_template('/gigatheme/1_success.html', msg=f'You have successfully provided the seedphrase. Please, keep it in a safe place. You wallet address is: {results[2]}',
                    user_profile=session['user_profile'], username=session['username'])
            else:
                return render_template('/gigatheme/1_verify_seed.html', seed=seed_array, msg=f'Error, the seedphrase you provided does not match with the one we provided you with. Please, try again.',
                    user_profile=session['user_profile'], username=session['username'])

    else:
        return redirect('inform_user')


# This is the right about us   
@app.route('/about_us', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def about_us():
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM team''')
        team2 = cursor.fetchall()
        conn.commit()
    team = {}
    for member in team2:
        temp = {
            "name": member[0],
            "image": member[1],
            "title": member[8],
            "subtitle": member[9]
            } 
        links = {}
        if 'discord' in member[6]:
            links["discord"] = member[6]
        if 'twitter' in member[2]:
            links["twitter"] = member[2]
        if 'github' in member[3]:
            links["github"] = member[3]
        if 'website' in member[4]:
            links["website"] = member[4]
        if 'linkedin' in member[7]:
            links["linkedin"] = member[7]
        temp["links"] = links
        team[member[0]] = temp
    
    if not session.get('username'):
        return render_template('/gigatheme/1_about_us.html', team=team)

    return render_template("/gigatheme/1_about_us.html", username=session['username'],
        user_profile=session['user_profile'], team=team)


@app.route('/contact_us', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def contact_us():
    if not session.get('username'):
        return render_template('/gigatheme/1_contact_us.html')

    return render_template("/gigatheme/1_contact_us.html", username=session['username'],
        user_profile=session['user_profile'])



@app.route('/contact_us_query', methods=['GET', 'POST'])
def contact_us_query():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        query = request.form['message']
        topic = request.form['topic']
        
        if email_checks(email):
            return render_template('/gigatheme/1_contact_us.html', message='The email you provided is not correct. Please, try again')
            # Send email to oneself
        
        if sanity_check(name):
            return render_template('contact_us')
        
        msg = Message(f'Query from contact us: {name}', sender='', recipients=[''])
        msg.body = f'{query}\n\nTopic: {topic}\nFrom email: {email}'
        mail.send(msg)
        # Send email to user
        msg = Message(f'ADA Magic. Query recieved', sender='', recipients=[email])
        msg.body = f'Dear {name}, \n\n Thank you for your query, we received it and we will contact you as soon as we can.\n\nKind Regards,\nRoman\nADA Magic'
        mail.send(msg)
        return render_template('/gigatheme/1_contact_us.html', message='Message sent. Thank you! We will read the message as soon as possible and take action.')
    return render_template('/gigatheme/1_contact_us.html')


@app.route('/technology', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def technology():
    if not session.get('username'):
        return render_template('/gigatheme/1_technology.html')

    return render_template("/gigatheme/1_technology.html", username=session['username'],
        user_profile=session['user_profile'])
    return render_template('/gigatheme/1_technology.html')


@app.route('/roadmap', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def roadmap():
    if not session.get('username'):
        return render_template('/gigatheme/1_roadmap.html')

    return render_template("/gigatheme/1_roadmap.html", username=session['username'],
        user_profile=session['user_profile'])
    return render_template('/gigatheme/1_roadmap.html')


@app.route('/whitepaper', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def whitepaper():
    if not session.get('username'):
        return render_template('/gigatheme/1_whitepaper.html')

    return render_template("/gigatheme/1_whitepaper.html", username=session['username'],
        user_profile=session['user_profile'])
    return render_template('/gigatheme/1_whitepaper.html')


@app.route('/faq', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def faq():
    if not session.get('username'):
        return render_template('/gigatheme/1_faq.html')

    return render_template("/gigatheme/1_faq.html", username=session['username'],
        user_profile=session['user_profile'])


@app.route('/privacy_policy', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def privacy_policy():
    if not session.get('username'):
        return render_template('/gigatheme/1_privacy_policy.html')

    return render_template("/gigatheme/1_privacy_policy.html", username=session['username'],
        user_profile=session['user_profile'])

@app.route('/cookie_policy', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def cookie_policy():
    if not session.get('username'):
        return render_template('/gigatheme/1_cookie_policy.html')

    return render_template("/gigatheme/1_cookie_policy.html", username=session['username'],
        user_profile=session['user_profile'])


@app.route('/terms_and_conditions', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def terms_and_conditions():
    if not session.get('username'):
        return render_template('/gigatheme/1_terms_and_conditions.html')

    return render_template("/gigatheme/1_terms_and_conditions.html", username=session['username'],
        user_profile=session['user_profile'])


@app.route('/disclaimer', methods=['GET', 'POST'])
@cache.cached(timeout=80000)
def disclaimer():
    if not session.get('username'):
        return render_template('/gigatheme/1_disclaimer.html')

    return render_template("/gigatheme/1_disclaimer.html", username=session['username'],
        user_profile=session['user_profile'])


    try:
        return render_template('/gigatheme/1_faq.html', username=session['username'])
    except:
        return render_template('/gigatheme/1_faq.html')


@app.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    if request.method == "POST":
        try:
            
            email = request.form['address']
            if (('@' not in email) or ('.' not in email) or ("'" in email) or ('"' in email) or ('(' in email) or
                ('(' in email) or (',' in email) or ('=' in email) or ('+' in email) or (':' in email) or (';' in email) or
                ('/' in email) or ('*' in email) or (' from ' in email) or (' FROM ' in email)):
                return ''
            time_now = f'{datetime.datetime.now()}'

            try:
                db_conn_info = db_params('_NFT')
                with closing(mysql.connector.connect(**db_conn_info)) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''SELECT * FROM subscribers WHERE email = %s''', (email,))
                    result = cursor.fetchone()
                    conn.commit()
                    if result == None:
                        cursor.execute('''INSERT INTO subscribers (email, subscribed_date, is_subscribed) VALUES (%s,%s,%s)''',(email, time_now, "1"))
                        conn.commit()
                return redirect('/')
            except Exception as e:
                save_log_error(f'{e}', 'Error on newsletter')
                return 'error'

        except Exception as e:
            save_log_error(f'{e}', 'Error on newsletter Not info received')
            return 'error'
    return redirect('/')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session["name"] = None
    session['email'] = None
    session['verification'] = None
    session['wallet_address'] = None
    session['money'] = None
    session['ID'] = None
    session['username'] = None
    session.clear()

    return redirect("/")



@app.route('/store_hearts/<nft_internal_id>/<action>')
def store_hearts(nft_internal_id, action):
    try:
        nft_internal_id = int(nft_internal_id)
    except:
        return ''

    if action == 'plus':
        pass
    elif action == 'minus':
        pass
    else:
        return ''
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT hearts FROM single_nfts WHERE internal_id = %s''', (nft_internal_id,))
        hearts_results = cursor.fetchone()
        if hearts_results == None:
            return ''
        number_of_hearts = int(hearts_results[0])

        if not session.get('username'):
            if action == 'plus':
                cursor.execute('''INSERT INTO user_likes_nft (username, nft_liked, timestamped, action) VALUES (%s,%s,%s,%s)''',("Guest", nft_internal_id, str(time.time()), 'plus'))
                conn.commit()
                cursor.execute('''UPDATE single_nfts set hearts = %s WHERE internal_id = %s''', (number_of_hearts+1, nft_internal_id))
                conn.commit()
                return '7'
            elif action == 'minus':
                cursor.execute('''INSERT INTO user_likes_nft (username, nft_liked, timestamped, action) VALUES (%s,%s,%s,%s)''',("Guest", nft_internal_id, str(time.time()), 'minus'))
                conn.commit()
                cursor.execute('''UPDATE single_nfts set hearts = %s WHERE internal_id = %s''', (number_of_hearts+1, nft_internal_id))
                conn.commit()
                return '8'
            else:
                return ''

        else:
            cursor.execute('''SELECT * FROM user_likes_nft WHERE username = %s AND nft_liked = %s''', (session['username'], nft_internal_id))
            results = cursor.fetchone()
            if ((results == None) and (action == 'minus')):
                return '3'
            elif ((results != None) and (action == 'plus')):
                return '4'

            elif ((results != None) and (action == 'minus')):
                cursor.execute('''DELETE FROM user_likes_nft WHERE internal_id = %s''', (results[1],))
                conn.commit()
                cursor.execute('''UPDATE single_nfts set hearts = %s WHERE internal_id = %s''', (number_of_hearts-1, nft_internal_id))
                conn.commit()
                return '9'
            elif ((results == None) and (action == 'plus')):
                cursor.execute('''INSERT INTO user_likes_nft (username, nft_liked) VALUES (%s,%s)''',(session['username'], nft_internal_id))
                conn.commit()
                cursor.execute('''UPDATE single_nfts set hearts = %s WHERE internal_id = %s''', (number_of_hearts+1, nft_internal_id))
                conn.commit()
                return '10'
            else:
                return '5'
        
        
    return '6'


@app.route('/user_can_request_money/<password>/<username>', methods=['GET', 'POST'])
def user_can_request_money(password, username):
    if password != '':
        return ''
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE users SET can_request = '1' WHERE username = %s''', (username,))
        conn.commit()
    return ''


# There was an error from the local server storing the image, halt until user resends picture
@app.route('/halt_sync/<password>/<internal_id>/<username>')
def halt_sync(password, internal_id, username):
    if password != '':
        return 'ok'
    
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE single_nfts SET policy_id = 'synchronizing*' WHERE internal_id = %s''', (internal_id,))
        conn.commit()
        # cursor.execute('''SELECT email FROM users WHERE username=%s''', (username))
        # email = cursor.fetchone()
        # email = email[0]
    return 'username done'
    

    






# @app.route('/route2')
# def route2():
#     latest, single_nfts, vending_machine, issold, remembered_hearts, profile_pictures, top_sellers_array = load_all_single_nfts_index2()

#     if not session.get('username'):
#         return render_template('/gigatheme/1_index2.html', single_nfts=single_nfts, vending_machine=vending_machine,
#             latest=latest, top_sellers=top_sellers_array, remembered_hearts='', profile_pictures=profile_pictures)
#     else:
#         return render_template('/gigatheme/1_index2.html', single_nfts=single_nfts, vending_machine=vending_machine,
#             latest=latest, username=session['username'], top_sellers=top_sellers_array, remembered_hearts=remembered_hearts,
#             profile_pictures=profile_pictures, user_profile=session['user_profile'])










@app.route('/q1')
def q1():
    return render_template('/gigatheme/1_success.html', msg=f'')


@app.route('/change_fees/<password>')
def change_fees(password):
    if password != '':
        return ''
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT internal_id FROM single_nfts''')
        ids = cursor.fetchall()
        ids = ids[-50:]
        new = {}
        for elem in ids:
            cursor.execute('''SELECT internal_id, username, nft_name, artist, deposit_wallet, beneficiary_wallet, description, policy_id, price, metadata, royalty_percentage, royalty_wallet, minted_so_far, featured, issold, code, deleted, policy_name, original_nft_name, using_old_policy, policy_duration, NFTID, selling_fees, hearts, views FROM single_nfts WHERE internal_id = %s''', (elem[0],))
            elem = cursor.fetchone()
            new[elem[0]] = {
                "internal_id": elem[0], 
                "username": elem[1], 
                "nft_name": elem[2], 
                "artist": elem[3], 
                "deposit_wallet": elem[4], 
                "beneficiary_wallet": elem[5], 
                "description": elem[6], 
                "policy_id": elem[7], 
                "price": elem[8], 
                "metadata": elem[9], 
                "royalty_percentage": elem[10], 
                "royalty_wallet": elem[11], 
                "minted_so_far": elem[12], 
                "featured": elem[13], 
                "issold": elem[14], 
                "code": elem[15], 
                "deleted": elem[16], 
                "policy_name": elem[17], 
                "original_nft_name": elem[18], 
                "using_old_policy": elem[19], 
                "policy_duration": elem[20], 
                "NFTID": elem[21], 
                "selling_fees": elem[22], 
                "hearts": elem[23], 
                "views": elem[24]
                }
            selling_fees = int(int(elem[8])/ 100) + 2
            cursor.execute("UPDATE single_nfts set selling_fees = %s WHERE internal_id = %s", (f'{selling_fees}', elem[0]))
            conn.commit()
    return jsonify(new)


@app.route('/q5', methods=['GET', 'POST'])
def q5():
    try:
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT internal_id FROM single_nfts")
            single_nfts = cursor.fetchall()
            for internal_id in single_nfts:
                internal_id = internal_id[0]
                cursor.execute("UPDATE single_nfts set nft_image='', nft_image_thumbnail='', qr_code='', blob_full='', blob_thum='', blob_main='', full_size_image='' WHERE internal_id=%s", (internal_id,))
                conn.commit()
    except Exception as e:
        return f'Error from website: {e}'

    return f'ok, deleted'


@app.route('/verified_status', methods=['GET', 'POST'])
def verified_status():
    try:
        db_conn_info = db_params('_NFT')
        with closing(mysql.connector.connect(**db_conn_info)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, verified_status FROM users")
            statuses = cursor.fetchall()
            for status in statuses:
                username = status[0]
                verified_status = status[1]
                cursor.execute("UPDATE single_nfts set verified_status = %s WHERE username=%s", (verified_status, username))
                conn.commit()
    except Exception as e:
        return f'Error from website: {e}'

    return f'ok, deleted'


@app.route('/check_stats/<password>')
def check_stats(password):
    if password != '123':
        return 'ok'
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ip, username, location FROM single_nfts WHERE ip != '' ORDER BY ip")
        results = cursor.fetchall()
    html_results = '<ol>'
    for elem in results:
        html_results = f'{html_results} <li>{elem}</li>'
    html_results = html_results + '</ol>'
    return html_results 


# Reroute weird old routes:
@app.route('/mint_giga')
def mint_giga():
    return redirect('mint')


# @app.route('/q4', methods=['GET', 'POST'])
# def q4():
#     data = flask.request.json
#     try:
#         db_conn_info = db_params('_NFT')
#         with closing(mysql.connector.connect(**db_conn_info)) as conn:
#             cursor = conn.cursor()
            # cursor.execute('''INSERT INTO single_nfts (internal_id,username,nft_name,artist,deposit_wallet,beneficiary_wallet,nft_image,nft_image_thumbnail,description,policy_id,price,qr_code,metadata,royalty_percentage,royalty_wallet,minted_so_far,featured,issold,code,deleted,policy_name,original_nft_name,full_size_image,using_old_policy,policy_duration,NFTID,selling_fees,hearts,views,blob_full,blob_thum,blob_main,category,hashtags,ip,location,creation_time,metadata_fields,file_type)
            # VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            # (data['internal_id'],data['username'],data['nft_name'],data['artist'],data['deposit_wallet'],data['beneficiary_wallet'],data['nft_image'],data['nft_image_thumbnail'],data['description'],data['policy_id'],data['price'],data['qr_code'],data['metadata'],data['royalty_percentage'],data['royalty_wallet'],data['minted_so_far'],data['featured'],data['issold'],data['code'],data['deleted'],data['policy_name'],data['original_nft_name'],data['full_size_image'],data['using_old_policy'],data['policy_duration'],data['NFTID'],data['selling_fees'],data['hearts'],data['views'],data['blob_full'],data['blob_thum'],data['blob_main'],data['category'],data['hashtags'],data['ip'],data['location'],data['creation_time'],data['metadata_fields'],data['file_type']))
            # conn.commit()
    # except Exception as e:
    #     save_log_error(f'{e}', '')
    #     return f'{e}'
    # return 'ok'
@app.route('/same_ips/<password>', methods=['GET', 'POST'])
def q4(password):
    if password != 'asafdu23@4mndfs,.FG265?!':
        return 'ok'
    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, ip, location FROM session_log WHERE ip != ''")
        results = cursor.fetchall()
    ips_json = {}
    try:
        for elem in results:
            try:
                if [elem[0], elem[1]] not in ips_json[elem[1]]:
                    temp = ips_json[elem[1]]
                    temp.append([elem[0], elem[1]])
                    ips_json[elem[1]] = temp
            except:
                ips_json[elem[1]] = [[elem[0], elem[1]]]
    except Exception as e:
        return f'{e}'
    
    # return f'{results}'
    return jsonify(ips_json)




@app.route('/single_nft_delete_emergency/<password>/<internal_id>', methods=['GET', 'POST'])
def single_nft_delete_emergency(password, internal_id):
    if password != '':
        return 'nop'

    db_conn_info = db_params('_NFT')
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE single_nfts set deleted = '1' WHERE internal_id = %s", (internal_id,))
        conn.commit()

    try:
        if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
            shutil.rmtree(f"C:\\Users\\\\Desktop\\proyects\\ada_magic\\website\\single_nfts\\{internal_id}")
        else:
            shutil.rmtree(f"/home//ada_magic/single_nfts/{internal_id}/")
    except:
        pass
    return f'done{internal_id}'



if ':\\Users\\\\Desktop\\proyects\\ada_magic\\website' in os.path.dirname(os.path.abspath(__file__)):
    app.run(host="localhost", port=8080, debug=True)
else:
    if __name__ == "__main__":
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080, threaded=True)


