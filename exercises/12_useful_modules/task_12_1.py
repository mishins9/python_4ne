# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess
import ipaddress

def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError as err:
        return False

def ping_ip_addresses(list_ip):
    ipv4 = [i for i in list_ip if check_ip(i)]
    available = []
    notavailable = []
    for ip in ipv4:
        result = subprocess.run(['ping', '-c', '3', '-n', ip])
        if result.returncode != 0:
            notavailable.append(ip)
        else :
            available.append(ip)
    return available, notavailable

if __name__ == '__main__':
    ip_list = ['10.1.1.1', '8.8.8.8', '2.2.2']
    print(ping_ip_addresses(ip_list))


