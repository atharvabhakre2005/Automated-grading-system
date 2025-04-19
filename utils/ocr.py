import google.generativeai as genai
import PIL.Image
import io
from pypdf import PdfReader
from utils.helper import check_file_extension

GOOGLE_API_KEY = 'AIzaSyBx8hsXA7hbEPwztlrHJiFDDYA56FqJgsQ' 
genai.configure(api_key=GOOGLE_API_KEY)

def OCR_Gemini_Model(file, edit=False):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    filetype = check_file_extension(file.name)
    if filetype == "PDF":
        reader = PdfReader(file)
        page = reader.pages[0]
        image_bytes = page.images[0].data
        image = PIL.Image.open(io.BytesIO(image_bytes))
    else:
        image = PIL.Image.open(file)

    edit_text = "edit words written incorrectly" if edit else "do not edit any word"
    response = model.generate_content([
        f"Extract only the text written in the area labeled 'Answer' and {edit_text}.",
        image
    ])

    return response.text.strip()
