import streamlit as st
import subprocess
import sys
import requests
import json
import os

# Initialize session state for confirmation dialog and expanded states
if 'show_clear_confirmation' not in st.session_state:
    st.session_state.show_clear_confirmation = False

# Initialize session state for expanded conversations
if 'expanded_conversations' not in st.session_state:
    st.session_state.expanded_conversations = {}

# initialise conversation history session state
if 'conversations' not in st.session_state:
    st.session_state.conversations = []
if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None

# JSON file path
JSON_FILE = "data.json"

def truncate_text(text, max_length=20):
    """Truncate text to max_length characters and add ... if longer"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def toggle_expand(conv_index):
    """Toggle the expanded state for a conversation"""
    st.session_state.expanded_conversations[conv_index] = not st.session_state.expanded_conversations.get(conv_index, False)

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
    st.session_state.expanded_conversations = {}
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
    initial_sidebar_state="collapsed"  # Collapse sidebar since we're not using it
)

BACKGROUND_COLOUR = "#040417"  # background colour

st.markdown(f"""
<style>
    .stApp {{
        background-color: {BACKGROUND_COLOUR};
    }}
    .chat-history {{
        margin-top: 20px;
        padding: 15px;
        border-radius: 10px;
        background-color: #1a1a2e;
    }}
    .user-message {{
        background-color: #2a2a3e;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 3px solid #4CC9F0;
        cursor: pointer;
        transition: background-color 0.3s;
    }}
    .user-message:hover {{
        background-color: #3a3a4e;
    }}
    .ai-message {{
        background-color: #1e1e2e;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 3px solid #F72585;
        cursor: pointer;
        transition: background-color 0.3s;
    }}
    .ai-message:hover {{
        background-color: #2e2e3e;
    }}
    .warning-box {{
        background-color: #2a1a1a;
        border: 1px solid #ff6b6b;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }}
    .expand-icon {{
        float: right;
        font-weight: bold;
        color: #4CC9F0;
    }}
</style>
""", unsafe_allow_html=True)

# main content area
st.title("Paladins of Pi")

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
                        
                        # Save conversation to JSON file
                        add_conversation(prompt_input, ai_response)
                        
                        # Display response
                        st.text_area("Response:", value=ai_response, height=200, key="response_area")
                        
                        # Refresh to update chat history
                        st.rerun()
                    else:
                        st.error(f"Error: {response.status_code}")    
            except subprocess.TimeoutExpired:
                st.error("Request timed out after 30 seconds")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a prompt first!")

# Display chat history below the response area
if st.session_state.conversations:
    st.markdown("---")
    st.subheader("Chat History")
    
    # Clear history button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Clear History", use_container_width=True):
            st.session_state.show_clear_confirmation = True
    
    # Show confirmation dialog if triggered
    if st.session_state.show_clear_confirmation:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.warning("⚠️ Are you sure you want to clear all chat history? This action cannot be undone.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Yes, Clear All", type="primary", use_container_width=True):
                clear_all_conversations()
                st.session_state.show_clear_confirmation = False
                st.success("Chat history cleared!")
                st.rerun()
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_clear_confirmation = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display all conversations in reverse order (newest first)
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    
    for i, conv in enumerate(reversed(st.session_state.conversations)):
        # Calculate the original index (since we're displaying in reverse)
        original_index = len(st.session_state.conversations) - 1 - i
        
        # Check if this conversation is expanded
        is_expanded = st.session_state.expanded_conversations.get(original_index, False)
        
        # Display user message with expand/collapse functionality
        user_display_text = conv["user_message"] if is_expanded else truncate_text(conv["user_message"])
        expand_icon = "▼" if is_expanded else "▶"
        
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(f"**You:** {user_display_text}", 
                        key=f"user_{original_index}",
                        use_container_width=True,
                        help="Click to expand/collapse"):
                toggle_expand(original_index)
                st.rerun()
        
        with col2:
            st.markdown(f'<div class="expand-icon">{expand_icon}</div>', unsafe_allow_html=True)
        
        # Display AI message with expand/collapse functionality
        if conv["ai_response"]:
            ai_display_text = conv["ai_response"] if is_expanded else truncate_text(conv["ai_response"])
            
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"**AI:** {ai_display_text}", 
                            key=f"ai_{original_index}",
                            use_container_width=True,
                            help="Click to expand/collapse"):
                    toggle_expand(original_index)
                    st.rerun()
            
            with col2:
                st.markdown(f'<div class="expand-icon">{expand_icon}</div>', unsafe_allow_html=True)
        
        # Add separator between conversations (except for the last one)
        if i < len(st.session_state.conversations) - 1:
            st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)