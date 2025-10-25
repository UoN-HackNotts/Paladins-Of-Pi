import streamlit as st
import requests
import json

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

# Backend configuration
BACKEND_URL = "http://localhost:8000"  # Adjust port if your backend runs on different port

def query_backend(prompt):
    """Send prompt to backend script"""
    try:
        # Prepare parameters for GET request
        params = {
            "q": prompt,  # q=query, carries the main text
            "page": 1     # You can modify this based on your needs
        }
        
        # Send GET request to backend
        response = requests.get(f"{BACKEND_URL}/generate", params=params)
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Parse and return JSON response
        data = response.json()
        return data
        
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to backend. Make sure your backend server is running on {BACKEND_URL}")
        return {"error": "Cannot connect to backend service"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error connecting to backend: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

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

# Button to send the prompt to backend
if st.button("Send to Backend"):
    if prompt_input:
        with st.spinner("Waiting for backend response..."):
            response_data = query_backend(prompt_input)
        
        st.success("✅ Prompt sent to backend successfully!")
        
        # Display the results
        st.subheader("Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Your Prompt:**")
            st.info(prompt_input)
        
        with col2:
            st.write("**Backend Response:**")
            
            # Handle different response formats
            if isinstance(response_data, dict) and 'error' in response_data:
                st.error(response_data['error'])
            elif isinstance(response_data, dict):
                st.success("Backend processed successfully!")
                st.json(response_data)
            else:
                st.write(response_data)
        
        # Show additional info if available
        if isinstance(response_data, dict) and 'error' not in response_data:
            with st.expander("Response Details"):
                st.write("**Full response JSON:**")
                st.json(response_data)
            
    else:
        st.warning("⚠️ Please enter a prompt first!")

# Setup instructions in sidebar
with st.sidebar:
    st.header("Setup Instructions")
    st.write("To use this application, make sure you:")
    st.write("1. Have your backend script (`ollama_chat.py`) running")
    st.write("2. The backend should be accessible at the configured URL")
    st.write("3. Keep the backend server running in the background")
    
    # Quick test button
    if st.button("Test Backend Connection"):
        test_response = query_backend("Test connection")
        if isinstance(test_response, dict) and 'error' not in test_response:
            st.success("✅ Backend connection successful!")
        else:
            st.error("❌ Backend connection failed")