# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений
  и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv),
   в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена
  информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы (именно в этом порядке):
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается
на sh_vers. Вы можете раскомментировать строку print(sh_version_files),
чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob
import csv
import re

sh_version_files = glob.glob("sh_vers*")
#print(sh_version_files)

headers = ["hostname", "ios", "image", "uptime"]

def parse_sh_version(string_output_sh):
#    print(string_output_sh)
    spisok = []
    regex = (r'Cisco IOS Software, .+, Version (?P<ios>\S+),'
             r'|router uptime is (?P<uptime>\d+ \w+, \d+ \w+, \d+ \w+)'
             r'|System image file is "(?P<image>.+)"')

    match = re.finditer(regex, string_output_sh)
    for item in match:
        spisok.append(item.group(item.lastgroup))
    ios1, uptime1, image1 = spisok
    ret_tuple = [ios1, image1, uptime1]
    return tuple(ret_tuple)
"""
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений

Cisco IOS Software, 1841 Software (C1841-ADVIPSERVICESK9-M), Version 12.4(15)T1, RELEASE SOFTWARE (fc2)
System image file is "flash:c1841-advipservicesk9-mz.124-15.T1.bin"
router uptime is 15 days, 8 hours, 32 minutes

* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"
"""

def write_inventory_to_csv(data_filenames, csv_filename):
    with open(csv_filename, "w") as dest:
        writer = csv.writer(dest)
        writer.writerow(headers)
        for item in data_filenames:
            with open(item) as src:
                content = src.read()
                parsed_data = parse_sh_version(content)
                hostname = re.search(r'sh_version_(\w+\d+).', item).group(1)
                writer.writerow([hostname] + list(parsed_data))
                print(f'{hostname} {parsed_data}')
"""
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv),
   в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает

* с помощью функции parse_sh_version, из каждого вывода должна быть получена
  информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл
* hostname, ios, image, uptime
"""

if __name__ == '__main__':
    write_inventory_to_csv(sh_version_files, 'routers_inventory.csv')
