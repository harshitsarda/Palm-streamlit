import streamlit as st
import speech_recognition as sr 
import google.generativeai as palm
from streamlit_chat import message

palm.configure(api_key='AIzaSyCxnS9lj_8QJEZVYLOv0Dn94vTuFf2ZmEw') 

st.title("AI Assitant")

choice = st.radio("Choose input mode", ["Text", "Voice"])

if 'generate' not in st.session_state:
    st.session_state['generate']=[]
if 'past' not in st.session_state:
    st.session_state['past']=[]
    
def response_api(prompt):
    response = palm.chat(context='Reply always in a friendly tone.', messages=prompt)  
    message = response.last
    return message

user_text = ""  # Initialize user_text outside the if conditions

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

if user_text:  
    output = response_api(user_text)
    
    st.session_state.generate.append(output)
    st.session_state.past.append(user_text)
        
if st.session_state['generate']:
    for i in range(len(st.session_state['generate'])-1,-1,-1):
        message(st.session_state["past"][i], is_user=True, key=str(i)+'_user')
        message(st.session_state['generate'][i], key=str(i))
