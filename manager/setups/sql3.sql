create table querysql
(id serial8 primary key,
dowhat text,
querysql text,
detail text,
update_time timestamp)
insert into querysql(dowhat) values('test');
