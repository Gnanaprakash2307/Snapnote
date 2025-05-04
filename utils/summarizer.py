import os
import re
import sys
import google.generativeai as genai

# Import the API key from config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Set the Gemini API key
genai.configure(api_key=config.GEMINI_API_KEY)


def summarize_text(text, max_length=150):
    """
    Summarize text using Google's Gemini 1.5 Flash model
    """
    try:
        # Clean the text
        cleaned_text = re.sub(r'\s+', ' ', text).strip()

        # If text is already short, return it
        if len(cleaned_text.split()) <= max_length:
            return cleaned_text

        # Initialize the Gemini model
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        # Format the prompt for summarization
        prompt = f"Summarize the following text in a concise and clear way:\n\n{cleaned_text}"

        # Generate response
        response = model.generate_content(prompt)

        # Extract and return the summary
        return response.text.strip()

    except Exception as e:
        raise Exception(f"Summarization error: {str(e)}")
