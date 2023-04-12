from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
 
 
app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2312'
app.config['MYSQL_DB'] = 'geeklogin'
mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user=request.form['user']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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

if __name__=="__main__":
    app.run(debug=True)