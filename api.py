import uuid
from flask import * 
from Geminiapi import generate_gemini_response
from database import * 


api=Blueprint('api',__name__) 

@api.route('/user_home',methods=['get','post'])
def user_home():
    return render_template("user_home.html")
@api.route('/user_view_request',methods=['get','post'])
def user_view_request():
    data={}
    r="select * from request inner join users using(user_id) where request.user_id='%s'"%(session['uid'])
    data['view']=select(r)
    print("dddddddddddddd",r)
    return render_template("user_view_request.html",data=data)
@api.route('/user_request_amount',methods=['get','post'])
def user_request_amount():
    data={}
    if 'submit' in request.form:
        request_id=request.args['request_id']
        u="update request set status='paid' where request_id='%s'"%(request_id)
        update(u)
        return redirect(url_for('api.user_home'))
    return render_template("user_request_amount.html",data=data)

@api.route('/userview_doctors', methods=['GET', 'POST'])
def userview_doctors():
    data = {}

    rating_filter = request.form.get('rating')  # Get user input for rating filter

    # Fetch doctors with their average rating
    qry = """
    SELECT doctors.*, 
           IFNULL(ROUND(AVG(ratings.rate), 1), 'No Rating') AS avg_rating
    FROM doctors
    LEFT JOIN ratings ON doctors.doctor_id = ratings.doctor_id
    WHERE doctors.status = 'Accepted'
    GROUP BY doctors.doctor_id
    """

    # Apply rating filter if provided
    if rating_filter:
        qry += f" HAVING avg_rating >= {rating_filter}"

    data['view_doctor'] = select(qry)
    
    return render_template('userview_doctor.html', data=data)

  

@api.route('/send_complaint')
def send_complaint():
    data={}
    complaint=request.args['complaint']
    lid=request.args['logid']

    qry3="insert into complaints values(null,(select user_id from users where login_id='%s'),'%s','pending',now())"%(lid,complaint)
    res3=insert(qry3)

    if res3:
        data['status']='success'
        data['data']=res3
    else:
        data['status']='failed'
    data['method']='send'
    return str(data)



   

@api.route('/view_ufees')
def view_ufees():
    data={}
    did=request.args['docid']
    
    qry5="SELECT fee.amount, fee.date_time FROM fee INNER JOIN consulting_times ON fee.consulting_id = consulting_times.consulting_id WHERE consulting_times.doctor_id ='%s'"%(did)
    res5=select(qry5)
    print(res5)
    if res5:
        data['status']='success'
        data['data']=res5
    else:
        data['status']='failed'
    data['method']="view_fees"
    return str(data)
@api.route('/user_addrating',methods=['get','post'])
def user_addrating():
    data={}
    if 'submit' in request.form:
        print("dddddddddddddd")
        rate=request.form['rating']
        did=request.args['doctor_id']
        print("dddddddddddddd",did)
        
        review=request.form['review']
        r="insert into ratings values(null,'%s','%s','%s','%s',curdate())"%(session['uid'],did,rate,review)
        insert(r)
    return render_template('user_add_rating.html',data=data)



@api.route('/userviewconsulting_times',methods=['get','post'])
def userviewconsulting_times():
  
    data={}
    did=request.args['doctor_id']
    qry7="SELECT * FROM consulting_times INNER JOIN fee USING(consulting_id) where doctor_id='%s'"%(did)
    data['view']=select(qry7)
    return render_template('userviewconsulting_times.html',data=data)
@api.route('/make_payment',methods=['get','post'])
def make_payment():
  
    data={}
    booking_id=request.args['booking_id']
    u="update bookings set status='Paid' where booking_id='%s'"%(booking_id)
    update(u)
    
    
    return render_template('make_payment.html',data=data)

import datetime
from flask import request

import datetime

import datetime

# Function to generate 15-minute slots between start_time and end_time, accounting for crossing midnight
def generate_time_slots(start_time, end_time):
    slots = []
    
    # Convert string input times into datetime objects in the "%H:%M" format (24-hour time)
    current_time = datetime.datetime.strptime(start_time, "%H:%M")
    end_time = datetime.datetime.strptime(end_time, "%H:%M")
    
    # If the end time is earlier than the start time, it means we are crossing midnight
    if end_time < current_time:
        end_time += datetime.timedelta(days=1)  # Add one day to the end time to handle midnight crossover
    
    # Generate slots in 15-minute increments
    while current_time < end_time:
        # Calculate next time slot (15-minute increment)
        next_time = current_time + datetime.timedelta(minutes=15)
        
        # Format the slots in 24-hour railway time format (HH:MM)
        slots.append(f"{current_time.strftime('%H:%M')} - {next_time.strftime('%H:%M')}")
        
        # Move to the next slot
        current_time = next_time
    
    return slots

