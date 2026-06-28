# backend/main.py

# Csomagok és modulok importálása
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
