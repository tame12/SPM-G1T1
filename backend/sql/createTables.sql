-- WARNING: WILL DROP AND RECREATE ALL TABLES

drop database if exists `is212_G1T1`;
create database if not exists `is212_G1T1` default character set utf8 collate utf8_general_ci;
use `is212_G1T1`;

create table if not exists `is212_G1T1`.`Position` (
    `Position_ID` int auto_increment not null,
    `Position_Name` varchar(50) not null,
    primary key (`Position_ID`)
) engine = InnoDB default charset = utf8;

create table if not exists `is212_G1T1`.`Staff` (
  `Staff_ID` int not null,
  `Staff_FName` varchar(50) not null,
  `Staff_LName` varchar(50) not null,
  `Dept` varchar(50) not null,
  `Email` varchar(50) not null,
  `Position_ID` int not null,
  primary key (`Staff_ID`),
  foreign key (`Position_ID`) references `is212_G1T1`.`Position` (`Position_ID`)
) engine=InnoDB default charset=utf8;

create table if not exists `is212_G1T1`.`Course` (
    `Course_ID` varchar(20) not null,
    `Course_Name` varchar(50) not null,
    `Course_Desc` varchar(255),
    `Course_Is_Active` bit not null,
    `Course_Type` varchar(10),
    `Course_Category` varchar(50),
    primary key (`Course_ID`)
) engine = InnoDB default charset = utf8;

create table if not exists `is212_G1T1`.`Skill` (
    `Skill_ID` int auto_increment not null,
    `Skill_Name` varchar(50) not null,
    `Skill_Is_Active` bit not null,
    primary key (`Skill_ID`)
) engine = InnoDB default charset = utf8;

create table if not exists `is212_G1T1`.`Registration` (
    `Reg_ID` int auto_increment not null,
    `Course_ID` varchar(20),
    `Staff_ID` int,
    `Reg_Status` varchar(20),
    `Completion_Status` varchar(20),
    primary key (`Reg_ID`),
    foreign key (`Staff_ID`) references `is212_G1T1`.`Staff` (`Staff_ID`),
    foreign key (`Course_ID`) references `is212_G1T1`.`Course` (`Course_ID`)
) engine = InnoDB default charset = utf8;

create table if not exists `is212_G1T1`.`Role` (
    `Role_ID` int auto_increment not null,
    `Role_Name` varchar(50) not null,
    `Role_Desc` varchar(255),
    `Role_Is_Active` bit not null,
    primary key (`Role_ID`)
) engine = InnoDB default charset = utf8;



create table if not exists `is212_G1T1`.`Course_Skill` (
    `Course_ID` varchar(20) not null,
    `Skill_ID` int not null,
    primary key (`Course_ID`, `Skill_ID`),
    foreign key (`Course_ID`) references `is212_G1T1`.`Course` (`Course_ID`),
    foreign key (`Skill_ID`) references `is212_G1T1`.`Skill` (`Skill_ID`)
) engine = InnoDB default charset = utf8;

create table if not exists `is212_G1T1`.`Skill_Role` (
    `Skill_ID` int not null,
    `Role_ID` int not null,
    primary key (`Skill_ID`, `Role_ID`),
    foreign key (`Skill_ID`) references `is212_G1T1`.`Skill` (`Skill_ID`),
    foreign key (`Role_ID`) references `is212_G1T1`.`Role` (`Role_ID`)
) engine = InnoDB default charset = utf8;

create table if not exists `is212_G1T1`.`Learning_Journey` (
    `LJ_ID` int auto_increment not null,
    `Staff_ID` int not null,
    `Role_ID` int not null,
    `LJ_Number` int not null, -- backend need to auto increment LJ_Number within each staff
    primary key (`LJ_ID`),
    foreign key (`Staff_ID`) references `is212_G1T1`.`Staff` (`Staff_ID`), 
    foreign key (`Role_ID`) references `is212_G1T1`.`Role` (`Role_ID`)
) engine = InnoDB default charset = utf8;

create table if not exists `is212_G1T1`.`Learning_Journey_Course` (
    `LJ_ID` int not null,
    `Course_ID` varchar(20) not null,
    `Skill_ID` int not null,
    primary key (`LJ_ID`, `Course_ID`),
    foreign key (`LJ_ID`) references `is212_G1T1`.`Learning_Journey` (`LJ_ID`) on delete cascade,
    foreign key (`Course_ID`) references `is212_G1T1`.`Course` (`Course_ID`),
    foreign key (`Skill_ID`) references `is212_G1T1`.`Skill` (`Skill_ID`)
) engine = InnoDB default charset = utf8;

insert into `is212_G1T1`.`Position` (`Position_ID`, `Position_Name`) values 
(1, 'Admin'),
(2, 'User'),
(3, 'Manager'),
(4, 'Trainer');