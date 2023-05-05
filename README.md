# SWE-Project-Team30
In order to run the Script, you can install the requirements using:
```
pip install -r requirements.txt
```

## Running the website
Start mysql server
```
mysql -u root -p
```
And create a database named 'test2'
```
use test2;
source 'path to new.sql';
source 'path to forms.sql';
```
Note that paths to new.sql and forms.sql should be **absolute** and relative paths.
Navigate to the project folder and open a bash terminal there and run the following command.
```python3 backend.py```

**Note that you need change the MySQL password in backend.py and in testing.py to make the code work.**

Then open the following link [Website](http://127.0.0.1:5000/)



## If you are a student
### To register
Click on the register button and fill in the details, make sure that the email you entered is valid and belongs to IITH 

### To login
Make sure that you have an account login using the student option.

### To submit a form
Select submit a new form option from the nav bar, this opens a list of available forms, select one and you will be sent to that form page.

### To check history
Select the submitted forms button from the navbar and here you can see a list of all forms submitted by you, click on expand for a detailed view.

## If you are an admin
### To open admin panel
Since no admins have been fixed we have implemented a dummy admin account with the following login details.\
Email : cs20btech11002@iith.ac.in\
Password : 2712\
Make sure that you login using Admin option selected

### To create a new form
Click the create a new form option which will send you to the page, Name and Roll No are mandatory, you can increase or decrease the number of fields that need to be filled by the student by selecting the appropirate option. Similarily for the approver fields which decides how many approvers does the form have.

### To check submitted forms.
Here you can see all the forms submitted by the students and you can filter them based on the form type or roll no of the student you want the form of.

## To test the code.
Run the following command 
```
source 'path to testing.sql'
python3 -m pytest testing.py
```
Path to testing.sql should be **absolute**


