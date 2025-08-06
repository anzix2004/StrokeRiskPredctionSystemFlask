import datetime
import uuid
from flask import * 
from database import * 
doctor=Blueprint('doctor',__name__) 

@doctor.route('/doctor')
def doctor_home():
    if 'did' in session: 
        response = make_response(render_template("doctorhome.html")) 
    else: 
        response = make_response(""" 
    <script> 
        alert('Session Timeout...Login Again'); window.location.href = '/'; 
    </script> 
    """) 
    # Set headers to prevent caching 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache' 
    response.headers['Expires'] = '0' 
    return response


@doctor.route('/fees',methods=['get','post'])
def fees():
    id=request.args['id']
    if 'submit' in request.form:
        amount=request.form['amount']

        zz="select * from fee where consulting_id='%s'"%(id)
        xx=select(zz)

        if not xx:
            
            qry="insert into fee values(null,'%s','%s',now())"%(id,amount)
            res=insert(qry)
            return """<script>alert('Amount Submitted');window.location='/consulting_time'</script>"""
        else:
            c="update fee set amount='%s' where consulting_id='%s'"%(amount,id)
            update(c)
            return """<script>alert('Amount Updated');window.location='/consulting_time'</script>"""
    data={}
    qry1="select * from fee where consulting_id='%s'"%(id)
    res=select(qry1)
    data['fees']=res
    return render_template("doctor_fees.html",data=data)

@doctor.route('/consulting_time',methods=['get','post'])
def consulting_time():
    if 'did' in session: 
        if 'action' in request.args:
            action=request.args['action']
            id=request.args['id']
        else:
            action=None
        if action=='delete':
            u="delete from consulting_times where consulting_id='%s'"%(id)
            delete(u)
        
        if 'submit' in request.form:
            day=request.form['day']
            start_time=request.form['start_time']
            end_time=request.form['end_time']
            qry="insert into consulting_times values(null,'%s','%s','%s','%s',now())"%(session['did'],day,start_time,end_time)
            res=insert(qry)
        data={}
        qry2="select * from consulting_times where doctor_id='%s'"%(session['did'])
        res2=select(qry2)
        data['consulting_times']=res2
        response = make_response(render_template("doctor_consulting_time.html",data=data)) 
    else: 
        response = make_response(""" 
    <script> 
        alert('Session Timeout...Login Again'); window.location.href = '/'; 
    </script> 
    """) 
    # Set headers to prevent caching 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache' 
    response.headers['Expires'] = '0' 
    return response
    # if 'submit' in request.form:
    #     day=request.form['day']
    #     start_time=request.form['start_time']
    #     end_time=request.form['end_time']
    #     qry="insert into consulting_times values(null,'%s','%s','%s','%s',now())"%(session['did'],day,start_time,end_time)
    #     res=insert(qry)
    # data={}
    # qry2="select * from consulting_times where doctor_id='%s'"%(session['did'])
    # res2=select(qry2)
    # data['consulting_times']=res2
    # return render_template("doctor_consulting_time.html",data=data)

# @doctor.route('/view_booking',methods=['get','post'])
# def view_booking():
#     if 'did' in session: 
#         data={}
#         qry3="SELECT * FROM bookings INNER JOIN users USING(user_id)inner join consulting_times where status!='Rejected' and doctor_id='%s'"%(session['did'])
#         res3=select(qry3)
#         data['view_booking']=res3

#         if 'action' in request.args:
#             act=request.args['action']
#             ids=request.args['id']
#         else:
#             act=None

#         if act == "accept":
#             q="UPDATE `bookings` SET `status`='Accepted' WHERE user_id='%s'"%(ids)
#             update(q)
#             return redirect(url_for("doctor.view_booking"))
        
