import os
import sqlite3
import re
import yaml

sw_filename = 'switches.yml'
data_filename = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
db_filename = 'dhcp_snooping.db'
regex = re.compile(r'(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

def search_data(data_f):
    with open(data_f) as data:
        result = []
        data_switch = data_f.split('_')[0]
        for line in data:
            match = regex.search(line)
            if match:
#                sum_match = list(match.groups())
#                sum_match.append(data_switch)
#                result.append(tuple(sum_match))
                result.append(match.groups() + (data_switch,))

    return result

def add_switch(base, data):
    print('Добавляю данные в таблицу switches...')
    conn = sqlite3.connect(base)
    with open(data) as f:
        templates = yaml.safe_load(f)
#        list_keys = list(templates.keys())
        slovar2 = templates[list(templates.keys())[0]]
        for sw in slovar2:
            city, street = slovar2[sw].split(',')
            row = (sw, city, street.strip()) 

            try:
                with conn:
                    query = "insert into switches (switch, city, street) values (?, ?, ?)"
                    conn.execute(query, row)
            except sqlite3.IntegrityError as e:
                print("При добавлении данных: {} Возникла ошибка:".format(row), e)

    conn.close()

def add_dhcp(base, data):
    conn = sqlite3.connect(base)
    print('Добавляю данные в таблицу dhcp ...')
    for file_name in data:
        result_data = search_data(file_name)

        for row in result_data:
            try:
                with conn:
                    query = '''insert into dhcp (mac, ip, vlan, interface, switch) values (?, ?, ?, ?, ?)'''
                    conn.execute(query, row)
            except sqlite3.IntegrityError as e:
                print("При добавлении данных: {} Возникла ошибка:".format(row), e)

    conn.close()

db_exists = os.path.exists(db_filename)
if not db_exists:
    print('База данных не существует. Перед добавлением данных, ее надо создать...')
else:
    print('Database exists, assume dhcp and switches table does, too.')
    add_dhcp(db_filename, data_filename)
    add_switch(db_filename, sw_filename)
