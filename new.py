from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail,Message
import mysql.connector
import MySQLdb.cursors
from flask_mysqldb import MySQL

app = Flask(__name__)

db_host = 'localhost'
db_password = 'Vasisht@27'
db_database = 'test'
db_user = 'root'





app.secret_key = 'your secret key'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cs20btech11035@iith.ac.in'
app.config['MAIL_PASSWORD'] = 'fgbboncngfheozws'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['MYSQL_HOST'] = db_host
app.config['MYSQL_USER'] = db_user
app.config['MYSQL_PASSWORD'] = db_password
app.config['MYSQL_DB'] = db_database

mail = Mail(app)
app.secret_key = 'your secret key'
sender_mail = "cs20btech11035@iith.ac.in"
sender_password = "fgbboncngfheozws"

Mysql = MySQL(app)
cursor_mysql = Mysql.connection.cursor(MySQLdb.cursors.DictCursor)


mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vasisht@27",
        database="test"
        )
cursor = mydb.cursor()

print(cursor_mysql.description)