#         if act == "reject":
#             qq="UPDATE `bookings` SET `status`='Rejected' WHERE user_id='%s'"%(ids)
#             update(qq)
#         response = make_response(render_template("doctor_view_booking.html",data=data)) 
#     else: 
#         response = make_response(""" 
#     <script> 
#         alert('Session Timeout...Login Again'); window.location.href = '/'; 
#     </script> 
#     """) 
        

    # Set headers to prevent caching 
    # response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    # response.headers['Pragma'] = 'no-cache' 
    # response.headers['Expires'] = '0' 
    # return response


    # data={}
    # qry3="SELECT * FROM bookings INNER JOIN users USING(user_id)inner join consulting_times where status!='Rejected' and doctor_id='%s'"%(session['did'])
    # res3=select(qry3)
    # data['view_booking']=res3

    # if 'action' in request.args:
    #     act=request.args['action']
    #     ids=request.args['id']
    # else:
    #     act=None

    # if act == "accept":
    #     q="UPDATE `bookings` SET `status`='Accepted' WHERE user_id='%s'"%(ids)
    #     update(q)
    #     return redirect(url_for("doctor.view_booking"))
    
    # if act == "reject":
    #     qq="UPDATE `bookings` SET `status`='Rejected' WHERE user_id='%s'"%(ids)
    #     update(qq)
    # return render_template("doctor_view_booking.html",data=data)

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# from flask_mail import Mail, Message
# import random
# import string
# import smtplib
# from email.mime.text import MIMEText

# def send_email(to_email):
#     try:
#         gmail = smtplib.SMTP('smtp.gmail.com', 587)
#         gmail.ehlo()
#         gmail.starttls()
#         gmail.login('hariharan0987pp@gmail.com', 'rjcbcumvkpqynpep')

#         msg = MIMEMultipart()
#         msg['From'] = 'hariharan0987pp@gmail.com'
#         msg['To'] = to_email
#         msg['Subject'] = 'Booking Status'

#         body = 'Your item has been successfully added to your shopping cart. Happy shopping!'
#         msg.attach(MIMEText(body, 'plain'))

#         gmail.send_message(msg)
#         gmail.quit()
#         print("Email sent successfully")

#     except smtplib.SMTPException as e:
#         print(f"Failed to send email: {e}")
#         raise


from flask import render_template, redirect, url_for, request, make_response, session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_mail import Mail, Message

# Assuming you have a select and update function that interacts with your database

@doctor.route('/view_booking', methods=['get', 'post'])
def view_booking():
    if 'did' in session: 
        data = {}
        qry3 = """SELECT * 
FROM bookings 
INNER JOIN users USING(user_id) 
INNER JOIN consulting_times ON bookings.consulting_id = consulting_times.consulting_id
WHERE bookings.status != 'Rejected' 
AND consulting_times.doctor_id = '%s';
""" % (session['did'])
        res3 = select(qry3)
        print(res3)
        print("Booking Data:", res3)  
        data['view_booking'] = res3

        if 'action' in request.args:
            act = request.args['action']
            ids = request.args['id']
            b_id= request.args['booking_id']
        else:
            act = None

        if act == "accept" and ids and b_id:
            # Update the status to 'Accepted'
            q = "UPDATE `bookings` SET `status`='Accepted' WHERE user_id='%s' and booking_id='%s'" % (ids,b_id)
            update(q)
            
            # Get the user's email (assuming you have user details like email in the response)
            qry_email = "SELECT email FROM users WHERE user_id='%s'" % (ids)
            res_email = select(qry_email)
            print(res_email,"+++++++++++++++++++++++++++")
            if res_email:
                to_email = res_email[0]['email']  # Extract the user's email
                send_email(to_email)
            
            return redirect(url_for("doctor.view_booking"))
        
        if act == "reject":
            qq = "UPDATE `bookings` SET `status`='Rejected' WHERE user_id='%s' and booking_id='%s'" % (ids,b_id)
            update(qq)
            qry_email = "SELECT email FROM users WHERE user_id='%s'" % (ids)
            res_email = select(qry_email)
            print(res_email,"+++++++++++++++++++++++++++")
            if res_email:
                to_email = res_email[0]['email']  # Extract the user's email
                reject_email(to_email)
            
            return redirect(url_for("doctor.view_booking"))
        response = make_response(render_template("doctor_view_booking.html", data=data))
    else: 
        response = make_response(""" 
        <script> 
            alert('Session Timeout...Login Again'); window.location.href = '/'; 
        </script> 
        """) 
    
    # Set headers to prevent caching 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache' 
    response.headers['Expires'] = '0' 
    
    return response
