from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail,Message
import mysql.connector
import MySQLdb.cursors
import math


def encrypt(form_id):
    return form_id **2 + form_id

def decrypt(form_id):
    return int((-1 + math.sqrt(4*form_id+1))/2)

app = Flask(__name__)
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
        password="Vasisht@27",
        database="test2"
        )
cursor = mydb.cursor()


def get_forms():
    query = 'SELECT * from forms_table'
    cursor.execute(query)
    records = cursor.fetchall()
    dict = {}
    for row in records:
        dict[row[1]] = row[0]
    print(dict)
    return dict




#Implementing Login
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
            homepage='studenthomepage.html'
            session['type'] = "Student"
        elif user=='Admin':
            query='SELECT * FROM adminlogin WHERE email = %s AND password = %s'
            cursor.execute(query, (email, password))
            user_account = cursor.fetchone()
            homepage='adminhomepage.html'
            session['type'] = "Admin"
        if user_account and session['type'] == "Admin":
            session['loggedin'] = True
            session['id']=user_account[0]
            session['name'] = user_account[1]
            session['email'] = user_account[3]
            return render_template(homepage,message = "Hello admin")
        elif user_account and session['type'] == "Student":
            session['loggedin'] = True
            session['id'] = user_account[0]
            session['name'] = user_account[1]
            session['department'] = user_account[5]
            session['email'] = user_account[3]
            session['rollno'] = user_account[4]
            message = 'Logged in successfully !'
            return render_template(homepage, message = message)
        else:
            message = 'Invalid credentials. Try again.'
    return render_template('login.html', message = message)


#Implementing logout
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'department' in request.form and 'rollno' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        rollno = request.form['rollno']
        department = request.form['department']
        # cursor = mysql.connection.cursor(cursor.DictCursor)
        values = (str(email),)
        cursor.execute('SELECT * FROM studentlogin WHERE email = %s', values)
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not username or not password or not email or not rollno or not department:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO studentlogin (name,password,email,rollno,department) VALUES (%s,%s, %s, %s, %s)', (username, password, email, rollno, department))
            mydb.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', message = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    print(msg)
    return render_template('register.html', message = msg)

@app.route('/homepage')
def homepage():
    # print("Here")
    print(session)
    if session['loggedin']==False:
        return render_template('login.html', message='Please login to continue !')
    if session['type'] == 'Admin':
        return render_template('adminhomepage.html',message = "Hello admin")
    elif session['id'] and session['email']:
        return render_template('studenthomepage.html')
    
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    #session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session['loggedin']=False
    return render_template('login.html')


@app.route('/formlist')
def formlist():
    forms_dictionary = get_forms()
    if session['loggedin']==False:
        return redirect(url_for('login'))
    session['forms'] = forms_dictionary
    return render_template('formslist.html')


@app.route('/create_instance',methods = ['GET','POST'])
def create_instance():
    if session['loggedin']==False:
        return redirect(url_for('login'))
    table_name = request.form['Form_type']
    # print(table_name)
    #now we have table name we need to find the coloumns.
    query = 'SELECT * from ' + table_name
    cursor.execute(query)
    records = cursor.fetchall()
    col_names = [i[0] for i in cursor.description]
    #now we have a list of coloumn Names
    col_names = col_names[3:-1]
    return render_template('new_form.html',col_names = col_names,form_name = table_name)




@app.route('/save_instance',methods = ['GET','POST'])
def save_instance():
    if session['loggedin']==False:
        return redirect(url_for('login'))
    table_name = request.form['table_name']
    form_name=get_forms()[table_name]
    #Now we push the submitted form into submitted_forms table.
    query1 = 'INSERT INTO submittedforms (formtype,rollno,status) VALUES (%s,%s,%s)'
    values1 = [table_name,request.form['Roll_No'],'0']
    cursor.execute(query1,values1)
    mydb.commit()

    #Now we get the id from the form_table
    query2 = 'SELECT * from submittedforms where rollno = %s and formtype = %s'
    values2 = (request.form['Roll_No'],request.form['table_name'])
    cursor.execute(query2,values2)
    records = cursor.fetchall()
    row = records[-1]
    form_id = row[0]
    form_id_enc = encrypt(form_id)
    #now we need number of coloumns from the table
    query = 'SELECT * from ' + table_name
    cursor.execute(query)
    records = cursor.fetchall()
    col_names = [i[0] for i in cursor.description]
    num = len(col_names)
    print(num)
    #Now we need to insert into 
    per_s =''
    for i in range(num-1):
        per_s += '%s,'
    per_s += '%s'
    print(per_s)
    query3 = 'INSERT INTO '+request.form['table_name'] + ' VALUES ('+per_s+')'
    values = []
    values.append(form_id)
    for keys in request.form.keys():
        if keys!= 'table_name':
                values.append(request.form[keys])
    values.append('0')
    print(values)
    cursor.execute(query3,values)
    mydb.commit()
    #finding number of approvers
    query4= 'SELECT * from forms_table where table_name=%s'
    values4=[table_name]
    cursor.execute(query4,values4)
    row = cursor.fetchone()
    no_of_approvers=int(row[-1])
    approver=col_names[-no_of_approvers-1]
    msg = Message(
        "#" + str(form_id) + form_name+"  Approval",
        sender = sender_mail,
        recipients= [request.form[approver]])
    msg.html=render_template('template1.html',details=request.form,form_id=form_id_enc,approvelevel=0,form_name=form_name)
    mail.send(msg)
    return render_template('studenthomepage.html', message ='mail sent to first approver')


