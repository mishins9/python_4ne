# -*- coding: utf-8 -*-
"""
Задание 19.3a

Создать функцию send_command_to_devices, которая отправляет список указанных
команд show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какие команды. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом каждой
команды надо написать имя хоста и саму команду):

R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


Для выполнения задания можно создавать любые дополнительные функции,
а также использовать функции созданные в предыдущих заданиях.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime
import time
import yaml
import subprocess
import re
from netmiko import (
        ConnectHandler,
        NetmikoTimeoutException,
        NetmikoAuthenticationException,
)
from itertools import repeat

logging.getLogger('paramiko').setLevel(logging.WARNING)

logging.basicConfig(
        format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
        level=logging.INFO,
)

def send_show_command(device, command):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    logging.info(start_msg.format(datetime.now().time(), device['host']))
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            prompt = ssh.find_prompt()
            output = ssh.send_command(command, strip_command=False)
            logging.info(received_msg.format(datetime.now().time(), device['host']))
            return f"{prompt}{output}\n"
    except (NetmikoTimeoutException,NetmikoAuthenticationException) as error:
        print(error)
   

def send_command_to_devices(devices, commands_dict, filename, limit = 3):
    future_list = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        for device in devices:
            commands = commands_dict[device['host']]
            for command in commands:
                future = executor.submit(send_show_command, device, command)
                future_list.append(future)
        with open(filename, 'w') as dest:
            for f in future_list:
                dest.write(f.result())

if __name__ == '__main__':

# Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
# тест берет адреса из файла devices.yaml
    commands = {
        "192.168.100.3": ["sh ip int br", "sh ip route | ex -"],
        "192.168.100.1": ["sh ip int br", "sh int desc"],
        "192.168.100.2": ["sh int desc"],
}

    filename= 'output_show_dict_more_thread.txt'
    with open("devices.yaml") as f:
        list_hosts = yaml.safe_load(f)
    send_command_to_devices(list_hosts, commands, filename)