@doctor.route('/delete_consulting_time/<int:consulting_id>', methods=['GET'])
def delete_consulting_time(consulting_id):
    try:
        qry = f"DELETE FROM consulting_times WHERE consulting_id = {consulting_id}"
        delete(qry)  # Assuming you have a delete function

        flash("Consulting time deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting consulting time: {str(e)}", "danger")

    return redirect(url_for('doctor.consulting_time'))

def reject_email(to_email):
    try:
        # Set up the email server (Gmail in this case)
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('delivoproject@gmail.com', 'dluynczzgoezguoidluynczzgoezguoi')  # Your Gmail login details

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = 'delivoproject@gmail.com'
        msg['To'] = to_email
        msg['Subject'] = 'Booking Status'

        # Body of the email
        body = 'We regret to inform you that your booking with the doctor has been rejected. As a result, your payment will be fully refunded. The refund will be processed within 10-15 business days.'
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        gmail.send_message(msg)
        gmail.quit()
        print("Email sent successfully")

    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        raise

def send_email(to_email):
    try:
        # Set up the email server (Gmail in this case)
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('delivoproject@gmail.com', 'dluynczzgoezguoi')  # Your Gmail login details

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = 'delivoproject@gmail.com'
        msg['To'] = to_email
        msg['Subject'] = 'Booking Status'

        # Body of the email
        body = 'Your booking has been accepted by the doctor. We look forward to seeing you!'
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        gmail.send_message(msg)
        gmail.quit()
        print("Email sent successfully")

    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        raise


@doctor.route('/view_payment',methods=['get','post'])
def view_payment():
    if 'did' in session: 
        data={}
        qry4="SELECT * FROM payments"
        res4=select(qry4)
        data['view_payment']=res4
        response = make_response(render_template("doctor_view_payment.html",data=data)) 
    else: 
        response = make_response(""" 
    <script> 
        alert('Session Timeout...Login Again'); window.location.href = '/'; 
    </script> 
    """) 
    # Set headers to prevent caching 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache' 
    response.headers['Expires'] = '0' 
    return response
    # data={}
    # qry4="SELECT * FROM payments"
    # res4=select(qry4)
    # data['view_payment']=res4
    # return render_template("doctor_view_payment.html",data=data)

@doctor.route('/view_rating',methods=['get','post'])
def view_rating():
    if 'did' in session: 
        data={}
        qry5="SELECT * FROM ratings INNER JOIN users USING(user_id) WHERE doctor_id='%s'"%(session['did'])
        res5=select(qry5)
        data['view_rating']=res5
        response = make_response(render_template("doctor_view_rating.html",data=data)) 
    else: 
        response = make_response(""" 
    <script> 
        alert('Session Timeout...Login Again'); window.location.href = '/'; 
    </script> 
    """) 
    # Set headers to prevent caching 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache' 
    response.headers['Expires'] = '0' 
    return response
    # data={}
    # qry5="SELECT * FROM ratings INNER JOIN users USING(user_id) WHERE doctor_id='%s'"%(session['did'])
    # res5=select(qry5)
    # data['view_rating']=res5
    # return render_template("doctor_view_rating.html",data=data)

@doctor.route('/view_msg',methods=['get','post'])
def view_msg():
    if 'did' in session: 
        data={}
        qry6="SELECT DISTINCT chat.sender_id, users.first_name FROM chat INNER JOIN users ON chat.sender_id=users.login_id WHERE receiver_id='%s'"%(session['lid'])
        res6=select(qry6)
        data['view_msg']=res6
        response = make_response(render_template("doctor_msg.html",data=data)) 
    else: 
        response = make_response(""" 
    <script> 
        alert('Session Timeout...Login Again'); window.location.href = '/'; 
    </script> 
    """) 
    # Set headers to prevent caching 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache' 
    response.headers['Expires'] = '0' 
    return response
    # data={}
    # qry6="SELECT DISTINCT chat.sender_id, users.first_name FROM chat INNER JOIN users ON chat.sender_id=users.user_id WHERE receiver_id='%s'"%(session['did'])
    # res6=select(qry6)
    # data['view_msg']=res6
    # return render_template("doctor_msg.html",data=data)


