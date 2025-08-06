import uuid
from flask import * 
from database import * 


laboratory=Blueprint('laboratory',__name__) 

@laboratory.route('/laboratoryhome',methods=['get','post'])
def laboratoryhome():
    return render_template("laboratoryhome.html")

@laboratory.route('/lab_view_request',methods=['get','post'])
def lab_view_request():
    data={}
    u="select * from request inner join users using(user_id) where laboratory_id='%s'"%(session['llid'])
    data['view_requests']=select(u)
    return render_template("lab_view_request.html",data=data)

@laboratory.route('/lab_add_amount',methods=['get','post'])
def lab_add_amount():
    data={}
    if 'submit' in request.form:
        amount=request.form['amount']
        request_id=request.args['request_id']
        qry="update request set amount='%s' where request_id='%s'"%(amount,request_id)
        insert(qry)
        return '''<script>alert("Amount added");window.location='/lab_view_request'</script>'''
    
    return render_template("lab_add_amount.html",data=data)
@laboratory.route('/lab_add_file',methods=['get','post'])
def lab_add_file():
    data={}
    if 'submit' in request.form:
        request_id=request.args['request_id']
        f=request.files['file']
        path="static/images/"+str(uuid.uuid4())+f.filename
        f.save(path)
        print("ddddddddddddddddddddd",request_id)
        qry="update request set file='%s' where request_id='%s'"%(path,request_id)
        insert(qry)
        return '''<script>alert("File added");window.location='/lab_view_request'</script>'''
       
    
    return render_template("lab_add_file.html",data=data)


@laboratory.route('/lab_profile_update', methods=['GET', 'POST']) 
def lab_profile_update():
    data = {}

    # Fetch current lab details
    qry = "SELECT * FROM laboratory WHERE laboratory_id='%s'" % (session['llid'])
    data['up'] = select(qry)

    if 'submit' in request.form:
        name = request.form['name']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']

        # Check if a new image is uploaded
        if 'image' in request.files and request.files['image'].filename:
            image = request.files['image']
            path = "static/images/" + str(uuid.uuid4()) + image.filename
            image.save(path)
        else:
            path = data['up'][0]['path']  # Keep the existing image if no new image is uploaded

        # Update lab profile
        qry2 = """UPDATE laboratory 
                  SET name='%s', place='%s', phone='%s', email='%s', path='%s' 
                  WHERE laboratory_id='%s'""" % (name, place, phone, email, path, session['llid'])
        res2 = update(qry2)

        flash("Profile updated successfully!", "success")
        return redirect(url_for('laboratory.lab_profile_update'))

    return render_template('lab_profile_update.html', data=data)
