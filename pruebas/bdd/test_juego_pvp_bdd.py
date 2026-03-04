# Pruebas: pruebas/bdd/test_juego_pvp_bdd.py
# Propósito: Step definitions para los escenarios BDD del modo PvP.
#
# Conecta los pasos Gherkin de juego_pvp.feature con el servicio JuegoPvP.

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.servicios.juego_pvp import JuegoPvP

# Cargar todos los escenarios del archivo .feature de PvP
scenarios("features/juego_pvp.feature")


# ── Fixtures de contexto ────────────────────────────────────────────────────

@pytest.fixture
def contexto():
    """Almacén compartido de estado entre los pasos de un escenario."""
    return {}


# ── Pasos: Given (Dado que...) ──────────────────────────────────────────────

@given(parsers.parse('dos jugadores llamados "{j1}" y "{j2}"'))
def dado_dos_jugadores(contexto, j1, j2):
    """Registra los nombres de los dos jugadores."""
    contexto["j1"] = j1
    contexto["j2"] = j2


@given(parsers.parse('una sesión PvP activa entre "{j1}" y "{j2}"'))
def dado_sesion_pvp_activa(contexto, j1, j2):
    """Crea una sesión PvP nueva entre dos jugadores."""
    contexto["j1"] = j1
    contexto["j2"] = j2
    contexto["juego"] = JuegoPvP(j1, j2)


@given(parsers.parse('una sesión PvP lista para jugar entre "{j1}" y "{j2}"'))
def dado_sesion_pvp_lista(contexto, j1, j2):
    """Crea una sesión PvP con ambos números secretos ya configurados."""
    contexto["j1"] = j1
    contexto["j2"] = j2
    juego = JuegoPvP(j1, j2)
    juego.configurar_secreto(j1, "1234")
    juego.configurar_secreto(j2, "5678")
    contexto["juego"] = juego


@given(parsers.parse('una sesión PvP lista para jugar entre "{j1}" y "{j2}" con secreto de "{j}" siendo "{secreto}"'))
def dado_sesion_pvp_con_secreto_especifico(contexto, j1, j2, j, secreto):
    """Crea una sesión PvP con secretos específicos para pruebas determinísticas."""
    contexto["j1"] = j1
    contexto["j2"] = j2
    juego = JuegoPvP(j1, j2)
    # Asignar secreto genérico al jugador sin secreto específico
    for jugador in [j1, j2]:
        if jugador != j:
            juego.configurar_secreto(jugador, "0987")
    juego.configurar_secreto(j, secreto)
    contexto["juego"] = juego


# ── Pasos: When (Cuando...) ─────────────────────────────────────────────────

@when(parsers.parse('crean una nueva sesión PvP'))
def cuando_crean_sesion(contexto):
    """Instancia el objeto JuegoPvP."""
    contexto["juego"] = JuegoPvP(contexto["j1"], contexto["j2"])


@when(parsers.parse('"{jugador}" configura su secreto con "{secreto}"'))
def cuando_configura_secreto(contexto, jugador, secreto):
    """Ejecuta la configuración del secreto de un jugador."""
    contexto["resultado"] = contexto["juego"].configurar_secreto(jugador, secreto)


@when(parsers.parse('"{jugador}" intenta adivinar con "{numero}"'))
def cuando_intenta_adivinar(contexto, jugador, numero):
    """Ejecuta un intento de adivinar dentro de la partida PvP."""
    contexto["resultado"] = contexto["juego"].realizar_intento(jugador, numero)


@when(parsers.parse('"{jugador}" intenta adivinar antes de que sea su turno'))
def cuando_intenta_fuera_de_turno(contexto, jugador):
    """Intenta jugar con el jugador que NO tiene el turno activo."""
    # El turno inicial es del jugador 1, así que jugador 2 juega fuera de turno
    contexto["resultado"] = contexto["juego"].realizar_intento(jugador, "1357")


# ── Pasos: Then (Entonces...) ───────────────────────────────────────────────

@then("la sesión debe crearse exitosamente")
def entonces_sesion_creada(contexto):
    """Verifica que la sesión PvP fue creada correctamente."""
    assert contexto["juego"] is not None
    assert len(contexto["juego"].jugadores) == 2


@then(parsers.parse('el secreto de "{jugador}" queda registrado'))
def entonces_secreto_registrado(contexto, jugador):
    """Verifica que el secreto del jugador fue guardado."""
    assert contexto["juego"].secretos[jugador] is not None


@then("el juego entra en fase de juego")
def entonces_fase_juego(contexto):
    """Verifica que la fase cambió a 'juego'."""
    assert contexto["juego"].fase == "juego"


@then("el sistema retorna picas y fijas")
def entonces_retorna_picas_fijas(contexto):
    """Verifica que el resultado contiene la clave 'resultado' con picas y fijas."""
    assert "resultado" in contexto["resultado"]
    assert "fijas" in contexto["resultado"]["resultado"]
    assert "picas" in contexto["resultado"]["resultado"]


@then(parsers.parse('el siguiente turno es de "{jugador}"'))
def entonces_siguiente_turno(contexto, jugador):
    """Verifica que el turno cambió al jugador correcto."""
    assert contexto["juego"].jugador_en_turno == jugador


@then(parsers.parse('"{jugador}" ha ganado la partida PvP'))
def entonces_gano_pvp(contexto, jugador):
    """Verifica que el jugador indicado fue marcado como ganador."""
    assert contexto["resultado"]["gano"] is True
    assert contexto["juego"].ganador == jugador


@then("el sistema rechaza el intento con un mensaje de error")
def entonces_rechazado(contexto):
    """Verifica que el intento fue rechazado por turno incorrecto."""
    assert contexto["resultado"]["valido"] is False
