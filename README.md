# Virtuális Próbafülke GCP AI-al - MVP (élő kódoláshoz)

Ez a projekt egy virtuális próbafülke MVP (Minimum Viable Product) implementációja, amely lehetővé teszi a felhasználók számára, hogy élőben próbálják ki a ruhákat egy webes alkalmazás segítségével. A cél az, hogy a felhasználók valós idejű visszajelzést kapjanak a ruhák illeszkedéséről és megjelenéséről.

Maga a példa a Mentor Klub "Google Cloud Platform AI – Építsünk valós AI alkalmazást egy nap alatt" élő, egynapos képzéséhez készült, és a képzés során a résztvevők megismerkedhetnek a Google Cloud Platform AI kódbázási lehetőségeivel, valamint a virtuális próbafülke MVP fejlesztésének alapjaival.

Az egyes demók fázisnonként jelennek meg és külön branch-ekben és tag-ekben is elérhetők, így a résztvevők könnyen követhetik a fejlesztési folyamatot és megérthetik az egyes lépések jelentőségét.

## Branch-ek és tag-ek

- `main`: A fő branch, amely a legfrissebb, teljes megoldást tartalmazza.
- `demo/1-backend-api`: Az első demó, amely a backend API alapjait mutatja be. Itt egy Python alapú FastAPI szerver kerül implementálásra. Ehhez tartozó tag: `1-backend-api`.
- `demo/2-frontend`: A második demó, amely a frontend integrációt mutatja be. Itt a frontend és a backend közötti kommunikáció kerül implementálásra. Ehhez tartozó tag: `2-frontend`.
- `demo/3-backend-virtual-try-on`: A harmadik demó, amely a virtuális próbafülke backend logikáját mutatja be. Itt a ruhák illeszkedésének és megjelenésének feldolgozása kerül implementálásra. Itt kötjük össze a backend-et a Google Cloud AI szolgáltatásaival. (Enterprise Agent Platform) Ehhez tartozó tag: `3-backend-virtual-try-on`.
- `demo/4-frontend-virtual-try-on`: A negyedik demó, amely a virtuális próbafülke frontend logikáját mutatja be. Itt a felhasználói interakciók kerülnek implementálásra, és a backend API-t használja a ruhák illeszkedésének és megjelenésének feldolgozásához. Ehhez tartozó tag: `4-frontend-virtual-try-on`.
- `demo/5-deploy-cloudrun`: Az ötödik demó, amely a teljes alkalmazás felhőbe történő telepítését mutatja be. Itt a CloudRun szolgáltatás segítségével a frontend és a backend külön-külön kerül telepítésre, így bemutatva a skálázható és rugalmas, több-rétegű architektúra előnyeit. Ehhez tartozó tag: `5-deploy-cloudrun`.

## Fejlesztési lépések

1. **Backend API**: A backend implementálása FastAPI segítségével, amely egy egyszerű API-t biztosít számunkra. Részletek a [1-backend-api.md](docs/1-backend-api.md) fájlban találhatók.

2. **Frontend**: A frontend implementálása egy egyszerű html fájl formájában történik, amely a backend API-t használja a felhasználói interakciókhoz. Részletek a [2-frontend.md](docs/2-frontend.md) fájlban találhatók.

3. **Backend Virtual Try-On**: A virtuális próbafülke backend logikájának implementálása, amely a ruhák illeszkedését és megjelenését kezeli. Részletek a [3-backend-virtual-try-on.md](docs/3-backend-virtual-try-on.md) fájlban találhatók.

4. **Frontend Virtual Try-On**: A virtuális próbafülke frontend logikájának implementálása, amely a felhasználói interakciókat kezeli és a backend API-t használja a ruhák illeszkedésének és megjelenésének feldolgozásához. Részletek a [4-frontend-virtual-try-on.md](docs/4-frontend-virtual-try-on.md) fájlban találhatók.

5. **Alkalmazás telepítése a felhőbe**: A teljes alkalmazást úgy dosítjuk, hogy futtatható legyen CloudRun-on, amely lehetővé teszi a felhasználók számára, hogy a webes alkalmazást a felhőben futtassák. Részletek a [5-deploy-cloudrun.md](docs/5-deploy-cloudrun.md) fájlban találhatók. A telepítéshet a CloudBuild szolgáltatást használjuk, amely lehetővé teszi a kód automatikus buildelését és telepítését a felhőbe. Mind a frontend, mind a backend szolgáltatás külön-külön CloudRun-ba telepítjük, így mutatjuk be a skálázható és rugalmas, több-rétegű architektúra előnyeit.
