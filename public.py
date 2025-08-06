from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib
import uuid
from flask import * 
from database import * 
public=Blueprint('public',__name__)

@public.route('/') 
def home():
    return render_template("home.html")

@public.route('/login',methods=['get','post'])
def login():
    session.clear()
    if 'submit' in request.form:
        username=request.form['uname']
        password=request.form['psw']

        qry1="select * from login where username = '%s' and password = '%s'"%(username,password)
        res=select(qry1)


        if res:
            session['lid']=res[0]['login_id']

            if res[0]['user_type']=='user':

                u="SELECT * FROM users WHERE login_id='%s'"%( session['lid'])
                r=select(u)
                session['uid']=r[0]['user_id']
                return redirect(url_for('api.user_home'))
            

            if res[0]['user_type']=='admin':
                return redirect(url_for('admin.admin_home'))
            if res[0]['user_type']=='Laboratory':

                a="SELECT * FROM laboratory WHERE login_id='%s'"%(session['lid'])
                ree=select(a)
                print("ssssssssssssssssss",a)
                session['llid']=ree[0]['laboratory_id']

                return redirect(url_for('laboratory.laboratoryhome'))

            if res[0]['user_type']=='Doctor':

                a="SELECT * FROM doctors WHERE login_id='%s'"%( session['lid'])
                re=select(a)

                session['did']=re[0]['doctor_id']

                return redirect(url_for('doctor.doctor_home'))
           
            if res[0]['user_type']=='pending':
                return'''<script>alert("You are not approved yet");window.location='/login'</script>'''
        else:
            
            return'''<script>alert("Invalid username or password");window.location='/login'</script>'''
    response = make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache' 
    response.headers['Expires'] = '0' 
    return response

            
        


    return render_template("login.html")

@public.route('/doctorreg', methods=['GET', 'POST']) 
def doctorreg():
    if 'submit' in request.form:
        username = request.form['uname']
        password = request.form['psw']
        first_name = request.form['fname']
        last_name = request.form['lname']
        house_name = request.form['hname']
        place = request.form['place']
        landmark = request.form['lmark']
        qualification = request.form['qualification']
        phone = request.form['phone']
        email = request.form['email']
        image = request.files['image']
        path = "static/images/" + str(uuid.uuid4()) + image.filename
        image.save(path)

        # Check if email already exists
        check_email_qry = "SELECT * FROM doctors WHERE email='%s'" % email
        existing = select(check_email_qry)
        if existing:
            return'''<script>alert("Email already registered. Try another");window.location='/doctorreg'</script>'''
            # return render_template("doctors.html", msg="Email already registered. Try another.")

        # Insert login info
        qry3 = "INSERT INTO login VALUES (NULL, '%s', '%s', 'pending')" % (username, password)
        res3 = insert(qry3)

        # Insert doctor info
        qry4 = """INSERT INTO doctors 
                  VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 'pending', '%s')""" % (
                  res3, first_name, last_name, house_name, place, landmark, qualification, phone, email, path)
        res4 = insert(qry4) 

        if res4:
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            send_email(email, otp)
            return redirect(url_for('public.verify_otp'))

    return render_template("doctors.html")


 
@public.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@public.route('/user_reg', methods=['GET', 'POST']) 
def user_reg():
    data = {}
    if 'submit' in request.form:
        username = request.form['uname']
        password = request.form['psw']
        first_name = request.form['fname']
        last_name = request.form['lname']
        house_name = request.form['hname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']
        image = request.files['image']

        # Check if email already exists
        check_email_qry = "SELECT * FROM users WHERE email='%s'" % email
        existing = select(check_email_qry)
        if existing:
            return'''<script>alert("Email already registered. Try another");window.location='/user_reg'</script>'''


        # Save image
        path = "static/images/" + str(uuid.uuid4()) + image.filename
        image.save(path)

        # Insert into login table
        qry = "INSERT INTO login VALUES(NULL, '%s', '%s', 'user')" % (username, password)
        res = insert(qry)

        # Insert into users table
        qry2 = """INSERT INTO users 
                  VALUES(NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (
                  res, first_name, last_name, house_name, place, phone, email, path)
        res2 = insert(qry2)

        if res2:
            # Generate a 6-digit OTP
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            send_email(email, otp)
            return redirect(url_for('public.verify_otp'))

    return render_template('user_register.html', data=data)



@public.route('/Laboratory_reg', methods=['GET', 'POST']) 
def Laboratory_reg():
    data = {}
    if 'submit' in request.form:
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']
        image = request.files['image']

        # Check if email already exists
        check_email_qry = "SELECT * FROM laboratory WHERE email='%s'" % email
        existing = select(check_email_qry)
        if existing:
            return'''<script>alert("Email already registered. Try another");window.location='/Laboratory_reg'</script>'''

        # Save image
        path = "static/images/" + str(uuid.uuid4()) + image.filename
        image.save(path)

        # Insert into login table
        qry = "INSERT INTO login VALUES(NULL, '%s', '%s', 'pending')" % (username, password)
        res = insert(qry)

        # Insert into laboratory table
        qry2 = """INSERT INTO laboratory 
                  VALUES(NULL, '%s', '%s', '%s', '%s', '%s', '%s')""" % (
                  res, name, place, phone, email, path)
        res2 = insert(qry2)

        if res2:
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            send_email(email, otp)
            return redirect(url_for('public.verify_otp'))

    return render_template('Laboratory.html', data=data)


@public.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST' and 'submit' in request.form:
        username = request.form['uname']
        password = request.form['password']
        
        # Fetch login ID using provided email
        i = "SELECT login_id FROM users WHERE email='%s'" % (username)
        log = select(i)
        
        if log:
            loginid = log[0]['login_id']
            # Update the password
            i = "UPDATE login SET password='%s' WHERE login_id='%s'" % (password, loginid)
            res2 = update(i)
            
            if res2:
                # Generate and send OTP
                otp = str(random.randint(100000, 999999))
                session['otp'] = otp
                session['email'] = username  # Store email for verification step
                send_email(username, otp)
                
                return redirect(url_for('public.verify_otp'))

        return render_template('forgot.html', error="Invalid email or update failed")
    
    return render_template('forgot.html')



def send_email(to_email, otp):
    try:
        # Connect to Gmail SMTP server
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('delivoproject@gmail.com', 'dluynczzgoezguoi' \
        '')  # Use app password, not your real one

        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = 'delivoproject@gmail.com'
        msg['To'] = to_email
        msg['Subject'] = 'Confirm Your Registration'

        # Message content with OTP
        body = f'''
        Welcome to Our Platform!

        Thank you for registering. To complete your registration, please enter the following OTP:

        🔐 Your OTP: {otp}

        This code will expire in 5 minutes. If you didn’t request this, please ignore this email.

        Best regards,  
        The Team
        '''
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        gmail.send_message(msg)
        gmail.quit()
        print("Confirmation email sent successfully.")

    except smtplib.SMTPException as e:
        print(f"Failed to send confirmation email: {e}")
        raise
from flask import request, redirect, session, flash, render_template, url_for

@public.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        actual_otp = session.get('otp')

        if entered_otp == actual_otp:
            return'''<script>alert("Successfully");window.location='/login'</script>'''

        else:
            flash("Invalid OTP. Please try again.")
            return redirect(url_for('public.verify_otp'))  # Reload OTP page

    return render_template('verify_otp.html')