# Example usage
start_time = "21:15"  # Start time in 24-hour format (railway time)
end_time = "00:15"    # End time in 24-hour format





@api.route('/booking_time')
def booking_time():
    data = {}
    cid = request.args['consulting_id']  # Consulting ID
    
    qry8 = "SELECT start_time, end_time FROM consulting_times WHERE consulting_id='%s'" % (cid)
    res8 = select(qry8)

    if res8:
        start_time = res8[0]['start_time']
        end_time = res8[0]['end_time']
        
        slots = generate_time_slots(start_time, end_time)
        
        available_slots = []
        for slot in slots:
            qry = "SELECT * FROM bookings WHERE consulting_id='%s' AND time='%s'" % (cid, slot)
            res = select(qry)
            
            if not res:  # If slot is free, add it
                available_slots.append(slot)
        
        if available_slots:
            data['status'] = 'success'
            data['available_slots'] = available_slots
        else:
            data['status'] = 'failed'
            data['message'] = 'No slots available'
    else:
        data['status'] = 'failed'
        data['message'] = 'Consulting session not found'
    
    return render_template('booking_time.html', data=data)


@api.route('/ubook')
def ubook():
    data = {}
    cid = request.args['conid']
    lid = request.args['logid']
    
    qry_user = "SELECT user_id FROM users WHERE login_id='%s'" % (lid)
    res_user = select(qry_user)
    
    if res_user:
        user_id = res_user[0]['user_id']
        
        qry_time_slots = "SELECT start_time, end_time FROM consulting_times WHERE consulting_id='%s'" % (cid)
        res_time_slots = select(qry_time_slots)
        
        if res_time_slots:
            start_time = res_time_slots[0]['start_time']
            end_time = res_time_slots[0]['end_time']
            
            slots = generate_time_slots(start_time, end_time)
            
            available_slots = []
            for slot in slots:
                qry_check = "SELECT * FROM bookings WHERE consulting_id='%s' AND time='%s' AND status IN ('pending', 'Accepted');" % (cid, slot)
                res_check = select(qry_check)
                
                if not res_check:
                    available_slots.append(slot)
            
            if available_slots:
                chosen_slot = available_slots[0]
                
                qry_booking = "INSERT INTO bookings (user_id, consulting_id, date_time, book_date, status, time) VALUES ('%s', '%s', NOW(), CURDATE(), 'pending', '%s')" % (user_id, cid, chosen_slot)
                res_booking = insert(qry_booking)
                
                
                if res_booking:
                    booking_id = res_booking  
                    
                    qry_payment = "INSERT INTO payments (booking_id, date_time, status) VALUES ('%s', NOW(), 'pending')" % (booking_id)
                    insert(qry_payment)
                    
                    data['status'] = 'success'
                    data['data'] = booking_id
                    data['slot'] = chosen_slot
                else:
                    data['status'] = 'failed'
                    data['message'] = 'Booking failed'
            else:
                data['status'] = 'failed'
                data['message'] = 'No available slots for today'
        else:
            data['status'] = 'failed'
            data['message'] = 'Consulting session not found'
    else:
        data['status'] = 'failed'
        data['message'] = 'User not found'
    
    return render_template('ubook.html', data=data)



# @api.route('/booking_time')
# def booking_time():
#     data={}
#     cid=request.args['conid']
#     qry8="select date_time from consulting_times where consulting_id='%s'"%(cid)
#     res8=select(qry8)
#     if res8:
#         data['status']='success'
#         data['data']=res8
#     else:
#         data['status']='failed'
#     data['method']="booking_time"
#     # print(data,'+++++++++++++')
#     return str(data)

