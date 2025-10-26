import streamlit as st
import requests

# website name
st.set_page_config(
    page_title="Paladins of Pi",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# title
st.title("Paladins of Pi")

# input label
st.subheader("Prompt Input")
st.write("**Using:**")

# text input box
prompt_input = st.text_area(
    "Enter your prompt for the backend:",
    placeholder="Type your prompt here...",
    height=150,
    key="prompt_input",
    help="This prompt will be sent to your custom backend script"
)

# button to send
if st.button("Send to Dungeon Master"):
    if prompt_input.strip():
        with st.spinner("Processing your prompt..."):
            try:
                # call backend flask server
                response = requests.get("http://localhost:8000/generate", params={"q": prompt_input})

                if response.status_code == 200:
                    data = response.json()
                    st.text_area("Response:", value=data.get("ai_text", ""), height=200)
                else:
                    st.error(f"Error: {response.status_code}")

            except requests.exceptions.Timeout:
                st.error("Request timed out after 30 seconds")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a prompt first")
