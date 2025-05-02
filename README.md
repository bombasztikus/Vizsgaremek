![kép](https://github.com/bombasztikus/Vizsgaremek/blob/main/docs/img/wip/index.jpg)

# EttermiFoglaloRendszer

- Iskola: Pogány Frigyes Technikum
- Osztály: 13/E
- Tanulók:
    - Simon Attila Tibor ([GitHub](https://github.com/kanszaghadnagy))
    - Kőszegi Tamás Attila ([GitHub](https://github.com/Hentai-IsArt))
    - Halász Wilhelm Bendegúz ([GitHub](https://github.com/bombasztikus))

# Dokumentáció, prezentáció
- Dokumentáció: [https://1drv.ms/w/c/7021dbc09f1f29d0/EdqMabXVNERCgB9AwJ2vLcEBTcImepnXHcpLOWkEhsrgAQ?e=Mqo4JN](https://1drv.ms/w/c/7021dbc09f1f29d0/EdqMabXVNERCgB9AwJ2vLcEBTcImepnXHcpLOWkEhsrgAQ?e=Mqo4JN)
- Prezentáció: [https://1drv.ms/p/c/54181cab4b8b3e60/ERd6NVrcQ3NCgA-k6wPgX9oBw7X_h3Lvogq1nI5M8xdI_g?e=heRgNn](https://1drv.ms/p/c/54181cab4b8b3e60/ERd6NVrcQ3NCgA-k6wPgX9oBw7X_h3Lvogq1nI5M8xdI_g?e=heRgNn)

# Repository struktúra
- `api/` - Backend/REST API
- `frontend/` - Web/Kiosk felület

# Utasítások a futtatáshoz

```sh
docker-compose up -d --build
```

Amennyiben nem tudod, vagy nem akarod Docker-rel futtatni, lásd a dokumentáció Futtatás c. fejezetét.

# Admin kliens

[https://github.com/creppzguy/Viszgaremek_Admin](https://github.com/creppzguy/Viszgaremek_Admin)

# Demó adatok

Alkalmazotti fiók:
- Email: `admin@localhost`
- Jelszó: `admin123`
  
Sima felhasználó:
- Email: `demo@localhost`
- Jelszó: `demo123`

A demó adatok betöltéséhez futtasd le a `api/generate_db.py` scriptet. Ne felejtsd el beállítani a környezeti változókat.
