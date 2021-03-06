# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import glob
import csv
import re


def parse_sh_cdp_neighbors(output_sh_cdp):
    regex =  (r'(?P<intf>\S+) +(?P<lintf>Eth \S+) +'
              r'(?P<hold>\d+) +[\w ]+ +'
              r'(?P<platf>\S+) +'
              r'(?P<port_id>Eth \S+)')
    match = re.finditer(regex, output_sh_cdp)
    slovar = {}
    regex_show = re.search(r'(?P<device>\w+)>', output_sh_cdp)
    slovar_int = {}
    for item in match:
        intf, lintf, hold, platf, port_id = item.groups()
        slovar_int[lintf] = {intf:port_id}
    out_slovar = slovar.setdefault(regex_show.group('device'), slovar_int)
#    print(slovar)
    return slovar

if __name__ == "__main__":
    sh_cdp_file = glob.glob("sh_cdp_n_sw1.txt")
    for filename in sh_cdp_file:
        with open(filename) as src:
            content = src.read()
            parse_sh_cdp_neighbors(content)
    
