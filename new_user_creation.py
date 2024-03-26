from flask import *
from flask import Flask, request, send_from_directory, session
from flask_session import Session
import json
import hashlib
import os
import sys
from PIL import Image
import io
import paramiko
import time
import mysql.connector
import random
from flask_mail import *
import bcrypt
from os.path import exists
from PIL import Image
import requests
from time import strftime,localtime
import datetime
import qrcode



@app.route('/newUserForm', methods=['GET', 'POST'])
def newUserForm():
    return render_template('/NFT/createNewUser.html')

@app.route('/newUserCreation', methods=['GET', 'POST'])
def newUserCreation():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        conn = mysql.connector.connect(
                        host='localhost', 
                        user='nicehqrq', 
                        password='BvhR8i1redKd', 
                        database='nicehqrq_NFT')

        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE username = %s''', (username,))
        results = False
        results = cursor.fetchone()

        # Flush buffer
        try:
            cursor.fetchall()
        except:
            pass

        if results != None:
            return render_template('NFT/createNewUser.html', username='Username already exists')

        cursor.execute('''SELECT * FROM users WHERE email = %s''', (email,))
        results = cursor.fetchone()

        # Flush buffer
        try:
            cursor.fetchall()
        except:
            pass

        if results != None:
            return render_template('NFT/createNewUser.html', email='Email already exists')
        cursor.execute('''INSERT INTO users (username, email, emailVerification) VALUES (%s,%s,%s)''', (username, email, 0))
        conn.commit()
        conn.close()
        session['username'] = username
        session['email']    = email
        
        return redirect("verifyEmailAddress")

    return render_template('/NFT/createNewUser.html')

#Validation number
otp = random.randint(000000,999999)
@app.route('/verifyEmailAddress', methods=['GET', 'POST'])
def verifyEmailAddress():
    email = session['email']

    response = requests.get("https://isitarealemail.com/api/email/validate",
     params = {'email': email})
    status = response.json()['status']
    if status == "invalid":
        return render_template('/NFT/createNewUser.html', email='Please enter a valid email')

    msg = Message('ADA Magic Marketplace. Verification code', sender='info@adamagic.io', recipients=[email])
    msg.body = str(otp)  
    mail.send(msg)
    
    return render_template('/NFT/verification.html')

@app.route('/verified', methods=['GET', 'POST'])
def verified():
    session['verification'] = False
    if request.method == "POST":
        userOPT = request.form['verificationNumber']
        try:
            if int(otp) == int(userOPT):
                session['verification'] = True

                #email is verified, add to database and wait for new password
                return render_template('/NFT/newPassword.html')
        except:
            return render_template('/NFT/success.html', email='UNSUCCESSFUL')
    else:
        return render_template('/NFT/success.html', email='UNSUCCESSFUL')


@app.route('/enterNewPassword', methods=['GET', 'POST'])
def enterNewPassword():
    if session['verification'] == False:
        return redirect('verifyEmailAddress')
    if request.method == "POST":

        #Get password, hash it and store it in the database
        password0 = request.form['password0']
        password1 = request.form['password1']
        if password0 != password1:
            return render_template('NFT/newPassword.html', result='Passwords did not match, please try again')
        password0 = password0.encode()
        hashed = bcrypt.hashpw(password0, bcrypt.gensalt(rounds=16))
        hashed = hashed.decode('utf-8')
        conn = mysql.connector.connect(host='localhost', 
                        user='nicehqrq', 
                        password='BvhR8i1redKd',
                        database='nicehqrq_NFT')
        cursor = conn.cursor()
        cursor.execute('''UPDATE users set password = %s, emailVerification = %s WHERE username = %s''', (hashed, 1, session['username']))
        conn.commit()
        cursor.execute('''INSERT INTO password_recovery (email, is_valid, email_opt, time_now) VALUES (%s,%s,%s,%s)''', (session['email'], "False", "0", "0"))
        conn.commit()
        conn.close()

        user = session['username']
        home_path = '/home/yop/Downloads/cardano-node1.30.0/'
        commands = [
                    'export CARDANO_NODE_SOCKET_PATH=/home/yop/Downloads/cardano/db1.33.0/node.socket',
                    f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/createFolder.py {user}',
                    f'{home_path}cardano-wallet recovery-phrase generate > {home_path}keys/{user}/{user}SeedPhrase.txt',
                    f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/readSeed.py {user}'
                    ]
        try:
            outdata, errdata = connect_paramiko(commands)
        except:
            save_log_error('Could not connect to SSH', session['username'])
            return render_template('/NFT/verification.html', error='We are experiencing delays from the server. Please, try again later')
        try:
            seed = outdata.split('keyword555')[1]
            if seed[-1:] == ' ':
                seed = seed[:-1]
        except:
            save_log_error('Seed could not be loaded',[session['username'], outdata])
            seed = 'Seed will be sent by email'

        return render_template('/NFT/repeatSeed.html', seed=seed)

    return render_template('/NFT/createNewUser.html')


@app.route('/checkSeed', methods=['GET', 'POST'])
def checkSeed():
    if not session.get('username'): return redirect('login')
    if request.method == "POST":
        userSeedInput   = request.form['seed']

        # There is an error and a space at the end of the seedphrase is been sent. Correct that
        if userSeedInput[-1:] == ' ':
            userSeedInput = userSeedInput[:-1]
        userSeedInput = userSeedInput.replace('\n', '')
        userSeedInput = userSeedInput.split(' ')
        user = session['username']
        home_path = '/home/yop/Downloads/cardano-node1.30.0/'
        commands = [
                    f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/readSeed.py {user}'
                    ]
        try:
            outdata, errdata = connect_paramiko(commands)
        except:
            return render_template('/NFT/verification.html', error='We are experiencing delays from the server. Please, try again later')

        try:
            seed = outdata.split('keyword555')
            seed = seed[1]
            seed = seed.replace('keyword555', '')
            seed = seed.replace('\n', '')
            if seed[-1:] == ' ':
                seed = seed[:-1]
            seed = seed.split(' ')

        except:
            save_log_error('Error parsing seed to check with users input', [session['username'], outdata, ['user input:', userSeedInput]])
            seed = 'Seed will be sent by email'

        flag = True
        try:
            for x, word in enumerate(seed):
                if seed[x] != userSeedInput[x]:
                    flag = False
        except:
            return render_template('/NFT/repeatSeed.html', seed=seed)
        if flag:
            address = ''
            try:
                #The user has the seed phrase, create wallet and delete the seed
                home_path = '/home/yop/Downloads/cardano-node1.30.0/'
                commands = [
                        f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/2createNewWallet.py {user}',
                        f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/3deleteSeed.py {user}',
                        f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/4readAddress.py {user}'
                        ]

                try:
                    outdata, errdata = connect_paramiko(commands)
                except:
                    return render_template('/NFT/seedPhrase.html', address='See address once logged in', username=session['username'])

                address = outdata.split('keyword555')
                address = address[1]

            except:
                save_log_error('error creating address', [outdata, address])
                date_local  = strftime("%A, %d %b %Y", localtime())
                conn        = mysql.connector.connect(host='localhost', 
                            user='nicehqrq', 
                            password='BvhR8i1redKd', 
                            database='nicehqrq_NFT')
                cursor      = conn.cursor()
                cursor.execute("UPDATE users set creationDate = %s WHERE username = %s", (date_local, session['username']))
                conn.commit()
                conn.close()
                return render_template('/NFT/seedPhrase.html', address='See address once logged in', username=session['username'])


            date_local  = strftime("%A, %d %b %Y", localtime())
            conn        = mysql.connector.connect(host='localhost', 
                        user='nicehqrq', 
                        password='BvhR8i1redKd', 
                        database='nicehqrq_NFT')
            cursor      = conn.cursor()

            cursor.execute("UPDATE users set address = %s, creationDate = %s WHERE username = %s", (address, date_local, session['username']))
            conn.commit()
            conn.close()

            return render_template('/NFT/seedPhrase.html', address=address, username=session['username'])
        else:
            return render_template('/NFT/repeatSeed.html', seed=seed)
    return render_template('/NFT/login.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template("/NFT/password_recovery.html")


@app.route('/forgot_recovery', methods=['GET', 'POST'])
def forgot_recovery():
    if request.method == "POST":
        email_opt = random.randint(000000, 999999)
        email = request.form['email']
        conn = mysql.connector.connect(host='localhost', 
            user='nicehqrq', 
            password='BvhR8i1redKd', 
            database='nicehqrq_NFT')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE email = %s''', (email,))
        results = cursor.fetchone()
        email = results[2]
        username = results[0]
        # Flush buffer
        try:
            cursor.fetchall()
        except:
            pass

        
        

        if results != None:  # The email is actually in the database
            cursor.execute('''UPDATE password_recovery set is_valid = %s, email_opt = %s, time_now = %s WHERE email = %s''', ("True", str(email_opt), str(int(time.time())), email))
            conn.commit()
            conn.close()
            composed = email + str(email_opt)
            composed = bytes(composed, 'utf-8')
            sha_obj = hashlib.sha256()
            sha_obj.update(composed)
            hexadecimal = sha_obj.hexdigest()
            link = f'http://adamagic.io/new_password_recover/{username}/{hexadecimal}'

            msg = Message('ADA Magic Marketplace. Password recovery', sender='info@adamagic.io', recipients=[email])
            msg.body = f"""
                This email is sent to you because you requested a password recovery. If is wasn't you, please ignore this email.\n\n
                Click on this link to create a new password.\n
                Please, verify that the link redirects to the original website: https://adamagic.io\n
                {link}
                """
            mail.send(msg)

            return render_template("/NFT/password_recovery.html", message='An email was sent for you to create a new password')
        else:
            conn.close()
            return render_template("/NFT/password_recovery.html")


    return render_template("/NFT/password_recovery.html")


        

