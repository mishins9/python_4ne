# -*- coding: utf-8 -*-
"""
Задание 6.2

Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
В зависимости от типа адреса (описаны ниже), вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

in_address = input("IP-адрес в формате 10.0.1.1 : ")
list_ip = in_address.split(".")
oct1, oct2, oct3, oct4 = [int(list_ip[0]),
                          int(list_ip[1]),
                          int(list_ip[2]),
                          int(list_ip[3])]


if oct1 == 255:
    print("local broadcast")
elif oct1 == 0:
    print("unassigned")
elif oct1 in range(1,240):
    if oct1 in range(224,240):
        print("multicast")
    else: print("unicast")
else: print("unused")



