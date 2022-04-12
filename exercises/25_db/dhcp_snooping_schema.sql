create table if not exists dhcp (
    mac          text not NULL primary key,
    ip           text,
    vlan         text,
    interface    text,
    switch       text
);
create table if not exists switches(
    switch         text not NULL primary key,
    city           text,
    street         text
);
