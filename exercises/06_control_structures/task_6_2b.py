# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
while True : 
    in_address = input("IP-адрес в формате 10.0.1.1 : ")

    list_ip = in_address.split(".")
    correct = len(list_ip) == 4

    for ip in list_ip:
        correct = ip.isdigit() and 0 <= int(ip) <= 255 and correct
    if correct:
        break
    print("Неправильный IP-адрес")


list_ip_int = [int(i) for i in list_ip]

if in_address == "255.255.255.255":
    print("local broadcast")
elif in_address == "0.0.0.0":
    print("unassigned")
elif list_ip_int[0] in range(1,240):
    if list_ip_int[0] in range(224,240):
        print("multicast")
    else: print("unicast")
else: print("unused")

