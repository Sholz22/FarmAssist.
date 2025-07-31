import logging 
import requests
from src.config import weather_api_key


Tools = [
    {
        "function_declarations": [
            {
                "name": "get_weather",
                "description": "Get current weather information for a specific location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The location to get the weather for, e.g., 'Lagos', 'Abuja', etc."
                        }
                    },
                    "required": ["location"]
                }
            }
        ]
    }

]


# Tool function
def get_weather(location: str):
    """Get current weather information for a specific location using OpenWeatherMap API."""
    logging.info(f"Tool called: get_weather | Location: {location}")
    
    api_key = weather_api_key  # Make sure this is defined elsewhere
    if not api_key:
        logging.error("Missing weather API key.")
        return "⚠️ Weather API key is not configured."

    if not location:
        logging.warning("No location provided.")
        return "⚠️ Please specify a location to get weather information."

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            logging.error(f"Weather API error {response.status_code}: {response.text}")
            return f"⚠️ Hmm, I couldn't fetch the weather for '{location}'. Maybe try a nearby town?"

        data = response.json()
        weather_desc = data.get("weather", [{}])[0].get("description", "Unknown conditions").title()
        temp_c = data.get("main", {}).get("temp", "N/A")
        feels_like = data.get("main", {}).get("feels_like", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")
        wind_speed = data.get("wind", {}).get("speed", "N/A")

        return (
            f"It's currently {weather_desc.lower()} in {location.title()}, with a temperature of {temp_c}°C "
            f"that feels like {feels_like}°C. The humidity is around {humidity}%, and the wind is blowing at "
            f"{wind_speed} m/s.\n\n"
            f"🌾 You might want to plan lighter activities if you're working outside. Shall I suggest anything?"
        )


    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {str(e)}")
        return "⚠️ Network error while fetching weather. Please try again."
    
    except Exception as e:
        logging.exception("Unexpected error occurred in get_weather")
        return "⚠️ Something went wrong while getting the weather."




# translation_models = {
#     "yo": pipeline("translation", model="Davlan/afro-xlmr-mini-en-yo"),
#     "ig": pipeline("translation", model="Davlan/afro-xlmr-mini-en-ig"),
#     "ha": pipeline("translation", model="Davlan/afro-xlmr-mini-en-ha"),
# }


# def translate_text(text: str, target_language: str) -> str:
#     logging.info(f"Tool called: translate_text | Text: {text}, Target Language: {target_language}")
#     if target_language not in translation_models:
#         return "Unsupported language"
    
#     translator = translation_models[target_language]
#     result = translator(text)
#     return result[0]["translation_text"]