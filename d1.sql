-- drop table if exists e;
-- drop table if exists ei;
-- drop table if exists s;
-- drop table if exists ranges;
create temp table e(c number);
.import d1.txt e
insert into e values ('');
create temp table ei as select row_number() over () as i, c from e;
create temp table s as select row_number() over () as rn, i from ei as s where s.c = '';
create temp table ranges as select coalesce(s2.i, 0) as f, s.i as t from s left join s as s2 on s2.rn = s.rn - 1;

select r.f, r.t, sum(e.c) as cls from ei as e join ranges as r on e.i > r.f and e.i < r.t 
group by r.f, r.t
order by cls desc limit(3);