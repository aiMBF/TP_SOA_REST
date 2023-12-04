from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import re
import textract


app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

def clean_text(text):
    cleaned_text = re.sub(r'[^\x00-\x7F]+|\n|\t', ' ', text)
    return cleaned_text.strip()

def extract_text(file_path):
    try:
        text = textract.process(file_path).decode("utf-8")
        return clean_text(text)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error extracting text: {e}")


@app.get("/home/", response_class=HTMLResponse)
async def add_loan(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), clientId: str = Form(...)):
    # Sauvegarder le fichier
    extracted_text=""
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
        print(f)
        print(file.filename)
        extracted_text = extract_text(file.filename)
        print("Text extracted and cleaned:", extracted_text)
    client_data={'clientID':clientId, 'letter':extracted_text}
    return {"filename": client_data}