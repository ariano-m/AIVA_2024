CREATE USER 'admin'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE DATABASE `MY_IMAGE`;

USE `MY_IMAGE`;

CREATE TABLE  USER (
    `USER` varchar(255) NOT NULL PRIMARY KEY,
    `PASSWORD` varchar(255) NOT NULL
);


CREATE TABLE  IMAGE (
    `ID` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `USER` varchar(255) NOT NULL,
    `IMAGE` LONGBLOB,
    `DATE` DATETIME NOT NULL,
    FOREIGN KEY (`USER`) REFERENCES `USER`(`USER`)
);


CREATE TABLE  BBOX (
    `ID` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `USER` varchar(255) NOT NULL,
    `X1` int NOT NULL,
    `Y1` int NOT NULL,
    `X2` int NOT NULL,
    `Y2` int NOT NULL,
    `MARGIN` boolean NOT NULL,
    `DATE` DATETIME NOT NULL,
    FOREIGN KEY (`USER`) REFERENCES `IMAGE`(`USER`)
);


INSERT INTO USER (USER, PASSWORD) VALUES ('user1234', '1234');