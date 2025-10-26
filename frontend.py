import streamlit as st
import subprocess
import sys
import requests
import json
import os

# initialise session state for confirmation dialog
if 'show_clear_confirmation' not in st.session_state:
    st.session_state.show_clear_confirmation = False

# initialise conversation history session state
if 'conversations' not in st.session_state:
    st.session_state.conversations = []
if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None

# JSON file path
JSON_FILE = "data.json"

def load_conversations():
    """Load conversations from JSON file"""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as f:
                data = json.load(f)
                # convert the flat list format to conversation groups
                conversations = []
                current_conversation = {"user_message": "", "ai_response": ""}
                
                for item in data:
                    if "user" in item:
                        if current_conversation["user_message"]:  # if we already have a user message, save the previous conversation
                            conversations.append(current_conversation.copy())
                            current_conversation = {"user_message": "", "ai_response": ""}
                        current_conversation["user_message"] = item["user"]
                    elif "ai" in item and current_conversation["user_message"]:
                        current_conversation["ai_response"] = item["ai"]
                        conversations.append(current_conversation.copy())
                        current_conversation = {"user_message": "", "ai_response": ""}
                
                # add the last conversation if it has a user message but no AI response
                if current_conversation["user_message"]:
                    conversations.append(current_conversation.copy())
                
                return conversations
        except (json.JSONDecodeError, KeyError) as e:
            st.error(f"Error loading conversations: {e}")
            return []
    return []

def save_conversations():
    """Save conversations to JSON file in the specified format"""
    data = []
    for conv in st.session_state.conversations:
        data.append({"user": conv["user_message"]})
        if conv["ai_response"]:  # only add AI response if it exists
            data.append({"ai": conv["ai_response"]})
    
    try:
        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving conversations: {e}")

def add_conversation(user_message, ai_response):
    """Add a new conversation and save to JSON"""
    new_conversation = {
        'user_message': user_message,
        'ai_response': ai_response
    }
    st.session_state.conversations.append(new_conversation)
    st.session_state.current_conversation = len(st.session_state.conversations) - 1
    save_conversations()

def clear_all_conversations():
    """Clear all conversations from session state and JSON file"""
    st.session_state.conversations = []
    st.session_state.current_conversation = None
    try:
        with open(JSON_FILE, 'w') as f:
            json.dump([], f)
    except Exception as e:
        st.error(f"Error clearing conversations: {e}")

# load conversations from JSON file on startup
if not st.session_state.conversations:
    st.session_state.conversations = load_conversations()

# website name
st.set_page_config(
    page_title="Paladins of Pi",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

BACKGROUND_COLOUR = "#040417"  # background colour #040417 is dark blueish

st.markdown(f"""
<style>
    .stApp {{
        background-color: {BACKGROUND_COLOUR};
    }}
    .sidebar .sidebar-content {{
        background-color: #0f0f23;
    }}
    .conversation-item {{
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 6px;
        cursor: pointer;
        background-color: #1a1a2e;
        color: white;
        border-left: 3px solid #4CC9F0;
    }}
    .conversation-item:hover {{
        background-color: #2a2a3e;
    }}
    .conversation-item.active {{
        background-color: #4CC9F0;
        color: black;
    }}
    .warning-box {{
        background-color: #2a1a1a;
        border: 1px solid #ff6b6b;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }}
</style>
""", unsafe_allow_html=True)

# sidebar - conversation History
st.sidebar.title("Paladins of Pi")
st.sidebar.markdown("---")

# new conversation button
if st.sidebar.button("+ New Chat", use_container_width=True):
    st.session_state.current_conversation = None
    st.rerun()

st.sidebar.markdown("### Previous Conversations")

# display conversation history
for i, conv in enumerate(st.session_state.conversations):
    # display conversation preview (first few words of user message)
    preview = conv['user_message'][:30] + "..." if len(conv['user_message']) > 30 else conv['user_message']
    
    # style based on whether this is the current conversation
    is_active = st.session_state.current_conversation == i
    item_class = "conversation-item active" if is_active else "conversation-item"
    
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        st.markdown(f'<div class="{item_class}">{preview}</div>', 
                   unsafe_allow_html=True)
    
    # add click functionality using buttons
    if st.sidebar.button("Load", key=f"load_{i}", use_container_width=True):
        st.session_state.current_conversation = i
        st.rerun()

st.sidebar.markdown("---")

# clear history button with confirmation
if st.sidebar.button("Clear History", use_container_width=True):
    st.session_state.show_clear_confirmation = True

# show confirmation dialog if triggered
if st.session_state.show_clear_confirmation:
    st.sidebar.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.sidebar.warning("⚠️ Are you sure you want to clear all chat history? This action cannot be undone.")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.sidebar.button("Yes, Clear All", type="primary", use_container_width=True):
            clear_all_conversations()
            st.session_state.show_clear_confirmation = False
            st.success("Chat history cleared!")
            st.rerun()
    
    with col2:
        if st.sidebar.button("Cancel", use_container_width=True):
            st.session_state.show_clear_confirmation = False
            st.rerun()
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# main content area
st.title("Paladins of Pi")

# display current conversation if one is selected
if st.session_state.current_conversation is not None:
    current_conv = st.session_state.conversations[st.session_state.current_conversation]
    st.subheader("Current Conversation")
    st.write(f"**You:** {current_conv['user_message']}")
    st.write(f"**AI:** {current_conv['ai_response']}")
    st.markdown("---")

# text subheaders above input box
st.subheader("Prompt Input")

prompt_input = st.text_area(
    "Ask thou question:",
    placeholder="It thirsts for your command...",
    height=150,
    key="prompt_input",
    help="This command will be sent to the Dungeon Master."
)

# button to send to ollama
if st.button("Send to Dungeon Master"):
    if prompt_input.strip():
        with st.spinner(""):
            try:
                with st.spinner("Awaiting the Dungeon Master's response..."):
                    response = requests.get("http://localhost:8501/generate", params={"q": prompt_input})
                    if response.status_code == 200:
                        data = response.json()
                        ai_response = data["ai_text"]
                        
                        # save conversation to JSON file
                        add_conversation(prompt_input, ai_response)
                        
                        # display response
                        st.text_area("Response:", value=ai_response, height=200)
                        
                        # Rrfresh to update sidebar
                        st.rerun()
                    else:
                        st.error(f"Error: {response.status_code}")    
            except subprocess.TimeoutExpired:
                st.error("Request timed out after 30 seconds")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a prompt first!")