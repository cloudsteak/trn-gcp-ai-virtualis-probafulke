# Alkalmazás telepítése a felhőbe

Ebben a fejlesztési lépések és a kódtöredékek találhatók lépésről-lépésre.

## Alap információk

- Kód mappa: `backend`, `frontend`
- Kód nyelv: Python, HTML, JavaScript
- Kód célja: A teljes alkalmazás felhőbe történő telepítésének bemutatása. Itt a CloudRun szolgáltatás segítségével a frontend és a backend külön-külön kerül telepítésre, így bemutatva a skálázható és rugalmas, több-rétegű architektúra előnyeit.
- Frontend struktúra:

```
..
└── frontend/
    ├── index.html           ← a frontend logika itt van
    ├── Dockerfile           ← a frontend Dockerfile-ja
    ├── .dockerignore        ← a frontend Dockerfile-hoz tartozó .dockerignore fájl
    └── style.css            ← a frontend stíluslapja (AI generált)
```

- Backend struktúra:

```
..
└── backend/
    ├── main.py              ← minden backend logika itt van
    ├── requirements.txt     ← pip függőségek
    ├── Dockerfile           ← a backend Dockerfile-ja
    └── .dockerignore        ← a backend Dockerfile-hoz tartozó .dockerignore fájl
```

## Fejlesztési lépések

### Backend telepítése a felhőbe

1. **Dockerfile létrehozása**: A `backend` mappában hozz létre egy `Dockerfile` fájlt, amely tartalmazza a backend konténerének konfigurációját.

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PORT=8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
```

_Megjegyzés_: Ezzel már bármilyen docker környezetben futtatható a backend.

2. **.dockerignore fájl létrehozása**: A `backend` mappában hozz létre egy `.dockerignore` fájlt, amely tartalmazza a Docker build során figyelmen kívül hagyandó fájlokat és mappákat. Ide tesszük a virtuális környezetet, a cache fájlokat és a log fájlokat.

```
.env
example.env
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.pytest_cache/
.mypy_cache/
Dockerfile
.dockerignore
```

3. **Backend kód finomhangolása**: A `main.py` fájlból távolítsd el a `print` utasítást, amely a GCP Agent Platform válaszát írja ki a konzolra. Ez nem szükséges a felhőben történő futtatáshoz, és a logokban is megjelenik.

```python
# Ezt töröld: print("Result from GCP Agent Platform:", result)
```

### Frontend telepítése a felhőbe

1. **HTML fájl finomhangolása**: A `index.html` fájlban a JavaScript kódot módosítsd úgy, hogy a backend API hívás a CloudRun URL-jére mutasson. Ehhez kecseréljük a jelenlegi `API_URL` változót egy olyan karaktersorozatra, amelyet majd a CloudRunk futásakor cserélünk ki a tényleges URL-re egy környezeti változó segítségével.

```javascript
const API_URL = "__API_URL__";
```

Ezt majd a Dockerfile-ban a build során cseréljük ki a tényleges CloudRun URL-re.

2. **Dockerfile létrehozása**: A `frontend` mappában hozz létre egy `Dockerfile` fájlt, amely tartalmazza a frontend konténerének konfigurációját. Mivel ez egy nagyon egyszerű html fájl, ezért a `nginx` webszervert használjuk a kiszolgálásához. Ráadásul a ht

```dockerfile
FROM nginx:alpine

ENV PORT=8080 \
    API_URL=http://localhost:8000

COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/

CMD sed -i 's/listen[: ]*80;/listen '"$PORT"';/' /etc/nginx/conf.d/default.conf \
    && sed -i 's|__API_URL__|'"$API_URL"'|g' /usr/share/nginx/html/index.html \
    && nginx -g 'daemon off;'