# @api.route('/ubook')
# def ubook():
#     data={}
#     cid=request.args['conid']
#     lid=request.args['logid']
#     qry9="insert into bookings values(null,(select user_id from users where login_id='%s'),'%s',now(),curdate(),'pending')"%(lid,cid)
#     res9=insert(qry9)
#     qry11="insert into payments values(null,'%s',now(),'pending')"%(res9)
#     insert(qry11)
#     if res9:
#         data['status']='success'
#         data['data']=res9
#     else:
#         data['status']='failed'
#     data['method']="book"
#     return str(data)

@api.route('/ureply')
def ureply():
    data={}
    lid=request.args['logid']
    qry10="select * from complaints where user_id=(select user_id from users where login_id='%s')"%(lid)
    res10=select(qry10)
    print(res10,"////")
    if res10:
        data['status']='success'
        data['data']=res10
    else:
        data['status']='failed'
    data['method']="ureply"
    return str(data)

# @api.route('/send_rating')
# def send_rating():
#     data={}
#     review=request.args['review']
#     star=request.args['star_rating']
#     lid=request.args['logid']
#     did=request.args['docid']
#     qry12="insert into ratings values(null,(select user_id from users where login_id='%s'),'%s','%s','%s',now())"%(lid,did,star,review)
#     res12=insert(qry12)

#     if res12:
#         data['status']='success'
      
#     else:
#         data['status']='failed'
    
#     return str(data)






# # from flask import Flask, request, jsonify
# from predict import *  # Assuming predict.py has all the relevant functions defined
# import numpy as np
# from tensorflow.keras.models import load_model
# from sklearn.preprocessing import MinMaxScaler
# import os



# # Load the Pre-trained Model and Scaler
# def load_resources():
#     try:
#         model = load_model("stroke_prediction_lstm_2.h5", compile=False)  # Avoid re-compiling if not necessary
#         scaler = np.load("scaler.npy", allow_pickle=True).item()
#         print("Model and scaler loaded successfully!")
#         return model, scaler
#     except FileNotFoundError as e:
#         print(f"Error: {e}")
#         print("Ensure the model file 'stroke_prediction_lstm.h5' and scaler file 'scaler.npy' are in the same directory.")
#         exit()

# # Step 3: Preprocess User Input
# def preprocess_input(user_input, scaler):
#     # Map user input to the expected feature names
#     input_data = {
#         "age": user_input["age"],
#         "hypertension": user_input["hypertension"],
#         "heart_disease": user_input["heart_disease"],
#         "avg_glucose_level": user_input["avg_glucose_level"],
#         "bmi": user_input["bmi"],
#         "gender_Male": 1 if user_input["gender"] == "male" else 0,
#         "ever_married_Yes": 1 if user_input["ever_married"] == "yes" else 0,
#         "work_type_Private": 1 if user_input["work_type"] == "private" else 0,
#         "work_type_Self-employed": 1 if user_input["work_type"] == "self-employed" else 0,
#         "work_type_Govt_job": 1 if user_input["work_type"] == "govt_job" else 0,
#         "work_type_Children": 1 if user_input["work_type"] == "children" else 0,
#         "Residence_type_Urban": 1 if user_input["residence_type"] == "urban" else 0,
#         "smoking_status_smokes": 1 if user_input["smoking_status"] == "smokes" else 0,
#         "smoking_status_formerly smoked": 1 if user_input["smoking_status"] == "formerly smoked" else 0,
#         "smoking_status_never smoked": 1 if user_input["smoking_status"] == "never smoked" else 0,
#     }

#     # Align with training features
#     all_features = scaler.feature_names_in_
#     input_array = np.zeros(len(all_features))
#     for i, feature in enumerate(all_features):
#         if feature in input_data:
#             input_array[i] = input_data[feature]

#     # Scale the input
#     input_scaled = scaler.transform([input_array])
#     return input_scaled.reshape(1, 1, -1)  # Reshape for LSTM input
# from tensorflow.keras.activations import sigmoid
# # Step 4: Predict Stroke Risk
# def predict_stroke(input_data, model):
#     prediction = model.predict(input_data)
#     print(prediction,"[[[[[[[[[[]]]]]]]]]]"*100)
#     probability = sigmoid(prediction)  # Apply sigmoid if needed
#     print(f"Prediction Probability: {probability}") 

#     if probability > 0.2:
#         risk = "High risk of stroke"
#     else:
#         risk = "Low risk of stroke"
#     return risk# Convert to binary (0 or 1)

