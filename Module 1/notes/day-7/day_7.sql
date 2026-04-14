show databases;
use world;
show tables;
select *
from city;
select avg(Population)
from city;
select avg(LifeExpectancy)
from country;
select sum(Population)
from city;
use seller;
show tables;
select *
from persons;
insert into persons
values (1, 'Rusnandi', 'Fikri', 'Jalan Merdeka', 'Jakarta');
insert into persons
values
	(2, 'John', 'Wick', 'Boulevard Street', 'London'),
    (3, 'Tony', 'Stark', 'Manhatan Street', 'New York');
use world;
select *
from city
where Population > 1000000;
select Name
from city
where Population > 1000000;
select count(distinct Name)
from city
where Population > 1000000;
select *
from city
where Name like 'X%';
select count(distinct Name)
from city
where Name like 'X%';