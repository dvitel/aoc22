create table lines(l TEXT);
.import d8.txt lines
create table l as select row_number() over () as i, * from lines;
-- with recursive r(j) as (
--     select 1 union select j+1 from r where j <= (select length(l.l) from l limit 1)
-- )
create table grid as 
select l.i, l0.i as j, cast(substr(l.l, l0.i, 1) as number) as h from l cross join l l0;

--select * from grid where i = 1;

-- select i, j, 0 from grid where i = 1 or j = 1
--     union
select g.i, g.j, sum(case when g1.j is null then 0 else 1 end) as s 
    from grid g 
    left join 
    (select *, 
        case when g.i = g1.i and g1.j < g.j then 1 else 0 end as l,
        case when g.i = g1.i and g1.j > g.j then 1 else 0 end as r,
        case when g.j = g1.j and g1.i < g.i then 1 else 0 end as t,
        case when g.j = g1.j and g1.i > g.i then 1 else 0 end as b
     from grid g1) as g1 on g1.h >= g.h 
where l + r + b + t > 0
group by g.i, g.j having s < 4;
--where g1.j is null;
--where g.i != 1 and g.j != 1
--group by g.i, g.j; having count(*) = g.j - 1
--     union 
-- select g.i, g.j, count(*) from grid g join grid g1 on g.j = g1.j and g1.i < g.i and g1.h < g.h
-- where g.i != 1 and g.j != 1
-- group by g.i, g.j having count(*) = g.i - 1
--     union 
-- select g.i, g.j, count(*) from grid g join grid g1 on g.j = g1.j and g1.i < g.i and g1.h < g.h
-- where g.i != 1 and g.j != 1
-- group by g.i, g.j having count(*) = g.i - 1
--     union 
-- select g.i, g.j, count(*) from grid g join grid g1 on g.j = g1.j and g1.i < g.i and g1.h < g.h
-- where g.i != 1 and g.j != 1
-- group by g.i, g.j having count(*) = g.i - 1


-- select g.i, g.j, sum(case when g1.j is null then 0 else 1 end) from grid g left join grid g1 on g.i = g1.i and g1.j < g.j
-- group by g.i, g.j 

--having count(*) = g.j - 1