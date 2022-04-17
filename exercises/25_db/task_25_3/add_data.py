import glob
import os
import sqlite3
import re
import yaml
from tabulate import tabulate

sw_filename = 'switches.yml'
db_filename = 'dhcp_snooping.db'
regex = re.compile(r'(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

def search_data(data_f):
    with open(data_f) as data:
        result = []
        data_switch = re.search(r"(\w+)_dhcp_snooping.txt", data_f).group(1)
        for line in data:
            match = regex.search(line)
            if match:
                result.append(match.groups() + (data_switch,))

    return result

def conn_execute(connection, query, row):
    try:
        with connection:
            connection.execute(query, row)
    except sqlite3.IntegrityError as e:
        print("При добавлении данных: {} Возникла ошибка:".format(row), e)


def add_switch(base, data):
    print('Добавляю данные в таблицу switches...')
    conn = sqlite3.connect(base)
    with open(data) as f:
        templates = yaml.safe_load(f)
        slovar2 = templates[list(templates.keys())[0]]
        query = "insert into switches (hostname, location) values (?, ?)"
        for sw in slovar2:
            location = slovar2[sw]
            row = (sw, location) 
            conn_execute(conn, query, row)

    conn.close()

def add_dhcp(base, data):
    conn = sqlite3.connect(base)
    print('Добавляю данные в таблицу dhcp ...')
    query = "replace into dhcp values (?, ?, ?, ?, ?, ?)"
#    query = "insert into dhcp (mac, ip, vlan, interface, switch, active) values (?, ?, ?, ?, ?, ?)"
    conn.execute("update dhcp set active = 0")
    for file_name in data:
        result_data = search_data(file_name)
        for row in result_data:
            conn_execute(conn, query, row + (1,))

    conn.close()


db_exists = os.path.exists(db_filename)
#dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
dhcp_snoop_files = glob.glob("new_data/sw*_dhcp_snooping.txt")

if not db_exists:
    print('База данных не существует. Перед добавлением данных, ее надо создать...')
else:
    print('Database exists, assume dhcp and switches table does, too.')
    add_dhcp(db_filename, dhcp_snoop_files)
    add_switch(db_filename, sw_filename)
