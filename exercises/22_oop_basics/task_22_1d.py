# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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
    
    top = Topology(topology_example)
    print(top.topology)
    top.add_link(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
    top.add_link(('SW1', 'Eth0/4'),('R1', 'Eth0/4'))

