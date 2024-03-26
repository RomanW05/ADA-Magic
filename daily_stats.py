import requests
from datetime import datetime
import mysql.connector
from contextlib import closing
import subprocess
import csv

def get_data(month):
    month = '072022'

    password = 'sdanjpoi56,.@!fewsadfjyOdfnm2XGDA,.agm@$TGssdvcxf'
    url = f'https://www.adamagic.io/awstats/{password}/{month}'

    myfile = requests.get(url)

    open('C:/Users/yop/Desktop/proyects/ada_magic/website/stats/today_stats.txt', 'wb').write(myfile.content)

    # seed = "C:/Users/yop/Downloads/php-8.1.8-nts-Win32-vs16-x64/php.exe C:/Users/yop/Downloads/awstats_extractor-master/awstats_extractor-master/cli.php C:/Users/yop/Desktop/proyects/ada_magic/website/stats/today_stats.txt C:/Users/yop/Desktop/proyects/ada_magic/website/stats/today_stats.csv"
    # results = subprocess.call(seed, shell=True)
    # print(results)


    # with open('C:/Users/yop/Desktop/proyects/ada_magic/website/stats/today_stats.csv') as text:
    #     csv_file = []
    #     csvr = csv.reader(text)
    #     for line in csvr:
    #         csv_file.append(line)
    
    # return csv_file
    lines = []
    with open('C:/Users/yop/Desktop/proyects/ada_magic/website/stats/today_stats.txt') as text:
        text = text.readlines()
        for line in text:
            lines.append(line)
    
    return lines


def store_data(data):
    db_conn_info = {
            "user": "1234",
            "password": "1234",
            "host": "localhost",
            "database": f"stats"
            }
    with closing(mysql.connector.connect(**db_conn_info)) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT internal_id FROM daily''')
        ids = cursor.fetchall()


def todays_date():
    currentMonth = str(datetime.now().month)
    if len(currentMonth) == 1:
        currentMonth = '0' + currentMonth
    currentYear = str(datetime.now().year)
    print(currentMonth, currentYear)

    month = currentYear + currentMonth
    return month


def structure_data(data):
    episodes = []
    start = 0
    for x, row in enumerate(data):
        if len(row) == 1:  # New episode
            episodes.append(data[start:x])
            start = x
    episodes.append(data[start:])

    return episodes


def analyze(data):
    # chapter 0: 
    # chapter 1: 
    # chapter 2: General, unique visitors, total visits
    # chapter 3: 
    # chapter 4: 
    # chapter 5: 
    # chapter 6: 
    # chapter 7: 
    # chapter 8: 
    # chapter 9: 
    # chapter 10: 
    # chapter 11: 
    # chapter 12: 
    # chapter 13: 
    # chapter 14: 
    # chapter 15: 
    # chapter 16: 
    # chapter 17: 
    # chapter 18: 
    # chapter 19: 
    # chapter 20: 
    # chapter 21: 
    # chapter 22: 
    # chapter 23: 
    # chapter 24: 
    # chapter 25: 
    # chapter 26: 
    # chapter 27: 
    # chapter 28: 
    # chapter 29: 
    for x, chapter in enumerate(data):
        if x == 2:
            total_views = chapter[14][12:]
            unique_views = chapter[15][12:]
            print(total_views, unique_views)







def main():
    data = []
    with open('C:/Users/yop/Desktop/proyects/ada_magic/website/stats/today_stats.txt') as text:
        text = text.readlines()
        for line in text:
            line = line.replace('  ', '')
            data.append(line)
    
    # month = todays_date()
    # data = get_data(data)
    data = structure_data(data)
    analyze(data)


    
    # print(data[1])

    # Data



main()