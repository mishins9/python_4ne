import ipaddress

subnet1 = ipaddress.ip_network('172.16.0.0/16')
list_subnet = list(subnet1.subnets(prefixlen_diff=8))

spisok_ip = []
for ip in list_subnet[9]:
    spisok_ip.append(ip)
print(len(spisok_ip))
print(list_subnet)
