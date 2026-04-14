show databases;
use world;
show tables;

-- check data
select *
from country
limit 5;

-- Saya mau ambil negara yang populasinya di atas rata-rata (cara manual)
--     1. Cari nilai average population
select avg(Population)
from country;
--     2. Nilai AVG Population di copy paste ke statement WHERE
select Name, Region, Population
from country
where Population > 25434098.1172;

-- Saya mau ambil negara yang populasinya di atas rata-rata (cara subquery)
select Name, Region, Population
from country
where Population > 
(select avg(Population) from country);

-- subquery in list of columns
select Name, Region, LifeExpectancy, 
(select min(LifeExpectancy) from country) MinLifeExpectancy,
(select max(LifeExpectancy) from country) MaxLifeExpectancy
from country;

-- subquery in from clause
select Code, Name, LifeExpectancy
from 
(select *
from country
where LifeExpectancy > 70) as GoodCountry;
-- buktikan apakah ada table GoodCountry di database world
show tables;

-- coba cek table city dan country
select * from city;
select * from country;

-- Kita mau ambil nama kota/city yang ada di dalam negara dengan LifeExpectancy > 75
select Name, CountryCode, Population
from city
where CountryCode in (select Code from country where LifeExpectancy > 75);

-- implicit join
select ci.Name, ci.Population, co.Code, co.LifeExpectancy
from city ci, country co
where ci.CountryCode = co.Code;

-- implicit join dengan alias
select ci.Name CityName, ci.Population CityPopulation, co.Name CountryName, co.Population CountryPopulation, co.Code, co.LifeExpectancy
from city ci, country co
where ci.CountryCode = co.Code;

-- inner join
select ci.Name, ci.Population, co.Code, co.LifeExpectancy
from city ci
join country co
on ci.CountryCode = co.Code;

select ci.Name, ci.Population, co.Code, co.LifeExpectancy
from city ci join country co
on ci.CountryCode = co.Code
where co.LifeExpectancy > 75;