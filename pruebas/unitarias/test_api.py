# Pruebas: pruebas/unitarias/test_api.py
# Propósito: Verificar que los endpoints de la API responden correctamente.
#
# Usa el TestClient de FastAPI, que NO necesita un servidor corriendo.
# Simula peticiones HTTP directamente sobre la aplicación en memoria.
#
# Historias de usuario cubiertas: HU-1, HU-2, HU-3 (capa de API)

import pytest
from fastapi.testclient import TestClient
from src.interfaz.api import app

# TestClient permite hacer peticiones sin levantar servidor real
cliente = TestClient(app)


# ── Health check ─────────────────────────────────────────────────────────────

def test_health_check_responde_ok():
    """El endpoint de health debe devolver estado ok."""
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


def test_pagina_inicio_devuelve_html():
    """La raíz debe retornar HTML con el título del juego."""
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert "text/html" in respuesta.headers["content-type"]


def test_pagina_tablero_devuelve_html():
    """La ruta /tablero debe retornar HTML."""
    respuesta = cliente.get("/tablero")
    assert respuesta.status_code == 200
    assert "text/html" in respuesta.headers["content-type"]


# ── Modo Solo ─────────────────────────────────────────────────────────────────

class TestApiModoSolo:
    """Pruebas de integración para los endpoints del modo un jugador."""

    def test_crear_partida_solo_retorna_sesion_id(self):
        """POST /solo/nuevo debe crear una sesión y retornar su ID."""
        respuesta = cliente.post("/solo/nuevo", json={"nombre_jugador": "Carlos"})
        assert respuesta.status_code == 200
        datos = respuesta.json()
        assert "sesion_id" in datos
        assert datos["intentos_restantes"] == 10

    def test_intento_invalido_en_modo_solo(self):
        """Un número con dígitos repetidos debe ser rechazado."""
        res = cliente.post("/solo/nuevo", json={"nombre_jugador": "Ana"})
        sesion_id = res.json()["sesion_id"]

        respuesta = cliente.post("/solo/intento", json={
            "sesion_id": sesion_id, "intento": "1123"
        })
        assert respuesta.status_code == 200
        datos = respuesta.json()
        assert datos["valido"] is False

    def test_intento_valido_retorna_picas_y_fijas(self):
        """Un intento válido debe retornar picas y fijas calculadas."""
        res = cliente.post("/solo/nuevo", json={"nombre_jugador": "Luis"})
        sesion_id = res.json()["sesion_id"]

        respuesta = cliente.post("/solo/intento", json={
            "sesion_id": sesion_id, "intento": "1234"
        })
        assert respuesta.status_code == 200
        datos = respuesta.json()
        assert "resultado" in datos
        assert "fijas" in datos["resultado"]
        assert "picas" in datos["resultado"]

    def test_sesion_no_encontrada_retorna_404(self):
        """Un ID de sesión inexistente debe devolver 404."""
        respuesta = cliente.post("/solo/intento", json={
            "sesion_id": 99999, "intento": "1234"
        })
        assert respuesta.status_code == 404

    def test_obtener_estado_sesion_solo(self):
        """GET /solo/{id} debe devolver el estado actual de la partida."""
        res = cliente.post("/solo/nuevo", json={"nombre_jugador": "Elena"})
        sesion_id = res.json()["sesion_id"]

        respuesta = cliente.get(f"/solo/{sesion_id}")
        assert respuesta.status_code == 200
        datos = respuesta.json()
        assert datos["nombre_jugador"] == "Elena"
        assert datos["terminado"] is False

    def test_intento_en_partida_terminada_retorna_400(self):
        """No se puede jugar en una partida ya finalizada."""
        res = cliente.post("/solo/nuevo", json={"nombre_jugador": "Marco"})
        sesion_id = res.json()["sesion_id"]

        # Agotar los 10 intentos con números que existirán como inválidos para la lógica
        # Usamos intentos válidos que no aciertan (no conocemos el secreto)
        for n in ["1234", "5678", "2345", "6789", "3456", "7890", "4567", "0123", "8901", "2460"]:
            cliente.post("/solo/intento", json={"sesion_id": sesion_id, "intento": n})

        # Una vez terminada la partida, otro intento debe dar 400
        respuesta = cliente.post("/solo/intento", json={
            "sesion_id": sesion_id, "intento": "1357"
        })
        assert respuesta.status_code == 400


# ── Modo PvP ──────────────────────────────────────────────────────────────────

