from pathlib import Path
from typing import List

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.logic import EntradaInvalida, analizar, convertir_equipos, convertir_numero

base = Path(__file__).parent
app = FastAPI(title="EnergiaHogar")
plantillas = Jinja2Templates(directory=str(base / "templates"))


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return plantillas.TemplateResponse(request, "index.html", {"error": None})


@app.post("/analizar", response_class=HTMLResponse)
def calcular(
    request: Request,
    nombre: List[str] = Form(...),
    potencia: List[str] = Form(...),
    horas: List[str] = Form(...),
    tarifa: str = Form(...),
    reduccion: str = Form("0"),
):
    try:
        equipos = convertir_equipos(nombre, potencia, horas)
        resultado = analizar(
            equipos,
            convertir_numero(tarifa, "tarifa"),
            convertir_numero(reduccion, "reduccion"),
        )
    except EntradaInvalida as e:
        return plantillas.TemplateResponse(request, "index.html", {"error": str(e)}, status_code=400)
    return plantillas.TemplateResponse(request, "resultado.html", {"r": resultado})
