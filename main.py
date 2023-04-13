from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
import MySQLdb.cursors
import re
import smtplib
import mysql.connector
 
 
app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vasisht@27'
app.config['MYSQL_DB'] = 'SWE'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cs20btech11035@iith.ac.in'
app.config['MAIL_PASSWORD'] = 'fgbboncngfheozws'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
mysql2 = MySQL(app)

sender_mail = "teamswe30@gmail.com"
sender_password = "txaxmstjnwhwofpi"

forms_dictionary = {
    '1' : "Addtional Course Conversion",
    '2' : "Assessment Commitee form"
}


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user=request.form['user']
        cursor = mysql2.connection.cursor(MySQLdb.cursors.DictCursor)
        if user=='Student':
            cursor.execute('SELECT * FROM studentlogin WHERE username = % s AND password = % s', (username, password, ))
            user_account = cursor.fetchone()
            homepage='studenthomepage.html'
        elif user=='Admin':
            cursor.execute('SELECT * FROM adminlogin WHERE username = % s AND password = % s', (username, password, ))
            user_account = cursor.fetchone()
            homepage='adminhomepage.html'
        if user_account:
            session['loggedin'] = True
            session['id'] = user_account['id']
            session['username'] = user_account['username']
            message = 'Logged in successfully !'
            return render_template(homepage, message = message)
        else:
            message = 'Invalid credentials. Try again.'
    return render_template('login.html', message = message)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/formlist')
def formlist():
    return render_template('formslist.html')

@app.route('/create_forms',methods = ['GET','POST'])
def create_forms():
    if request.method == 'POST' and 'Form_type' in request.form:
        session['formname'] = forms_dictionary[request.form['Form_type']]
    return render_template('additionalcourseconversion.html')

@app.route('/process_form',methods = ['GET','POST'])
def process_form():
    msg = Message(
        request.form['subject'],
        sender = sender_mail,
        recipients= [request.form['email']]
    )
    msg.body = request.form['message']
    mail.send(msg)
    return 'sent'


class AdditionalCourseConversionForm:
    def create_instance():
        return render_template('additionalcourseconversion.html')
    def save_instance(dict):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vasisht@27",
        database="SWE"
        )
        query2 = 'INSERT INTO submittedforms (formtype,rollno,status) VALUES (%s,%s,%s)'
        values2 = (
            dict['Form_type'],
            dict['RollNo'],
            0
        )
        mycursor = mydb.cursor()
        mycursor.execute(query2,values2)
        mydb.commit()
        query3 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
        values3 = (dict['RollNo'],dict['Form_type'])
        mycursor.execute(query3,values3)
        records = mycursor.fetchall()
        row = records[-1]
        form_id = row[0]
        query1 = 'INSERT INTO additionalcourseconversion VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        values1 = (
            form_id,
            dict['CourseName1'],
            dict['CourseNumber1'],
            int(dict['Credits1']),
            int(dict['Semester1']),
            dict['CourseName2'],
            dict['CourseNumber2'],
            int(dict['Credits2']),
            int(dict['Semester2']),
            dict['Guidemail'],
            dict['HoDmail'],
            dict['Registrarmail'],
            dict['Deanmail'],
            0
        )
        mycursor.execute(query1, values1)
        mydb.commit()
        return "Form submitted"

def Factory(forms = '1'):
    forms_dict = {'1' : AdditionalCourseConversionForm}
    return forms_dict[forms]

@app.route('/create_instance',methods=['GET','POST'])
def create_instance():
    if request.method == 'POST':
        form_obj = Factory(request.form['Form_type'])
    return form_obj.create_instance()   

@app.route('/save_instance',methods = ['GET','POST'])
def save_instance():
    if request.method == "POST":
        form_obj = Factory(request.form['Form_type'])
    return form_obj.save_instance(request.form)





    



if __name__=="__main__":
    app.run(debug=True)