class TestApiModoPvP:
    """Pruebas de integración para los endpoints del modo dos jugadores."""

    def test_crear_sesion_pvp_retorna_sesion_id(self):
        """POST /pvp/nuevo debe crear la sesión y retornar su ID."""
        respuesta = cliente.post("/pvp/nuevo", json={
            "nombre_jugador1": "Alice",
            "nombre_jugador2": "Bob"
        })
        assert respuesta.status_code == 200
        assert "sesion_id" in respuesta.json()

    def test_configurar_secreto_pvp(self):
        """Un jugador puede registrar su número secreto."""
        res = cliente.post("/pvp/nuevo", json={
            "nombre_jugador1": "Alice", "nombre_jugador2": "Bob"
        })
        sesion_id = res.json()["sesion_id"]

        respuesta = cliente.post("/pvp/secreto", json={
            "sesion_id": sesion_id,
            "nombre_jugador": "Alice",
            "secreto": "1234"
        })
        assert respuesta.status_code == 200
        assert respuesta.json()["valido"] is True

    def test_secreto_invalido_en_pvp_es_rechazado(self):
        """Un número con dígitos repetidos es rechazado como secreto."""
        res = cliente.post("/pvp/nuevo", json={
            "nombre_jugador1": "Alice", "nombre_jugador2": "Bob"
        })
        sesion_id = res.json()["sesion_id"]

        respuesta = cliente.post("/pvp/secreto", json={
            "sesion_id": sesion_id,
            "nombre_jugador": "Alice",
            "secreto": "1122"
        })
        assert respuesta.json()["valido"] is False

    def test_flujo_pvp_completo(self):
        """Ambos configuran secreto y Alice adivina el de Bob correctamente."""
        res = cliente.post("/pvp/nuevo", json={
            "nombre_jugador1": "Alice", "nombre_jugador2": "Bob"
        })
        sesion_id = res.json()["sesion_id"]

        # Ambos configuran su secreto
        cliente.post("/pvp/secreto", json={
            "sesion_id": sesion_id, "nombre_jugador": "Alice", "secreto": "1234"
        })
        cliente.post("/pvp/secreto", json={
            "sesion_id": sesion_id, "nombre_jugador": "Bob", "secreto": "5678"
        })

        # Alice adivina el secreto de Bob
        respuesta = cliente.post("/pvp/intento", json={
            "sesion_id": sesion_id, "nombre_jugador": "Alice", "intento": "5678"
        })
        datos = respuesta.json()
        assert datos["gano"] is True
        assert datos["terminado"] is True

    def test_intento_pvp_sesion_no_encontrada(self):
        """Un ID de sesión PvP inexistente debe devolver 404."""
        respuesta = cliente.post("/pvp/intento", json={
            "sesion_id": 99999, "nombre_jugador": "Alice", "intento": "1234"
        })
        assert respuesta.status_code == 404

    def test_secreto_pvp_sesion_no_encontrada_retorna_404(self):
        """Configurar secreto en sesión inexistente debe devolver 404 (api.py:182)."""
        respuesta = cliente.post("/pvp/secreto", json={
            "sesion_id": 99999, "nombre_jugador": "Alice", "secreto": "1234"
        })
        assert respuesta.status_code == 404

    def test_estado_solo_sesion_no_encontrada_retorna_404(self):
        """Consultar estado de sesión solo inexistente debe devolver 404 (api.py:148)."""
        respuesta = cliente.get("/solo/99999")
        assert respuesta.status_code == 404

    def test_intento_pvp_en_partida_terminada_retorna_400(self):
        """Intentar en una partida PvP ya terminada debe devolver 400 (api.py:195)."""
        res = cliente.post("/pvp/nuevo", json={
            "nombre_jugador1": "X", "nombre_jugador2": "Y"
        })
        sesion_id = res.json()["sesion_id"]
        # Configurar secretos
        cliente.post("/pvp/secreto", json={"sesion_id": sesion_id, "nombre_jugador": "X", "secreto": "1234"})
        cliente.post("/pvp/secreto", json={"sesion_id": sesion_id, "nombre_jugador": "Y", "secreto": "5678"})
        # X adivina y gana
        cliente.post("/pvp/intento", json={"sesion_id": sesion_id, "nombre_jugador": "X", "intento": "5678"})
        # Intento extra después de que terminó
        respuesta = cliente.post("/pvp/intento", json={
            "sesion_id": sesion_id, "nombre_jugador": "Y", "intento": "1234"
        })
        assert respuesta.status_code == 400
