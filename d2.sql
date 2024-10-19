create temp table e(o TEXT, u TEXT);
.separator ' '
.import d2.txt e
.separator '|'
create table s (u TEXT, v number);
insert into s values ('X', 1), ('Y', 2), ('Z', 3);
create table b (o TEXT, u TEXT, v number);
insert into b values ('A', 'X', 3), ('A','Y', 6), ('A','Z', 0),('B', 'X', 0), ('B','Y', 3), ('B','Z', 6),('C', 'X', 6), ('C','Y', 0), ('C','Z', 3);
select sum(b.v + s.v) from e join s on s.u = e.u join b on b.o = e.o and b.u = e.u;

select sum(b.v + s.v) from e join b on b.o = e.o and b.v = (case e.u when 'X' then 0 when 'Y' then 3 when 'Z' then 6 end) join s on s.u = b.u 
