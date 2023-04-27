from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail,Message
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField,HiddenField,TextAreaField, IntegerField, BooleanField,RadioField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileRequired
from flask_bootstrap import Bootstrap
from markupsafe import Markup


app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'your secret key'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cs20btech11035@iith.ac.in'
app.config['MAIL_PASSWORD'] = 'fgbboncngfheozws'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = 'your secret key'
sender_mail = "cs20btech11035@iith.ac.in"
sender_password = "fgbboncngfheozws"

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="test"
        )
cursor = mydb.cursor()

forms_dictionary = {
    '1' : "Addtional Course Conversion",
    '2' : "Leave form"
}

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    session['loggedin'] = False
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        user=request.form['user']
        if user=='Student':
            query = 'SELECT * FROM studentlogin WHERE email = %s AND password = %s'
            cursor.execute(query, (email, password))
            user_account = cursor.fetchone()
            print(user_account)
            homepage='studenthomepage.html'
        elif user=='Admin':
            query='SELECT * FROM adminlogin WHERE email = % s AND password = % s'
            cursor.execute(query, (email, password))
            user_account = cursor.fetchone()
            homepage='adminhomepage.html'
        if user_account:
            session['loggedin'] = True
            session['id'] = user_account[0]
            session['email'] = user_account[3]
            session['rollno'] = user_account[4]
            message = 'Logged in successfully !'
            return render_template(homepage, message = message)
        else:
            message = 'Invalid credentials. Try again.'
    return render_template('login.html', message = message)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        rollno = request.form['rollno']
        department = request.form['department']
        # cursor = mysql.connection.cursor(cursor.DictCursor)
        values = (str(email), )
        cursor.execute('SELECT * FROM studentlogin WHERE email = %s', values)
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO studentlogin (name,password,email,rollno,department) VALUES (%s,%s, %s, %s, %s)', (username, password, email, rollno, department))
            mydb.commit()
            print("You came here")
            msg = 'You have successfully registered !'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', message = msg)

@app.route('/homepage')
def homepage():
    if session['loggedin']==False:
        return redirect(url_for('login', message='Please login to continue !'))
    if session['id'] and session['email']:
        return render_template('studenthomepage.html')
    else:
        return redirect(url_for('login'))


