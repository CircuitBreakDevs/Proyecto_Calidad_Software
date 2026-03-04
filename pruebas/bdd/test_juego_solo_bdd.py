# Pruebas: pruebas/bdd/test_juego_solo_bdd.py
# Propósito: Step definitions para los escenarios BDD del modo un jugador.
#
# Conecta los pasos Gherkin de juego_solo.feature con el código de los servicios.
# Usa el servicio JuegoSolo directamente (sin base de datos) para mayor velocidad.

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.servicios.juego_solo import JuegoSolo

# Cargar todos los escenarios definidos en el archivo .feature correspondiente
scenarios("features/juego_solo.feature")


# ── Fixtures de contexto ────────────────────────────────────────────────────

@pytest.fixture
def contexto():
    """Almacén compartido de estado entre los pasos de un escenario."""
    return {}


# ── Pasos: Given (Dado que...) ──────────────────────────────────────────────

@given(parsers.parse('un jugador con nombre "{nombre}"'))
def dado_jugador_con_nombre(contexto, nombre):
    """Registra el nombre del jugador en el contexto del escenario."""
    contexto["nombre"] = nombre


@given(parsers.parse('tiene una partida en modo solo activa'))
def dado_partida_activa(contexto):
    """Crea una partida en modo solo con un secreto genérico."""
    contexto["juego"] = JuegoSolo(nombre_jugador=contexto["nombre"])


@given(parsers.parse('tiene una partida en modo solo activa con secreto "{secreto}"'))
def dado_partida_con_secreto(contexto, secreto):
    """Crea una partida con un número secreto predefinido (para pruebas determinísticas)."""
    contexto["juego"] = JuegoSolo(
        nombre_jugador=contexto["nombre"],
        numero_secreto=secreto
    )


# ── Pasos: When (Cuando...) ─────────────────────────────────────────────────

@when("inicia una partida en modo solo")
def cuando_inicia_partida(contexto):
    """Crea el objeto JuegoSolo que representa la partida."""
    contexto["juego"] = JuegoSolo(nombre_jugador=contexto["nombre"])


@when(parsers.parse('el jugador intenta con el número "{numero}"'))
def cuando_realiza_intento(contexto, numero):
    """Ejecuta un intento con el número dado y guarda el resultado."""
    contexto["resultado"] = contexto["juego"].realizar_intento(numero)


@when("el jugador realiza 10 intentos incorrectos")
def cuando_realiza_10_intentos(contexto):
    """
    Simula el agotamiento de intentos usando números que no son el secreto.
    Se asegura de que los intentos sean válidos (4 dígitos únicos distintos al secreto).
    """
    intentos_validos = [
        "1234", "5678", "2345", "6789", "3456",
        "7890", "4567", "0123", "8901", "2468"
    ]
    secreto = contexto["juego"].numero_secreto
    ultimo = None
    for intento in intentos_validos:
        if intento != secreto and contexto["juego"].intentos_restantes > 0:
            ultimo = contexto["juego"].realizar_intento(intento)
    contexto["resultado"] = ultimo


# ── Pasos: Then (Entonces...) ───────────────────────────────────────────────

@then("la partida debe crearse exitosamente")
def entonces_partida_creada(contexto):
    """Verifica que el objeto juego existe y tiene un número secreto."""
    assert contexto["juego"] is not None
    assert len(contexto["juego"].numero_secreto) == 4


@then(parsers.parse('el jugador tiene {cantidad} intentos disponibles'))
def entonces_intentos_disponibles(contexto, cantidad):
    """Verifica la cantidad de intentos restantes."""
    assert contexto["juego"].intentos_restantes == int(cantidad)


@then("el sistema debe responder que el número es inválido")
def entonces_invalido(contexto):
    """Verifica que el resultado indica que el número no es válido."""
    assert contexto["resultado"]["valido"] is False


@then(parsers.parse('el resultado debe tener al menos "{n}" fija'))
def entonces_al_menos_n_fijas(contexto, n):
    """Verifica que hay al menos N fijas en el resultado del intento."""
    assert contexto["resultado"]["resultado"]["fijas"] >= int(n)


@then("el número de intentos restantes disminuye")
def entonces_intentos_disminuyen(contexto):
    """Verifica que el contador de intentos bajó al menos una unidad."""
    assert contexto["juego"].intentos_restantes < 10


@then("el jugador ha ganado")
def entonces_gano(contexto):
    """Verifica que el resultado indica que el jugador ganó."""
    assert contexto["resultado"]["gano"] is True


@then("la partida está terminada")
def entonces_terminada(contexto):
    """Verifica que la partida fue marcada como terminada."""
    assert contexto["juego"].terminado is True


@then("el jugador no ha ganado")
def entonces_no_gano(contexto):
    """Verifica que la partida terminó sin que el jugador ganara."""
    assert contexto["juego"].gano is False
