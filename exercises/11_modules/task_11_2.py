# -*- coding: utf-8 -*-
"""
Задание 11.2

Создать функцию create_network_map, которая обрабатывает
вывод команды show cdp neighbors из нескольких файлов и объединяет его в одну
общую топологию.

У функции должен быть один параметр filenames, который ожидает как аргумент
список с именами файлов, в которых находится вывод команды show cdp neighbors.

Функция должна возвращать словарь, который описывает соединения между
устройствами. Структура словаря такая же, как в задании 11.1:
    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}


Cгенерировать топологию, которая соответствует выводу из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt

Не копировать код функций parse_cdp_neighbors и draw_topology.
Если функция parse_cdp_neighbors не может обработать вывод одного из файлов
с выводом команды, надо исправить код функции в задании 11.1.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]

def clear_line(stroka, n_space):
    spisok = stroka.split(n_space)
    spisok_wo = list(filter(lambda x: x.rstrip(), spisok))
    clear_stroka = [i.strip() for i in spisok_wo]
    return clear_stroka

def parse_cdp_neighbors(command_output):
    """
    Тут мы передаем вывод команды одной строкой потому что именно в таком виде будет
    получен вывод команды с оборудования. Принимая как аргумент вывод команды,
    вместо имени файла, мы делаем функцию более универсальной: она может работать
    и с файлами и с выводом с оборудования.
    Плюс учимся работать с таким выводом.
    """
    result = command_output.split('\n')

    atr_table = {}
    priznak = False

    for line in result:
        line = line.rstrip()
        if line:
            if 'show cdp neighbors' in line :
                source_dev = line[:line.find('show cdp neighbors')].replace('>', '')
            elif 'Device ID' in line :
                head_slovar = {}
                r_head = clear_line(line, '  ')    
            #    spisok = line.split('  ')
            #    spisok_wo = list(filter(lambda x: x.rstrip(), spisok))
            #    clear_stroka = [i.strip() for i in spisok_wo]
                for i in r_head:
                    head_slovar[i] = (line.find(i), len(i))
                priznak = True
            elif priznak == True:
                r_atr = []
                for key, value in head_slovar.items():
                    begin, end = value
                    r_atr.append(line[begin:begin+end+1]) 
                key_spisok = (source_dev, r_atr[1].replace(' ', '').strip())
                value_spisok = (r_atr[0].strip(), r_atr[-1].replace(' ', '').strip())
                atr_table[key_spisok] = value_spisok
    return atr_table

def create_network_map(filenames):
     sum_files = {}
     for infile in filenames:
         with open(infile) as f:
             sum_files.update(parse_cdp_neighbors(f.read()))
     return sum_files


if __name__ == "__main__":
    print(create_network_map(infiles))
