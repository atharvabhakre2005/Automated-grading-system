import google.generativeai as genai
import PIL.Image
import io
from pypdf import PdfReader
from utils.helper import check_file_extension

GOOGLE_API_KEY = ''  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

def OCR_Gemini_Model(file, edit=False):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Check file extension (path or uploaded file)
    if isinstance(file, str):  # If the file is a path (string)
        filetype = check_file_extension(file)
        with open(file, "rb") as f:
            file_data = f.read()
    else:  # If the file is an uploaded file object
        filetype = check_file_extension(file.name)
        file_data = file.read()

    # Process based on file type (PDF or image)
    if filetype == "PDF":
        # For PDF, use PdfReader to extract images
        reader = PdfReader(io.BytesIO(file_data))
        page = reader.pages[0]  # Assuming we're extracting from the first page
        image_bytes = page.images[0].data  # Extract image data from PDF
        image = PIL.Image.open(io.BytesIO(image_bytes))
    else:
        # For image, directly open with PIL
        image = PIL.Image.open(io.BytesIO(file_data))

    edit_text = "edit words written incorrectly" if edit else "do not edit any word"
    
    # Generate content using Gemini
    response = model.generate_content([
        f"Extract only the text written in the area labeled 'Answer' and {edit_text}.",
        image
    ])

    return response.text.strip()
