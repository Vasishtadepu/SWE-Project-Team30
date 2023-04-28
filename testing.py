# from new import app # Flask instance of the API

# def test_index_route():
#     response = app.test_client().get('/')
#     assert response.status_code == 200

import pytest
from new import app
import MySQLdb
import mysql.connector
import MySQLdb.cursors
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
            


def test_student_login_success(client):
    response = client.post('/login', data=dict(
        email='cs20btech11035@iith.ac.in',
        password='2312',
        user='Student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data

def test_admin_login_success(client):
    response = client.post('/login', data=dict(
        email='cs20btech11002@iith.ac.in',
        password='2711',
        user='Admin'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Hello admin' in response.data


def test_student_login_failure(client):
    response = client.post('/login', data=dict(
        email='cs20btech11035@iith.ac.in',
        password='2711',
        user='Student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid credentials. Try again.' in response.data

def test_admin_login_failure(client):
    response = client.post('/login', data=dict(
        email='cs20btech11035@iith.ac.in',
        password='2312',
        user='Admin'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid credentials. Try again.' in response.data

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

def test_new_student_missing_details_register(client):
    response = client.post('/register', data=dict(
        email='cs20btech11035@iith.ac.in',
        rollno='CS20BTECH11035',
        department='CSE',
        user='Student'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Please fill out the form !' in response.data


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
    cur.execute("DELETE FROM studentlogin WHERE email='cs20btech11055@iith.ac.in' ")
    conn.commit()