create table if not exists theme (
    id int primary key,
    name text not null,
    parent_id int null references theme(id)
)