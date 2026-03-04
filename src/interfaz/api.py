# ─────────────────────────────────────────────────────────────────────────────
# Módulo: src/interfaz/api.py
# Propósito: Definir todos los endpoints REST de la aplicación.
#
# NOTA DE DISEÑO: El estado de las partidas se guarda en memoria (dict Python).
# No se usa base de datos para mantener el proyecto simple y portable.
# Un dict en el proceso del servidor es suficiente para uso académico.
#
# Rutas disponibles:
#   GET  /             → Página de inicio (HTML)
#   GET  /tablero      → Tablero del juego (HTML)
#   GET  /salud        → Health check para Docker
#   POST /solo/nuevo   → Crea partida modo un jugador
#   POST /solo/intento → Registra intento en modo solo
#   GET  /solo/{id}    → Estado actual de una partida solo
#   POST /pvp/nuevo    → Crea sesión PvP
#   POST /pvp/secreto  → Un jugador configura su número secreto
#   POST /pvp/intento  → Registra intento en modo PvP
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.servicios.juego_solo import JuegoSolo
from src.servicios.juego_pvp import JuegoPvP

# ── Configuración de la aplicación ────────────────────────────────────────────
app = FastAPI(
    title="Picas y Fijas",
    description="Juego de lógica para adivinar un número de 4 dígitos únicos.",
    version="1.0.0",
)
templates = Jinja2Templates(directory="src/interfaz/templates")

# ── Almacén en memoria de las partidas activas ────────────────────────────────
# Clave: ID entero autoincremental. Valor: instancia del servicio de juego.
_partidas_solo: dict[int, JuegoSolo] = {}
_partidas_pvp: dict[int, JuegoPvP] = {}
_siguiente_id: int = 1  # Contador de IDs


def _nuevo_id() -> int:
    """Genera un ID único para una nueva partida."""
    global _siguiente_id
    id_actual = _siguiente_id
    _siguiente_id += 1
    return id_actual


# ── Modelos de entrada (schemas de la API) ─────────────────────────────────────

class NuevoJuegoSoloRequest(BaseModel):
    """Datos para iniciar una partida en modo solo."""
    nombre_jugador: str


class IntentoSoloRequest(BaseModel):
    """Datos para registrar un intento en modo solo."""
    sesion_id: int
    intento: str


class NuevoJuegoPvPRequest(BaseModel):
    """Datos para iniciar una partida PvP."""
    nombre_jugador1: str
    nombre_jugador2: str


class ConfigurarSecretoRequest(BaseModel):
    """Datos para que un jugador registre su número secreto en PvP."""
    sesion_id: int
    nombre_jugador: str
    secreto: str


class IntentoPvPRequest(BaseModel):
    """Datos para registrar un intento en modo PvP."""
    sesion_id: int
    nombre_jugador: str
    intento: str


# ── Rutas de Interfaz Web (HTML) ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, summary="Página de inicio")
async def pagina_inicio(request: Request):
    """Muestra la pantalla inicial donde el jugador ingresa su nombre."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/tablero", response_class=HTMLResponse, summary="Tablero del juego")
async def pagina_tablero(request: Request):
    """Muestra el tablero del juego donde el jugador realiza sus intentos."""
    return templates.TemplateResponse("tablero.html", {"request": request})


# ── Health Check ──────────────────────────────────────────────────────────────

@app.get("/health", summary="Health check")
async def health():
    """
    Endpoint de verificación de estado.
    Docker lo usa para saber si la webapp está lista antes de correr los tests.
    """
    return {"estado": "ok"}


# ── Endpoints: Modo Solo ───────────────────────────────────────────────────────

@app.post("/solo/nuevo", summary="Iniciar partida modo solo")
async def nuevo_juego_solo(datos: NuevoJuegoSoloRequest):
    """
    Crea una nueva partida modo solo y la registra en memoria.
    El sistema genera automáticamente el número secreto.
    """
    id_partida = _nuevo_id()
    _partidas_solo[id_partida] = JuegoSolo(nombre_jugador=datos.nombre_jugador)

    return {
        "sesion_id": id_partida,
        "nombre_jugador": datos.nombre_jugador,
        "intentos_restantes": 10,
        "mensaje": f"Partida iniciada. Tienes 10 intentos, {datos.nombre_jugador}.",
    }


@app.post("/solo/intento", summary="Realizar intento en modo solo")
async def intento_juego_solo(datos: IntentoSoloRequest):
    """
    Registra un intento del jugador y retorna cuántas picas y fijas obtuvo.
    """
    partida = _partidas_solo.get(datos.sesion_id)
    if not partida:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    if partida.terminado:
        raise HTTPException(status_code=400, detail="Esta partida ya terminó.")

    return partida.realizar_intento(datos.intento)


@app.get("/solo/{sesion_id}", summary="Estado de partida solo")
async def estado_juego_solo(sesion_id: int):
    """Retorna el estado actual de una partida en modo solo."""
    partida = _partidas_solo.get(sesion_id)
    if not partida:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    return {
        "sesion_id": sesion_id,
        "nombre_jugador": partida.nombre_jugador,
        "intentos": partida.intentos_realizados,
        "terminado": partida.terminado,
        "gano": partida.gano,
    }


# ── Endpoints: Modo PvP ────────────────────────────────────────────────────────

@app.post("/pvp/nuevo", summary="Iniciar sesión PvP")
async def nuevo_juego_pvp(datos: NuevoJuegoPvPRequest):
    """
    Crea una nueva sesión PvP. Cada jugador deberá configurar
    su número secreto por separado antes de que empiece el juego.
    """
    id_partida = _nuevo_id()
    _partidas_pvp[id_partida] = JuegoPvP(datos.nombre_jugador1, datos.nombre_jugador2)

    return {
        "sesion_id": id_partida,
        "mensaje": f"Sesión creada. {datos.nombre_jugador1}, configura tu número secreto.",
    }


@app.post("/pvp/secreto", summary="Configurar secreto en PvP")
async def configurar_secreto_pvp(datos: ConfigurarSecretoRequest):
    """
    Permite a un jugador registrar su número secreto antes de comenzar la partida.
    """
    partida = _partidas_pvp.get(datos.sesion_id)
    if not partida:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    return partida.configurar_secreto(datos.nombre_jugador, datos.secreto)


@app.post("/pvp/intento", summary="Realizar intento en PvP")
async def intento_pvp(datos: IntentoPvPRequest):
    """
    Registra el intento de un jugador. Solo puede jugar quien tiene el turno activo.
    """
    partida = _partidas_pvp.get(datos.sesion_id)
    if not partida:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    if partida.terminado:
        raise HTTPException(status_code=400, detail="Esta partida ya terminó.")
    return partida.realizar_intento(datos.nombre_jugador, datos.intento)
