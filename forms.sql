
CREATE TABLE Additional_Course_Conversion_Form(
    `id` INT(11) ,
    `Name` VARCHAR(100) ,
    `Roll_No` VARCHAR(100) ,
    `Course1` VARCHAR(100) ,
    `Course_Number1` VARCHAR(100) ,
    `Credits1` VARCHAR(100) ,
    `Semester1` VARCHAR(100) ,
    `Course2` VARCHAR(100) ,
    `Course_Number2` VARCHAR(100) ,
    `Credits2` VARCHAR(100) ,
    `Semester2` VARCHAR(100) ,
    `Guide_Name` VARCHAR(100) ,
    `HoD_Name` VARCHAR(100) ,
    `Guide_Mail` VARCHAR(100) ,
    `HoD_Mail` VARCHAR(100) ,
    `Deputy_Registrar_Mail` VARCHAR(100) ,
    `Dean_Mail` VARCHAR(100) ,
    `approvelevel` VARCHAR(150) ,
    PRIMARY KEY(id)

);


CREATE TABLE Leave_Form(
    `id` INT(11) ,
    `Name` VARCHAR(100) ,
    `Roll_No` VARCHAR(100) ,
    `Semester` VARCHAR(100) ,
    `Leave_from` VARCHAR(100) ,
    `Leave_to` VARCHAR(100) ,
    `No_of_days` VARCHAR(100) ,
    `Reason` VARCHAR(100) ,
    `Phone` VARCHAR(100) ,
    `Guide_Name` VARCHAR(100) ,
    `HoD_Name` VARCHAR(100) ,
    `Guide_Mail` VARCHAR(100) ,
    `HoD_Mail` VARCHAR(100) ,
    `Dealing_Assistant_Mail` VARCHAR(100) ,
    `approvelevel` VARCHAR(150) ,
    PRIMARY KEY(id)

);


create table JRF_to_SRF_conversion_Form(
    `id`  INT(11) ,
    `Name`  VARCHAR(100) ,
    `Roll_No`  VARCHAR(100) ,
    `Joining_Date`  VARCHAR(100) ,
    `Department`  VARCHAR(100) ,
    `External_Member_Name`  VARCHAR(100) ,
    `HoD_or_Dean_Name`  VARCHAR(100) ,
    `Guide_Name`  VARCHAR(100) ,
    `Date_of_Assessment`  VARCHAR(100) ,
    `Time` VARCHAR(100) ,
    `Venue`  VARCHAR(100) ,
    `Assessment_of_committee`  VARCHAR(100) ,
    `External_Member_Mail`  VARCHAR(100) ,
    `Guide_Mail`  VARCHAR(100) ,
    `HoD_Mail`  VARCHAR(100) ,
    `Deptuty_Resgistrar_Mail`  VARCHAR(100) ,
    `Dean_Mail`  VARCHAR(100) ,
    `approvelevel`  VARCHAR(150) );

create table Guide_Consent_Form(
    `id`  INT(11) ,
    `Name` VARCHAR(100) ,
    `Roll_No`  VARCHAR(100) ,
    `Joining_Date`  VARCHAR(100) ,
    `Department` VARCHAR(100) ,
    `Choose_the_supervisor_at_end_or_at_last_of_first_Semester`  VARCHAR(100) ,
    `Faculty1_Name`  VARCHAR(100) ,
    `Faculty2_Name` VARCHAR(100) ,
    `Faculty3_Name`  VARCHAR(100) ,
    `Faculty4_Name`  VARCHAR(100) ,
    `Faculty5_Name`  VARCHAR(100) ,
    `Faculty1_Mail`  VARCHAR(100) ,
    `Faculty2_Mail`  VARCHAR(100) ,
    `Faculty3_Mail`  VARCHAR(100) ,
    `Faculty4_Mail`  VARCHAR(100) ,
    `Faculty5_Mail`  VARCHAR(100) ,
    `Guide_Mail`  VARCHAR(100) ,
    `CoGuide_Mail`  VARCHAR(100) ,
    `DPGC_Mail`  VARCHAR(100) ,
    `HoD_Mail`  VARCHAR(100) ,
    `approvelevel`  VARCHAR(150) );


create table Guide_Change_Consent_Form(
    `id`  INT(11) ,
    `Name` VARCHAR(100) ,
    `Roll_No`  VARCHAR(100) ,
    `Department`  VARCHAR(100) ,
    `Present_Guide_Name`  VARCHAR(100) ,
    `Proposed_Guide_Name`  VARCHAR(100) ,
    `HoD_Name`  VARCHAR(100) ,
    `Present_Guide_Mail`  VARCHAR(100) ,
    `Proposed_Guide_Mail`  VARCHAR(100) ,
    `Deputy_Registrar_Mail`  VARCHAR(100) ,
    `Dean_Mail`  VARCHAR(100) ,
    `approvelevel`  VARCHAR(150) );


create table Fellowship_Form(
    `id`  INT(11) ,
    `Name`  VARCHAR(100) ,
    `Roll_No`  VARCHAR(100) ,
    `Department`  VARCHAR(100) ,
    `Joining_Year`  VARCHAR(100) ,
    `Stream`  VARCHAR(100) ,
    `Scholarship_Month`  VARCHAR(100) ,
    `Number_of_Days_Attended`  VARCHAR(100) ,
    `Amount_of_Stipend`  VARCHAR(100) ,
    `Scholarship_Type`  VARCHAR(100) ,
    `Project`  VARCHAR(100) ,
    `Supervisor_Name`  VARCHAR(100) ,
    `Faculty_Name`  VARCHAR(100) ,
    `Supervisor_Mail`  VARCHAR(100) ,
    `Faculty_Mail`  VARCHAR(100) ,
    `approvelevel`  VARCHAR(150) );

INSERT INTO forms_table(form_name,table_name,no_of_approvers)  VALUES ('Additional Course Conversion','Additional_Course_Conversion_Form','4');
INSERT INTO forms_table(form_name,table_name,no_of_approvers) VALUES('Leave Form', 'Leave_Form','3');
INSERT INTO forms_table(form_name,table_name,no_of_approvers) VALUES('JRF to SRF Conversion', 'JRF_to_SRF_conversion_Form','5');
INSERT INTO forms_table(form_name,table_name,no_of_approvers) VALUES('Guide Consent Form', 'Guide_Consent_Form','9');
INSERT INTO forms_table(form_name,table_name,no_of_approvers) VALUES('Guide Change Consent Form', 'Guide_Change_Consent_Form','4');
INSERT INTO forms_table(form_name,table_name,no_of_approvers) VALUES('Fellowship Form', 'Fellowship_Form','2');
