import streamlit as st
import speech_recognition as sr 
import google.generativeai as palm
from streamlit_chat import message
import PyPDF2
import io

# Configure Google PaLM API
palm.configure(api_key='AIzaSyCxnS9lj_8QJEZVYLOv0Dn94vTuFf2ZmEw')

# Custom CSS for better UI
st.markdown(
    """
    <style>
    .main {
        background-color: #128C7E;
    }
    .stTextInput, .stTextArea, .stFileUploader, .stButton, .stRadio {
        margin-bottom: 15px;
    }
    .stButton button {
        background-color: #25D366;
        color: black;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #128C7E;
    }
    .message {
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #128C7E;
        align-self: flex-right;
    }
    .bot-message {
        background-color: black;
        align-self: flex-start;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page title and layout
st.title("AI Assistant")
st.markdown("### Chat with the AI Assistant or Upload a PDF for Contextual Responses")

# Chatbot mode selection
mode = st.radio("Choose chatbot mode", ["Normal Chatbot", "PDF Chatbot"])

# PDF content initialization
pdf_text = ""

if mode == "PDF Chatbot":
    # PDF upload functionality
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Read PDF content
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        st.success("PDF uploaded successfully!")

# Input mode selection
choice = st.radio("Choose input mode", ["Text", "Voice"])

# Initialize session state
if 'generate' not in st.session_state:
    st.session_state['generate'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# API response function
def response_api(prompt):
    context = f'Reply always in a friendly tone.'
    if pdf_text:
        context += f' Base your answers on the following content: {pdf_text}'
    response = palm.chat(context=context, messages=prompt)
    message = response.last
    return message

# User input processing
user_text = ""  # Initialize user_text

if choice == "Text":
    user_text = st.text_input("Enter text:") 
else:
    if st.button("Start Voice Input"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Speak now...")
            audio = r.listen(source) 
        
        try:
            user_text = r.recognize_google(audio)
            st.text("Voice Input: " + user_text)
            
        except:
            user_text = ""  

# Generate response if there is user input
if user_text:
    output = response_api(user_text)
    
    st.session_state.generate.append(output)
    st.session_state.past.append(user_text)
    

# Display chat messages in reverse order for latest at the bottom
chat_container = st.container()
with chat_container:
    for i in range(len(st.session_state['generate'])-1, -1, -1):
        user_msg_key = f"{i}_user"
        bot_msg_key = f"{i}"
        
        st.markdown(f'<div class="message bot-message">{st.session_state["generate"][i]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="message user-message">{st.session_state["past"][i]}</div>', unsafe_allow_html=True)

