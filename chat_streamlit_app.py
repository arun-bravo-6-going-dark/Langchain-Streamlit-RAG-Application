import streamlit as st
import os
from langchain_core.messages import AIMessage, HumanMessage
import config
from PIL import Image
from functions import main_app, login_page

api_key = config.openai_key
os.environ["OPENAI_API_KEY"] = api_key
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Streamlit app setup
# Set page configuration with title and layout
st.set_page_config(page_title='Timeshare AI Assistant', layout='wide')

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None  # To store the current logged-in user's details
if 'conversation_starter_used' not in st.session_state:
    st.session_state['conversation_starter_used'] = False

# Display the login page or the main application based on the login status
if st.session_state.logged_in:
    user_details = st.session_state['current_user']
    # Sidebar with user details and logout
    with st.sidebar:
        # Displaying user name and membership level
        image_path = user_details['profile_picture']
        image = Image.open(image_path)
        st.image(image, width=110)
        st.markdown("#### Name")
        st.write(f"{user_details['name']}")
        st.write('--------')
        st.markdown("#### Membership Level")
        st.write(f"{user_details['membership_level']}")
        st.write('--------')
        st.markdown("#### Member Since")
        st.write(f"{user_details['joining_year']}")
        
        # Display logout button and main application if logged in
        # if st.button("Logout"):
        if st.button("Logout", type="primary"):
            st.session_state.logged_in = False
            st.session_state['chat_history'] = []  # Clear the chat history
            st.session_state['current_user'] = None  # Clear the current user details
            st.session_state['greeted'] = False
            st.session_state['conversation_starter_used'] = False
            st.rerun()  # Rerun the app to refresh the page and variables
    
    main_app(user_details)
    
else:
    login_page()

