from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import re
import textract
import requests


app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

app = FastAPI()


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

def extraction_loan_infos(letter: str):
    extraction_service_url = "http://172.30.0.1:8003/extract"
    data_to_send = {"letter": letter}
    print(f'data_to_send {data_to_send}')
    response = requests.post(extraction_service_url, params=data_to_send)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error from extraction service: {response.text}")

@app.get("/home/", response_class=HTMLResponse)
async def add_loan(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), clientId: str = Form(...)):
    # Sauvegarder le fichier
    extracted_text=""
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
        print(file.filename)
        extracted_text = extract_text(file.filename)
        print("Text extracted and cleaned:", extracted_text)
    loan_infos = extraction_loan_infos(extracted_text)
    client_loan_info={'clientID':clientId, 'infos':loan_infos}
    return {"data": client_loan_info}