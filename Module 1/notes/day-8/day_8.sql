show databases;
use world;
show tables;

select * 
from city;

-- LIKE
 select *
 from city
 where Name like 'R%';
 select Name, Population
 from city
 where Name like '%us%';
 select Name, Population
 from city
 where Name like 'A___%';
 
 -- BETWEEN and NOT BETWEEN
 select Name, Population
 from country
 where LifeExpectancy between 45 AND 90;
 select Name, LifeExpectancy
 from country
 where LifeExpectancy not between 45 and 75;
 
 -- ORDER BY
 select * from country
 order by Name;
 select Region, Name, Population
 from country
 order by Region, Name;
 
 -- GROUP BY
 -- basic group by
 select count(ID), CountryCode
 from city
 group by CountryCode;
 select CountryCode, avg(Population)
 from city
 group by CountryCode;
 -- group by and where
 select District, avg(Population)
 from city
 where CountryCode = 'IDN'
 group by District;
 -- group by, where, and as
  select District as Provinsi, avg(Population) as Rata_Rata
 from city
 where CountryCode = 'IDN' and Population > 500000
 group by District;
 -- group by, where, as, and having
  select District as Provinsi, avg(Population) as Rata_Rata
 from city
where CountryCode = 'IDN'
 group by District
 having Rata_Rata > 500000;
 select District as Provinsi, avg(Population) as Rata_Rata
 from city
where CountryCode = 'IDN' and District like 'S%'
 group by District;
 -- saya mau data top 3 provinsi di Indonesia (IDN) yang berawalan huruf 'S' berdasarkan rata-rata populasinya (Population)
  select District as Provinsi, avg(Population) as Rata_Rata
 from city
where CountryCode = 'IDN'
 group by District
 having Provinsi like 'S%'
 order by Rata_Rata desc
 limit 3;