import os
import sqlite3
import re

data_filename = 'dhcp_snooping.txt'
db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'

regex = re.compile(r'(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
result = []

def create_database(name_db, name_schema):
    db_exists = os.path.exists(name_db)
    conn = sqlite3.connect(name_db)
   
    if not db_exists:
        print('Создаю базу данных..._')
        with open(name_schema, 'r') as f:
            schema = f.read()
            conn.executescript(schema)
    else:
        print('База данных существует.')
    conn.close()

create_database(db_filename, schema_filename)


