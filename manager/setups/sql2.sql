--SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
--SELECT datname FROM pg_database;

--SELECT column_name FROM information_schema.columns WHERE table_name ='account';
--SELECT  column_name,column_default,is_nullable,data_type,udt_name FROM information_schema.columns WHERE table_name ='account';
--select datname from pg_database
EXPLAIN   (SELECT column_name,column_default,is_nullable,data_type,udt_name ,ordinal_position,dtd_identifier FROM information_schema.columns WHERE table_name ='pg_database') 