@app.route('/update_instance',methods = ['GET','POST'])
def update_instance():
    if session['loggedin']==False:
        return redirect(url_for('login'))
    form_id = request.form['form_id']
    form_id_enc = encrypt(int(form_id))
    action = request.form['approve']
    query = 'SELECT * from submittedforms where id=%s'
    values = [int(form_id)]
    cursor.execute(query,values)
    records = cursor.fetchall()
    row = records[-1]
    table_name=row[1]
    student_mail = session['email']
    query = 'SELECT * from forms_table where table_name=%s'
    values = [table_name]
    cursor.execute(query,values)
    records = cursor.fetchall()
    row = records[-1]
    form_name=row[0]
    no_of_approvers=row[-1]
    #if approver rejects form
    if action=='2':
        #update submittedforms table that form is rejected
        query2 = 'UPDATE submittedforms SET status=%s WHERE id=%s'
        values2 = (action,int(form_id))
        cursor.execute(query2,values2)
        mydb.commit()

        #send mail to student that form is rejected
        msg = Message("#" + str(form_id) + form_name+" Rejected",
                      sender = sender_mail,
                      recipients= [student_mail])
        msg.body=form_name+" is rejected"
        mail.send(msg)
        ret="form rejected."
    #if approver rejects form
    elif action=='1':
        
        query = 'SELECT * from '+table_name+' where id=%s'
        values = [int(form_id)]
        cursor.execute(query,values)
        records = cursor.fetchall()
        row = records[-1]
        approvelevel = int(row[-1])+1
        print(records[-1][-1])


        query1='UPDATE '+table_name+' set approvelevel=%s WHERE id=%s'
        values1=(str(approvelevel),int(form_id))
        cursor.execute(query1,values1)
        mydb.commit()
        # print('xxxxxx=',approvelevel)
        if approvelevel>=int(no_of_approvers):
                 #update submittedforms table that form is approved
                 query2 = 'UPDATE submittedforms SET status=%s WHERE id=%s'
                 values2 = (action,int(form_id))
                 cursor.execute(query2,values2)
                 mydb.commit()
                #  print("it came here...")
                 #send mail to student that form is approved                
                 msg = Message("#" + str(form_id) +form_name+" Approved",
                               sender = sender_mail,
                               recipients= [student_mail])
                 msg.body="Your "+form_name+" is approved."
                 mail.send(msg)
                 ret="completed approval."
        else:
                 query = 'SELECT * from '+table_name+' where id=%s'
                 values = [int(form_id)]
                 cursor.execute(query,values)
                 req_dict = [dict(line) for line in [zip([column[0] for column in cursor.description],row) for row in cursor.fetchall()]]
                 #find number of approvers
                 #now we have table name we need to find the coloumns.
                 query = 'SELECT * from ' + table_name
                 cursor.execute(query)
                 records = cursor.fetchall()
                 col_names = [i[0] for i in cursor.description]
                 approver=col_names[-int(no_of_approvers)-1+approvelevel]
                 #send mail to next approver
                 approver_mail = req_dict[0][approver]
                 msg = Message('#'+str(form_id)+form_name + " Approval",
                               sender = sender_mail,
                               recipients= [approver_mail])
                 msg.html=render_template('template1.html',details=req_dict[0],form_id=form_id_enc,approvelevel=approvelevel,form_name=form_name)
                 mail.send(msg)
                 ret="sent mail to next person."
    return ret

    
@app.route('/approve/<form_id>/<approvelevel>')
def approve(form_id,approvelevel):
    # print(type(form_id),type(approvelevel))
    query1 = 'SELECT * from submittedforms where id=%s'
    form_id = decrypt(int(form_id))
    values1 = [int(form_id)]
    cursor.execute(query1,values1)
    records = cursor.fetchall()
    row = records[-1]
    status=row[-1]
    table=row[1]
    query = 'SELECT * from '+table+' where id=%s'
    values = [int(form_id)]
    cursor.execute(query,values)
    records = cursor.fetchall()
    row = records[-1]
    req_dict = [dict(line) for line in [zip([column[0] for column in cursor.description],row1) for row1 in records]]
    print(row)
    current_approvelevel = row[-1]
    if current_approvelevel==approvelevel and status!='2':
        return render_template('approve.html',form_id=form_id,approve_level=int(approvelevel),row = req_dict[0],form_name = table)
    return "already responded"