# # API route to make prediction
# @api.route('/api_prediction', methods=['GET'])
# def api_prediction():
#     data = {}
#     user_input = {}
#     import tensorflow as tf
#     # print("TensorFlow version:", tf._version_)

#     user_input['age'] = float(request.args['age'])
#     user_input['gender'] = request.args['gender'].lower()
#     user_input['hypertension'] = int(request.args['hyper'])
#     user_input['heart_disease'] = int(request.args['heart'])
#     user_input['ever_married'] = request.args['mrg'].lower()
#     user_input['work_type'] = request.args['wrk_type'].lower()
#     user_input['residence_type'] = request.args['residence'].lower()
#     user_input['avg_glucose_level'] = float(request.args['glucose'])
#     user_input['bmi'] = float(request.args['bmi'])
#     user_input['smoking_status'] = request.args['smoke'].lower()

#     # Now you can print or pass user_input to preprocessing or prediction
#     print(user_input,"PPPPPPPPPPPPPPPPPPPPPPPPPP")


#     # Load model and scaler
#     model, scaler = load_resources()

#     # Preprocess the input
#     preprocessed_input = preprocess_input(user_input, scaler)
#     print(preprocess_input,"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")

#     # Make prediction
#     result = predict_stroke(preprocessed_input, model)
    
#     print(result,"===================================")
#     data["prediction"] = result

#     # # Send response
#     # if result == 1:
       
#     #     print(data['prediction'])
#     # else:
#     #     data["prediction"] = "Low risk of stroke."


#     return jsonify(data)


# =====================OLD CODE============



# from flask import Flask, request, jsonify
# from predict import *  # Assuming predict.py has all the relevant functions defined
# import numpy as np
# from tensorflow.keras.models import load_model
# from sklearn.preprocessing import MinMaxScaler
# import os
# from tensorflow.keras.activations import sigmoid



# # Load the Pre-trained Model and Scaler
# def load_resources():
#     try:
#         model = load_model("stroke_prediction_lstm_2.h5", compile=False)  # Avoid re-compiling if not necessary
#         scaler = np.load("scaler.npy", allow_pickle=True).item()
#         print("Model and scaler loaded successfully!")
#         return model, scaler
#     except FileNotFoundError as e:
#         print(f"Error: {e}")
#         print("Ensure the model file 'stroke_prediction_lstm.h5' and scaler file 'scaler.npy' are in the same directory.")
#         exit()

# # Step 3: Preprocess User Input
# def preprocess_input(user_input, scaler):
#     # Map user input to the expected feature names
#     input_data = {
#         "age": user_input["age"],
#         "hypertension": user_input["hypertension"],
#         "heart_disease": user_input["heart_disease"],
#         "avg_glucose_level": user_input["avg_glucose_level"],
#         "bmi": user_input["bmi"],
#         "gender_Male": 1 if user_input["gender"] == "male" else 0,
#         "ever_married_Yes": 1 if user_input["ever_married"] == "yes" else 0,
#         "work_type_Private": 1 if user_input["work_type"] == "private" else 0,
#         "work_type_Self-employed": 1 if user_input["work_type"] == "self-employed" else 0,
#         "work_type_Govt_job": 1 if user_input["work_type"] == "govt_job" else 0,
#         "work_type_Children": 1 if user_input["work_type"] == "children" else 0,
#         "Residence_type_Urban": 1 if user_input["residence_type"] == "urban" else 0,
#         "smoking_status_smokes": 1 if user_input["smoking_status"] == "smokes" else 0,
#         "smoking_status_formerly smoked": 1 if user_input["smoking_status"] == "formerly smoked" else 0,
#         "smoking_status_never smoked": 1 if user_input["smoking_status"] == "never smoked" else 0,
#     }

#     # Align with training features
#     all_features = scaler.feature_names_in_
#     input_array = np.zeros(len(all_features))
#     for i, feature in enumerate(all_features):
#         if feature in input_data:
#             input_array[i] = input_data[feature]

#     # Scale the input
#     input_scaled = scaler.transform([input_array])
#     return input_scaled.reshape(1, 1, -1)  # Reshape for LSTM input

# # Step 4: Predict Stroke Risk
# def predict_stroke(input_data, model):
#     prediction = model.predict(input_data)
#     print(f"Raw Prediction: {prediction}")
    
#     # If your model outputs a probability, you can directly use it
#     probability = prediction[0][0]  # Access the probability value
#     print(f"Prediction Probability: {probability}")

