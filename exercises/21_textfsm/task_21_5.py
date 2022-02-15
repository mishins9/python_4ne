# -*- coding: utf-8 -*-
"""
Задание 21.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в
параллельных потоках функцию send_and_parse_show_command из задания 21.4.

Параметры функции send_and_parse_command_parallel:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* templates_path - путь к каталогу с шаблонами TextFSM
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать словарь:
* ключи - IP-адрес устройства с которого получен вывод
* значения - список словарей (вывод который возвращает функция send_and_parse_show_command)

Пример словаря:
{'192.168.100.1': [{'address': '192.168.100.1',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '192.168.200.1',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}],
 '192.168.100.2': [{'address': '192.168.100.2',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '10.100.23.2',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}]}

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

import os
from concurrent.futures import ThreadPoolExecutor
import yaml
import subprocess
from itertools import repeat
from task_21_4 import send_and_parse_show_command

def send_and_parse_command_parallel(devices, command, templates_path, limit = 3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(send_and_parse_show_command, devices,
                              repeat(command), repeat(templates_path))
        l_out = {device['host']: output for device, output in zip(devices, result)}
    return l_out

if __name__ == '__main__':
    full_pth = os.path.join(os.getcwd(), "templates")
    command = 'sh ip int br'
    with open("devices.yaml") as f:
        list_hosts = yaml.safe_load(f)
    print(send_and_parse_command_parallel(list_hosts, command, full_pth))
