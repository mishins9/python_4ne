import sys
import sqlite3
from tabulate import tabulate

db_filename = 'dhcp_snooping.db'

def print_activ(data, active=True):
    data = list(data)
    if data:
        print(
        "\n{active} записи:\n".format(active="Активные" if active else "Неактивные")
        )
        print(tabulate(data))


def number_arg(*args):
    len_args = len(args)
    return len_args

def get_all_data(db_name):
    print('В таблице dhcp такие записи:')
    query = 'select * from dhcp where active = ?'
    conn = sqlite3.connect(db_name)
    for active in (1, 0):
        result = conn.execute(query, (active,))
        print_activ(result, active)
    conn.close()

def get_from_dhcp(db_name):
    key, value = sys.argv[1:]
    keys = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active']
    if key in keys:
        print('Информация об устройствах с такими параметрами:', key, value)
        query = 'select * from dhcp where {} = ? and active = ?'.format(key)
        conn = sqlite3.connect(db_name)
        for active in (1, 0):
            result = conn.execute(query, (value, active))
            print_activ(result, active)
        conn.close()
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