#     # Check the probability and return risk
#     if probability > 1e-06  :  # Assuming the model outputs probability between 0 and 1
#         risk = "High risk of stroke"
#     else:
#         risk = "Low risk of stroke"
#     return risk

# # API route to make prediction
# @api.route('/api_prediction', methods=['GET'])
# def api_prediction():
#     data = {}
#     user_input = {}

#     # Capture user input from request arguments
#     user_input['age'] = float(request.args['age'])
#     user_input['gender'] = request.args['gender'].lower()
#     user_input['hypertension'] = int(request.args['hyper'])
#     user_input['heart_disease'] = int(request.args['heart'])
#     user_input['ever_married'] = request.args['mrg'].lower()
#     user_input['work_type'] = request.args['wrk_type'].lower()
#     user_input['residence_type'] = request.args['residence'].lower()
#     user_input['avg_glucose_level'] = float(request.args['glucose'])
#     user_input['bmi'] = float(request.args['bmi'])
#     user_input['smoking_status'] = request.args['smoke'].lower()

#     # Load model and scaler
#     model, scaler = load_resources()

#     # Preprocess the input
#     preprocessed_input = preprocess_input(user_input, scaler)

#     # Make prediction
#     result = predict_stroke(preprocessed_input, model)
    
#     print(f"Prediction result: {result}")
#     data["prediction"] = result  # Add result to response data

#     return jsonify(data)





# from flask import Flask, request, jsonify
# from predict import *  # Assuming predict.py has all the relevant functions defined
# import numpy as np
# from tensorflow.keras.models import load_model
# from sklearn.preprocessing import MinMaxScaler
# import os
# from tensorflow.keras.activations import sigmoid


# # Load the Pre-trained Model and Scaler
# def load_resources():
#     try:
#         model = load_model("stroke_prediction_lstm_2.h5", compile=False)  # Avoid re-compiling if not necessary
#         scaler = np.load("scaler.npy", allow_pickle=True).item()
#         print("Model and scaler loaded successfully!")
#         return model, scaler
#     except FileNotFoundError as e:
#         print(f"Error: {e}")
#         print("Ensure the model file 'stroke_prediction_lstm_2.h5' and scaler file 'scaler.npy' are in the same directory.")
#         exit()


# # Step 3: Preprocess User Input
# def preprocess_input(user_input, scaler):
#     # Map user input to the expected feature names
#     input_data = {
#         "age": user_input["age"],
#         "hypertension": user_input["hypertension"],
#         "heart_disease": user_input["heart_disease"],
#         "avg_glucose_level": user_input["avg_glucose_level"],
#         "bmi": user_input["bmi"],
#         "gender_Male": 1 if user_input["gender"] == "male" else 0,
#         "ever_married_Yes": 1 if user_input["ever_married"] == "yes" else 0,
#         "work_type_Private": 1 if user_input["work_type"] == "private" else 0,
#         "work_type_Self-employed": 1 if user_input["work_type"] == "self-employed" else 0,
#         "work_type_Govt_job": 1 if user_input["work_type"] == "govt_job" else 0,
#         "work_type_Children": 1 if user_input["work_type"] == "children" else 0,
#         "Residence_type_Urban": 1 if user_input["residence_type"] == "urban" else 0,
#         "smoking_status_smokes": 1 if user_input["smoking_status"] == "smokes" else 0,
#         "smoking_status_formerly smoked": 1 if user_input["smoking_status"] == "formerly smoked" else 0,
#         "smoking_status_never smoked": 1 if user_input["smoking_status"] == "never smoked" else 0,
#     }

#     # Align with training features
#     all_features = scaler.feature_names_in_
#     input_array = np.zeros(len(all_features))
#     for i, feature in enumerate(all_features):
#         if feature in input_data:
#             input_array[i] = input_data[feature]

#     # Scale the input
#     input_scaled = scaler.transform([input_array])
#     return input_scaled.reshape(1, 1, -1)  # Reshape for LSTM input


# # Step 4: Predict Stroke Risk
# def predict_stroke(input_data, model):
#     prediction = model.predict(input_data)
#     print(f"Raw Prediction: {prediction}")
    
#     # Assuming the model outputs a probability between 0 and 1
#     probability = prediction[0][0]  # Access the probability value
#     print(f"Prediction Probability: {probability}")

