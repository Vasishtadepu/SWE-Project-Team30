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
import requests

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
database="test2"
password="2312"

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
    conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM studentlogin WHERE email = 'cs20btech11055@iith.ac.in'")
    account = cur.fetchone()
    assert account
    cur.execute("DELETE FROM studentlogin WHERE email='cs20btech11055@iith.ac.in' ")
    conn.commit()
    cur.close()
    conn.close()

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
            sess['id']='1'
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
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
        # client.get('/')
      with captured_templates(app) as templates:
             response = client.get('/logout',follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             assert template.name == 'login.html'

#testing case when user tries to open create_instance without logging in
def test_create_instance_without_login(client):
        with client.session_transaction() as sess:
            sess['loggedin']=False
        # client.get('/')
        with captured_templates(app) as templates:
            response = client.get('/create_instance',follow_redirects=True)
            assert response.status_code == 200
            template, context = templates[0]
            assert template.name == 'login.html'

#testing create_instance when user selects Additional Course Conversion Form to fill
def test_create_instance_Additional_Course_Conversion_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Additional_Course_Conversion_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             assert template.name == 'new_form.html'
             assert 'Additional_Course_Conversion_Form' == context['form_name']
             assert 14==len(context['col_names'])

#testing create_instance when user selects Leave Form to fill
def test_create_instance_Leave_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Leave_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             assert template.name == 'new_form.html'
             assert 'Leave_Form' == context['form_name']
             assert 11==len(context['col_names'])

#testing create_instance when user selects JRF to SRF conversion Form to fill
def test_create_instance_JRF_to_SRF_conversion_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='JRF_to_SRF_conversion_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             assert template.name == 'new_form.html'
             assert 'JRF_to_SRF_conversion_Form' == context['form_name']
             assert 14==len(context['col_names'])

#testing create_instance when user selects Guide Consent Form to fill
def test_create_instance_Guide_Consent_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Guide_Consent_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             assert template.name == 'new_form.html'
             assert 'Guide_Consent_Form' == context['form_name']
             assert 17==len(context['col_names'])

#testing create_instance when user selects Guide Change Consent Form to fill
def test_create_instance_Guide_Change_Consent_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Guide_Change_Consent_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             assert template.name == 'new_form.html'
             assert 'Guide_Change_Consent_Form' == context['form_name']
             assert 8==len(context['col_names'])

#testing create_instance when user selects Fellowship Form to fill
def test_create_instance_Fellowship_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
             response = client.get('/create_instance',data=dict(Form_type='Fellowship_Form'),follow_redirects=True)
             assert response.status_code == 200
             template, context = templates[0]
             assert template.name == 'new_form.html'
             assert 'Fellowship_Form' == context['form_name']
             assert 12==len(context['col_names'])
    
#testing case when user tries to open save_instance without logging in
def test_save_instance_without_login(client):
        with client.session_transaction() as sess:
            sess['loggedin']=False
        # client.get('/')
        with captured_templates(app) as templates:
            response = client.get('/save_instance',follow_redirects=True)
            assert response.status_code == 200
            template, context = templates[0]
            assert template.name == 'login.html'

#testing save_instance when student submits Additional Course Conversion Form
def test_save_instance_Additional_Course_Conversion_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
          response = client.get(
                '/save_instance',data=dict(table_name='Additional_Course_Conversion_Form',Name='Manaswini',Roll_No='CS20BTECH11035',
                                            Course1='SWE',Course_Number1='CS4443',Credits1='3',Semester1='6',Course2='Fraud Analytics',
                                            Course_Number2='CS6890', Credits2='3',Semester2='6',Guide_Name= 'Dr.Ramakrishna Upadrasta',
                                            HoD_Name= 'Subramanyam Kalyansundaram',Guide_Mail ='manaswininyalapogula@gmail.com',HoD_Mail='manaswininyalapogula@gmail.com',
                                            Deputy_Registrar_Mail='manaswininyalapogula@gmail.com',Dean_Mail='manaswininyalapogula@gmail.com'
                                            ),follow_redirects=True)
          assert response.status_code == 200
          template, context = templates[-1]
          template1, context1 = templates[0]
          assert template1.name == 'template1.html'
          assert template.name == 'studenthomepage.html'
          assert 'mail sent to first approver' == context['message']
          conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
          cur = conn.cursor()
          query2 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
          values2 = ('CS20BTECH11035','Additional_Course_Conversion_Form')
          cur.execute(query2,values2)
          records = cur.fetchall()
          row = records[-1]
          form_id = row[0]
          cur.execute("SELECT * FROM Additional_Course_Conversion_Form WHERE id =%s",(str(form_id),))
          account = cur.fetchone()
          assert account
          cur.close()
          conn.close()


#testing save_instance when student submits Leave Form
def test_save_instance_Leave_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
          response = client.get(
                '/save_instance',data=dict(table_name='Leave_Form',Name='Manaswini',Roll_No='CS20BTECH11035',
                                            Semester='6',Leave_from='2/5/2023',Leave_to='10/5/2023',No_of_days='9',
                                            Reason='Health issues',Phone='6305238950',Guide_Name= 'Dr.Ramakrishna Upadrasta',
                                            HoD_Name= 'Subramanyam Kalyansundaram',Guide_Mail ='manaswininyalapogula@gmail.com',HoD_Mail='manaswininyalapogula@gmail.com',
                                            Dealing_Assistant_Mail='manaswininyalapogula@gmail.com'
                                            ),follow_redirects=True)
          assert response.status_code == 200
          template, context = templates[-1]
          template1, context1 = templates[0]
          assert template1.name == 'template1.html'
          assert template.name == 'studenthomepage.html'
          assert 'mail sent to first approver' == context['message']
          conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
          cur = conn.cursor()
          query2 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
          values2 = ('CS20BTECH11035','Leave_Form')
          cur.execute(query2,values2)
          records = cur.fetchall()
          row = records[-1]
          form_id = row[0]
          cur.execute("SELECT * FROM Leave_Form WHERE id =%s",(str(form_id),))
          account = cur.fetchone()
          assert account
          cur.close()
          conn.close()


#testing save_instance when student submits JRF to SRF conversion Form
def test_save_instance_JRF_to_SRF_conversion_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
          response = client.get(
                '/save_instance',data=dict(table_name='JRF_to_SRF_conversion_Form',Name='Manaswini',Roll_No='CS20BTECH11035',
                                            Joining_Date='2/5/2021',Department='CSE',External_Member_Name='Dr.Ramu' ,Guide_Name= 'Dr.Ramakrishna Upadrasta',
                                            HoD_or_Dean_Name= 'Subramanyam Kalyansundaram',Date_of_Assessment='5/5/2023',Time='2pm', Venue='Auditorium',
                                            Assessment_of_committee='accepted',External_Member_Mail='manaswininyalapogula@gmail.com',
                                            Guide_Mail ='manaswininyalapogula@gmail.com',HoD_Mail='manaswininyalapogula@gmail.com',
                                            Deputy_Registrar_Mail='manaswininyalapogula@gmail.com',Dean_Mail='manaswininyalapogula@gmail.com'
                                            ),follow_redirects=True)
          assert response.status_code == 200
          template, context = templates[-1]
          template1, context1 = templates[0]
          assert template1.name == 'template1.html'
          assert template.name == 'studenthomepage.html'
          assert 'mail sent to first approver' == context['message']
          conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
          cur = conn.cursor()
          query2 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
          values2 = ('CS20BTECH11035','JRF_to_SRF_conversion_Form')
          cur.execute(query2,values2)
          records = cur.fetchall()
          row = records[-1]
          form_id = row[0]
          cur.execute("SELECT * FROM JRF_to_SRF_conversion_Form WHERE id =%s",(str(form_id),))
          account = cur.fetchone()
          assert account
          cur.close()
          conn.close()


#testing save_instance when student submits Guide Change Consent Form
def test_save_instance_Guide_Change_Consent_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
          response = client.get(
                '/save_instance',data=dict(table_name='Guide_Change_Consent_Form',Name='Manaswini',Roll_No='CS20BTECH11035',
                                            Department='CSE',Present_Guide_Name='Dr.Ramu' ,Proposed_Guide_Name= 'Dr.Ramakrishna Upadrasta',
                                            HoD_Name= 'Subramanyam Kalyansundaram',Present_Guide_Mail='manaswininyalapogula@gmail.com',
                                            Proposed_Guide_Mail ='manaswininyalapogula@gmail.com',
                                            Deputy_Registrar_Mail='manaswininyalapogula@gmail.com',Dean_Mail='manaswininyalapogula@gmail.com'
                                            ),follow_redirects=True)
          assert response.status_code == 200
          template, context = templates[-1]
          template1, context1 = templates[0]
          assert template1.name == 'template1.html'
          assert template.name == 'studenthomepage.html'
          assert 'mail sent to first approver' == context['message']
          conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
          cur = conn.cursor()
          query2 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
          values2 = ('CS20BTECH11035','Guide_Change_Consent_Form')
          cur.execute(query2,values2)
          records = cur.fetchall()
          row = records[-1]
          form_id = row[0]
          cur.execute("SELECT * FROM Guide_Change_Consent_Form WHERE id =%s",(str(form_id),))
          account = cur.fetchone()
          assert account
          cur.close()
          conn.close()

#testing save_instance when student submits Guide Consent Form
def test_save_instance_Guide_Consent_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
          response = client.get(
                '/save_instance',data=dict(table_name='Guide_Consent_Form',Name='Manaswini',Roll_No='CS20BTECH11035',
                                           Joining_Date='2/5/2021',Department='CSE',Choose_the_supervisor_at_end_or_at_last_of_first_Semester='first' ,
                                           Faculty1_Name= 'Dr.Ramakrishna Upadrasta', Faculty2_Name= 'Dr.Ramakrishna Upadrasta', Faculty3_Name= 'Dr.Ramakrishna Upadrasta',
                                           Faculty4_Name= 'Dr.Ramakrishna Upadrasta',Faculty5_Name= 'Dr.Ramakrishna Upadrasta',
                                           Guide_Mail='manaswininyalapogula@gmail.com',
                                            CoGuide_Mail ='manaswininyalapogula@gmail.com',
                                            DPGC_Mail='manaswininyalapogula@gmail.com',HoD_Mail='manaswininyalapogula@gmail.com',
                                            Faculty1_Mail='manaswininyalapogula@gmail.com', Faculty2_Mail='manaswininyalapogula@gmail.com',Faculty3_Mail='manaswininyalapogula@gmail.com',
                                            Faculty4_Mail='manaswininyalapogula@gmail.com',Faculty5_Mail='manaswininyalapogula@gmail.com'
                                            ),follow_redirects=True)
          assert response.status_code == 200
          template, context = templates[-1]
          template1, context1 = templates[0]
          assert template1.name == 'template1.html'
          assert template.name == 'studenthomepage.html'
          assert 'mail sent to first approver' == context['message']
          conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
          cur = conn.cursor()
          query2 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
          values2 = ('CS20BTECH11035','Guide_Consent_Form')
          cur.execute(query2,values2)
          records = cur.fetchall()
          row = records[-1]
          form_id = row[0]
          cur.execute("SELECT * FROM Guide_Consent_Form WHERE id =%s",(str(form_id),))
          account = cur.fetchone()
          assert account
          cur.close()
          conn.close()

#testing save_instance when student submits Fellowship Form
def test_save_instance_Fellowship_Form(client):
     with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
     with captured_templates(app) as templates:
          response = client.get(
                '/save_instance',data=dict(table_name='Fellowship_Form',Name='Manaswini',Roll_No='CS20BTECH11035',
                                            Department='CSE',Joining_Year='2004',Stream='PHD', Scholarship_Month='5',
                                            Number_of_Days_Attended='30', Amount_of_Stipend='10,000 rupees',
                                            Scholarship_Type='CSIR', Project='CPS', Supervisor_Name='Dr.Aravind',
                                            Faculty_Name='Dr.Karteek',Supervisor_Mail='manaswininyalapogula@gmail.com',Faculty_Mail ='manaswininyalapogula@gmail.com'
                                            ),follow_redirects=True)
          assert response.status_code == 200
          template, context = templates[-1]
          template1, context1 = templates[0]
          assert template1.name == 'template1.html'
          assert template.name == 'studenthomepage.html'
          assert 'mail sent to first approver' == context['message']
          conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
          cur = conn.cursor()
          query2 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
          values2 = ('CS20BTECH11035','Fellowship_Form')
          cur.execute(query2,values2)
          records = cur.fetchall()
          row = records[-1]
          form_id = row[0]
          cur.execute("SELECT * FROM Fellowship_Form WHERE id =%s",(str(form_id),))
          account = cur.fetchone()
          assert account
          cur.close()
          conn.close()

#testing case student's form gets rejected
def test_update_instance_reject(client):
      with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
      response = client.post('/update_instance', data=dict(form_id='1',approve='2'), follow_redirects=True)
      conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
      cur = conn.cursor()
      query = 'SELECT * from submittedforms where id=%s'
      values = [1,]
      cur.execute(query,values)
      records = cur.fetchall()
      row = records[-1]
      status=int(row[-1])
      cur.close()
      conn.close()
      assert status==2
      assert response.status_code == 200
      assert b'form rejected.' in response.data


#testing save_instance when one approver approves and mails needs to be sent to next approver
def test_update_instance_next_approver(client):
      with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
      response = client.post('/update_instance', data=dict(form_id='2',approve='1'), follow_redirects=True)
      conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
      cur = conn.cursor()
      query = 'SELECT * from submittedforms where id=%s'
      values = [2,]
      cur.execute(query,values)
      records = cur.fetchall()
      row = records[-1]
      status=int(row[-1])
      query = 'SELECT * from Leave_Form where id=%s'
      values = [2,]
      cur.execute(query,values)
      records = cur.fetchall()
      row = records[-1]
      cur.close()
      conn.close()
      assert status==0
      assert response.status_code == 200
      assert b'sent mail to next person.' in response.data


#testing save_instance when one approver approves and mails needs to be sent to student that form is approved.
def test_update_instance_completed(client):
      with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
      conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
      cur = conn.cursor()
      query = 'SELECT * from submittedforms where id=%s'
      values = [1,]
      cur.execute(query,values)
      records = cur.fetchall()
      row = records[-1]
      table_name=row[1]
      status=int(row[-1])
      
      if status!=0:
            query = 'UPDATE submittedforms set status=%s where id=%s'
            values = ['0',1]
            cur.execute(query,values)
            conn.commit()
    #   query = 'SELECT * from forms_table where table_name=%s'
    #   values = [table_name,]
    #   cur.execute(query,values)
    #   records = cur.fetchall()
    #   row = records[-1]
    #   no_of_approvers=int(row[-1])
    #   query = 'SELECT * from '+table_name+' where id=%s'
    #   values = [1,]
    #   cur.execute(query,values)
    #   records = cur.fetchall()
    #   row = records[-1]
    #   approvelevel = int(row[-1])
    #   if approvelevel!=no_of_approvers-1:
    #         print('appp=',approvelevel,no_of_approvers)
            
    #         query1='UPDATE '+table_name+' set approvelevel = %s WHERE id = %s'
    #         values1=(str(no_of_approvers-1),1)
    #         print(values1)
    #         cur.execute(query1,values1)
    #         conn.commit()
            
    #   cur.close()
    #   conn.close()
    #   conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
    #   cur = conn.cursor()
    #   query2 = 'select * from '+table_name + ' where id = %s'
    #   values2 = [1]
    #   cur.execute(query2,values2)
    #   row = cur.fetchall()[-1][-1]
    #   print("approverlevel before update = ",row)
    #   cur.close()
    #   conn.close()
      response = client.post('/update_instance', data=dict(form_id='1',approve='1'), follow_redirects=True)
      response = client.post('/update_instance', data=dict(form_id='1',approve='1'), follow_redirects=True)
      response = client.post('/update_instance', data=dict(form_id='1',approve='1'), follow_redirects=True)
      response = client.post('/update_instance', data=dict(form_id='1',approve='1'), follow_redirects=True)
      conn = mysql.connector.connect(host="localhost",user="root",password=password,database=database)
      cur = conn.cursor()
      query = 'SELECT * from submittedforms where id=%s'
      values = [1,]
      cur.execute(query,values)
      records = cur.fetchall()
      row = records[-1]
      table_name=row[1]
      status=int(row[-1])
      cur.close()
      conn.close()
      assert b'completed approval.' in response.data
      assert status==1
      assert response.status_code == 200


#testing case when approver tries to approve a form that is already responded.
# def test_approve_responded(client):
#       with client.session_transaction() as sess:
#             sess['id']='1'
#             sess['name']='Manaswini'
#             sess['department']='CSE'
#             sess['email']='cs20btech11035@iith.ac.in'
#             sess['rollno']='CS20BTECH11035'
#             sess['loggedin']= True
#       response = requests.get('/approve/1/0')
#       assert b'already responded' in response.data


#testing case when user tries to open create_form without logging in
def test_create_form_admin(client):
        with client.session_transaction() as sess:
            sess['loggedin']=True
            sess['type']='Admin'
        # client.get('/')
        with captured_templates(app) as templates:
            response = client.get('/create_form',follow_redirects=True)
            assert response.status_code == 200
            template, context = templates[0]
            assert template.name == 'create_form.html'

#testing create_form 
def test_create_form_not_admin(client):
      with client.session_transaction() as sess:
            sess['id']='1'
            sess['name']='Manaswini'
            sess['department']='CSE'
            sess['email']='cs20btech11035@iith.ac.in'
            sess['rollno']='CS20BTECH11035'
            sess['loggedin']= True
            sess['type']='Student'
      with captured_templates(app) as templates:
          response = client.get('/create_form',follow_redirects=True)
          assert response.status_code == 200
          template, context = templates[-1]
          assert template.name == 'login.html'
           
      
      
        
      

