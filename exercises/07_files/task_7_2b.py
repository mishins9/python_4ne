# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv

ignore = ["duplex", "alias", "configuration"]
write_file= []

with open(argv[1], 'r') as f:
    for line in f:
        words = line.split()
        words_inter = set(words) & set(ignore)
        if line[0] != '!' and not words_inter:
            write_file.append(line.rstrip())

print(write_file)
f1 = open(argv[2], 'w')
write_file_string = '\n'.join(write_file)
f1.write(write_file_string)
f1.close()
