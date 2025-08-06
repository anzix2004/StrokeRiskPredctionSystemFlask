from flask import * 
from database import * 

admin=Blueprint('admin',__name__)
@admin.route('/admin')
def admin_home():
    if 'lid' in session: 
        user_count = 0
        doctor_count = 0
        qryu = "SELECT COUNT(*) FROM users"
        resu = select(qryu)
        user_count = resu[0]['COUNT(*)']
        qryd = "SELECT COUNT(*) FROM doctors where status='Accepted'"
        resd = select(qryd)
        doctor_count = resd[0]['COUNT(*)']
        cdata = [user_count, doctor_count]
        response = make_response(render_template("adminhome.html",cdata=cdata)) 
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

@admin.route('/docapprove', methods=['GET', 'POST'])
def docapprove():
    if 'lid' in session:
        data = {}
        qry1 = "SELECT * FROM doctors INNER JOIN login USING(login_id) WHERE user_type!='Rejected'"
        res = select(qry1)
        data['view_doc'] = res

        if 'action' in request.args and 'id' in request.args:
            act = request.args['action']
            ids = request.args['id']

            if act == "approve":
                qq = """
                UPDATE `login` AS l
                JOIN `doctors` AS d ON l.login_id = d.login_id
                SET l.user_type = 'Doctor', d.status = 'Accepted'
                WHERE l.login_id = '%s'
                """ % ids
                update(qq)
                return redirect(url_for("admin.docapprove"))

            elif act == "reject":
                qq = """
                UPDATE `login` AS l
                JOIN `doctors` AS d ON l.login_id = d.login_id
                SET l.user_type = 'Rejected', d.status = 'Rejected'
                WHERE l.login_id = '%s'
                """ % ids
                update(qq)
                return redirect(url_for("admin.docapprove"))

        response = make_response(render_template("admin_view_doc.html", data=data))
    else:
        response = make_response("""
        <script>
            alert('Session Expired'); window.location.href = '/';
        </script>
        """)
    # Set headers to prevent caching 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response




    # data={}
    # qry1="SELECT * FROM doctors INNER JOIN login USING(login_id) where user_type!='Rejected'"
    # res=select(qry1)
    # # print(res)
    # data['view_doc']=res

    # if 'action' in request.args:
    #     act=request.args['action']
    #     ids=request.args['id']
    # else:
    #     act=None

    # if act == "approve":
    #     qq="UPDATE `login` SET `user_type`='Doctor' WHERE login_id='%s'"%(ids)
    #     update(qq)
    #     return redirect(url_for("admin.docapprove"))
    
    # if act == "reject":
    #     qq="UPDATE `login` SET `user_type`='Rejected' WHERE login_id='%s'"%(ids)
    #     update(qq)

    # return render_template("admin_view_doc.html",data=data)

@admin.route('/view_user',methods=['get','post']) 
def view_user():
    if 'lid' in session: 
        data={}
        qry2="SELECT * FROM users"
        res=select(qry2)
        # print(res)
        data['view_user']=res
        if 'action' in request.args:
            action=request.args['action']
            id=request.args['id']
        else:
            action=None
        if action=='delete':
            u="delete from users where login_id='%s'"%(id)
            delete(u)
            u="delete from login where login_id='%s'"%(id)
            delete(u)
            return redirect(url_for('admin.view_user'))
        response = make_response(render_template("admin_view_user.html",data=data)) 
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
    # qry2="SELECT * FROM users"
    # res=select(qry2)
    # # print(res)
    # data['view_user']=res
    # return render_template("admin_view_user.html",data=data)
    

@admin.route('/view_complaint',methods=['get','post']) 
def view_complaint():
    if 'lid' in session: 
        data={}
        qry3="SELECT * FROM complaints"
        res=select(qry3)
        # print(res)
        data['view_complaint']=res
        response = make_response(render_template("admin_view_complaint.html",data=data)) 
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
    # qry3="SELECT * FROM complaints"
    # res=select(qry3)
    # # print(res)
    # data['view_complaint']=res
    # return render_template("admin_view_complaint.html",data=data)

@admin.route('/admin_send_reply',methods=['get','post']) 
def admin_send_reply():
    if 'lid' in session: 
        id=request.args['id']
        if 'submit' in request.form:
            reply=request.form['reply']

            reply = reply.replace("'", "''")
            
            qry5="UPDATE `complaints` SET `reply`='%s' WHERE complaint_id='%s'"%(reply,id)
            update(qry5)
            return redirect(url_for('admin.view_complaint'))
        response = make_response(render_template("admin_reply.html"))
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
    # id=request.args['id']
    # if 'submit' in request.form:
    #     reply=request.form['reply']
    #     qry5="UPDATE `complaints` SET `reply`='%s' WHERE complaint_id='%s'"%(reply,id)
    #     update(qry5)
    #     return redirect(url_for('admin.view_complaint'))
    # return render_template("admin_reply.html")


@admin.route('/view_doctor',methods=['get','post']) 
def view_doctor():
    if 'lid' in session: 
        data={}
        qry4="SELECT * FROM doctors INNER JOIN login USING(login_id) WHERE user_type='Doctor'"
        res=select(qry4)
        # print(res)
        data['view_doctor']=res
        response = make_response(render_template("admin_view_doctor.html",data=data)) 
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
    # qry4="SELECT * FROM doctors INNER JOIN login USING(login_id) WHERE user_type='Doctor'"
    # res=select(qry4)
    # # print(res)
    # data['view_doctor']=res
    # return render_template("admin_view_doctor.html",data=data)



@admin.route('/admin_view_lab',methods=['get','post'])
def admin_view_lab():
    data={}
    qry4="SELECT * FROM laboratory  inner join login using(login_id)"
    data['view']=select(qry4)
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='approve':
        u="update login set user_type='Laboratory' where login_id='%s'"%(id)
        update(u)
        return redirect(url_for('admin.admin_view_lab'))
    if action=='reject':
        u="update login set user_type='pending' where login_id='%s'"%(id)
        update(u)
        return redirect(url_for('admin.admin_view_lab'))
    
    return render_template('admin_view_lab.html',data=data)