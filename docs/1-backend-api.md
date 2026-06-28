# Backend API

Ebben a fejlesztési lépések és a kódtöredékek találhatók lépésről-lépésre.

## Alap információk

- Kód mappa: `backend`
- Kód nyelv: Python
- Kód keretrendszer: FastAPI
- Kód célja: Egy egyszerű API biztosítása a frontend felől érkező kérésekhez.
- Struktúra:

```
..
└── backend/
    ├── main.py              ← minden backend logika itt van
    └── requirements.txt     ← pip függőségek
```

## Fejlesztési lépések

1. **Függőségeket tartalmazó requirements.txt fájl**: A `requirements.txt` fájl tartalmazza a szükséges Python csomagokat, amelyeket a backend működéséhez telepíteni kell. A fájl tartalma:

```
fastapi
uvicorn[standard]
```

2. **Függőségek telepítése**: Hozz létre egy virtuális környezetet, és telepítsd a szükséges Python csomagokat a `requirements.txt` fájl alapján.

Győződj meg hogy a megfelelő Python verzió van telepítve (Python 3.11 vagy újabb).

```bash
python --version
```

A következő parancsokat futtasd a terminálban:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. **Alap FastAPI szerver implementálása**: A `main.py` fájlban implementáld az alap FastAPI szervert, amely jelenleg csak a `/health` végpontot tartalmazza. Ezt általában a szerver állapotának ellenőrzésére használjuk.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def read_health():
    return {"status": "ok"}
```

4. **Szerver indítása**: A FastAPI szerver helyi indításához használd az alábbi parancsot:

```bash
python -m uvicorn main:app --reload --port 8000
```

Ezután nyisd meg a böngészőt, és látogasd meg a `http://127.0.0.1:8000/health` URL-t a szerver állapotának ellenőrzéséhez.

5. **CORS beállítások**: Ha a frontend és a backend különböző url-eken fut, biztonsági okokból szükség van a CORS (Cross-Origin Resource Sharing) beállítására a FastAPI szerverben. Ha ez nem történik meg akkor a böngésző blokkolhatja a kéréseket. Ehhez telepítsd a `fastapi.middleware.cors` csomagot, és konfiguráld a CORS-t a `main.py` fájlban.

```python
from fastapi.middleware.cors import CORSMiddleware

...

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vagy specifikus domain-ek listája
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

5. **Tesztelés**: A szerver futtatása után teszteld a `/health` végpontot egy HTTP klienssel (pl. Insomnia, Postman, curl). Pl:

```bash
curl -X GET "http://127.0.0.1:8000/health"
```

6. Egyéb parancsok

- Virtuális környezet deaktiválása:

```bash
deactivate
```

- A szerver leállítása: A terminálban, ahol a szerver fut, nyomd meg a `Ctrl+C` billentyűkombinációt.
