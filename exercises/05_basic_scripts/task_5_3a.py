# -*- coding: utf-8 -*-
"""
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости
от выбранного режима, задавались разные вопросы в запросе о номере
VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
"""

access_template = [
    "switchport mode access",
    "switchport access vlan {}",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan {}",
]

input_access = 'Введите номер VLAN: '
input_trunk =  'Введите разрешенные VLANы: '

template = {"access":[access_template, input_access],
            "trunk":[trunk_template, input_trunk]}

mode =  input("Введите режим работы интерфейса (access/trunk): ") 
number_int = input("Введите тип и номер интерфейса: ")
number_vlan = input(template[mode][1])


print("interface {}".format(number_int))
print("\n".join(template[mode][0]).format(number_vlan))
