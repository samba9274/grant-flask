CREATE DATABASE bookshop;
CREATE USER 'bookshop'@'localhost' IDENTIFIED BY 'bookshop';
GRANT ALL PRIVILEGES ON bookshop.* TO 'bookshop'@'localhost';
USE bookshop;
CREATE TABLE users(
    userId int unsigned NOT NULL UNIQUE,
    name varchar(35) NOT NULL,
    email varchar(50) NOT NULL UNIQUE,
    password varchar(32) NOT NULL,
    mobile varchar(10) NOT NULL,
    latitude float,
    longitude float,
    role varchar(10) NOT NULL,
    PRIMARY KEY (userId)
);
CREATE TABLE donations(
	donationId int unsigned NOT NULL UNIQUE,
    donoruserId int unsigned NOT NULL,
    description varchar(300) NOT NULL,
    inventory int unsigned NOT NULL,
    donationDate datetime NOT NULL,
    recieveruserId int unsigned,
    acceptationDate datetime,
    donationStatus char(10) NOT NULL,
    PRIMARY KEY (donationId),
    FOREIGN KEY (donoruserId) REFERENCES users(userId),
    FOREIGN KEY (recieveruserId) REFERENCES users(userId)
);
CREATE TABLE images(
    imageId int unsigned NOT NULL UNIQUE,
    donationId int unsigned NOT NULL,
    image mediumblob NOT NULL,
    PRIMARY KEY (imageId),
    FOREIGN KEY (donationId) REFERENCES donations(donationId)
);
INSERT INTO users VALUES(1, "Yash Eksambekar", "yash@grant.com", "5d921054fb17b705f10ec46feefd3032", "0000000000", 0, 0, "ADMIN");
INSERT INTO users VALUES(2, "Shree Chatane", "shree@grant.com", "b32411354a214a8cf9c0d1c18fb115e7", "0000000000", 0, 0, "ADMIN");
INSERT INTO users VALUES(3, "Laxmi Panch", "laxmi@grant.com", "f2ce0b3555d41a6f8093798fc05090bb", "0000000000", 0, 0, "ADMIN");
INSERT INTO users VALUES(4, "Saba Syed", "saba@grant.com", "3fffc1296ad1a1f3550cbef44c0a5b20", "0000000000", 0, 0, "ADMIN");
INSERT INTO users VALUES(5, "Samiksha Dhote", "samiksha@grant.com", "6d473c1b20680652809ae39628c57238", "0000000000", 0, 0, "ADMIN");
