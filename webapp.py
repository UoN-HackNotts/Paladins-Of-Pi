import streamlit as st
from ollama_chat import query_ollama

# Set the website name properly
st.set_page_config(
    page_title="Sass SaaS Platform",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Main content
st.title("Sass SaaS Platform")
st.subheader("Your Software Solution")
st.write("Welcome to our Sass SaaS application!")

# # input testing
# st.write("[Learn more >](https://roblox.com)")


if st.button("Click Me"):
    st.write("[Button was clicked!](https://roblox.com)")


# my button runs williams scripts - which sends a request which goes back to me.
if st.button("Run Williams Script"):
    st.switch_page("test/ollama_chat_test_forjames")

# text input to run williams script
st.text_input("Enter your script input:", key="script_input")