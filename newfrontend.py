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

# game description box
st.markdown("""
**Your local Dungeon Master — no cloud, no accounts**

Tell the Dungeon Master something quick (one line is fine), hit **Send to Dungeon Master**, and in a few seconds you’ll get a tiny, vivid medieval scene — under 50 words — generated right here on this Raspberry Pi. It’s private, offline and a bit magical.

**How to use**
1. Type a short prompt (e.g. “a weary knight at dawn”).  
2. Click **Send to Dungeon Master**.  
3. Read the scene and find it saved in the sidebar.

If nothing appears, check the backend/Ollama is running on this device — otherwise you should be good to go.

""")

# input label
st.subheader("Converse with the Dungeon Master")

# text input box
prompt_input = st.text_area(
    "Enter your request for the dungeon master:",
    placeholder="Type your request here...",
    height=150,
    key="prompt_input",
    help="This request will be sent to the dungeon master"
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
