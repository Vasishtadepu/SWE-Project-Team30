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

CREATE TABLE IF NOT EXISTS `additionalcourseconversion`
(
    `id` int(11) NOT NULL,
    `name` varchar(50) NOT NULL,
    `rollno` varchar(50) NOT NULL,
    `course1` varchar(50) NOT NULL,
    `coursenumber1` varchar(50) NOT NULL,
    `credits1` varchar(50) NOT NULL,
    `semester1` varchar(50) NOT NULL,
    `course2` varchar(50) NOT NULL,
    `coursenumber2` varchar(50) NOT NULL,
    `credits2` varchar(50) NOT NULL,
    `semester2` varchar(50) NOT NULL,
    `Guide_mail` varchar(50) NOT NULL,
    `HoD_mail` varchar(50) NOT NULL,
    `Registrar_mail` varchar(50) NOT NULL,
    `Dean_mail` varchar(50) NOT NULL,
    `approvelevel` varchar(50) NOT NULL,
    PRIMARY KEY(id)

);


CREATE TABLE IF NOT EXISTS `leaveform`
(
    `id` int(11) NOT NULL,
    `name` varchar(50) NOT NULL,
    `rollno` varchar(50) NOT NULL,
    `semester` varchar(11) NOT NULL,
    `leavefrom` varchar(50) NOT NULL,
    `leaveto` varchar(50) NOT NULL,
    `noofdays` varchar(11) NOT NULL,
    `reason` varchar(50) NOT NULL,
    `phone` varchar(50) NOT NULL,
    `Guide_mail` varchar(50) NOT NULL,
    `HoD_mail` varchar(50) NOT NULL,
    `Dealing_Assistant_Mail` varchar(50) NOT NULL,
    `approvelevel` varchar(50) NOT NULL,
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

INSERT INTO forms_table(form_name,table_name,no_of_approvers)  VALUES ('Additional Course Conversion','additionalcourseconversion','4');
INSERT INTO forms_table(form_name,table_name,no_of_approvers) VALUES('Leave form', 'leaveform','3');