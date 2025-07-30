import google.generativeai as genai
from src.config import GEMINI_API_KEY, MODEL_NAME
import streamlit as st
from src.tools import Tools, get_weather

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

last_bot_reply = None

def get_gemini_response(prompt):
    """Get response from Gemini AI model, using tools only when explicitly called."""
    global last_bot_reply

    try:
        response = model.generate_content(
            prompt,
            tools=Tools,  
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1000,
                top_p=0.8,
                top_k=40
            )
        )

        replies = []

        for part in response.parts:
            if hasattr(part, "function_call") and part.function_call:
                func = part.function_call
                name = func.name
                args = func.args or {}

                # Handle tool call
                if name == "get_weather":
                    location = args.get("location", "unspecified")
                    result = get_weather(location)
                    replies.append(f"🌤️ Weather in {location}: {result}")

                else:
                    replies.append(f"⚠️ Tool `{name}` is not implemented.")
            
            elif hasattr(part, "text") and part.text.strip():
                # Natural language response
                replies.append(part.text.strip())

        final_reply = "\n\n".join(replies) if replies else "⚠️ No response generated."
        last_bot_reply = final_reply
        return final_reply

    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return "I'm sorry, I'm having trouble responding right now. Please try again shortly."




def validate_api_key():
    """Check if Gemini API key is configured."""
    if not GEMINI_API_KEY:
        st.error("Gemini API key not found. Please set your GEMINI_API_KEY in the .env file.")
        st.stop()
        return False
    return True

    
