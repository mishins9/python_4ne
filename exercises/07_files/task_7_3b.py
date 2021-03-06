# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
ivlan = input('Input number VLAN: ')
spisok = []
with open('CAM_table.txt', 'r') as f:
    for line in f:
        words = line.split()
        if line.count('.') == 2 and words[0].isdigit() and words[0] == ivlan:
            vlan, mac, _, intf = words
            spisok.append([int(vlan), mac, intf])

for line in sorted(spisok, key=lambda nint: nint[2]):
    print("{:<8} {:<19} {}".format(line[0], line[1], line[2]))

