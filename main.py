
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

sklad = {
    "jablko": {"cena": 0.50, "mnozstvo": 5},
    "mlieko": {"cena": 1.20, "mnozstvo": 3},
    "chlieb": {"cena": 1.50, "mnozstvo": 2}
}

kosik = []


@app.get("/", response_class=HTMLResponse)
def domov(request: Request):

    celkova_cena = 0

    for polozka in kosik:
        celkova_cena += sklad[polozka]["cena"]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sklad": sklad,
            "kosik": kosik,
            "cena": round(celkova_cena, 2),
            "zlava": 0,
            "finalna_cena": round(celkova_cena, 2),
            "sprava": ""
        }
    )


@app.post("/pridat", response_class=HTMLResponse)
def pridat(request: Request, nazov: str = Form(...)):

    if sklad[nazov]["mnozstvo"] > 0:
        kosik.append(nazov)
        sklad[nazov]["mnozstvo"] -= 1

    celkova_cena = 0

    for polozka in kosik:
        celkova_cena += sklad[polozka]["cena"]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sklad": sklad,
            "kosik": kosik,
            "cena": round(celkova_cena, 2),
            "zlava": 0,
            "finalna_cena": round(celkova_cena, 2),
            "sprava": "Položka bola pridaná do košíka."
        }
    )


@app.post("/zlava", response_class=HTMLResponse)
def pouzi_zlavu(request: Request, kod: str = Form(...)):

    celkova_cena = 0

    for polozka in kosik:
        celkova_cena += sklad[polozka]["cena"]

    if kod == "BELI10":
        zlava = round(celkova_cena * 0.10, 2)
        finalna_cena = round(celkova_cena - zlava, 2)
        sprava = "Zľava 10 % bola použitá."
    else:
        zlava = 0
        finalna_cena = round(celkova_cena, 2)
        sprava = "Zľavový kód nie je správny."

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sklad": sklad,
            "kosik": kosik,
            "cena": round(celkova_cena, 2),
            "zlava": zlava,
            "finalna_cena": finalna_cena,
            "sprava": sprava
        }
    )


@app.post("/platba", response_class=HTMLResponse)
def platba(request: Request, sposob: str = Form(...)):

    celkova_cena = 0

    for polozka in kosik:
        celkova_cena += sklad[polozka]["cena"]

    if sposob == "karta":
        sprava = "Platba kartou bola vybraná."
    else:
        sprava = "Platba hotovosťou bola vybraná."

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sklad": sklad,
            "kosik": kosik,
            "cena": round(celkova_cena, 2),
            "zlava": 0,
            "finalna_cena": round(celkova_cena, 2),
            "sprava": sprava
        }
    )