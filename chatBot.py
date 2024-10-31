from tkinter import image_names

from dotenv import load_dotenv
from streamlit import text_input, header

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key = ['Your-API-KEY'])
model = genai.GenerativeModel("gemini-1.5-pro-latest")


#  Intitialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


#  configuring page
st.set_page_config(
    page_title = "ChatBot",
    page_icon = "💬",
    layout = "centered"
)


# streamlit page title
st.title("Chinna's ChatBot")

#  display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message["content"])


#  input field for user's message
user_prompt = st.chat_input("Ask ChatBot...")

def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt, stream=True)
        response.resolve()
        return response.text
    except Exception as e:
        return f"An error occured: {e}"

if user_prompt:
    #add users message to chat and display it
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    st.chat_message("user").markdown(user_prompt)

    with st.spinner("Generating response..."):
        assistant_response = get_gemini_response(user_prompt)
    st.session_state.chat_history.append({"role":"assistant","content":assistant_response})

    #  display ChatBot response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)




