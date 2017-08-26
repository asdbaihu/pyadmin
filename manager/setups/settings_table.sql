--create table settings
create table settings(
id serial8 unique primary key,
tablename text,
dowhat text,
query text,
sqlcraeted text,
detail text,
updatetime timestamp default now());
insert into settings(tablename) values('test'); 
