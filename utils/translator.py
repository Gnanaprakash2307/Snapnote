import os
import re
import sys
import requests

# Import the API key config (optional, not used here)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def translate_text_libre(text, target_lang='ta'):
    """
    Translate text using LibreTranslate API
    """
    try:
        # Clean the text
        cleaned_text = re.sub(r'\s+', ' ', text).strip()

        # Prepare the API request
        url = "https://libretranslate.com/translate"
        payload = {
            'q': cleaned_text,
            'source': 'en',
            'target': target_lang,
            'format': 'text'
        }

        # Make the API call
        response = requests.post(url, data=payload)

        # Check for errors
        if response.status_code != 200:
            raise Exception(f"LibreTranslate API error: {response.text}")

        # Return the translated text
        return response.json()['translatedText']

    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

# Example usage
if __name__ == "__main__":
    original_text = "Welcome to your AI-powered note assistant!"
    translated = translate_text_libre(original_text, target_lang='ta')  # to Tamil
    print("Translated:", translated)
