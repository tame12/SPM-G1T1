drop database if exists `is212_G1T1`;
create database if not exists `is212_G1T1` default character set utf8 collate utf8_general_ci;
use `is212_G1T1`;

create table if not exists `is212_G1T1`.`Role` (
    `Role_ID` int auto_increment not null,
    `Role_Name` varchar(50) not null,
    primary key (`Role_ID`)
) engine = InnoDB default charset = utf8;

-- cannot change
create table if not exists `is212_G1T1`.`Staff` (
  `Staff_ID` int,
  `Staff_FName` varchar(50) not null,
  `Staff_LName` varchar(50) not null,
  `Dept` varchar(50) not null,
  `Email` varchar(50) not null,
  `Role` int,
  primary key (`Staff_ID`),
  foreign key (`Role`) references `is212_G1T1`.`Role` (`Role_ID`)
) engine=InnoDB default charset=utf8;

-- cannot change
create table if not exists `is212_G1T1`.`Course` (
    `Course_ID` varchar(20),
    `Course_Name` varchar(50) not null,
    `Course_Desc` varchar(255),
    primary key (`Course_ID`)
) engine = InnoDB default charset = utf8;

create table if not exists `is212_G1T1`.`Skill` (
    `Skill_ID` int,
    `Skill_Name` varchar(50) not null,
    -- `Skill_Desc` varchar(255),  
    primary key (`Skill_ID`)
) engine = InnoDB default charset = utf8;

insert into `is212_G1T1`.`Role` (`Role_ID`, `Role_Name`) values 
(1, 'Engineer'),
(2, 'Manager'),
(3, 'HR');

-- need to do some diagramming for learning journey 