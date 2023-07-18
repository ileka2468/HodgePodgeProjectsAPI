from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from api_utils import apiUtils
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import base64


app = FastAPI()

base_path = "/license"

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class licensePostBody(BaseModel):
    license_key: str = Field(min_length=40, max_length=40)
    machine_id: str = Field(min_length=5)

class emailPostBody(BaseModel):
    email: str = Field(min_length=1, max_length=200)


@app.get('/')
def greet():
    return {"status": "Hello Welcome to CloakAPI, you shouldn't be here are you lost?"}

@app.post(f"{base_path}/verify")
async def verify(data: licensePostBody):
    license_key = data.license_key
    machine_id = data.machine_id

    helper = apiUtils()
    response = await helper.verifyUser(license_key, machine_id)

    return {"status": response}

@app.post(f"{base_path}/activate")
async def activate(data: licensePostBody):
    license_key = data.license_key
    machine_id = data.machine_id

    helper = apiUtils()
    response = await helper.activateUser(license_key, machine_id)

    return {"status": response}

@app.post('/smecemail')
async def registerEmail(data: emailPostBody):
    email = data.email
    helper = apiUtils()
    response = await helper.registerEmail(email)

    if response == "Registered":
        html_email = open('welcome.html', "r").read()
        sent_html_email = html_email.replace("https://www.stmargaretschicago.org/unsubscribe", f"https://www.stmargaretschicago.org/unsubscribe/{base64.b64encode(email.encode()).decode()}")
        message = Mail(
            from_email='newsletter@stmargaretschicago.org',
            to_emails=email,
            subject='St. Margaret\'s Episcopal Church - Thanks for Subscribing!',
            html_content=sent_html_email)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            sgresponse = sg.send(message)
            print(sgresponse.status_code)
            print(sgresponse.body)
            print(sgresponse.headers)
        except Exception as e:
            print("Error sending email\n", e)

    return {"status": response}

