import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from PIL import Image
import retrieval_logic
import constants

#Import rag chain from retrieval_logic
rag_chain = retrieval_logic.rag_chain
# Define multiple credentials with additional details
credentials = constants.credentials
# JavaScript to manage the scroll position
scroll_js = constants.scroll_js

# Function to handle message sending
def send_message():
    user_input = st.session_state.user_input
    if user_input:
        # Process user message
        with st.spinner('Loading...'):
            ai_msg = rag_chain.invoke({"question": user_input, "chat_history": st.session_state['chat_history']})
        
        st.session_state['chat_history'].extend([HumanMessage(content=user_input), ai_msg])
        # Print chat history for debugging
        # print("Updated chat history:", st.session_state['chat_history'])
        print(ai_msg)
        st.session_state['conversation_starter_used'] = True #To make the conversation_starter disappear
        st.toast('AI Replied!', icon='✅')

# Conversation Starters
def display_starters():
    conversation_starters = ["Explain my benefits.", "Tell me a joke.", "Am I eligible for a membership upgrade?", "How does Club Blue Horizon work?"]
    for starter in conversation_starters:
        if st.button(starter):
            with st.spinner('Please wait for it...'):
                # Send the starter to the LLM and get a response
                ai_response = rag_chain.invoke({"question": starter, "chat_history": st.session_state['chat_history']})
                # Append the AI's response to the chat history
                st.session_state['chat_history'].extend([HumanMessage(content=starter), ai_response])
                st.toast('AI Replied!', icon='✅')
                st.session_state['conversation_starter_used'] = True
                st.rerun()

# Define the main application function
def main_app(user_details):
    with st.spinner('Loading...'):
        # Load your image
        image = Image.open("logo2.png")
        
        # Use columns for better layout
        col1, col2 = st.columns([1, 12])

        # Set the title and the image as a logo
        with col1:
            st.image(image, width=110)  # You can adjust the width to suit your design
        
        with col2:
            st.title("Timeshare AI Assistant")
        # st.title("Timeshare AI Assistant 🤖🏖️")
        
        # Greeting message to the user from the LLM
        with st.spinner('Please wait for it...'):
            if 'greeted' not in st.session_state or not st.session_state['greeted']:
                greeting_msg = f"My name is {user_details['name']}. My membership level in the timeshare is {user_details['membership_level']}. I'm a member since {user_details['joining_year']}. 1) Say Hello to me, 2) Tell me that you are pleased to have me as a {user_details['membership_level']} member since {user_details['joining_year']}."
                ai_greeting = rag_chain.invoke({"question": greeting_msg, "chat_history": []})
                st.session_state['chat_history'].append(ai_greeting)
                st.session_state['greeted'] = True  # Ensure greeting happens only once per session
        
        # Container for chat history
        with st.container():
            for message in st.session_state['chat_history']:
                if isinstance(message, HumanMessage):
                    with st.chat_message("user", avatar="🧑‍💻"):
                        st.write(message.content)
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(message.content)
                        
        # Chat input for user message
        st.chat_input("Your message:", key='user_input', on_submit=send_message)
        
        #Display Conversation Starters
        if not st.session_state['conversation_starter_used']:
            display_starters()
            
        st.markdown(scroll_js, unsafe_allow_html=True)

# Define the login page function
def login_page():
    st.markdown("###### LOG IN TO CLUB BLUE HORIZONS")
    st.markdown("## Let's get you on vacation 🏖️")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        with st.spinner('Loading...'):
        # Verify credentials
            if email in credentials and credentials[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state['current_user'] = credentials[email]  # Store user details
                st.rerun()  # Rerun the app to refresh the page and variables
            else:
                st.error("Incorrect email or password.")
