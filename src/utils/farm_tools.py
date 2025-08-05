import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from src.prompts import build_prompt, build_disease_prompt
from src.gemini_client import get_gemini_response, model as gemini_model
import logging
logging.basicConfig(level=logging.INFO)

class_names = [
    'Cashew anthracnose', 'Cashew gumosis', 'Cashew healthy', 'Cashew leaf miner', 'Cashew red rust',
    'Cassava bacterial blight', 'Cassava brown spot', 'Cassava green mite', 'Cassava healthy', 'Cassava mosaic',
    'Maize fall armyworm', 'Maize grasshoper', 'Maize healthy', 'Maize leaf beetle', 'Maize leaf blight',
    'Maize leaf spot', 'Maize streak virus',
    'Tomato healthy', 'Tomato leaf blight', 'Tomato leaf curl',
    'Tomato septoria leaf spot', 'Tomato verticulium wilt'
]

# Load CNN model
# model = tf.keras.models.load_model("models/crop_disease_model.h5")
model = tf.keras.models.load_model("models/mobilenetv2_best_model.h5")


# Verify that image is a crop using Gemini
def verify_crop_image_with_gemini(image):
    """Use Gemini to verify if the image contains a crop leaf"""
    try:
        verification_prompt = """
        Please analyze this image and determine if it shows a plant part or crop worm that could be analyzed for disease detection.

        I need you to check if this image contains:
        1. A visible plant part such as a crop leaf, tree trunk, bark, stem, or branch
        2. Clear visual signs or surface details that may allow for disease analysis
        3. A crop worm or insect that could be analyzed for pest detection
        4. No presence of humans, animals, or unrelated objects

        Please respond with ONLY one of these options:
        - "VALID_PLANT_IMAGE" if it's a suitable plant image for disease or health analysis
        - "NOT_PLANT_IMAGE" if it's not a plant or not suitable for analysis
        """

        # Generate response with image
        response = gemini_model.generate_content([verification_prompt, image])
        gemini_response = response.text.strip()

        return gemini_response == "VALID_PLANT_IMAGE"

    except Exception as e:
        print(f"Verification failed: {e}")
        # If Gemini verification fails, allow the image to proceed
        return True


# Preprocess image for CNN
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)


# Display a chat-style message
def display_chat_message(user_msg, bot_reply, user_name, uploaded_image=None):
    # User message with optional image
    user_content = f'<div class="message-content">{user_msg}</div>'
    if uploaded_image:
        # Convert image to base64 for display
        import base64
        import io
        buffered = io.BytesIO()
        uploaded_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        user_content = f'''
        <div class="message-content">
            <img src="data:image/png;base64,{img_str}" style="max-width: 200px; border-radius: 8px; margin-bottom: 8px;">
            <div>{user_msg}</div>
        </div>
        '''
    
    st.markdown(
        f"""
        <div class="user-message">
            <div class="message-header">👤 {user_name}</div>
            {user_content}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="bot-message">
            <div class="message-header">🌿 FarmAssist</div>
            <div class="message-content">{bot_reply}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Handle text-based prompt
def handle_prompt(prompt):
    if not prompt.strip():
        return False
    with st.spinner("Just a second..."):
        try:
            full_prompt = build_prompt(
                st.session_state.name,
                st.session_state.region,
                prompt,
                st.session_state.chat_history
            )
            reply = get_gemini_response(full_prompt)
            st.session_state.chat_history.append((prompt, reply, None)) 
            return True
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return False


# Handle image upload and analysis
def predict_crop_disease(uploaded_file):
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        
        with st.spinner("Verifying image content..."):
            # First, verify with Gemini if it's a crop leaf
            is_valid_crop = verify_crop_image_with_gemini(image)
            
            if not is_valid_crop:
                user_msg = "Uploaded an image for disease analysis"
                bot_response = f"""
                <b>Crop Image Verification Failed</b><br><br>
                I don't think this image shows a crop suitable for disease analysis.<br><br>
                <b>Please upload an image that shows:</b><br>
                • A clear photo of a plant or crop leaf<br>
                • From crops like: <b>Cashew, Cassava, Maize, or Tomato</b><br>
                • Single leaf or diseased part filling most of the image<br>
                • Good lighting and focus<br><br>
                If you have questions about crop diseases or farming in general, feel free to ask using the text chat!
                """
                st.session_state.chat_history.append((user_msg, bot_response, image))
                return True
        
        with st.spinner("Analyzing crop disease..."):
            processed = preprocess_image(image)
            prediction = model.predict(processed)
            class_index = np.argmax(prediction)
            confidence = prediction[0][class_index]
            label = class_names[class_index]
            
            # Set confidence threshold
            CONFIDENCE_THRESHOLD = 0.55
            
            # Check if confidence is too low
            if confidence < CONFIDENCE_THRESHOLD:
                user_msg = "Uploaded an image for disease analysis"
                bot_response = f"""
                <b>Prediction: {label}</b><br>
                <b>Low Confidence Warning:</b> I'm not very confident about this result.<br>
                <b>Please consider:</b><br>
                1. Uploading a clearer, well-lit photo of a crop leaf<br>
                2. Ensuring the crop is one of: <b>Cashew, Cassava, Maize, or Tomato</b><br>
                3. Making sure the leaf fills most of the image frame<br>
                The prediction above might not be accurate due to image quality or if this isn't one of the supported crops.<br>
                If you need help with other crops or general farming questions, feel free to ask me using the text chat!
                """
                st.session_state.chat_history.append((user_msg, bot_response, image))
                return True
            
            # Normal prediction with good confidence
            disease_prompt = build_disease_prompt(label, st.session_state.name, st.session_state.region)
            response = get_gemini_response(disease_prompt)
            
            user_msg = "Uploaded an image for disease analysis"
            bot_response = f"Disease Analysis: <b>{label}</b>\n\n{response}"
            st.session_state.chat_history.append((user_msg, bot_response, image))
            return True
    return False


