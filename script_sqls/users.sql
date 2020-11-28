use facultad;


create table users(
id int auto_increment primary key, 
user_type int (10) not null,
	dni int(10), 
   firstname varchar(20),
   lastname  varchar(20),
   email varchar(20),
   password varchar(50));