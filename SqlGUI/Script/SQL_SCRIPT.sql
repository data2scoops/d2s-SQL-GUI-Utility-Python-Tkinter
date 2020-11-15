CREATE DATABASE DEMO;

CREATE LOGIN 'your user name' WITH PASSWORD = 'your password';

GRANT
SELECT,
INSERT,
DELETE
to 'your user name';

CREATE TABLE Clients (
    ClientID int,
    LastName varchar(255),
    FirstName varchar(255),
    City varchar(255),
	PRIMARY KEY (ClientID)
);