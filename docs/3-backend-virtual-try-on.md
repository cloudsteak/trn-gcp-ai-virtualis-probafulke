# Backend Virtual Try-On fejlesztés

Ebben a fejlesztési lépések és a kódtöredékek találhatók lépésről-lépésre.

## Alap információk

- Kód mappa: `backend`
- Kód nyelv: Python
- Kód keretrendszer: FastAPI
- Kód célja: A virtuális próbafülke backend logikájának implementálása, amely a ruhák illeszkedését és megjelenését kezeli. Itt kötjük össze a backend-et a Google Cloud AI szolgáltatásaival (Enterprise Agent Platform).
- Struktúra:

```
..
└── backend/
    ├── main.py              ← minden backend logika itt van
    ├── requirements.txt     ← pip függőségek
    ├── example.env          ← másold .env-re és töltsd ki
    └── .env                 ← lokális beállítások (gitignore!)
```

- Előfeltételek:
  - gcloud CLI telepítése
  - A szükséges Google Cloud API-k engedélyezése a projektben (AI Platform, AI Generative Models)

## Bejelentkezés a Google Cloud Platformra

1. Nyisd meg a terminált és futtasd a következő parancsot:

```bash
gcloud auth login
```

2. Kövesd a megjelenő utasításokat a böngészőben történő bejelentkezéshez.

3. Alapértelmezett projekt beállítása (cseréld ki a `your-project-id`-t a saját projekt azonosítódra):

```bash
gcloud config set project your-project-id
```

4. ADC (Application Default Credentials) beállítása a következő paranccsal:

```bash
gcloud auth application-default login
```

5. Ellenőrizd a bejelentkezést a következő parancs futtatásával:

```bash
gcloud auth list
```

1. **Környezeti változók példafájl**: Hozz létre egy `example.env` fájlt a projekt gyökérkönyvtárában, amely példaként szolgál a környezeti változók beállításához. A fájl tartalmazza a szükséges Google Cloud projekt azonosítót és a régiót.

Tartalma:

```
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=europe-west1
```

2. **.env fájl létrehozása**: Másold az `example.env` fájlt `.env` néven, és töltsd ki a saját Google Cloud projekted adataival. Ez a fájl tartalmazza a szükséges környezeti változókat a backend működéséhez.

3. **Függőségek kibővítése**: Add hozzá a `requirements.txt` fájlhoz a szükséges Python csomagokat, amelyeket a backend működéséhez telepíteni kell. A fájl tartalma:

```
fastapi
uvicorn[standard]
python-multipart
google-auth
requests
python-dotenv
```

4. **Függőségek telepítése**: A létező virtuális környezetben, és telepítsd a szükséges Python csomagokat a `requirements.txt` fájl alapján.

```bash
pip install -r requirements.txt
```

5. **Környezeti változók betöltése**: A `.env` fájlban található környezeti változókat a `python-dotenv` csomag segítségével töltsd be a backend alkalmazásba. A FastAPI alkalmazás indításakor a következő kódot használhatod:

```python
from dotenv import load_dotenv
import os

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION = os.getenv("GCP_LOCATION")
```

6. **Szerver indítása**: A FastAPI szerver helyi indításához használd az alábbi parancsot:

```bash
python -m uvicorn main:app --reload --port 8000
```

_Megjegyzés:_ Ez minden kódváltoztatás után újraindítja a szervert, így azonnal láthatod a változtatások hatását.

7. **A `/virtual-try-on` végpont**: Ez a legfontosabb végpont, amely a virtuális próbafülke logikáját kezeli. A frontendről érkező képeket fogadja, és a Google Cloud AI szolgáltatásait használja a ruhák illeszkedésének és megjelenésének feldolgozására. Két képet fogadunk multipart form-data formátumban: az egyik a modell (felhasználó) képe, a másik a ruhadarab képe. A végpont feldolgozza ezeket a képeket, és visszaadja az eredményt a frontendnek.

```python
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response

# ...

@app.post("/virtual-try-on")
async def virtual_try_on(model_image: UploadFile = File(...), clothing_image: UploadFile = File(...)):

    # A feltöltött képek beolvasása
    model_bytes = await model_image.read()
    clothing_bytes = await clothing_image.read()

    # TODO: GCP AI szolgáltatások hívása a képek feldolgozására

    return Response(content=b"Processed image bytes", media_type="image/png")
```

8. **Új végpont tesztelése**: A curl paranccsal teszteljük le a képfeltöltést.

_Megjegyzés_: Ellenőrizd,hogy a `no_1.jpg` és `n_ruha.jpg` képek az `images` mappában vannak.

```bash
curl -X POST "http://localhost:8000/virtual-try-on" -F "model_image=@../images/no_1.jpg" -F "clothing_image=@../images/n_ruha.jpg" --output proba.jpg
```

Ebben a lépésben még üres a válasz – de a végpont már fogad fájlokat.

9. **GCP AI hívás megvalósítása**: A következő lépés a GCP AI szolgáltatásainak integrálása a `/virtual-try-on` végpontba. Ehhez a Google Cloud AI generatív modellek API-ját használjuk, amely lehetővé teszi a képek feldolgozását és a ruhák illeszkedésének vizualizálását.

Hogyan működik a GCP AI hívás:

1. Lekéri az ADC tokent (`gcloud auth application-default login`)
2. Base64-re kódolja a két képet
3. POST-ot küld az Agent Platform `:predict` endpointjára
4. Visszakapott base64 képet PNG-ként adja tovább

```python
import base64

import google.auth
import google.auth.transport.requests
import requests

# ... virtual_try_on függvényen belül, a read után ...
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
                        "bytesBase64Encoded": base64.b64encode(person_bytes).decode()
                    }
                },
                "productImages": [
                    {
                        "image": {
                            "bytesBase64Encoded": base64.b64encode(product_bytes).decode()
                        }
                    }
                ],
            }
        ],
        "parameters": {"baseSteps": 10},
    },
)

result = response.json()
return Response(
    base64.b64decode(result["predictions"][0]["bytesBase64Encoded"]),
    media_type="image/png",
)
```

### Mi történik itt?

```
Böngésző                    Backend                         Vertex AI
   │                           │                                │
   │  POST /virtual_try-on     │                                │
   │  (2 kép)                  │                                │
   │ ─────────────────────────>│                                │
   │                           │  POST .../virtual-try-on-001:predict
   │                           │  (base64 képek + ADC token)    │
   │                           │ ──────────────────────────────>│
   │                           │                                │
   │                           │  PNG (base64 a JSON-ban)       │
   │                           │ <──────────────────────────────│
   │  image/png                │                                │
   │ <─────────────────────────│                                │
```

Ha a curl parancs most már jól működik és PNG-t ad vissza, a backend kész.
