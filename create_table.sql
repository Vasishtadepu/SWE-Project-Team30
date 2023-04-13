
CREATE TABLE IF NOT EXISTS `studentlogin`
(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(50) NOT NULL,
    `email` varchar(50) NOT NULL,
    'rollno' varchar(50) NOT NULL,
    'department' varchar(50) NOT NULL,
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
    `formtype` int(11) NOT NULL,
    `rollno` varchar(50) NOT NULL,
    PRIMARY KEY(id)

);

CREATE TABLE IF NOT EXISTS `additionalcourseconversion`
(
    `id` int(11) NOT NULL,
    `course1` varchar(50) NOT NULL,
    `coursenumber1` varchar(50) NOT NULL,
    `credits1` int(11) NOT NULL,
    'semester1' int(11) NOT NULL,
    `course2` varchar(50) NOT NULL,
    `coursenumber2` varchar(50) NOT NULL,
    `credits2` int(11) NOT NULL,
    'semester2' int(11) NOT NULL,
    'approver1' varchar(50) NOT NULL,
    'approver2' varchar(50) NOT NULL,
    'approver3' varchar(50) NOT NULL,
    'approver4' varchar(50) NOT NULL,
    PRIMARY KEY(id)

);

INSERT INTO studentlogin(username,password,email) VALUES ('Manaswini','2312','cs20btech11035@iith.ac.in');
INSERT INTO adminlogin(username,password,email) VALUES ('Vasisht','2711','cs20btech11002@iith.ac.in');