#     # Adjust the threshold for high risk (increase threshold if needed)
#     if probability >1e-10:  # Assuming anything greater than 0.5 indicates high risk
#         risk = "High risk of stroke"
#     else:
#         risk = "Low risk of stroke"
#     return risk


# # API route to make prediction
# @api.route('/api_prediction', methods=['GET'])
# def api_prediction():
#     data = {}
#     user_input = {}

#     # Capture user input from request arguments
#     user_input['age'] = float(request.args['age'])
#     user_input['gender'] = request.args['gender'].lower()
#     user_input['hypertension'] = int(request.args['hyper'])
#     user_input['heart_disease'] = int(request.args['heart'])
#     user_input['ever_married'] = request.args['mrg'].lower()
#     user_input['work_type'] = request.args['wrk_type'].lower()
#     user_input['residence_type'] = request.args['residence'].lower()
#     user_input['avg_glucose_level'] = float(request.args['glucose'])
#     user_input['bmi'] = float(request.args['bmi'])
#     user_input['smoking_status'] = request.args['smoke'].lower()

#     # Load model and scaler
#     model, scaler = load_resources()

#     # Preprocess the input
#     preprocessed_input = preprocess_input(user_input, scaler)

#     # Make prediction
#     result = predict_stroke(preprocessed_input, model)
    
#     print(f"Prediction result: {result}")
#     data["prediction"] = result  # Add result to response data

#     return jsonify(data)




from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

# Load the Pre-trained Model and Scaler
def load_resources():
    try:
        model = load_model(r"C:\\Users\\USER\Downloads\\Project\\Project\stroke_prediction_lstm_2.h5", compile=False)
        scaler = np.load(r"C:\\Users\\USER\Downloads\\Project\\Project\scaler.npy", allow_pickle=True).item()
        print("Model and scaler loaded successfully!")
        return model, scaler
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Ensure the model file and scaler file are in the correct directory.")
        exit()







import pandas as pd
import tensorflow as tf
import numpy as np

# Function to preprocess user input
def preprocess_input(user_input, scaler):
    input_data = {
        "age": user_input.get("age", 0),
        "hypertension": user_input.get("hypertension", 0),
        "heart_disease": user_input.get("heart_disease", 0),
        "avg_glucose_level": user_input.get("avg_glucose_level", 0),
        "bmi": user_input.get("bmi", 0),
        "gender_Male": 1 if user_input.get("gender") == "male" else 0,
        "gender_Other": 1 if user_input.get("gender") == "other" else 0,  
        "ever_married_Yes": 1 if user_input.get("ever_married") == "yes" else 0,
        "work_type_Never_worked": 1 if user_input.get("work_type") == "never_worked" else 0,
        "work_type_Private": 1 if user_input.get("work_type") == "private" else 0,
        "work_type_Self-employed": 1 if user_input.get("work_type") == "self-employed" else 0,
        "work_type_children": 1 if user_input.get("work_type") == "children" else 0,
        "Residence_type_Urban": 1 if user_input.get("residence_type") == "urban" else 0,
        "smoking_status_formerly smoked": 1 if user_input.get("smoking_status") == "formerly smoked" else 0,
        "smoking_status_never smoked": 1 if user_input.get("smoking_status") == "never smoked" else 0,
        "smoking_status_smokes": 1 if user_input.get("smoking_status") == "smokes" else 0,
    }

    input_df = pd.DataFrame([input_data])

    try:
        input_df = input_df[scaler.feature_names_in_]
    except KeyError as e:
        print(f"Error: Missing columns in input data: {e}")
        return None  

    input_scaled = scaler.transform(input_df)

    input_reshaped = input_scaled.reshape(1, 1, -1)  

    return input_reshaped, user_input  # Return both scaled and original input


# Define the Prediction Function
@tf.function
def make_prediction(input_data, model):
    return model(input_data, training=False)

