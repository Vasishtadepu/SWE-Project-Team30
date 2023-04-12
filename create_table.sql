
CREATE TABLE IF NOT EXISTS `studentlogin`
(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(50) NOT NULL,
    `email` varchar(50) NOT NULL,
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

INSERT INTO studentlogin(username,password,email) VALUES ('Manaswini','2312','cs20btech11035@iith.ac.in');
INSERT INTO adminlogin(username,password,email) VALUES ('Vasisht','2711','cs20btech11002@iith.ac.in');
