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
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'test'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cs20btech11035@iith.ac.in'
app.config['MAIL_PASSWORD'] = 'fgbboncngfheozws'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
mysql2 = MySQL(app)

sender_mail = "cs20btech11035@iith.ac.in"
sender_password = "fgbboncngfheozws"

forms_dictionary = {
    '1' : "Addtional Course Conversion",
    '2' : "Assessment Commitee form"
}


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        user=request.form['user']
        cursor = mysql2.connection.cursor(MySQLdb.cursors.DictCursor)
        if user=='Student':
            cursor.execute('SELECT * FROM studentlogin WHERE email = % s AND password = % s', (email, password, ))
            user_account = cursor.fetchone()
            homepage='studenthomepage.html'
        elif user=='Admin':
            cursor.execute('SELECT * FROM adminlogin WHERE email = % s AND password = % s', (email, password, ))
            user_account = cursor.fetchone()
            homepage='adminhomepage.html'
        if user_account:
            session['loggedin'] = True
            session['id'] = user_account['id']
            session['email'] = user_account['email']
            message = 'Logged in successfully !'
            return render_template(homepage, message = message)
        else:
            message = 'Invalid credentials. Try again.'
    return render_template('login.html', message = message)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))
 
@app.route('/formlist')
def formlist():
    session['forms'] = forms_dictionary
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
        password="1234",
        database="test"
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
        msg = Message(
        "Additional Course Conversion Form Approval",
        sender = sender_mail,
        recipients= [dict['Guidemail']])
        #msg.body="Follow this link to approve or deny. http://127.0.0.1:5000/approve/"+str(form_id)
        msg.html=render_template('template1.html',details=dict,form_id=form_id,approvelevel=0)
        mail.send(msg)
        return 'mail sent to first approver'
    def update_instance(form_id,action):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="test"
        )
        mycursor = mydb.cursor()
        if action=='2':
             query2 = 'UPDATE submittedforms SET status=%s WHERE id=%s'
             values2 = (action,int(form_id))
             
             mycursor.execute(query2,values2)
             mydb.commit()
             query = 'SELECT * from submittedforms where id=%s'
             values = [int(form_id)]
             mycursor.execute(query,values)
             records = mycursor.fetchall()
             row = records[-1]
             student_mail = row[2]+'@iith.ac.in'
             msg = Message("Additional Course Conversion Form Rejected",
                           sender = sender_mail,
                           recipients= [student_mail])
             #msg.body="Follow this link to approve or deny. http://127.0.0.1:5000/approve/"+str(form_id)
             msg.body="Your Additional Course Conversion Form is rejected"
             mail.send(msg)
             ret="form rejected."
        elif action=='1':
             query = 'SELECT * from additionalcourseconversion where id=%s'
             values = [int(form_id)]
             mycursor.execute(query,values)
             records = mycursor.fetchall()
             row = records[-1]
             approvelevel = int(row[-1])+1
             print(int(row[-1]),approvelevel)
             query1='UPDATE additionalcourseconversion set approvelevel=%s WHERE id=%s'
             values1=(approvelevel,int(form_id))
             
             mycursor.execute(query1,values1)
             mydb.commit()
             if approvelevel==4:
                 query2 = 'UPDATE submittedforms SET status=%s WHERE id=%s'
                 values2 = (action,int(form_id))
                 mycursor.execute(query2,values2)
                 mydb.commit()
                 query = 'SELECT * from submittedforms where id=%s'
                 values = [int(form_id)]
                 mycursor.execute(query,values)
                 records = mycursor.fetchall()
                 row = records[-1]
                 student_mail = row[2]+'@iith.ac.in'
                 msg = Message("Additional Course Conversion Form Approved",
                               sender = sender_mail,
                               recipients= [student_mail])
                 #msg.body="Follow this link to approve or deny. http://127.0.0.1:5000/approve/"+str(form_id)
                 msg.body="Your Additional Course Conversion Form is approved."
                 mail.send(msg)
                 ret="completed approval."
             else:
                 query = 'SELECT * from additionalcourseconversion where id=%s'
                 values = [int(form_id)]
                 mycursor.execute(query,values)
                 req_dict = [dict(line) for line in [zip([column[0] for column in mycursor.description],row) for row in mycursor.fetchall()]]
                 
                 mycursor.execute(query,values)
                 records = mycursor.fetchall()
                 row = records[-1]
                 approver_mail = row[9+approvelevel]
                 msg = Message("Additional Course Conversion Form Approval",
                               sender = sender_mail,
                               recipients= [approver_mail])
                 #msg.body="Follow this link to approve or deny. http://127.0.0.1:5000/approve/"+str(form_id)
                 msg.html=render_template('template1.html',details=req_dict[0],form_id=form_id,approvelevel=approvelevel)
                 mail.send(msg)
                 ret="sent mail to next person."
        return ret
                 
    

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


@app.route('/form_handling',methods = ['GET','POST'])
def form_handling():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="test"
        )
    mycursor = mydb.cursor()
    if request.method == "POST":
        form_id=request.form['form_id']
        action=request.form['approve']
        query1 = 'SELECT * from submittedforms where id = %s'
        values1 = [int(form_id)]
        mycursor.execute(query1,values1)
        records = mycursor.fetchall()
        row = records[-1]
        form_type=row[1]
        form_obj = Factory(str(form_type))
    return form_obj.update_instance(form_id,action)

@app.route('/approve/<form_id>')
def approve(form_id):
    return render_template('approve.html',form_id=form_id)
    



if __name__=="__main__":
    app.run(debug=True)