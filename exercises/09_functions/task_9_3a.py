# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    with open(config_filename, 'r') as f:
        slovar_access = {}
        slovar_trunk = {}
        for line in f:
            if line.startswith('interface'):
                _, port = line.strip().split()
#                print(port)
            elif line.count('allowed vlan'):
                spisok_vlan  = line.split()[-1].split(',')
                slovar_trunk[port] = [int(i) for i in spisok_vlan]
#                print(slovar_trunk[port])
            elif line.count('mode access'):
                slovar_access[port] = 1
            elif line.count('access vlan'):
                slovar_access[port] = int(line.split()[-1])
#                print(slovar_access[port])
#tuple_keys = tuple(list_keys)
    return slovar_access, slovar_trunk
result = get_int_vlan_map('config_sw2.txt')
print(result)