# Predict Stroke Risk with Additional Conditions
def predict_stroke(input_data, model, threshold=0.5):
    input_scaled, user_input = input_data  # Extract scaled and original data

    raw_prediction = make_prediction(input_scaled, model)[0][0].numpy()

    # **Check if model output needs sigmoid**
    if raw_prediction < 0 or raw_prediction > 1:
        probability = 1 / (1 + np.exp(-raw_prediction))  # Apply sigmoid for logits
    else:
        probability = raw_prediction  # Already a probability

    # **Additional High-Risk Conditions**
    high_risk_conditions = (
        (user_input["age"] >= 65 and user_input["hypertension"] == 1) or
        (user_input["age"] >= 55 and user_input["heart_disease"] == 1) or
        (user_input["avg_glucose_level"] >= 180) or  # High glucose
        (user_input["bmi"] >= 35 and user_input["smoking_status"] == "smokes")  # Obesity + smoking
    )

    print(f"Raw Model Output: {raw_prediction}")
    print(f"Final Probability (after sigmoid if applied): {probability}")
    print(f"Threshold: {threshold}")

    if probability > threshold or high_risk_conditions:
        return "HIGH STROKE CONDITION"
    else:
        return "LOW STROKE CONDITION"


    
 

# API Route to Make Predictions
@api.route('/api_prediction', methods=['GET', 'POST'])
def api_prediction():
    data = {}
    
    if 'submit' in request.form:
        user_input = {
            'age': float(request.form['age']),
            'gender': request.form['gender'].lower(),
            'hypertension': int(request.form['hyper']),
            'heart_disease': int(request.form['heart']),
            'ever_married': request.form['mrg'].lower(),
            'work_type': request.form['wrk_type'].lower(),
            'residence_type': request.form['residence'].lower(),
            'avg_glucose_level': float(request.form['glucose']),
            'bmi': float(request.form['bmi']),
            'smoking_status': request.form['smoke'].lower(),
        }

        # Load model and scaler
        model, scaler = load_resources()

        # Preprocess input
        preprocessed_input = preprocess_input(user_input, scaler)
        print(f"Preprocessed Input: {preprocessed_input}")

        # Make prediction
        result = predict_stroke(preprocessed_input, model)
        print(f"Prediction Result: {result}")

        # Convert result to a meaningful string
        prediction_text = "High Stroke Risk" if result == 1 else "Low Stroke Risk"

        # Insert into prediction table
        qry = """
        INSERT INTO prediction 
        VALUES (null,'%s', '%s',curdate())
        """ % (
           session['uid'],result
        )
        
        insert(qry)  # Assuming `insert()` is a function to execute SQL queries

        # Pass the prediction result to the frontend
        data['prediction'] = result

    return render_template('medical_form.html', data=data)

@api.route('/prediction_history', methods=['GET'])
def prediction_history():
    # Fetch prediction history from the database
    qry = "SELECT result, date FROM prediction where user_id='%s' ORDER BY date DESC"%(session['uid'])
    history = select(qry)  # Fetch data

    return render_template('prediction_history.html', history=history)
@api.route('/user_view_laboratory', methods=['GET'])
def user_view_laboratory():
    data={}
    # Fetch prediction history from the database
    qry = "SELECT * from laboratory"
    data['view_laboratories'] = select(qry)  # Fetch data
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['lab_id']
    else:
        action=None
    if action=='request':
        r="insert into request values(null,'%s','%s','pending','pending',curdate(),'pending')"%(id,session['uid'])
        insert(r)
        
    return render_template('user_view_laboratory.html', data=data)\


@api.route('/send_msg',methods=['get','post'])
def send_msg():
    data={}
    receiver_id=request.args['doctor_id']
    f="SELECT * FROM chat WHERE sender_id='%s' AND receiver_id=(select login_id from doctors where doctor_id='%s') UNION SELECT * FROM chat WHERE sender_id=(select login_id from doctors where doctor_id='%s') AND receiver_id='%s' ORDER BY date_time"%(session['lid'],receiver_id,receiver_id,session['lid'])
    data['view_chat']=select(f)
    print("wwwwwwwwwwwwwww",f)
    if 'send' in request.form:
        msg=request.form['msg']
        did=request.args['doctor_id']
        d="select login_id from doctors where doctor_id='%s'"%(did)
        docid=select(d)
        if docid:
            dlid=docid[0]['login_id']
        qry13="insert into chat values(null,'%s','user','%s','doctor','%s',now())"%(session['lid'],dlid,msg)
        res13=insert(qry13)

    return render_template('send_msg.html',data=data)



