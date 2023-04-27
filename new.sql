CREATE TABLE IF NOT EXISTS `studentlogin`
(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `password` varchar(50) NOT NULL,
    `email` varchar(50) NOT NULL,
    `rollno` varchar(50) NOT NULL,
    `department` varchar(50) NOT NULL,
    PRIMARY KEY(id)

);

CREATE TABLE IF NOT EXISTS `adminlogin`
(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(50) NOT NULL,
    `email` varchar(50) NOT NULL,
    PRIMARY KEY(id)

);

CREATE TABLE IF NOT EXISTS `submittedforms`
(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `formtype` varchar(100) NOT NULL,
    `rollno` varchar(50) NOT NULL,
    `status` varchar(50) NOT NULL,
    PRIMARY KEY(id)

);



INSERT INTO studentlogin(name,password,email,rollno,department) VALUES ('Manaswini','2312','cs20btech11035@iith.ac.in','CS20BTECH11035','CSE');
INSERT INTO adminlogin(username,password,email) VALUES ('Vasisht','2711','cs20btech11002@iith.ac.in');




CREATE TABLE IF NOT EXISTS `forms_table`
(
    `form_name` varchar(100) NOT NULL,
    `table_name` varchar(100) NOT NULL,
    `no_of_approvers` varchar(100) NOT NULL
);

