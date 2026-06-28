# backend/main.py

# Csomagok és modulok importálása
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Virtual try-on működéséhez szükséges modulok importálása
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response

import base64
import google.auth
import google.auth.transport.requests
import requests

# Környezeti változók betöltése a .env fájlból
from dotenv import load_dotenv
import os

# Környezeti változók betöltése
load_dotenv()

GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_LOCATION = os.environ["GCP_LOCATION"]

# Alap FastAPI alkalmazás létrehozása
app = FastAPI()

# CORS beállítások
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Engedélyezett eredetek (pl. frontend alkalmazás URL-je)
    allow_credentials=True,
    allow_methods=["*"],  # Engedélyezett HTTP metódusok
    allow_headers=["*"],  # Engedélyezett HTTP fejlécek
)


# Egészségügyi ellenőrzés végpont - Ez a végpont ellenőrzi, hogy a szerver fut-e és elérhető-e. Ez fonts Kubernetes vagy más szolgáltatások számára, hogy ellenőrizzék a backend állapotát.
# Metódus: GET
# URL: /health
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Virtual Try-on végpont - Ez a végpont kezeli a virtuális próbafülke funkciót. A felhasználó feltölthet egy képet, és a szerver feldolgozza azt, majd visszaküldi a módosított képet.
# Metódus: POST
# URL: /virtual-try-on
@app.post("/virtual-try-on")
async def virtual_try_on(
    model_image: UploadFile = File(...),
    clothing_image: UploadFile = File(...),
):

    model_bytes = await model_image.read()
    clothing_bytes = await clothing_image.read()

    credentials, _ = google.auth.default()
    credentials.refresh(google.auth.transport.requests.Request())

    url = (
        f"https://{GCP_LOCATION}-aiplatform.googleapis.com/v1"
        f"/projects/{GCP_PROJECT_ID}/locations/{GCP_LOCATION}"
        f"/publishers/google/models/virtual-try-on-001:predict"
    )

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {credentials.token}"},
        json={
            "instances": [
                {
                    "personImage": {
                        "image": {
                            "bytesBase64Encoded": base64.b64encode(model_bytes).decode()
                        }
                    },
                    "productImages": [
                        {
                            "image": {
                                "bytesBase64Encoded": base64.b64encode(
                                    clothing_bytes
                                ).decode()
                            }
                        }
                    ],
                }
            ],
            "parameters": {
                "baseSteps": 10,
            },
        },
    )

    result = response.json()
    print("Result from GCP Agent Platform:", result)
    return Response(
        base64.b64decode(result["predictions"][0]["bytesBase64Encoded"]),
        media_type="image/png",
    )
