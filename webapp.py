import streamlit as st

# Set the website name properly
st.set_page_config(
    page_title="SASS SAAS Platform",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Main content
st.title("SASS SAAS Platform")
st.subheader("Your Software Solution")
st.write("Welcome to our SASS SAAS application!")

# # input testing
# st.write("[Learn more >](https://roblox.com)")


if st.button("Click Me"):
    st.write("[Button was clicked!](https://roblox.com)")


# my button runs williams scripts - which sends a request which goes back to me.
if st.button("Run Williams Script"):
    st.switch_page("test/ollama_chat_test_forjames")