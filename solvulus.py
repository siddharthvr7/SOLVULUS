import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key="AIzaSyBJ5Fn-Bo-IEDTmubX-pRzz2HdOKEz6F_w")

model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input_text,image_data,prompt):
    response=model.generate_content([input_text,image_data[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("no file uploaded")
    
st.set_page_config(page_title="Solvulus")
st.sidebar.header("Your Calculus Problem Solver")
st.sidebar.write("Made by Sid")
st.sidebar.write("Powered by Google Gemini AI")
st.header("Solvulus")
st.subheader("Calculus made easy!")

input = st.text_input("What do you want me to do?" , key="input")
uploaded_file = st.file_uploader("Select image of the problem" , type=["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

ssubmit = st.button("Lets Go!")

input_prompt= """You are a calculus problem solving expert. 
An image will be uploaded as a calculus problem and you will have to solve the problem based on the question asked.
Make sure to greet the user first and then provide the required information. Make sure to maintain a uniform font and size.
Make sure to a give step by step solution of the problem. Make sure the subsequent steps follow line by line order, i.e every 'equal-to (=) sign' in different line.
Make sure to provide graphs along with the solutions. At the end, repeat the name of our app "Solvulus" and encourage the user to use it again"""
if ssubmit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Here's what you need to know")
    st.write(response)

