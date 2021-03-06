# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
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
   

def send_show_command_to_devices(devices, command, filename, limit = 3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(send_show_command, devices, repeat(command))
        with open(filename, 'a') as dest:
            for device, output in zip(devices, result):
                dest.write(output)

if __name__ == '__main__':
    command = 'sh ip int br'
    filename= 'output_show_thread.txt'
    with open("devices.yaml") as f:
        list_hosts = yaml.safe_load(f)
    send_show_command_to_devices(list_hosts, command, filename)
