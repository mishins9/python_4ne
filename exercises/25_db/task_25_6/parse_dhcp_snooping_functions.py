import os
import sqlite3
import re
import yaml
from tabulate import tabulate
from datetime import timedelta, datetime

def search_data(data_f):
    regex = re.compile(r'(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

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

def create_db(name_db, name_schema):
    db_exists = os.path.exists(name_db)
    conn = sqlite3.connect(name_db)
   
    if not db_exists:
        with open(name_schema, 'r') as f:
            schema = f.read()
            conn.executescript(schema)
    else:
        print('База данных существует.')
    conn.close()


def add_data_switches(base, data):
    db_exists = os.path.exists(base)
    if not db_exists:
        print('База данных не существует. Перед добавлением данных, ее надо создать...')
        return

    conn = sqlite3.connect(base)
    for item in data:
        print('Добавляю данные from {} в таблицу switches...'.format(item))
        with open(item) as f:
            templates = yaml.safe_load(f)
            slovar2 = templates[list(templates.keys())[0]]
            query = "insert into switches (hostname, location) values (?, ?)"
            for sw in slovar2:
                location = slovar2[sw]
                row = (sw, location) 
                conn_execute(conn, query, row)
    conn.close()

def remove_old_records(conn):
    now = datetime.today().replace(microsecond=0)
    week_ago = str(now - timedelta(days=7))
    query = "delete from dhcp where last_active < ?"
    conn.execute(query, (week_ago,))
    conn.commit()


def add_data(base, data):
    db_exists = os.path.exists(base)
    if not db_exists:
        print('База данных не существует. Перед добавлением данных, ее надо создать...')
        return

    conn = sqlite3.connect(base)
    remove_old_records(conn)
    query = "replace into dhcp values (?, ?, ?, ?, ?, ?, datetime('now'))"
    conn.execute("update dhcp set active = 0")
    for file_name in data:
        result_data = search_data(file_name)
        for row in result_data:
            conn_execute(conn, query, row + (1,))

    conn.close()

def print_activ(data, active=True):
    data = list(data)
    if data:
        print(
        "\n{active} записи:\n".format(active="Активные" if active else "Неактивные")
        )
        print(tabulate(data))


def get_all_data(db_name):
    query = 'select * from dhcp where active = ?'
    conn = sqlite3.connect(db_name)
    for active in (1, 0):
        result = conn.execute(query, (active,))
        print_activ(result, active)
    conn.close()

def get_data(db_name, key, value):
    query = 'select * from dhcp where {} = ? and active = ?'.format(key)
    conn = sqlite3.connect(db_name)
    for active in (1, 0):
        result = conn.execute(query, (value, active))
        print_activ(result, active)
    conn.close()