@app.route('/formlist')
def formlist():
    if session['loggedin']==False:
        return redirect(url_for('login'))
    session['forms'] = forms_dictionary
    return render_template('formslist.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

class AdditionalCourseConversionFormdetails(FlaskForm):
    Form_type = HiddenField('Form_type')
    StudentName = StringField(label='StudentName', validators=[DataRequired()])
    RollNo = StringField(label='RollNo', validators=[DataRequired()])
    Department = StringField(label='Department', validators=[DataRequired()])
    CourseName1 = StringField(label='CourseName1', validators=[DataRequired()])
    CourseNumber1 = StringField(label='CourseNumber1', validators=[DataRequired()])
    Credits1 = IntegerField(label='Credits1', validators=[DataRequired()])
    Semester1 = IntegerField(label='Semester1', validators=[DataRequired()])
    CourseName2 = StringField(label='CourseName2', validators=[DataRequired()])
    CourseNumber2 = StringField(label='CourseNumber2', validators=[DataRequired()])
    Credits2 = IntegerField(label='Credits2', validators=[DataRequired()])
    Semester2 = IntegerField(label='Semester2', validators=[DataRequired()])
    Guidemail = StringField(label='Guidemail', validators=[DataRequired(), Email(granular_message=True)])
    HoDmail = StringField(label='HoDmail', validators=[DataRequired(), Email(granular_message=True)])
    Registrarmail = StringField(label='Registrarmail', validators=[DataRequired(), Email(granular_message=True)])
    Deanmail = StringField(label='Deanmail', validators=[DataRequired(), Email(granular_message=True)])
    # submit = SubmitField(label="submit")


class AdditionalCourseConversionForm:

    def create_instance():
        cform=AdditionalCourseConversionFormdetails(request.values,Form_type="1")
        return render_template('form.html',form=cform)

    def save_instance(dict):
        dict={key: val for key,val in dict.items() if key!='csrf_token'}
        query2 = 'INSERT INTO submittedforms (formtype,rollno,status) VALUES (%s,%s,%s)'
        values2 = (
            dict['Form_type'],
            dict['RollNo'],
            0
        )
        cursor.execute(query2,values2)
        mydb.commit()

        query3 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
        values3 = (dict['RollNo'],dict['Form_type'])
        cursor.execute(query3,values3)
        records = cursor.fetchall()
        row = records[-1]
        form_id = row[0]

        query1 = 'INSERT INTO additionalcourseconversion VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values1 = (
            form_id,
            dict['StudentName'],
            dict['RollNo'],
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
        cursor.execute(query1, values1)
        mydb.commit()
        msg = Message(
        "Additional Course Conversion Form Approval",
        sender = sender_mail,
        recipients= [dict['Guidemail']])
        msg.html=render_template('template1.html',details=dict,form_id=form_id,approvelevel=0)
        mail.send(msg)
        return render_template('studenthomepage.html', message ='mail sent to first approver')
    

    def update_instance(form_id,action):
        if action=='2':
             
             query2 = 'UPDATE submittedforms SET status=%s WHERE id=%s'
             values2 = (action,int(form_id))
             cursor.execute(query2,values2)
             mydb.commit()

             query = 'SELECT * from submittedforms where id=%s'
             values = [int(form_id)]
             cursor.execute(query,values)
             records = cursor.fetchall()
             row = records[-1]
             student_mail = row[2]+'@iith.ac.in'
             msg = Message("Additional Course Conversion Form Rejected",
                           sender = sender_mail,
                           recipients= [student_mail])
             msg.body="Your Additional Course Conversion Form is rejected"
             mail.send(msg)
             ret="form rejected."
        elif action=='1':
             query = 'SELECT * from additionalcourseconversion where id=%s'
             values = [int(form_id)]
             cursor.execute(query,values)
             records = cursor.fetchall()
             row = records[-1]
             approvelevel = int(row[-1])+1


             query1='UPDATE additionalcourseconversion set approvelevel=%s WHERE id=%s'
             values1=(approvelevel,int(form_id))
             cursor.execute(query1,values1)
             mydb.commit()
             if approvelevel==4:
                 query2 = 'UPDATE submittedforms SET status=%s WHERE id=%s'
                 values2 = (action,int(form_id))
                 cursor.execute(query2,values2)
                 mydb.commit()


                 query = 'SELECT * from submittedforms where id=%s'
                 values = [int(form_id)]
                 cursor.execute(query,values)
                 records = cursor.fetchall()
                 row = records[-1]
                 student_mail = row[2]+'@iith.ac.in'
                 msg = Message("Additional Course Conversion Form Approved",
                               sender = sender_mail,
                               recipients= [student_mail])
                 msg.body="Your Additional Course Conversion Form is approved."
                 mail.send(msg)
                 ret="completed approval."
             else:
                 query = 'SELECT * from additionalcourseconversion where id=%s'
                 values = [int(form_id)]
                 cursor.execute(query,values)
                 req_dict = [dict(line) for line in [zip([column[0] for column in cursor.description],row) for row in cursor.fetchall()]]
                 
                 cursor.execute(query,values)
                 records = cursor.fetchall()
                 row = records[-1]
                 approver_mail = row[11+approvelevel]
                 msg = Message("Additional Course Conversion Form Approval",
                               sender = sender_mail,
                               recipients= [approver_mail])
                 msg.html=render_template('template1.html',details=req_dict[0],form_id=form_id,approvelevel=approvelevel)
                 mail.send(msg)
                 ret="sent mail to next person."
        return ret

class LeaveFormdetails(FlaskForm):
    Form_type = HiddenField('Form_type')
    StudentName = StringField(label='StudentName', validators=[DataRequired()])
    RollNo = StringField(label='RollNo', validators=[DataRequired()])
    semester = IntegerField(label='semester', validators=[DataRequired()])
    leavefrom = StringField(label='leavefrom', validators=[DataRequired()])
    leaveto = StringField(label='leaveto', validators=[DataRequired()])
    noofdays = IntegerField(label='noofdays', validators=[DataRequired()])
    reason = StringField(label='reason', validators=[DataRequired()])
    phone = StringField(label='phone', validators=[DataRequired()])
    proof = FileField()
    Guidemail = StringField(label='Guidemail', validators=[DataRequired(), Email(granular_message=True)])
    HoDmail = StringField(label='HoDmail', validators=[DataRequired(), Email(granular_message=True)])
    DAmail = StringField(label='DAmail', validators=[DataRequired(), Email(granular_message=True)])
    # submit = SubmitField(label="submit")

class LeaveForm:

    def create_instance():
        cform=LeaveFormdetails(request.values,Form_type="2")
        return render_template('form.html',form=cform)
    
    def save_instance(dict):
        dict={key: val for key,val in dict.items() if key!='csrf_token'}
        query2 = 'INSERT INTO submittedforms (formtype,rollno,status) VALUES (%s,%s,%s)'
        values2 = (
            dict['Form_type'],
            dict['RollNo'],
            0
        )
        cursor.execute(query2,values2)
        mydb.commit()

        query3 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
        values3 = (dict['RollNo'],dict['Form_type'])
        cursor.execute(query3,values3)
        records = cursor.fetchall()
        row = records[-1]
        form_id = row[0]

        query1 = 'INSERT INTO leaveform VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values1 = (
            form_id,
            dict['StudentName'],
            dict['RollNo'],
            int(dict['semester']),
            dict['leavefrom'],
            dict['leaveto'],
            int(dict['noofdays']),
            dict['reason'],
            dict['phone'],
            dict['Guidemail'],
            dict['HoDmail'],
            dict['DAmail'],
            0
        )
        cursor.execute(query1, values1)
        mydb.commit()
        msg = Message(
        "Leave Form Approval",
        sender = sender_mail,
        recipients= [dict['Guidemail']])
        msg.html=render_template('template1.html',details=dict,form_id=form_id,approvelevel=0)
        mail.send(msg)
        return render_template('studenthomepage.html', message ='mail sent to first approver')
    

    def update_instance(form_id,action):
        if action=='2':
             
             query2 = 'UPDATE submittedforms SET status=%s WHERE id=%s'
             values2 = (action,int(form_id))
             cursor.execute(query2,values2)
             mydb.commit()

             query = 'SELECT * from submittedforms where id=%s'
             values = [int(form_id)]
             cursor.execute(query,values)
             records = cursor.fetchall()
             row = records[-1]
             student_mail = row[2]+'@iith.ac.in'
             msg = Message("Leave Form Rejected",
                           sender = sender_mail,
                           recipients= [student_mail])
             msg.body="Your Leave Form is rejected"
             mail.send(msg)
             ret="form rejected."
        elif action=='1':
             query = 'SELECT * from leaveform where id=%s'
             values = [int(form_id)]
             cursor.execute(query,values)
             records = cursor.fetchall()
             row = records[-1]
             approvelevel = int(row[-1])+1


             query1='UPDATE leaveform set approvelevel=%s WHERE id=%s'
             values1=(approvelevel,int(form_id))
             cursor.execute(query1,values1)
             mydb.commit()
             if approvelevel==3:
                 query2 = 'UPDATE submittedforms SET status=%s WHERE id=%s'
                 values2 = (action,int(form_id))
                 cursor.execute(query2,values2)
                 mydb.commit()


                 query = 'SELECT * from submittedforms where id=%s'
                 values = [int(form_id)]
                 cursor.execute(query,values)
                 records = cursor.fetchall()
                 row = records[-1]
                 student_mail = row[2]+'@iith.ac.in'
                 msg = Message("leave Form Approved",
                               sender = sender_mail,
                               recipients= [student_mail])
                 msg.body="Your leave Form is approved."
                 mail.send(msg)
                 ret="completed approval."
             else:
                 query = 'SELECT * from leaveform where id=%s'
                 values = [int(form_id)]
                 cursor.execute(query,values)
                 req_dict = [dict(line) for line in [zip([column[0] for column in cursor.description],row) for row in cursor.fetchall()]]
                 
                 cursor.execute(query,values)
                 records = cursor.fetchall()
                 row = records[-1]
                 approver_mail = row[9+approvelevel]
                 msg = Message("leave Form Approval",
                               sender = sender_mail,
                               recipients= [approver_mail])
                 msg.html=render_template('template1.html',details=req_dict[0],form_id=form_id,approvelevel=approvelevel)
                 mail.send(msg)
                 ret="sent mail to next person."
        return ret

    
