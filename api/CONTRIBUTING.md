# Segítség, hogy te is tudj fejleszteni

## Programok amik kellenek

- [Git](https://git-scm.com/downloads)
    - A telepítőben a Git Bash telepítését ajánlom engedélyezni
- [Visual Studio Code](https://code.visualstudio.com/download)
    - [Live Share plugin](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare)
    - [Python plugin](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - [Python Environment Manager plugin](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-environment-manager)
    - [Python Auto Venv plugin](https://marketplace.visualstudio.com/items?itemName=WolfiesHorizon.python-auto-venv)
    - [SQLite3 Editor](https://marketplace.visualstudio.com/items?itemName=yy0931.vscode-sqlite3-editor)
- [Python 3.11.4 64bit](https://www.python.org/downloads)


## Tippek

- Gyakran pullolj/fetchelj GitHubról vagy kapcsold be a kiegészítőben VS Code-ban
- Ne felejts el bejelentkezni a GitHub fiókodba

## Parancsok

- Futtatás
    1. `cd EttermiRendeloRendszer`
    2. Virtuális környezet aktiválása
        - Windows: `.venv/Scripts/activate.bat`
        - Mac & Linux: `source .venv/bin/activate`
    3. Alkalmazás elindítása
        - Windows: `python run.py`
        - Mac & Linux: `python3 run.py`
- Kilépés a virtuális környezetből (nem kötelező, elég bezárnod a parancssort)
    - Windows: `.venv/Scripts/deactivate.bat`
    - Mac & Linux: `deactivate`
 - Git parancsok (használati sorrendben)
    1. `git pull` - Letölti a módosításokat amiket te vagy mások csináltak (értsd: szinkronizálod a lokális fájlokat a távoliakkal)
    2. `git add <fájl vagy könytár elérési út, vagy "." (pont) karakter, hogy mindent kijelölj>` - Hozzáadja a Git Stage-hez a megadott fájlokat, hogy commitolhasd őket
    3. `git commit -m "<rövid, lényegre törő összefoglalás a munkádról>"` - Elmenti a Git Stage-ben lévő módosításokat egy üzenettel, hogy pusholhasd őket
    4. `git push` - Feltöltöd a Git repository-ba a commitolt módosításokat
