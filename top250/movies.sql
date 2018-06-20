drop table if exists movies;
create table movies(
id int(10) unsigned primary key auto_increment,
ranking int(10) not null,
poster varchar(255) not null,
title varchar(32) not null,
alias varchar(64) null,
link varchar(64) not null,
star varchar(32) not null,
info varchar(128) not null,
`describe` text not  null
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table if exists musics;
create table musics(
id int(11) unsigned primary key auto_increment,
poster varchar(255) not null,
title varchar(64) not null,
link varchar(255) not null,
author varchar(32) not null,
`time` time not null,
star varchar(11) not null
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

