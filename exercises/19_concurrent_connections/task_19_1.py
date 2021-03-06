# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime
import time
import yaml
import subprocess
import re

logging.getLogger('paramiko').setLevel(logging.WARNING)

logging.basicConfig(
        format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
        level=logging.INFO,
)

def ping_ip_address(ip_add):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    logging.info(start_msg.format(datetime.now().time(), ip_add))
    result = subprocess.run(['ping', '-c', '3', '-n', ip_add],
                            stdout=subprocess.DEVNULL)
    logging.info(received_msg.format(datetime.now().time(), ip_add))
    return result
   

def ping_ip_addresses(list_host, limit = 3):
    access = []
    notaccess = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip_address, list_host)
        for device, output in zip(list_host, result):
            regex = 'returncode=0'
            if re.search(regex, str(output)):
                access.append(device)
            else:
                notaccess.append(device)
    return (access, notaccess)

if __name__ == '__main__':
#    with open("devices.yaml") as f:
#        devices = yaml.safe_load(f)
#        ip_list= [item for item in devices]
    ip_list = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
    print(ping_ip_addresses(ip_list))
