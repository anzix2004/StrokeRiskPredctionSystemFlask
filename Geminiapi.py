import google.generativeai as genai

# Google Gemini API Key
GOOGLE_API_KEY = 'AIzaSyCkNiXT_JNr8VoWYXc8s2r27XOakZukQeM'

# Configure the Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Set the model explicitly to a currently supported one
model = genai.GenerativeModel('gemini-1.5-flash')  # or 'gemini-1.5-pro'

# Function to generate response
def generate_gemini_response(prompt):
    context_prompt = (
        "This conversation focuses on stroke awareness, prevention, symptoms, "
        "treatment, and rehabilitation. " + prompt
    )
    response = model.generate_content(context_prompt)
    return response.text

# Example usage
user_message = "What are the early signs of a stroke and how can it be prevented?"
gemini_response = generate_gemini_response(user_message)

# Display output as paragraph
for idx, line in enumerate(gemini_response.split('\n'), start=1):
    line = line.strip()
    if line:
        print(f"{idx}. {line}")