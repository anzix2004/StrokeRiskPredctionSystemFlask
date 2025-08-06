

from flask import * 
from public import public
from api import api
from doctor import doctor
from admin import admin
from laboratory import laboratory


import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

app=Flask(__name__) 
app.secret_key="kjhjgffd"
app.register_blueprint(public)
app.register_blueprint(api)
app.register_blueprint(doctor)
app.register_blueprint(admin)
app.register_blueprint(laboratory)

app.run(debug=True,host='0.0.0.0',port=5009)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'delivoproject@gmail.com'
app.config['MAIL_PASSWORD'] = 'dluynczzgoezguoi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)



