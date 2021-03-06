# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""
from task_12_1 import ping_ip_addresses
#check_ip(ip), ping_ip_addresses(list_ip) 
from task_12_2 import convert_ranges_to_ip_list
# convert_ranges_to_ip_list(ip_list)
from tabulate import tabulate

def print_ip_table(avail, notavail):
    slovar = {}
    slovar['Reachable'] = avail
    slovar['Unreachable'] = notavail
    print(tabulate(slovar, headers="keys"))

if __name__ == '__main__':

    list_ip = ['8.8.4.4', '1.1.1.1-2', '172.21.41.128-172.21.41.130']
    ip_list = convert_ranges_to_ip_list(list_ip)
    ip1, ip2 = ping_ip_addresses(ip_list)
    print_ip_table(ip1, ip2)
