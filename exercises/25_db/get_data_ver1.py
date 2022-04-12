import sys
import sqlite3

db_filename = 'dhcp_snooping.db'

key, value = sys.argv[1:]
keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
keys.remove(key)

conn = sqlite3.connect(db_filename)
#Позволяет далее обращаться к данным в колонках, по имени колонки
conn.row_factory = sqlite3.Row

print('Detailed information for host(s) with', key, value)
print('-' * 40)

query = 'select * from dhcp where {} = ?'.format(key)
result = conn.execute(query, (value, ))

for row in result:
    for k in keys:
        print('{:12}: {}'.format(k, row[k]))
    print('-' * 40)
