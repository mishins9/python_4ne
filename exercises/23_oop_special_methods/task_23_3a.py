# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        slovar = {}
        for key1, value1 in topology_dict.items():
            if not slovar.get(key1) and not slovar.get(value1):
                slovar[key1] = (value1)
        return slovar

    def delete_link(self, one_pair, two_pair):
        for key, value in list(self.topology.items()):
            if  key == one_pair:
                if value == two_pair:
                    del self.topology[key]
            elif  value == one_pair:
                if key == two_pair:
                    del self.topology[key]
            else:
                print("Такого соединения нет")

    def delete_node(self, node):
        for key, value in list(self.topology.items()):
            if key[0] == node or value[0] == node:
                del self.topology[key]
            else:
                print("Такого устройства нет")

    def add_link(self, src_link, dst_link):
        result = "Add Link"
        temp_keys  = list(self.topology.keys())
        temp_values = list(self.topology.values())
        t1 = [item for item in zip(temp_keys, temp_values) if src_link in item
              or dst_link in item]
        if t1:
            result = "Cоединение с одним из портов существует"
            if t1[0] == (src_link, dst_link) or t1[0] == (dst_link, src_link):
                result = "Такое соединение существует"
        else:
            self.topology.update({src_link:dst_link})
        print(result)

    def __add__(self, other):
        return Topology({**self.topology, **other.topology})

    def __iter__(self):
        return iter(self.topology.items())

if __name__ == "__main__":
    topology_example = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("R3", "Eth0/1"): ("R4", "Eth0/0"),
        ("R3", "Eth0/2"): ("R5", "Eth0/0"),
        ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
        ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
        ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
    }


    t1 = Topology(topology_example)
    for link in t1:
        print(link)