@doctor.route('/view_chat/<int:sender_id>', methods=['GET', 'POST'])
def view_chat(sender_id):
   
    data={}
    cht={}
    qry7 = "SELECT * FROM chat WHERE (sender_id='%s' AND receiver_id='%s') OR (sender_id='%s' AND receiver_id='%s')ORDER BY date_time ASC"%(sender_id,session['lid'],session['lid'],sender_id)
    res7=select(qry7)
    print(res7)
    cht['view_chat']=res7
    if 'send' in request.form:
        msg=request.form['msg']
        msg=msg.replace("'", "''")
        qry8="INSERT INTO chat VALUES(null,'%s','doctor','%s','user','%s',now())"%(session['lid'],sender_id,msg)
        res8=insert(qry8)
        if res8:
            data['status']='success'
            data['data']=res8
        else:
            data['status']='failed'
        qry9="SELECT * FROM chat WHERE (sender_id='%s' AND receiver_id='%s') OR (sender_id='%s' AND receiver_id='%s')ORDER BY date_time ASC"%(sender_id,session['lid'],session['lid'],sender_id)
        res9=select(qry9)
        cht['view_chat']=res9
    return render_template("doctor_uchat.html", cht=cht, sender_id=sender_id)

from datetime import datetime, timedelta

def expire(sid):
    qrye = """SELECT bookings.book_date 
    FROM bookings 
    INNER JOIN consulting_times
    ON bookings.consulting_id = consulting_times.consulting_id
    INNER JOIN users ON bookings.user_id = users.user_id
    WHERE users.login_id = '%s' 
    AND consulting_times.doctor_id = '%s' AND bookings.status='Accepted'
    ORDER BY book_date DESC
    LIMIT 1;""" % (sid, session['did'])

    rese = select(qrye)
    print(rese)

    if rese:
        latest_date_str = rese[0]['book_date']
        print(f"Latest Booking Date (String): {latest_date_str}")

        # Convert string to datetime object
        try:
            latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")  
        except ValueError as e:
            print(f"Error converting date: {e}")
            return False

        expiration_date = latest_date + timedelta(days=14)
        print(f"Expiration Date: {expiration_date}")
        
        current_time = datetime.utcnow()
        print(f"Current UTC Time: {current_time}")

        return current_time > expiration_date

    return False




@doctor.route('/doctor_update_profile', methods=['GET', 'POST']) 
def doctor_update_profile():
    data = {}

    # Fetch current doctor details
    qry = "SELECT * FROM doctors WHERE doctor_id='%s'" % (session['did'])
    data['up'] = select(qry)

    if 'submit' in request.form:
        first_name = request.form['fname']
        last_name = request.form['lname']
        house_name = request.form['hname']
        place = request.form['place']
        landmark = request.form['lmark']
        qualification = request.form['qualification']
        phone = request.form['phone']
        email = request.form['email']

        # Check if a new image is uploaded
        if 'image' in request.files and request.files['image'].filename:
            image = request.files['image']
            path = "static/images/" + str(uuid.uuid4()) + image.filename
            image.save(path)
        else:
            path = data['up'][0]['path']  # Keep the existing image if no new image is uploaded

        # Update doctor profile
        qry4 = """UPDATE doctors 
                  SET first_name='%s', last_name='%s', house_name='%s', place='%s', 
                      landmark='%s', qualification='%s', phone='%s', email='%s', path='%s' 
                  WHERE doctor_id='%s'""" % (first_name, last_name, house_name, place, landmark, qualification, phone, email, path, session['did'])
        res4 = update(qry4) 

        flash("Profile updated successfully!", "success")
        return redirect(url_for('doctor.doctor_update_profile'))

    return render_template("doctor_update_profile.html", data=data)
