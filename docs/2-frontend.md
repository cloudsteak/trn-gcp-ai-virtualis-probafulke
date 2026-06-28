# Frontend (weboldal) fejlesztés

Ebben a fejlesztési lépések és a kódtöredékek találhatók lépésről-lépésre.

## Alap információk

- Kód mappa: `frontend`
- Kód nyelv: HTML, JavaScript
- Kód célja: A frontend implementálása egy egyszerű html fájl formájában, amely a backend API-t használja a felhasználói interakciókhoz.
- Struktúra:

```
..
└── frontend/
    └── index.html           ← minden frontend logika itt van
```

## Fejlesztési lépések

1. **index.html fájl létrehozása**: Hozz létre egy `index.html` fájlt a `frontend` mappában, amely tartalmazza az alap HTML struktúrát.

_Megjegyzés:_ Ha a **[HTML Boilerplate](https://marketplace.visualstudio.com/items?itemName=sidthesloth.html5-boilerplate)** kiterjesztés használod, akkor az alábbi parancsot írd be az index.html fájlba: `html:5` majd nyomd meg a `Tab` gombot. Ez automatikusan létrehozza az alap HTML struktúrát.

````bash

```html
<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Virtuális Próbafülke</title>
</head>
<body>
    <h1>Virtuális Próbafülke</h1>
</body>
</html>
````

2. Ezt nyisd meg a böngésződben, és ellenőrizd, hogy a HTML fájl helyesen jelenik-e meg.

Mac/Linux:

```bash
cd frontend
open frontend/index.html        # macOS
xdg-open frontend/index.html    # Linux
start frontend/index.html       # Windows
```

3. **Backend API hívás implementálása**: A frontend és a backend közötti kommunikációt JavaScript segítségével valósítjuk meg. A `index.html` fájlban adj hozzá egy `<div>` elemet a fejléc alá, majd egy `<script>` szekciót a `<body>` végéhez, amely tartalmazza a backend API hívását.

```html
<div id="api_valasz"></div>

<!-- A JavaScript kód a backend API hívásához  -->
<script>
  const API_URL = "http://localhost:8000";

  async function getHealthStatus() {
    try {
      const response = await fetch(`${API_URL}/health`);
      const data = await response.json();
      document.getElementById("api_valasz").innerText =
        `Backend állapot: ${data.status}`;
    } catch (error) {
      console.error("Hiba a backend hívás során:", error);
      document.getElementById("api_valasz").innerText =
        "Hiba a backend hívás során.";
    }
  }

  // Hívjuk meg a függvényt az oldal betöltésekor
  window.onload = getHealthStatus;
</script>
```
