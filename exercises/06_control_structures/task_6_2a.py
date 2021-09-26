# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
in_address = input("IP-адрес в формате 10.0.1.1 : ")

try:
    list_ip = in_address.split(".")
    if len(list_ip) != 4:
        raise ValueError()
    list_ip_int = [int(i) for i in list_ip]

    for ip in list_ip_int:
        if ip not in range(0,256):
            raise ValueError()

except (ValueError):
    print("Неправильный IP-адрес")
else:
    if in_address == "255.255.255.255":
        print("local broadcast")
    elif in_address == "0.0.0.0":
        print("unassigned")
    elif list_ip_int[0] in range(1,240):
        if list_ip_int[0] in range(224,240):
            print("multicast")
        else: print("unicast")
    else: print("unused")

