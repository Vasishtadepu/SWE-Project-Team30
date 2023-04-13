# importing libraries
from flask import Flask
from flask_mail import Mail, Message
   
app = Flask(__name__)
mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cs20btech11035@iith.ac.in'
app.config['MAIL_PASSWORD'] = 'fgbboncngfheozws'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
   
# message object mapped to a particular URL ‘/’
@app.route("/")
def index():
   msg = Message(
                'Hello',
                sender ='cs20btech11035@iith.ac.in',
                recipients = ['cs20btech11002@iith.ac.in']
               )
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg)
   return 'Sent'


   
if __name__ == '__main__':
   app.run(debug = True)