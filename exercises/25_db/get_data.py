import sys
import sqlite3

db_filename = 'dhcp_snooping.db'

def number_arg(*args):
    len_args = len(args)
    return len_args

def print_data(res):
    print('-' * 40)
    for row in res:
        print('{:12} {:16} {:3} {:12} {:4}'.format(row[0], row[1], row[2], row[3], row[4],))
    print('-' * 40)

def get_all_data(db_name):
    print('В таблице dhcp такие записи:')
    query = 'select * from dhcp'
    conn = sqlite3.connect(db_name)
    result = conn.execute(query)
    print_data(result)

def get_from_dhcp(db_name):
    key, value = sys.argv[1:]
    keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
    if key in keys:
        print('Информация об устройствах с такими параметрами:', key, value)
        query = 'select * from dhcp where {} = ?'.format(key)
        conn = sqlite3.connect(db_name)
        result = conn.execute(query, (value, ))
        print_data(result)
    else:
        print('Данный параметр не поддерживается.')
        print("допустимые значения параметров: {}".format(", ".join(keys)))


len_input = number_arg(*sys.argv[1:])

if len_input == 0:
    get_all_data(db_filename)
elif len_input == 2:
    get_from_dhcp(db_filename)
else:
    print('Пожалуйста, введите два или ноль аргументов')