@app.route('/new_password_recover/<username>/<composed>', methods=['GET', 'POST'])
def new_password_recover(username, composed):
    conn = mysql.connector.connect(host='localhost', 
            user='nicehqrq', 
            password='BvhR8i1redKd', 
            database='nicehqrq_NFT')
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT * FROM users WHERE username = %s''', (username,))
        results0 = cursor.fetchone()
        email = results0[2]
        username = results0[0]
        # Flush buffer
        try:
            cursor.fetchall()
        except:
            pass
    except:
        conn.close()
        return render_template("/NFT/password_recovery.html")
    cursor.execute('''SELECT * FROM password_recovery WHERE email = %s''', (email,))
    results1 = cursor.fetchone()
    email = results1[0]
    email_opt = results1[1]
    is_valid = results1[2]
    old_time = int(results1[3])

    if is_valid == "False":
        cursor.execute('''UPDATE password_recovery set is_valid = %s, email_opt = %s, time_now = %s WHERE email = %s''', ("False", "0", "0", email))
        conn.commit()
        conn.close()
        return render_template("/NFT/password_recovery.html", message='Time expired. Please, try again')

    time_now = int(time.time())
    if time_now - old_time > 900:
        cursor.execute('''UPDATE password_recovery set is_valid = %s, email_opt = %s, time_now = %s WHERE email = %s''', ("False", "0", "0", email))
        conn.commit()
        conn.close()
        return render_template("/NFT/password_recovery.html", message='Time expired. Please, try again')

    composed_check = email + str(email_opt)
    composed_check = bytes(composed_check, 'utf-8')
    sha_obj = hashlib.sha256()
    sha_obj.update(composed_check)
    hexadecimal = sha_obj.hexdigest()

    if hexadecimal == composed:
        session['username'] = username
        conn.close()
        return render_template("/NFT/type_new_password.html", hexadecimal=hexadecimal)
    conn.close()
    return render_template("/NFT/password_recovery.html")


@app.route('/new_password_recover_continue/', methods=['GET', 'POST'])
def new_password_recover_continue():
    if not session.get('username'):
        return render_template('/NFT/login.html')
    try:
        if request.method == "POST":
            password0 = request.form['password0']
            password1 = request.form['password1']
            hexadecimal = request.form['hexadecimal']
            if password0 != password1:
                return render_template("/NFT/type_new_password.html", hexadecimal=hexadecimal, message='Passwords are not the same')
            username = session['username']
            conn = mysql.connector.connect(host='localhost', 
                user='nicehqrq', 
                password='BvhR8i1redKd', 
                database='nicehqrq_NFT')
            cursor = conn.cursor()
            try:
                cursor.execute('''SELECT * FROM users WHERE username = %s''', (username,))
                results = cursor.fetchone()
                email = results[2]
                username = results[0]
                
                # Flush buffer
                try:
                    cursor.fetchall()
                except:
                    pass
            except:
                conn.close()
                return render_template("/NFT/type_new_password.html")

            cursor.execute('''SELECT * FROM password_recovery WHERE email = %s''', (email,))
            results = cursor.fetchone()
            composed_check = email + str(results[1])
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
                conn.close()
                return render_template("/NFT/success.html", success='You have successfully changed your password')
            return render_template('/NFT/login.html')
    except Exception as e:
        return render_template("/NFT/password_recovery.html")