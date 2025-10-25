import streamlit as st

import subprocess
import sys

# Set the website name properly
st.set_page_config(
    page_title="Sass SaaS Platform",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Main content
st.title("Sass SaaS Platform")
st.subheader("prompt!")
st.write("Welcome to our Sass SaaS application!")

# Text input for backend prompt
st.subheader("Backend Prompt Input")
st.write("**Using:** Custom Backend Script")

prompt_input = st.text_area(
    "Enter your prompt for the backend:",
    placeholder="Type your prompt here... This will be sent to your backend script",
    height=150,
    key="prompt_input",
    help="This prompt will be sent to your custom backend script"
)

# button to send to ollama
if st.button("Send to Ollama"):
    if prompt_input.strip():
        with st.spinner("Processing your prompt..."):
            try:
                # Run the ollama_chat.py script as a subprocess
                result = subprocess.run([
                    sys.executable,  # Use the same Python interpreter
                    "ollama_chat.py"
                ], 
                input=prompt_input.encode(),  # Pass input to the script
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
                )
                
                if result.returncode == 0:
                    st.success("Request completed!")
                    st.subheader("Response from Ollama:")
                    st.code(result.stdout, language="text")
                else:
                    st.error(f"Script failed: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                st.error("Request timed out after 30 seconds")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a prompt first!")


# colours, backgrounds

background_colour = "959595" # background colour

st.markdown(f"""
<style>
    .stApp {{
        background-color: {background_colour};
    }}
</style>
""", unsafe_allow_html=True)