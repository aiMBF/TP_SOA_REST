from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
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

def get_solvability(clientId: str):
    solvabilite_service_url = f"http://172.30.0.1:8002/client/{clientId}"
    response = requests.get(solvabilite_service_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error from solvabile service: {response.text}")

def get_eval_prop(taille: float, ville: str, adress: str):
    eval_service_url = "http://172.30.0.1:8001/evaluer"
    response = requests.post(eval_service_url, params={"taille":taille,"ville":ville,'adress':adress})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error from evaluation service: {response.text}")

def decision(valeur, propertyPrice, litiges, score, financial_cap, name):
    if (valeur <= propertyPrice) and (litiges == True) and (score > 50 and (financial_cap > 0)):
        return f"Bonjour Monsieur {name}, après étude de votre dossier, nous avons le plaisir de vous annoncer que le prêt pourra vous être accordé. Passer très vite à l'agence pour signer tous les documents nécessaires."
    return f"Bonjour Monsieur {name}, après étude de votre dossier, nous avons le regret de vous annoncer que votre situation actuelle ne vous permet pas de contracter ce prêt. Nous vous conseillons de revenir d'ici 6mois pour une nouvelle étude."


@app.get("/home/", response_class=HTMLResponse)
async def add_loan(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), clientId: str = Form(...)):
    # Sauvegarder le fichier
    extracted_text=""
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
        extracted_text = extract_text(file.filename)
        print("Text extracted and cleaned:", extracted_text)
    if extraction_loan_infos(extracted_text):
        loan_infos = json.loads(extraction_loan_infos(extracted_text))
        print(loan_infos)
        client_solvability = get_solvability(clientId)
        if loan_infos['description']:
            ville=""
            taille=0.0
            adresse=""
            if 'completeAdress' in loan_infos['description']['address'].keys():
                ville = loan_infos['description']['address']['town']
                taille = float(loan_infos['description']['surfaceArea'].split('m')[0])
                adresse = loan_infos['description']['address']['completeAdress']
            else:
                ville = loan_infos['description']['address']['town']
                taille = float(loan_infos['description']['surfaceArea'].split('m')[0])
                adresse = loan_infos['description']['address']['completeAddress']
            eval_result = get_eval_prop(taille, ville, adresse)
            print(type(eval_result))
            print(eval_result)
            final_decision = decision(eval_result['valeur_bien'], loan_infos['propertyPrice'],
                          eval_result['litiges_sur_le_bien'], client_solvability['score'], 
                          client_solvability['financial_cap'],loan_infos['name'])
            return final_decision
        return None
    return {"Oups": "Une erreur est survenue, veuillez réessayer plutard"}