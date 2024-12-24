# filepath: /c:/Projects/image-to-text-app/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from dotenv import load_dotenv
import json
import pytesseract
import io
import openai
import os

app = FastAPI()

load_dotenv()
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/image-to-data/")
async def image_to_data(file: UploadFile = File(...)):
    # Read the uploaded image file
    image = Image.open(io.BytesIO(await file.read()))
    
    # Extract text from the image using pytesseract
    extracted_text = pytesseract.image_to_string(image)
    
    # Send the extracted text to GPT-3 or GPT-4
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[
            {"role": "system", "content": 'assistance to extract prices from the image in a parsable json format:[{label : "item name",value : { currentPrice : 5555, recentPrice:5555, avgPrice: 555 } }], no additional characters '},
            {"role": "user", "content": extracted_text}
        ],
        max_tokens=1000
    )
    
    # Get the GPT response text
    gpt_text = response.choices[0].message.content

    
    return {"extracted_text": extracted_text, "gpt_text": json.loads(gpt_text)}