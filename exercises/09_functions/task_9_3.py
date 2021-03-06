# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
from sys import argv

def get_int_vlan_map(config_filename):
    with open(config_filename, 'r') as f:
        slovar_access = {}
        slovar_trunk = {}
        for line in f:
            if line.startswith('interface'):
                _, port = line.strip().split()
#                print(port)
            if line.count('allowed vlan'):
                spisok_vlan  = line.split()[-1].split(',')
                slovar_trunk[port] = [int(i) for i in spisok_vlan]
#                print(slovar_trunk[port])
            if line.count('access vlan'):
                slovar_access[port] = int(line.split()[-1])
#                print(slovar_access[port])
#tuple_keys = tuple(list_keys)
    return slovar_access, slovar_trunk
result = get_int_vlan_map('config_sw1.txt')
print(result)