```

3. **.dockerignore fájl létrehozása**: A `frontend` mappában hozz létre egy `.dockerignore` fájlt, amely tartalmazza a Docker build során figyelmen kívül hagyandó fájlokat és mappákat.

```
Dockerfile
.dockerignore
```

### Telepítés (Deployment) a CloudRun szolgáltatásba

1. **GitHub frissítése**: Győződj meg róla, hogy a legfrissebb kód van a GitHub repóban. Ha nem, akkor egy Pull Request-et hozz létre, és merge-eld a kódot a `main` branch-be.

2. **Service Account létrehozása Google Cloud-ban**: A CloudRun szolgáltatás használatához szükség van egy Service Account-ra, amely rendelkezik a megfelelő jogosultságokkal.
   Miért fontos ez? Mindig fontos a biztonság és ebben a minimum jogosultság elve alapján kell eljárni. Minden szolgáltatás valamilyen felhasználó nevében fut. A programozott felhasználókat Service Account-oknak nevezzük. A Service Account-okhoz különböző jogosultságokat rendelhetünk, így biztosítva, hogy a szolgáltatás csak a szükséges erőforrásokhoz férjen hozzá. Számunkkra egy olyan Service Account-ra van szükség, amely rendelkezik az alábbi jogosultságokkal:

- `Agent Platform User` - Ez a jogosultság lehetővé teszi, hogy a backend alkalmazás hozzáférjen a GCP Agent Platform szolgáltatáshoz, amely a ruhák illeszkedésének és megjelenésének feldolgozásához szükséges.
- `Logs Writer` - Ez a jogosultság lehetővé teszi, hogy a backend alkalmazás naplózza az eseményeket és hibákat a Google Cloud Logging szolgáltatásba, így könnyebben nyomon követhetők a problémák és a teljesítmény.
- `Monitoring Metric Writer` - Ez a jogosultság lehetővé teszi, hogy a backend alkalmazás metrikákat írjon a Google Cloud Monitoring szolgáltatásba, így nyomon követhetők az alkalmazás teljesítménye és állapota.

Ehhez az alábi lépéseket kell követni:

- **Console** > Service Accounts > **Create service account**
- Service Account Name: `virtualis-probafulke-futtato`
- Kattintsunk a **Create and Continue** gombra.
- Permissions részben adjuk hozzá a fent említett szerepköröket:
  - `Agent Platform User` (`roles/aiplatform.user`)
  - `Logs Writer` (`roles/logging.logWriter`)
  - `Monitoring Metric Writer` (`roles/monitoring.metricWriter`)
- Kattintsunk a **Continue** gombra.
- **Principals with access** — kihagyható.
- Kattintsunk a **Done** gombra.

3. **Backend telepítése a CloudRun szolgáltatásba**: A backend telepítéséhez a CloudRun szolgáltatásba, továbbra is a Google Cloud Console-t használjuk. A telepítéshez a CloudBuild funkciót használjuk az alábbi lépéseket követve:

- **Console** > Cloud Run > **Services** > **Connect repo**
- Itt válaszd a **Continuously deploy from a repository (source or function)** lehetőséget.
- Válaszd a **CloudBuild** lehetőséget.
- Kattintds a **Set up Cloud build** gombra.
- Source repository: **GitHub**
- Repository: **cloudsteak/trn-gcp-ai-virtualis-probafulke**
- Pipáldbe a **I understand that GitHub content...** checkbox-ot.
- Majd kattints a **Next** gombra.
- Branch: `^main$`
- Dockerfile: `/backend/Dockerfile`
- Mentsd el a beállításokat a **Save** gombbal.
- Service name: `virtualis-probafulke-backend`
- Region: `europe-west1`
- Authentication > Allow public access
- Auto scaling: 0 - 20
- Nyisd le a **Containers, Networking, Security** részt
- Security fülön a **Service account** mezőben válaszd ki a korábban létrehozott Service Account-ot: `virtualis-probafulke-futtato`
- Majd menj vissza a **Container** fülre, és a **Port** mezőbe írd be: `8080`
- **Variables & Secrets**:
  - GCP_PROJECT_ID: add meg a projekt azonosítóját
  - GCP_LOCATION: `europe-west1`
- Kattints a **Create** gombra.

Ezzel elkezdődik a backend telepítése a CloudRun szolgáltatásba. A telepítés befejezése után a CloudRun szolgáltatás URL-jét jegyezd fel, mert ezt fogjuk használni a frontend konfigurációjában.

4. **Frontend telepítése a CloudRun szolgáltatásba**: A frontend telepítéséhez a CloudRun szolgáltatásba, továbbra is a Google Cloud Console-t használjuk. A telepítéshez a CloudBuild funkciót használjuk az alábbi lépéseket követve:

- **Console** > Cloud Run > **Services** > **Connect repo**
- Itt válaszd a **Continuously deploy from a repository (source or function)** lehetőséget.
- Válaszd a **CloudBuild** lehetőséget.
- Kattintds a **Set up Cloud build** gombra.
- Source repository: **GitHub**
- Repository: **cloudsteak/trn-gcp-ai-virtualis-probafulke**
- Pipáldbe a **I understand that GitHub content...** checkbox-ot.
- Majd kattints a **Next** gombra.
- Branch: `^main$`
- Dockerfile: `/frontend/Dockerfile`
- Mentsd el a beállításokat a **Save** gombbal.
- Service name: `virtualis-probafulke-frontend`
- Region: `europe-west1`
- Authentication > Allow public access
- Auto scaling: 0 - 20
- Nyisd le a **Containers, Networking, Security** részt
- Security fülön a **Service account** mezőben válaszd ki a korábban létrehozott Service Account-ot: `virtualis-probafulke-futtato`
- Majd menj vissza a **Container** fülre, és a **Port** mezőbe írd be: `8080`
- **Variables & Secrets**:
  - API_URL: add meg a backend CloudRun szolgáltatás URL-jét, amelyet a telepítéskor kaptál. Például: `https://virtualis-probafulke-backend-abcdefg-uc.a.run.app`
- Kattints a **Create** gombra.

Ezzel elkezdődik a frontend telepítése a CloudRun szolgáltatásba. A telepítés befejezése után a CloudRun szolgáltatás URL-jét jegyezd fel, mert ezt fogjuk használni a webes alkalmazás eléréséhez.

5. **Alkalmazás tesztelése**: A telepítés befejezése után a frontend CloudRun szolgáltatás URL-jét megnyitva a böngészőben, ellenőrizheted, hogy az alkalmazás helyesen működik-e. A frontendnek képesnek kell lennie kommunikálni a backend API-val, és a felhasználói interakcióknak megfelelően kell működniük.

Töltsd fel egy moddl és egy ruhadarab képét, majd ellenőrizd, hogy a backend megfelelően dolgozza fel a képeket, és a frontend helyesen jeleníti meg az eredményeket.
