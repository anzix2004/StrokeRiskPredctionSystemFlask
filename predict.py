import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

# Step 1: Load the Pre-trained Model and Scaler
def load_resources():
    try:
        model = load_model("stroke_prediction_lstm_2.h5")
        scaler = np.load("scaler.npy", allow_pickle=True).item()
        print("Model and scaler loaded successfully!")
        return model, scaler
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Ensure the model file 'stroke_prediction_lstm_2.h5' and scaler file 'scaler.npy' are in the same directory.")
        exit()

# Step 2: Gather User Input
def get_user_input(age,):
    print("Enter the following details for stroke prediction:")
    age = float(age)
    gender = input("Gender (Male/Female): ").strip().lower()
    hypertension = int(input("Hypertension (0 = No, 1 = Yes): "))
    heart_disease = int(input("Heart Disease (0 = No, 1 = Yes): "))
    ever_married = input("Ever Married (Yes/No): ").strip().lower()
    work_type = input("Work Type (Private/Self-employed/Govt_job/Children/Never_worked): ").strip().lower()
    residence_type = input("Residence Type (Urban/Rural): ").strip().lower()
    avg_glucose_level = float(input("Average Glucose Level: "))
    bmi = float(input("BMI (Body Mass Index): "))
    smoking_status = input("Smoking Status (smokes/formerly smoked/never smoked/unknown): ").strip().lower()

    return {
        "age": age,
        "gender": gender,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "ever_married": ever_married,
        "work_type": work_type,
        "residence_type": residence_type,
        "avg_glucose_level": avg_glucose_level,
        "bmi": bmi,
        "smoking_status": smoking_status,
    }

# Step 3: Preprocess User Input
def preprocess_input(user_input, scaler):
    # Map user input to the expected feature names
    input_data = {
        "age": user_input["age"],
        "hypertension": user_input["hypertension"],
        "heart_disease": user_input["heart_disease"],
        "avg_glucose_level": user_input["avg_glucose_level"],
        "bmi": user_input["bmi"],
        "gender_Male": 1 if user_input["gender"] == "male" else 0,
        "ever_married_Yes": 1 if user_input["ever_married"] == "yes" else 0,
        "work_type_Private": 1 if user_input["work_type"] == "private" else 0,
        "work_type_Self-employed": 1 if user_input["work_type"] == "self-employed" else 0,
        "work_type_Govt_job": 1 if user_input["work_type"] == "govt_job" else 0,
        "work_type_Children": 1 if user_input["work_type"] == "children" else 0,
        "Residence_type_Urban": 1 if user_input["residence_type"] == "urban" else 0,
        "smoking_status_smokes": 1 if user_input["smoking_status"] == "smokes" else 0,
        "smoking_status_formerly smoked": 1 if user_input["smoking_status"] == "formerly smoked" else 0,
        "smoking_status_never smoked": 1 if user_input["smoking_status"] == "never smoked" else 0,
    }

    # Align with training features
    all_features = scaler.feature_names_in_
    input_array = np.zeros(len(all_features))
    for i, feature in enumerate(all_features):
        if feature in input_data:
            input_array[i] = input_data[feature]

    # Scale the input
    input_scaled = scaler.transform([input_array])
    return input_scaled.reshape(1, 1, -1)  # Reshape for LSTM input

# Step 4: Predict Stroke Risk
def predict_stroke(input_data, model):
    prediction = model.predict(input_data)
    return int(prediction > 0.5)  # Convert to binary (0 or 1)

# Step 5: Main Execution
if __name__ == "__main__":
    # Ensure the script is executed properly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Change to script's directory

    # Load model and scaler
    model, scaler = load_resources()

    # Get user input
    user_input = get_user_input()

    # Preprocess the input
    preprocessed_input = preprocess_input(user_input, scaler)

    # Make prediction
    result = predict_stroke(preprocessed_input, model)

    # Display result
    if result == 1:
        print("Prediction: High risk of stroke.")
    else:
        print("Prediction: Low risk of stroke.")