def Factory(forms = '1'):
    forms_dict = {'1' : AdditionalCourseConversionForm,
                  '2' : LeaveForm}
    return forms_dict[forms]

@app.route('/create_instance',methods=['GET','POST'])
def create_instance():
    if session['loggedin']==False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        form_obj = Factory(request.form['Form_type'])
    return form_obj.create_instance()   

@app.route('/save_instance',methods = ['GET','POST'])
def save_instance():
    if session['loggedin']==False:
        return redirect(url_for('login'))
    if request.method == "POST":
        form_obj = Factory(request.form['Form_type'])
        print('form type=',request.form['Form_type'])
    return form_obj.save_instance(request.form)


@app.route('/form_handling',methods = ['GET','POST'])
def form_handling():
    if request.method == "POST":
        form_id=request.form['form_id']
        action=request.form['approve']
        query1 = 'SELECT * from submittedforms where id = %s'
        values1 = [int(form_id)]
        cursor.execute(query1,values1)
        records = cursor.fetchall()
        row = records[-1]
        form_type=row[1]
        form_obj = Factory(str(form_type))
    return form_obj.update_instance(form_id,action)

forms_tables={1 : 'additionalcourseconversion',
              2 : 'leaveform'}

@app.route('/approve/<form_id>/<approvelevel>')
def approve(form_id,approvelevel):
    query1 = 'SELECT * from submittedforms where id=%s'
    values1 = [int(form_id)]
    cursor.execute(query1,values1)
    records = cursor.fetchall()
    row = records[-1]
    form_type=row[1]
    status=row[-1]
    #print('form_type=',form_type,type(form_type))
    table=forms_tables[form_type]
    query = 'SELECT * from '+table+' where id=%s'
    values = [int(form_id)]
    cursor.execute(query,values)
    records = cursor.fetchall()
    row = records[-1]
    current_approvelevel = row[-1]
    print(type(current_approvelevel),type(approvelevel))
    if current_approvelevel==approvelevel and status!='2':
        return render_template('approve.html',form_id=form_id,approvelevel=approvelevel)
    return "already responded"
    

