# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
import os
import re
from pprint import pprint
import yaml
from netmiko import (
        ConnectHandler,
        NetmikoTimeoutException,
        NetmikoAuthenticationException,
)
from jinja2 import Environment, FileSystemLoader
from task_20_5 import create_vpn_config

def number_tunnel(spisok1, spisok2):
    max1 = int(max(spisok1))
    max2 = int(max(spisok2))
    spisok_all = [item for item in range(1, max([max1, max2]) + 1)]
    free_spisok = []
    for item in spisok_all:
        if (str(item) not in spisok1):
            if (str(item) not in spisok2):
                free_spisok.append(item)
    if free_spisok:
            count = min(free_spisok)
    else:
            count = max([max1, max2]) + 1
    print(count)
    return count

def spisok_use_tunnel(spisok_intf):
    spisok_tunnel = []
    for item in spisok_intf:
        if "Tunnel" in item:
            reg_split = r'Tunnel(\d+)'
            reg_search = re.search(reg_split, item)
            spisok_tunnel.append(reg_search.group(1))
    return spisok_tunnel

def send_show_command(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

def send_config_commands(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            print("Connected")
            output = ssh.send_config_set(commands)
        return output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


def configure_vpn(src_device_params, dst_device_params, src_template,
                  dst_template, vpn_data_dict):
    show_commands = ["sh ip int br"]
    src_show  = send_show_command(src_device_params, show_commands)
    dst_show  = send_show_command(dst_device_params, show_commands)


    regex = r'(\S+) +([\d.]+|unassigned) +\w+ +\w+ +(up|down|administratively down) +(up|down)'

    for show_command in show_commands:
        src_result = [match.group(1) for match in re.finditer(regex,
                                                              src_show[show_command])]
        dst_result = [match.group(1) for match in re.finditer(regex,
                                                              dst_show[show_command])]

#        print(src_result)
#        print(dst_result)
    

    src_tunnels = spisok_use_tunnel(src_result)
    dst_tunnels = spisok_use_tunnel(dst_result)

    vpn_data_dict["tun_num"] = number_tunnel(src_tunnels, dst_tunnels)

    temp_r1, temp_r2 = create_vpn_config(src_template, dst_template, vpn_data_dict)
    send_temp_r1 = temp_r1.split('\n')
    send_temp_r2 = temp_r2.split('\n')

#    print(send_temp_r1)
    
    output_src = send_config_commands(src_device_params, send_temp_r1)
    output_dst = send_config_commands(dst_device_params, send_temp_r2)

    return output_src, output_dst

if __name__ == "__main__":

    data = {
        "tun_num": None,
        "wan_ip_1": "192.168.100.1",
        "wan_ip_2": "192.168.100.2",
        "tun_ip_1": "10.0.1.1 255.255.255.252",
        "tun_ip_2": "10.0.1.2 255.255.255.252",
    }

    temp_file1 = "templates/gre_ipsec_vpn_1.txt"
    temp_file2 = "templates/gre_ipsec_vpn_2.txt"

    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    src_params = devices[0]
    dst_params = devices[1]


    print(configure_vpn(src_params, dst_params, temp_file1, temp_file2, data))