@api.route('/user_view_booking',methods=['get','post'])
def user_view_booking():
    data={}
    
    qry15="""
SELECT 
    d.doctor_id,
    d.first_name,
    b.booking_id,
    b.status,
    b.book_date,
    f.amount,
    b.time
FROM 
    bookings b
JOIN 
    consulting_times ct ON b.consulting_id = ct.consulting_id
JOIN 
    doctors d ON ct.doctor_id = d.doctor_id
JOIN 
    fee f ON ct.consulting_id = f.consulting_id
WHERE 
    b.user_id = (SELECT user_id FROM users WHERE login_id='%s')
ORDER BY 
b.date_time DESC
""" % (session['lid'])
    data['view_booking']=select(qry15)
    return render_template('user_view_booking.html',data=data)

@api.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'lid' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in

    # Update the booking status to "Cancelled"
    qry_update = """
    UPDATE bookings 
    SET status = 'Cancelled', time = 'Cancelled' 
    WHERE booking_id = %s AND user_id = (SELECT user_id FROM users WHERE login_id='%s')
    """ % (booking_id, session['lid'])
    
    update(qry_update)
    
    flash("Booking has been successfully cancelled.", "success")
    return redirect(url_for('api.user_view_booking'))

@api.route('/user_doctor_chat')
def user_doctor_chat():
    data={}
    sender_id=request.args['sender_id']
    receiver_id=request.args['receiver_id']
    details=request.args['details']


    a="insert into chat values(null,'%s','user',(select login_id from doctors where doctor_id='%s'),'doctor','%s',now())"%(sender_id,receiver_id,details)
    res=insert(a)
    if res:
        data['status']="success"
    else:
        data['status']="failed"
    data['method']="chat"

    return str(data)


@api.route('/doctor_chat_details')
def doctor_chat_details():
    data={}
    sender_id=request.args['sender_id']
    receiver_id=request.args['receiver_id']
    f="SELECT * FROM chat WHERE sender_id='%s' AND receiver_id=(select login_id from doctors where doctor_id='%s') UNION SELECT * FROM chat WHERE sender_id=(select login_id from doctors where doctor_id='%s') AND receiver_id='%s' ORDER BY date_time"%(sender_id,receiver_id,receiver_id,sender_id)
    rg=select(f)
    if rg:
        data['status']="success"
        data['data']=rg
    else:
        data['status']="failed"
    data['method']="chatdetail"
    return str(data)


@api.route('/user_send_complaint',methods=['get','post'])
def user_send_complaint():
    data={}
    if 'submit' in request.form:
        comp=request.form['comp']
        i="insert into complaints values(null,'%s','%s','pending',curdate())"%(session['uid'],comp)
        insert(i)
        return redirect(url_for('api.user_send_complaint'))
    r="select * from complaints where user_id='%s'"%(session['uid'])
    data['view']=select(r)
    return render_template('user_send_complaint.html',data=data)

@api.route('/user_update_profile', methods=['GET', 'POST']) 
def user_update_profile():
    data = {}
    
    # Fetch user details
    qry = "SELECT * FROM users WHERE user_id='%s'" % (session['uid'])
    data['up'] = select(qry)
    
    if 'submit' in request.form:
        first_name = request.form['fname']
        last_name = request.form['lname']
        house_name = request.form['hname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']

        # Check if a new image is uploaded
        if 'image' in request.files and request.files['image'].filename:
            image = request.files['image']
            path = "static/images/" + str(uuid.uuid4()) + image.filename
            image.save(path)
        else:
            # Keep the existing image path if no new image is uploaded
            path = data['up'][0]['path']

        # Update user details
        qry2 = """UPDATE users 
                  SET first_name='%s', last_name='%s', house_name='%s', place='%s', 
                      phone='%s', email='%s', path='%s' 
                  WHERE user_id='%s'""" % (first_name, last_name, house_name, place, phone, email, path, session['uid'])
        res2 = update(qry2)
        
        flash("Profile updated successfully!", "success")
        return redirect(url_for('api.user_update_profile'))

    return render_template('user_update_profile.html', data=data)

from flask import render_template, request

@api.route('/user_chat_bot', methods=['GET', 'POST'])
def user_chat_bot():
    data = {}
    if 'submit' in request.form:
        chat = request.form['chat']
        gemini_response = generate_gemini_response(chat)
        
        # Split response into lines and store in 'out'
        data['out'] = gemini_response.split('\n')
    
    return render_template('chatbot.html', data=data)
