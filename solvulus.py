import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Use secrets.toml

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Custom Gemini prompt
input_prompt = """
You are a calculus problem solving expert. 
An image will be uploaded along with a question. You must:
- Greet the user.
- Explain every step with proper LaTeX formatting.
- Use clear math formatting: \\frac for fractions, \\int for integrals, and superscripts.
- Wrap equations using `$...$` on each line.
- Label steps clearly: Step 1, Step 2, etc.
- Avoid using <sub>, <sup>, or HTML-style markup.
- Make sure each mathematical expression is rendered cleanly.

At the end, mention the app name: "Solved with Solvulus!"
"""

# Image conversion helper
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Streamlit UI setup
st.set_page_config(page_title="Solvulus")
st.sidebar.header("🧠 Your Calculus Problem Solver")
st.sidebar.write("Powered by **Google Gemini AI**")

st.title("Solvulus")
st.subheader("Your calculus tutor in a click")

input = st.text_input("What do you want me to do?", key="input")
uploaded_file = st.file_uploader("Upload image of the problem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Handle click
if st.button("🚀 Let's Go!"):
    if not uploaded_file:
        st.warning("Please upload an image of the problem.")
    elif not input:
        st.warning("Please enter what you want me to do.")
    else:
        try:
            image_data = input_image_details(uploaded_file)
            with st.spinner("Solving your problem..."):
                response = model.generate_content([input_prompt, image_data[0], input])
                result = response.text

            st.subheader("✅ Here's your solution:")

            # Display formatted response
            for line in result.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if line.startswith("**Step") or line.lower().startswith("step"):
                    st.markdown(f"### {line}")
                elif line.startswith("$") and line.endswith("$"):
                    st.latex(line.strip("$"))
                else:
                    st.markdown(line)

            st.success("Solved with Solvulus. Come back anytime!")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