#Functions which handle history part of the code.

#Function which gives basic detail about the history.
@app.route('/submitted_forms/<table_name>/<roll_no>')
def submitted_forms(table_name,roll_no):
    if session['loggedin']==False:
        return redirect(url_for('login'))
    dict_status = {
        '0' : 'pending',
        '1' : 'accepted',
        '2' :'rejected'
    }
    #getting all the forms submitted by him from submitted forms table.
    if session['type'] == 'Admin':
        if table_name == "all" and roll_no == 'nil':
            query = 'SELECT * from submittedforms'
            cursor.execute(query)
        elif table_name != "all" and roll_no == 'nil':
            query = 'SELECT * from submittedforms WHERE formtype = %s'
            values = [table_name]
            cursor.execute(query,values)
        elif table_name == 'all' and roll_no != 'nil':
            query = 'SELECT * from submittedforms WHERE upper(rollno) = %s'
            values = [roll_no.upper()]
            cursor.execute(query,values)
        else:
            query = 'SELECT * from submittedforms WHERE upper(rollno) = %s and formtype = %s'
            values = [roll_no.upper(),table_name]
        records = cursor.fetchall()
        return render_template("history.html",records = records,dict_status = dict_status,forms_list = get_forms(), table_name=table_name,row_len = len(records))

    if table_name == "all":
        query = 'SELECT * from submittedforms WHERE upper(rollno) = %s'
        values = [session['rollno'].upper()]
    else:
        query = 'SELECT * from submittedforms WHERE upper(rollno) = %s and formtype = %s'
        values = [session['rollno'].upper(),table_name]
    cursor.execute(query,values)
    records = cursor.fetchall()
    # len = len(records)
    return render_template("history.html",records = records,dict_status = dict_status,forms_list = get_forms(), table_name=table_name,row_len = len(records))

#Function which gives detailed info about the form.
@app.route('/expanded_history/<form_id>/<form_type>')
def expanded_history(form_id,form_type):
    if session['loggedin']==False:
        return redirect(url_for('login'))
    dict_form_type = {
        '1' : 'additionalcourseconversion'
    }
    query = 'SELECT * from ' +form_type+' WHERE id = %s'
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
    return render_template("expanded.html",row = row[0],status = status,approve_level = approve_level,form_name=form_type)


'''This region handles all the functions related creating a new type of form.'''
@app.route('/create_form')
def create_form():
    if session['loggedin']==False:
        return redirect(url_for('login'))
    return render_template('create_form.html')

#This route handles the adding of the form into the table.
@app.route('/add_form',methods = ['GET','POST'])
def add_form():
    if session['loggedin']==False:
        return redirect(url_for('login'))
    #First we get the form name and the number of approvers.
    #To push into the forms_table.
    form_name = request.form['form_name']
    table_name = request.form['form_name'].replace(' ','_')
    keys_list = list(request.form.keys())
    no_of_approvers = 0
    for i in keys_list:
        if i[0] == "A":
            no_of_approvers = no_of_approvers + 1
    #now we need to push into forms_table
    query = "INSERT INTO forms_table values (%s,%s,%s)"
    values = [form_name,table_name,str(no_of_approvers)]
    cursor.execute(query,values)
    mydb.commit()
    
    #Now we need to add the table into the database
    #first we remove spaces from the coloumn_names
    col_names = ['id']
    col_data_type = ['INT(11)']
    for key in keys_list:
        if key == 'form_name':
            continue
        col_names.append(request.form[key].replace(' ','_'))
        col_data_type.append('VARCHAR(100)')
    col_names.append('approvelevel')
    col_data_type.append('VARCHAR(150)')
    # print(col_names)
    create_stement='create table '+table_name + '('
    i=0
    while i< len(col_names)-1 :
        create_stement =create_stement +col_names[i] +'  '+col_data_type[i]+' ,'
        i=i+1

    create_stement =create_stement +col_names[i] +'  '+col_data_type[i]+' )'
    print(create_stement)
    print(len(create_stement))
    cursor.execute(create_stement)
    mydb.commit()
    return render_template('adminhomepage.html',message = "Form Added")

@app.route('/filter',methods = ['GET','POST'])
def filter():
    roll_no = request.form['rollno']
    if request.form['rollno'] == '':
        roll_no = 'nil'
    return redirect(url_for('submitted_forms',table_name = request.form['table_name'],roll_no = roll_no))

if __name__=="__main__":
    app.run(debug=True)
