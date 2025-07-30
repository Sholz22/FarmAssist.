import streamlit as st
from PIL import Image
from src.styles.SL_chat_theme_Olusola import *
from src.utils.farm_tools import *

from src.config import APP_TITLE, APP_ICON
from src.gemini_client import validate_api_key, validate_weather_api_key

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Validate API key
validate_api_key()
validate_weather_api_key()

# Initialize session state
if "name" not in st.session_state:
    st.session_state.name = ""
if "region" not in st.session_state:
    st.session_state.region = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clean up any existing chat history with wrong format
if st.session_state.chat_history:
    cleaned_history = []
    for item in st.session_state.chat_history:
        if len(item) == 2:
            # Convert old format to new format
            user_msg, bot_reply = item
            cleaned_history.append((user_msg, bot_reply, None))
        elif len(item) == 3:
            # Already in correct format
            cleaned_history.append(item)
    st.session_state.chat_history = cleaned_history


# Main app
def main():
    # Custom chat theme
    theme = StreamlitChatTheme()
    theme.apply_theme()

    st.title("🌿 FarmAssist 🌿")
    st.markdown("### Your Go-To Buddy for Farm Matters in Nigeria")

    if not st.session_state.name:
        st.markdown("---")
        with st.form("user_info", clear_on_submit=True):
            st.subheader("Welcome! Let's get FARMiliar! 😜")
            st.markdown("Please provide your information to get personalized farming advice:")
            name = st.text_input("Your First Name *", placeholder="Enter your first name")
            region = st.text_input("Your Region/State in Nigeria", placeholder="e.g., Lagos, Kano, Ogun (optional)")
            submitted = st.form_submit_button("Start Chatting", type="primary")
            if submitted:
                if name.strip():
                    st.session_state.name = name.strip().title()
                    st.session_state.region = region.strip().title() if region.strip() else "Nigeria"
                    st.success(f"Welcome, {st.session_state.name}! Ready to help with your farming questions.")
                    st.rerun()
                else:
                    st.error("Please enter your name to continue.")
    else:
        st.markdown("---")

        # Chat history display
        if st.session_state.chat_history:
            st.subheader("Let's get FARMiliar! 😜")
            for chat_item in st.session_state.chat_history:
                try:
                    if len(chat_item) >= 3:
                        user_msg, bot_reply, uploaded_image = chat_item
                    else:
                        user_msg, bot_reply = chat_item
                        uploaded_image = None
                    display_chat_message(user_msg, bot_reply, st.session_state.name, uploaded_image)
                except:
                    continue  
            st.markdown("---")

        # Input interface
        if not st.session_state.chat_history:
            st.subheader(f"Hi {st.session_state.name}! How may I assist you today?")
        
        # Create a container for the input
        input_container = st.container()
        
        with input_container:
            # Create tabs for text and image input
            tab1, tab2 = st.tabs(["💬 **Ask Question**", "🖼️ **Upload Image**"])
            
            with tab1:
                with st.form("chat_form", clear_on_submit=True):
                    user_input = st.text_area(
                        "What would you like to know about farming?",
                        placeholder="Type your farming question here...",
                        height=68,
                        label_visibility="collapsed"
                    )
                    submitted = st.form_submit_button("Send Message", type="primary")
                    if submitted and user_input.strip():
                        if handle_prompt(user_input):
                            st.rerun()
            
            with tab2:
                with st.form("image_form", clear_on_submit=True):
                    st.markdown("**Upload a crop leaf image for disease detection**")
                    uploaded_file = st.file_uploader(
                        "Choose a leaf image...", 
                        type=["jpg", "jpeg", "png"],
                        label_visibility="collapsed"
                    )
                    
                    # Show preview if image is uploaded
                    if uploaded_file:
                        image = Image.open(uploaded_file).convert("RGB")
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.image(image, caption="Image Preview", width=200)
                    
                    submitted_image = st.form_submit_button("Analyze Image", type="primary")
                    if submitted_image:
                        if predict_crop_disease(uploaded_file):
                            st.rerun()
                        else:
                            st.error("Please upload an image first.")

        # Start new session
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Start a new session", help="Clear chat and start fresh"):
                for key in ["name", "region", "chat_history"]:
                    st.session_state.pop(key, None)
                st.rerun()

        # Quick suggestions for new users
        if not st.session_state.chat_history:
            st.markdown("---")
            st.subheader("Frequently Asked Questions")
            st.markdown("Here are some common questions to get you started:")
            col1, col2 = st.columns(2)
            suggestions = [
                ("🌱 Best crops for my region", "What are the best crops to grow in my region considering the climate and soil?"),
                ("💧 Irrigation methods", "What are the most effective irrigation methods for small-scale farming in Nigeria?"),
                ("🐛 Pest control strategies", "How can I protect my crops from common pests and diseases?"),
                ("💰 Crop market information", "What are the current market trends and prices for agricultural products?")
            ]
            for i, (btn_text, q) in enumerate(suggestions):
                col = col1 if i % 2 == 0 else col2
                with col:
                    if st.button(btn_text, key=f"suggestion_{i}"):
                        if handle_prompt(q):
                            st.rerun()

    # Footer
    st.markdown(
        "<div style='text-align: center; padding: 20px; color: #666;'>"
        "<a href='https://github.com/Sholz22/FarmAssist..git' target='_blank'>View Source Code on GitHub (Sholz22)</a>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()