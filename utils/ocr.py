import pytesseract
from PIL import Image


def extract_text_from_image(image_path):
    """
    Extract text from an image using OCR
    """
    try:
        # Open the image
        image = Image.open(image_path)

        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)

        return text
    except Exception as e:
        raise Exception(f"OCR processing error: {str(e)}")