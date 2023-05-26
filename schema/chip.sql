create table if not exists chip (
    product varchar(50),
    the_type text,
    release_date text,
    process_size decimal,
    tdp decimal,
    transistors decimal,
    frequency decimal,
    vendor char(15)
)