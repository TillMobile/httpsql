create extension hstore;

create table item (
  id serial primary key,
  name varchar,
  description varchar,
  attributes hstore
 );

 create function items_by_size(t_size varchar)
 returns setof item as $$
   select * from item where attributes->'size' = t_size;
 $$ language 'sql';