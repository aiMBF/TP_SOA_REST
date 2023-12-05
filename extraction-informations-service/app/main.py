from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
import openai
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


async def getLoanInformations(letter):
    print(letter)
    system_msg = 'You are a helpful assistant.'

    user_msg = f"""I want to extract information about the tenant from this letter, 
    such as his name, customer ID, description of what he wants to buy, address, 
    monthly income and expenses, price of the property he wants to buy, etc. 
    Here's the text: {letter}. You'll need to extract the result into a json. For the keys,you must 
    use camelcase. For the description, for example, create a json with the type 
    of accommodation, such as home or apartment, the surface area, such as 300m2, and the address 
    of the accommodation, such as town,code postal, all the interesting information
    about the accommodation.
    You also must not return text with the result.
    You just must return the json that content elements. 
    Here is the schema you must respect when returning results:
      {{{{"name": "John Doe",
        "customerId": "client-00X",
        "description": {{
            "accommodationType": "apartment",
            "surfaceArea": "300m2",
            "address": {{
            "town": "Paris",
            "postalCode": "75015",
            "completeAdress":"6e arrondissement de Paris"
            }}
        }},
        "contact": {{
            "phone": "+33 5 67784890",
            "email": "johndoe@gmail.com"
        }},
        "loanAmount": 12000,
        "monthlyIncome": 3700,
        "monthlyExpenses": 2400,
        "propertyPrice": 20000
        }}}}"""

    # Create a dataset using GPT
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                                      {"role": "user", "content": user_msg}])
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."
    return response["choices"][0]["message"]["content"]

@app.post("/extract")
async def extract_data(letter: str):
    user_loan_infos = await getLoanInformations(letter)
    return user_loan_infos
