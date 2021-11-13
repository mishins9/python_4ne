# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""
import csv
import re

def write_dhcp_snooping_to_csv(filenames, output):
    output_file = []
    regex = r'(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<port>\S+)'
    header = ["switch", "mac", "ip", "vlan", "interface"]
    for filename in filenames:
        device = re.match(r'\w+\d+', filename).group(0)
        with open(filename) as src:
            for line in src:
                match = re.search(regex, line)
                if match :
                    item_spisok = []
                    item_spisok.append(device)
                    for item in list(match.groups()):
                        item_spisok.append(item)
                    output_file.append(item_spisok)
    with open(output, 'w') as dest:
        writer = csv.writer(dest)
        writer.writerow(header)
        for line in output_file:
            writer.writerow(line)
        print(output_file)

if __name__ == '__main__':
    spisok_files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt',
                    'sw3_dhcp_snooping.txt']
    write_dhcp_snooping_to_csv(spisok_files, 'output_dhcp_snooping.csv')
