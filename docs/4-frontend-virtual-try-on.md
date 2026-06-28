# Frontend Virtual Try-On fejlesztés

Ebben a fejlesztési lépések és a kódtöredékek találhatók lépésről-lépésre.

## Alap információk

- Kód mappa: `frontend`
- Kód nyelv: HTML, JavaScript
- Kód célja: A virtuális próbafülke frontend logikájának implementálása, amely a felhasználói interakciókat kezeli és a backend API-t használja a ruhák illeszkedésének és megjelenésének feldolgozásához.
- Struktúra:
```
..
└── frontend/
    ├── index.html           ← a frontend logika itt van
    └── style.css            ← a frontend stíluslapja
``` 

## Fejlesztési lépések

1. **index.html fájl kibővítése**: A `index.html` fájlban adj hozzá egy `form` elemet, amely tartalmaz két `input` mezőt a modell- és a ruhadarab képének feltöltéséhez, egy `button` elemet a próbafülke indításához, és egy `img` elemet az eredmény megjelenítéséhez.

```html
<form id="virtual_try_on_form">
    <label for="model_image">Modell kép:</label>
    <input type="file" id="model_image" name="model_image" accept="image/*" required>
    <label for="clothing_image">Ruhadarab kép:</label>
    <input type="file" id="clothing_image" name="clothing_image" accept="image/*" required>
    <button type="submit">Próbafülke indítása</button>
</form>
<img id="result_image" alt="Eredmény" style="display:none; max-width: 800px;">
```

2. **JavaScript kód hozzáadása**: A `index.html` fájlban a `<script>` szekcióban implementáld a JavaScript kódot, amely kezeli a form elküldését, feltölti a képeket a backend API-hoz, és megjeleníti az eredményt.

```javascript
  document.getElementById("virtual_try_on_form").onsubmit = async function (e) {
    // Megakadályozzuk az alapértelmezett form elküldést
    e.preventDefault();
    // Létrehozunk egy FormData objektumot a képek feltöltéséhez
    const formData = new FormData();
    // Hozzáadjuk a feltöltött képeket a FormData-hoz
    formData.append("model_image", document.getElementById("model_image").files[0]);
    formData.append("clothing_image", document.getElementById("clothing_image").files[0]);
    // Meghívjuk a backend API-t a POST kéréssel
    const response = await fetch(API_URL + "/virtual-try-on", { method: "POST", body: formData });
    // Ellenőrizzük, hogy a válasz sikeres-e
    document.getElementById("result_image").src = URL.createObjectURL(await response.blob());
    // Megjelenítjük az eredmény képet
    document.getElementById("result_image").style.display = "block";
  };
```
