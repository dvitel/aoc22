create table lines(sz_or_prompt TEXT, cmd_or_file TEXT, dir TEXT null);
.separator ' '
.import d7.txt lines
.separator '|'
insert into lines values ('$', 'cd', '/');
create table l as select row_number() over () as i, * from lines;
create table cd as select row_number() over () as cd_i, * from l where sz_or_prompt = '$' and cmd_or_file = 'cd';
create table ranges as select cd.cd_i, cd.i as s, cd0.i as e from cd join cd as cd0 on cd0.cd_i - 1 = cd.cd_i;
create table dirs as 
with recursive fs(i, p) as (
        select 0, '' 
        union 
        select cd.cd_i, 
            case substr(cd.dir, 1, 1) 
            when '/' then cd.dir 
            when '.' then rtrim(rtrim(fs.p, replace(fs.p, '/', '')), '/')
            else rtrim(fs.p, '/') || '/' || cd.dir 
            end
        from fs join cd on fs.i + 1 = cd.cd_i) 
    select * from fs;
update dirs set p = '/' where p = '';

-- select * from dirs; 
create table fs as 
select d.i, d.p, cast(l.sz_or_prompt as number) as sz, l.cmd_or_file as f from dirs d 
    join ranges r on d.i = r.cd_i 
    join l on r.s < l.i and l.i < r.e 
    where l.sz_or_prompt != 'dir' and l.sz_or_prompt != '$';

create table dir_sz as 
select d.p, sum(d0.sz) as sz  
    from (select distinct p from dirs) as d 
    join fs as d0 on substr(d0.p, 1, length(d.p)) = d.p
group by d.p;
--part1
select sum(sz) from dir_sz where sz <= 100000;
--part2
select sz from dir_sz where sz >= (select 30000000 - 70000000 + sz from dir_sz where p = '/') order by sz limit 1;