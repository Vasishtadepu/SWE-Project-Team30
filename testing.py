# from new import app # Flask instance of the API

# def test_index_route():
#     response = app.test_client().get('/')
#     assert response.status_code == 200
import flask
import pytest
from new import app
import MySQLdb
import mysql.connector
import MySQLdb.cursors
import unittest

from flask import template_rendered
from contextlib import contextmanager

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # with app.app_context():
            # conn = mysql.connector.connect(host="localhost",user="root",password="2312",database="test2")
            # cur = conn.cursor()
            # cur.execute("CREATE TABLE IF NOT EXISTS studentlogin(`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `name` varchar(50) NOT NULL, `password` varchar(50) NOT NULL, `email` varchar(50) NOT NULL,`rollno` varchar(50) NOT NULL,`department` varchar(50) NOT NULL)")
            # conn.commit()
            # cur.execute("INSERT INTO studentlogin(name,password,email,rollno,department) VALUES ('Manaswini','2312','cs20btech11035@iith.ac.in','CS20BTECH11035','CSE')")
            # conn.commit()
            # cur.execute("CREATE TABLE IF NOT EXISTS adminlogin(`id` int(11) NOT NULL AUTO_INCREMENT,`username` varchar(50) NOT NULL,`password` varchar(50) NOT NULL,`email` varchar(50) NOT NULL,PRIMARY KEY(id))")
            # conn.commit()
            # cur.execute("INSERT INTO adminlogin(username,password,email) VALUES ('Vasisht','2711','cs20btech11002@iith.ac.in')")
            # conn.commit()


            
        yield client
        # with app.app_context():
        #     conn = mysql.connector.connect(host="localhost",user="root",password="2312",database="test2")
        #     cur = conn.cursor()
        #     # cur.execute("DROP TABLE IF EXISTS studentlogin")
        #     # cur.execute("DROP TABLE IF EXISTS adminlogin")
        #     conn.commit()
            

#testing case when student enters correct credentials
def test_student_login_success(client):
    response = client.post('/login', data=dict(
        email='cs20btech11035@iith.ac.in',
        password='2312',
        user='Student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data

#testing case when admin enters correct credentials
def test_admin_login_success(client):
    response = client.post('/login', data=dict(
        email='cs20btech11002@iith.ac.in',
        password='2711',
        user='Admin'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Hello admin' in response.data

#testing case when student enters wrong credentials
def test_student_login_failure(client):
    response = client.post('/login', data=dict(
        email='cs20btech11035@iith.ac.in',
        password='2711',
        user='Student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid credentials. Try again.' in response.data

#testing case when admin enters wrong credentials
def test_admin_login_failure(client):
    response = client.post('/login', data=dict(
        email='cs20btech11035@iith.ac.in',
        password='2312',
        user='Admin'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid credentials. Try again.' in response.data


#testing case when existing user tries to register.
def test_old_student_register(client):
    response = client.post('/register', data=dict(
        username='Manaswini',
        password='2312',
        email='cs20btech11035@iith.ac.in',
        rollno='CS20BTECH11035',
        department='CSE',
        user='Student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Account already exists !' in response.data


#testing case when new user doesn't provide all details
def test_new_student_missing_details_register(client):
    response = client.post('/register', data=dict(
        email='cs20btech11035@iith.ac.in',
        rollno='CS20BTECH11035',
        department='CSE',
        user='Student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Please fill out the form !' in response.data

#testing case when new user registers correctly.
def test_new_student_register(client):
    response = client.post('/register', data=dict(
        username='Shounik',
        password='2711',
        email='cs20btech11055@iith.ac.in',
        rollno='CS20BTECH11055',
        department='CSE',
        user='Student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'You have successfully registered !' in response.data
    conn = mysql.connector.connect(host="localhost",user="root",password="2312",database="test2")
    cur = conn.cursor()
    cur.execute("SELECT * FROM studentlogin WHERE email = 'cs20btech11055@iith.ac.in'")
    account = cur.fetchone()
    assert account
    cur.execute("DELETE FROM studentlogin WHERE email='cs20btech11055@iith.ac.in' ")
    conn.commit()

#testing case when user tries to open homepage without logging in
def test_home_page_without_login(client):
        with client.session_transaction() as sess:
            sess['loggedin']=False
        # client.get('/')
        response = client.get('/homepage',follow_redirects=True)
        assert b'Please login to continue !' in response.data


# testing case when student tries to open homepage
def test_home_page_student(client):
        with client.session_transaction() as sess:
            sess['loggedin']=True
            sess['email']='cs20btech11035@iith.ac.in'
            sess['id']='Manaswini'
            sess['type']='Student'
        with captured_templates(app) as templates:
             response = client.get('/homepage',follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             assert template.name == 'studenthomepage.html'
        


#testing case when admin tries to open homepage
def test_home_page_admin(client):
        with client.session_transaction() as sess:
            sess['type']='Admin'
            sess['loggedin']= True
        # client.get('/')
        response = client.get('/homepage',follow_redirects=True)
        # assert flask.session['loggedin']==True
        assert b'Hello admin' in response.data

#testing logout
def test_logout(client):
      with client.session_transaction() as sess:
            sess['id']='Manaswini'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['loggedin']= True
        # client.get('/')
      with captured_templates(app) as templates:
             response = client.get('/logout',follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             assert template.name == 'login.html'
        
#testing create_instance when user selects Additional Course Conversion Form to fill
def test_create_instance_additional_course_conversion_form(client):
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Additional_Course_Conversion_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             print('context=',context)
             assert template.name == 'new_form.html'
             assert 'Additional Course Conversion Form' == context['form_name']
             assert 16==len(context['col_names'])

#testing create_instance when user selects Leave Form to fill
def test_create_instance_Leave_Form(client):
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Leave_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             print('context=',context)
             assert template.name == 'new_form.html'
             assert 'Leave Form' == context['form_name']
             assert 13==len(context['col_names'])

#testing create_instance when user selects JRF to SRF conversion Form to fill
def test_create_instance_JRF_to_SRF_conversion_Form(client):
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='JRF_to_SRF_conversion_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             print('context=',context)
             assert template.name == 'new_form.html'
             assert 'JRF to SRF conversion Form' == context['form_name']
             assert 16==len(context['col_names'])

#testing create_instance when user selects Guide Consent Form to fill
def test_create_instance_Guide_Consent_Form(client):
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Guide_Consent_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             print('context=',context)
             assert template.name == 'new_form.html'
             assert 'Guide Consent Form' == context['form_name']
             assert 19==len(context['col_names'])

#testing create_instance when user selects Guide Change Consent Form to fill
def test_create_instance_Guide_Change_Consent_Form(client):
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Guide_Change_Consent_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             print('context=',context)
             assert template.name == 'new_form.html'
             assert 'Guide Change Consent Form' == context['form_name']
             assert 10==len(context['col_names'])

#testing create_instance when user selects Fellowship Form to fill
def test_create_instance_Fellowship_Form(client):
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Fellowship_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             print('context=',context)
             assert template.name == 'new_form.html'
             assert 'Fellowship Form' == context['form_name']
             assert 14==len(context['col_names'])