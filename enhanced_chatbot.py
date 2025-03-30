import streamlit as st

# Must be the first Streamlit command
st.set_page_config(page_title="Enhanced Q&A Chatbot")

from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

# Load API Key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Model Selection
model_options = {
    "Text Chatbot (Pro)": "gemini-1.5-pro-latest",
    "Fast Chatbot (Flash)": "gemini-1.5-flash-latest",
    "Image Generation": "gemini-2.0-flash-exp-image-generation"
}

# Sidebar for Model Selection
st.sidebar.title("Settings")
selected_model = st.sidebar.selectbox("Choose Model", list(model_options.keys()))

# App Title
st.title("🚀 Enhanced Gemini Chatbot")

# Initialize Chat History
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Text Input
user_input = st.text_input("Ask me anything:", key="input")
submit = st.button("Ask")

# Clear Chat Button
if st.sidebar.button("Clear Chat"):
    st.session_state['chat_history'] = []

# Function to Generate Text Response
def get_text_response(question, model_name):
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

# Function to Generate Images
def generate_image(prompt):
     model = genai.GenerativeModel(model_options["Image Generation"])
     response = model.generate_content(prompt)
     return response.text  # Ensure correct extraction

# Handle Chat Submission
if submit and user_input:
    st.session_state['chat_history'].append(("You", user_input))

    if selected_model in ["Text Chatbot (Pro)", "Fast Chatbot (Flash)"]:
        response = get_text_response(user_input, model_options[selected_model])
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

    elif selected_model == "Image Generation":
        response = generate_image(user_input)
        st.image(response, caption="Generated Image", use_column_width=True)

# Display Chat History
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"**{role}**: {text}")
