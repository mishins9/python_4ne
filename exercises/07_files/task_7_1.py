# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
f = open('ospf.txt')
res = f.readlines()
f.close()
viv = [i.split() for i in res]
spisok = ["Prefix", "AD/Metric", "Next-Hop", "Last update", "Outbound Interface"]

template = '''
{0:<20} {5}
{1:<20} {6}
{2:<20} {7}
{3:<20} {8}
{4:<20} {9}
'''
for line in viv:
    ln = [i.replace(',', '').replace('[', '').replace(']', '') for i in  line]
    print(template.format(spisok[0], spisok[1], spisok[2], spisok[3], spisok[4], ln[1], ln[2], ln[4], ln[5], ln[6]))

