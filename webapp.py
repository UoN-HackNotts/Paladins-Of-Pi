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
st.subheader("Your Software Solution")
st.write("Welcome to our Sass SaaS application!")

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"  # Specific model you want to use

def query_ollama(prompt):
    """Send prompt to Ollama using Phi3 Mini model"""
    try:
        # First, let's check if the model is available
        try:
            # Try POST method (standard Ollama API)
            payload = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(OLLAMA_URL, json=payload)
            
            # If we get a 404, the model might not be pulled yet
            if response.status_code == 404:
                st.error(f"Model '{MODEL_NAME}' not found. Please make sure you've pulled it with: ollama pull {MODEL_NAME}")
                return f"Error: Model {MODEL_NAME} not available"
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to Ollama. Make sure Ollama is running on localhost:11434")
            return "Error: Cannot connect to Ollama service"
        
        # Check for errors
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Text input for Ollama prompt
st.subheader("Ollama Prompt Input")
st.write(f"**Using model:** `{MODEL_NAME}`")

prompt_input = st.text_area(
    "Enter your prompt for Ollama:",
    placeholder=f"Type your prompt here... This will be sent to {MODEL_NAME}",
    height=150,
    key="prompt_input",
    help=f"This prompt will be sent to {MODEL_NAME} to generate a response"
)

# Button to send the prompt to Ollama
if st.button("Send to Phi3 Mini"):
    if prompt_input:
        with st.spinner(f"Waiting for {MODEL_NAME} response..."):
            response_data = query_ollama(prompt_input)
        
        st.success("✅ Prompt sent to Ollama successfully!")
        
        # Display the results
        st.subheader("Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Your Prompt:**")
            st.info(prompt_input)
        
        with col2:
            st.write(f"**{MODEL_NAME} Response:**")
            
            # Handle different response formats
            if isinstance(response_data, str):
                # Error message
                st.error(response_data)
            elif isinstance(response_data, dict):
                # Successful API response
                if 'response' in response_data:
                    st.success(response_data['response'])
                elif 'message' in response_data:
                    st.success(response_data['message'])
                else:
                    st.write("Unexpected response format:")
                    st.json(response_data)
            else:
                st.write(response_data)
        
        # Show additional info if available
        if isinstance(response_data, dict):
            with st.expander("Response Details"):
                if 'model' in response_data:
                    st.write(f"**Model:** {response_data['model']}")
                if 'created_at' in response_data:
                    st.write(f"**Generated at:** {response_data['created_at']}")
                if 'total_duration' in response_data:
                    st.write(f"**Total duration:** {response_data['total_duration']/1e9:.2f}s")
                
                st.write("**Full response JSON:**")
                st.json(response_data)
            
    else:
        st.warning("⚠️ Please enter a prompt first!")

# Setup instructions in sidebar
with st.sidebar:
    st.header("Setup Instructions")
    st.write(f"To use {MODEL_NAME}, make sure you:")
    st.write("1. Have Ollama installed")
    st.write(f"2. Pull the model: `ollama pull {MODEL_NAME}`")
    st.write("3. Start Ollama: `ollama serve`")
    st.write("4. Keep Ollama running in the background")
    
    # Quick test button
    if st.button("Test Ollama Connection"):
        test_response = query_ollama("Say 'Hello' in a creative way.")
        if isinstance(test_response, dict) and 'response' in test_response:
            st.success("✅ Connection successful!")
        else:
            st.error("❌ Connection failed")
