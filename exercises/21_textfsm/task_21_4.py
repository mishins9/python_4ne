# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
import os
import yaml
from netmiko import ConnectHandler
from task_21_3 import parse_command_dynamic


def send_and_parse_show_command(device_dict, command,
                                templates_path, index='index'):
    attr_dict = {'Command': command, 'Vendor': device_dict["device_type"]}
    with ConnectHandler(**device_dict) as r1:
        r1.enable()
        output = r1.send_command(command)
        result = parse_command_dynamic(output, attr_dict,
                                       templ_path=templates_path)
    return result


if __name__ == "__main__":
    full_pth = os.path.join(os.getcwd(), "templates")
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        res_dev = send_and_parse_show_command(dev, command,
                                              templates_path=full_pth)
        print(res_dev)

