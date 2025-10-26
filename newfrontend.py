import streamlit as st
import requests
import json
import os
import html

# initialise session state for confirmation dialog and expanded states
if 'show_clear_confirmation' not in st.session_state:
    st.session_state.show_clear_confirmation = False

# initialise session state for expanded conversations
if 'expanded_conversations' not in st.session_state:
    st.session_state.expanded_conversations = {}

# initialise conversation history session state
if 'conversations' not in st.session_state:
    st.session_state.conversations = []
if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None

# store the most recent exchange for the special box
if 'latest_user' not in st.session_state:
    st.session_state.latest_user = ""
if 'latest_ai' not in st.session_state:
    st.session_state.latest_ai = ""

JSON_FILE = "data.json"

def truncate_text(text, max_length=20):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def toggle_expand(conv_index):
    st.session_state.expanded_conversations[conv_index] = not st.session_state.expanded_conversations.get(conv_index, False)

def load_conversations():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as f:
                data = json.load(f)
                conversations = []
                current_conversation = {"user_message": "", "ai_response": ""}
                
                for item in data:
                    if "user" in item:
                        if current_conversation["user_message"]:
                            conversations.append(current_conversation.copy())
                            current_conversation = {"user_message": "", "ai_response": ""}
                        current_conversation["user_message"] = item["user"]
                    elif "ai" in item and current_conversation["user_message"]:
                        current_conversation["ai_response"] = item["ai"]
                        conversations.append(current_conversation.copy())
                        current_conversation = {"user_message": "", "ai_response": ""}
                
                if current_conversation["user_message"]:
                    conversations.append(current_conversation.copy())
                
                return conversations
        except:
            return []
    return []

def save_conversations():
    data = []
    for conv in st.session_state.conversations:
        data.append({"user": conv["user_message"]})
        if conv["ai_response"]:
            data.append({"ai": conv["ai_response"]})
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_conversation(user_message, ai_response):
    new_conversation = {'user_message': user_message, 'ai_response': ai_response}
    st.session_state.conversations.append(new_conversation)
    st.session_state.current_conversation = len(st.session_state.conversations) - 1
    save_conversations()

def clear_all_conversations():
    st.session_state.conversations = []
    st.session_state.current_conversation = None
    st.session_state.expanded_conversations = {}
    with open(JSON_FILE, 'w') as f:
        json.dump([], f)

if not st.session_state.conversations:
    st.session_state.conversations = load_conversations()

st.set_page_config(
    page_title="Paladins of Pi",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Updated colour palette
CREAM = "#F7F5EE"
DARK_BROWN = "#5A4636"
SAGE = "#657F69"
DEEP_TEAL = "#0F5B5B"
INK = "#2B2A26"

st.markdown(f"""
<style>
    .stApp {{
        background-color: {CREAM} !important;
    }}

    h1, h2 {{
        color: {DARK_BROWN} !important;
        text-align: center;
    }}

    .description-box {{
        background-color: #e9ddc5;
        border-left: 5px solid {DEEP_TEAL};
        padding: 14px 16px;
        border-radius: 8px;
        margin-bottom: 18px;
        color: {INK} !important;
        font-size: 15px;
    }}

    textarea, .stTextArea textarea {{
        background: #efe7cf !important;
        color: {INK} !important;
        border: 1px solid #b9ad96 !important;
        border-radius: 8px !important;
    }}

    .stButton>button {{
        background-color: {DEEP_TEAL};
        color: #F5F5DC;
        border: 1px solid #294847;
        border-radius: 8px;
        transition: 0.1s ease-in-out;
    }}

    .stButton>button:hover {{
        background-color: {SAGE} !important;
        color: {CREAM} !important;
        border: 1px solid #6d8574;
    }}

    .stButton>button:active {{
        background-color: #3d564c !important;
        color: {CREAM} !important;
        border: 1px solid #556e63;
    }}

    header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stHeader"] {{
        background-color: {CREAM} !important;
        color: {CREAM} !important;
        border: none !important;
        box-shadow: none !important;
    }}

    header div {{ display: none !important; }}

    /* latest response panel styles */
    .latest-wrap {{
        margin-top: 8px;
    }}
    .latest-title {{
        color: {DARK_BROWN};
        font-weight: 700;
        margin: 6px 2px;
        text-align: left;
    }}
    .latest-box {{
        background: #efe7cf;
        color: {INK};
        border: 1px solid #b9ad96;
        border-left: 6px solid {DEEP_TEAL};
        border-radius: 10px;
        padding: 14px 16px;
        white-space: pre-wrap;
        line-height: 1.35;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# title
st.title("Paladins of Pi")

# description
st.markdown("""
<div class="description-box">
You stand before a Dungeon Master of ancient code\n
Speak thy intentions, commands, emotions or deeds\n
The Lord of the Dungeon shall react and unfold as written fate\n
Write your request below to continue your tale...
</div>
""", unsafe_allow_html=True)

# prompt input box
prompt_input = st.text_area(
    "Ask thy question:",
    placeholder="What dost thou seek...",
    height=150,
    key="prompt_input"
)

# send request
if st.button("Send to Dungeon Master"):
    if prompt_input.strip():
        with st.spinner("Awaiting the Dungeon Master's response..."):
            try:
                response = requests.get("http://localhost:8000/generate", params={"q": prompt_input})
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data["ai_text"]

                    # save to history
                    add_conversation(prompt_input, ai_response)

                    # update latest panel content
                    st.session_state.latest_user = prompt_input
                    st.session_state.latest_ai = ai_response
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt first")

# --- latest response special box directly under the prompt ---
if st.session_state.latest_ai:
    safe_user = html.escape(st.session_state.latest_user)
    safe_ai = html.escape(st.session_state.latest_ai)
    st.markdown(
        f"""
        <div class="latest-wrap">
            <div class="latest-title">Latest response</div>
            <div class="latest-box">{safe_ai}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# chat history display
if st.session_state.conversations:
    st.markdown("---")
    st.subheader("Your Tale")

    if st.button("Clear History", use_container_width=True):
        st.session_state.show_clear_confirmation = True

    if st.session_state.show_clear_confirmation:
        st.warning("Are you sure you want to clear all chat history?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, Clear All", type="primary", use_container_width=True):
                clear_all_conversations()
                # also clear latest panel
                st.session_state.latest_user = ""
                st.session_state.latest_ai = ""
                st.session_state.show_clear_confirmation = False
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_clear_confirmation = False
                st.rerun()

    for i, conv in enumerate(reversed(st.session_state.conversations)):
        is_expanded = st.session_state.expanded_conversations.get(i, False)

        user_display = conv["user_message"] if is_expanded else truncate_text(conv["user_message"])
        ai_display = conv["ai_response"] if is_expanded else truncate_text(conv["ai_response"])

        if st.button(f"You: {user_display}", key=f"user_{i}", use_container_width=True):
            toggle_expand(i)
            st.rerun()

        if conv["ai_response"]:
            if st.button(f"DM: {ai_display}", key=f"ai_{i}", use_container_width=True):
                toggle_expand(i)
                st.rerun()
