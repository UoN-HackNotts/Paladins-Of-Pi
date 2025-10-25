import streamlit as st
import subprocess
import sys
import ollama  # ensure this is imported if needed elsewhere

# website name
st.set_page_config(
    page_title="Paladins of Pi",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

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
if st.button("Send to Ollama"):
    if prompt_input.strip():
        with st.spinner("Processing your prompt..."):
            try:
                # run the ollama_chat.py script as a subprocess
                # using command line arguments only (remove the input parameter)
                result = subprocess.run([
                    sys.executable,  # Use the same Python interpreter
                    "ollama_chat.py",
                    prompt_input
                ], 
                capture_output=True,
                text=True,
                timeout=30  # ?? second timeout
                )
                
                if result.returncode == 0:
                    st.success("Request completed!")
                    st.subheader("Response from Ollama:")
                    st.text_area("Response:", value=result.stdout, height=200)
                else:
                    st.error(f"Script failed with return code {result.returncode}")
                    st.text_area("Error details:", value=result.stderr, height=200)
                    
            except subprocess.TimeoutExpired:
                st.error("Request timed out after 10 seconds")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a prompt first!")

# # colours, backgrounds
# background_colour = "959595" # background colour
# st.markdown(f"""
# <style>
#     .stApp {{
#         background-color: #{background_colour};
#     }}
# </style>
# """, unsafe_allow_html=True)