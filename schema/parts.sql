drop table if exists parts;
create table if not exists parts (
    id int primary key,
    product text not null,
    parent_id int null references theme(id)
)