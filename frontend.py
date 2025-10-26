import streamlit as st
import subprocess
import sys
import requests


# website name
st.set_page_config(
    page_title="Paladins of Pi",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

BACKGROUND_COLOUR = "#06061f"  # Soft blue

st.markdown(f"""
<style>
    .stApp {{
        background-color: {BACKGROUND_COLOUR};
    }}
</style>
""", unsafe_allow_html=True)

# title
st.title("Paladins of Pi")

# text subheaders above input box
st.subheader("Prompt Input")
st.write("**Using:**")

prompt_input = st.text_area(
    "Enter your prompt for the backend:",
    placeholder="Type your prompt here...",
    height=150,
    key="prompt_input",
    help="This prompt will be sent to your custom backend script"
)

# button to send to ollama
if st.button("Send to Dungeon Master"):
    if prompt_input.strip():
        with st.spinner("Processing your prompt..."):
            try:
                with st.spinner("Processing your Request..."):
                    response = requests.get("http://localhost:8501/generate", params={"q": prompt_input})
                    if response.status_code == 200:
                        data = response.json()
                        st.text_area("Response:", value=data["ai_text"], height=200)
                    else:
                        st.error(f"Error: {response.status_code}")    
            except subprocess.TimeoutExpired:
                st.error("Request timed out after 30 seconds")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a prompt first!")

# sidebar

st.sidebar.title("Paladins of Pi")


# option for selection boxes

# option = st.selectbox(
#     "Select a previous prompt:",
#     ("Prompt 1", "Prompt 2", "Prompt 3"),
#     help="Select a prompt from your history",
#     index = None,
#     placeholder = "Select Contact method",
# )

# st.write("You selected:", option)


# # colours, backgrounds - probably wont use
# background_colour = "959595" # background colour
# st.markdown(f"""
# <style>
#     .stApp {{
#         background-color: #{background_colour};
#     }}
# </style>
# """, unsafe_allow_html=True)

