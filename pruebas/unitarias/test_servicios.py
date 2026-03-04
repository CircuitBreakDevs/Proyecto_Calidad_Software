# Pruebas: pruebas/unitarias/test_servicios.py
# Propósito: Cubrir los caminos de error internos de los servicios
# que el API intercepta antes de llegar a ellos.
# Estas líneas solo se alcanzan llamando al servicio directamente.

import pytest
from src.servicios.juego_solo import JuegoSolo
from src.servicios.juego_pvp import JuegoPvP


# ── JuegoSolo: caminos de error ───────────────────────────────────────────────

def test_realizar_intento_en_partida_terminada_lanza_error():
    """juego_solo.py:74 — ValueError si la partida ya terminó."""
    juego = JuegoSolo("Test", numero_secreto="1234")
    juego.realizar_intento("1234")  # Gana → terminado = True
    with pytest.raises(ValueError, match="ya ha terminado"):
        juego.realizar_intento("5678")


# ── JuegoPvP: caminos de error ────────────────────────────────────────────────

def test_configurar_secreto_jugador_no_reconocido():
    """juego_pvp.py:59 — Jugador desconocido es rechazado."""
    juego = JuegoPvP("Alice", "Bob")
    resultado = juego.configurar_secreto("Carlos", "1234")
    assert resultado["valido"] is False
    assert "no reconocido" in resultado["mensaje"]


def test_configurar_secreto_duplicado_rechazado():
    """juego_pvp.py:65 — No se puede configurar el secreto dos veces."""
    juego = JuegoPvP("Alice", "Bob")
    juego.configurar_secreto("Alice", "1234")
    resultado = juego.configurar_secreto("Alice", "5678")  # Segunda vez
    assert resultado["valido"] is False
    assert "ya configuró" in resultado["mensaje"]


def test_realizar_intento_pvp_en_partida_terminada_lanza_error():
    """juego_pvp.py:99 — ValueError si la partida PvP ya terminó."""
    juego = JuegoPvP("Alice", "Bob")
    juego.configurar_secreto("Alice", "1234")
    juego.configurar_secreto("Bob", "5678")
    juego.realizar_intento("Alice", "5678")  # Alice gana
    with pytest.raises(ValueError, match="ya ha terminado"):
        juego.realizar_intento("Bob", "1234")


def test_realizar_intento_pvp_fase_configuracion():
    """juego_pvp.py:102 — Intento rechazado si aún no inició el juego."""
    juego = JuegoPvP("Alice", "Bob")
    # Solo Alice configuró — juego no ha empezado
    juego.configurar_secreto("Alice", "1234")
    resultado = juego.realizar_intento("Alice", "5678")
    assert resultado["valido"] is False
    assert "no comenzó" in resultado["mensaje"]


def test_realizar_intento_pvp_numero_invalido():
    """juego_pvp.py:108 — Intento inválido rechazado en fase de juego."""
    juego = JuegoPvP("Alice", "Bob")
    juego.configurar_secreto("Alice", "1234")
    juego.configurar_secreto("Bob", "5678")
    resultado = juego.realizar_intento("Alice", "1123")  # Dígitos repetidos
    assert resultado["valido"] is False