@app.route('/submitted_forms')
def submitted_forms():
    #getting all the forms submitted by him from submitted forms table.
    if session['loggedin']==False:
        return redirect(url_for('login'))
    query = 'SELECT * from submittedforms WHERE rollno = %s'
    values = [session['rollno']]
    cursor.execute(query,values)
    records = cursor.fetchall()
    # len = len(records)
    dict_status = {
        '0' : 'pending',
        '1' : 'accepted',
        '2' :'rejected'
    }
    return render_template("history.html",records = records,dict_status = dict_status)

@app.route('/expanded_history/<form_id>/<form_type>')
def expanded_history(form_id,form_type):
    dict_form_type = {
        '1' : 'additionalcourseconversion'
    }
    query = 'SELECT * from ' +dict_form_type[form_type]+' WHERE id = %s'
    values = [form_id]
    cursor.execute(query,values)
    row = [dict(line) for line in [zip([column[0] for column in cursor.description],row) for row in cursor.fetchall()]]
    #finding status
    query = "SELECT status from submittedforms where id = %s"
    values = [form_id]
    cursor.execute(query,values)
    status = cursor.fetchone()
    status = int(status[-1])
    #finding who accepted and who rejected
    '''
    if status is rejected then till approver level everyone accepted
    if status is accepted then everyone accepted
    if status is pending then everyone till approver level accepted remaining pending
    '''
    approve_level = int(row[0]['approvelevel'])
    return render_template("expanded.html",row = row[0],status = status,approve_level = approve_level)


if __name__=="__main__":
    app.run(debug=True)