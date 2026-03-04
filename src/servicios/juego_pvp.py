# Módulo: src/servicios/juego_pvp.py
# Propósito: Gestionar el estado de una partida en modo PvP (jugador vs jugador).
#
# Responsabilidades:
#   - Cada jugador define su propio número secreto al inicio
#   - Los jugadores se turnan para adivinar el número del oponente
#   - Gana el primero que adivine el número del oponente
#   - No hay límite de intentos (solo quien adivine primero gana)

from src.modelos.logica import calcular_picas_fijas, es_ganador
from src.modelos.validacion import validar_numero


class JuegoPvP:
    """
    Representa y gestiona el estado de una partida en modo dos jugadores (PvP).
    Cada jugador elige un número secreto y ambos se turnan para intentar adivinarlo.
    """

    def __init__(self, nombre_jugador1: str, nombre_jugador2: str):
        """
        Inicializa la sesión PvP con los nombres de los dos jugadores.
        Los números secretos se configuran en una etapa posterior.

        Parámetros:
            nombre_jugador1: Nombre del primer jugador (comienza el juego).
            nombre_jugador2: Nombre del segundo jugador.
        """
        self.jugadores = [nombre_jugador1, nombre_jugador2]
        self.secretos = {nombre_jugador1: None, nombre_jugador2: None}
        self.intentos = {nombre_jugador1: [], nombre_jugador2: []}
        self.turno_actual = 0        # Índice en self.jugadores (0 o 1)
        self.terminado = False
        self.ganador = None
        self.fase = "configuracion"  # Fases: 'configuracion' → 'juego' → 'fin'

    @property
    def jugador_en_turno(self) -> str:
        """Retorna el nombre del jugador que debe jugar ahora."""
        return self.jugadores[self.turno_actual]

    @property
    def oponente_en_turno(self) -> str:
        """Retorna el nombre del oponente del jugador activo."""
        return self.jugadores[1 - self.turno_actual]

    def configurar_secreto(self, nombre_jugador: str, secreto: str) -> dict:
        """
        Permite a un jugador registrar su número secreto antes de comenzar.

        Parámetros:
            nombre_jugador: Nombre del jugador que configura su número.
            secreto: El número de 4 dígitos únicos que el jugador elige.

        Retorna:
            Diccionario con el resultado de la operación.
        """
        if nombre_jugador not in self.jugadores:
            return {"valido": False, "mensaje": "Jugador no reconocido."}

        if not validar_numero(secreto):
            return {"valido": False, "mensaje": "Número inválido: debe tener 4 dígitos únicos."}

        if self.secretos[nombre_jugador] is not None:
            return {"valido": False, "mensaje": "Este jugador ya configuró su número secreto."}

        self.secretos[nombre_jugador] = secreto

        # Si ambos jugadores configuraron su secreto, el juego puede comenzar
        ambos_listos = all(v is not None for v in self.secretos.values())
        if ambos_listos:
            self.fase = "juego"
            return {
                "valido": True,
                "mensaje": "¡Ambos jugadores están listos! Empieza " + self.jugadores[0],
                "juego_listo": True,
            }

        return {
            "valido": True,
            "mensaje": f"Secreto de {nombre_jugador} registrado.",
            "juego_listo": False,
        }

    def realizar_intento(self, nombre_jugador: str, intento: str) -> dict:
        """
        Procesa el intento de un jugador para adivinar el número del oponente.

        Parámetros:
            nombre_jugador: Nombre del jugador que realiza el intento.
            intento: El número de 4 dígitos que propone como guess.

        Retorna:
            Diccionario con:
                - 'valido': bool
                - 'resultado': dict — picas y fijas
                - 'gano': bool
                - 'terminado': bool
                - 'siguiente_turno': str — quién juega a continuación
                - 'mensaje': str
        """
        if self.terminado:
            raise ValueError("La partida ya ha terminado.")

        if self.fase != "juego":
            msg = "El juego aún no comenzó. Ambos jugadores deben configurar su secreto."
            return {"valido": False, "mensaje": msg}

        if nombre_jugador != self.jugador_en_turno:
            msg = f"No es el turno de {nombre_jugador}. Es el turno de {self.jugador_en_turno}."
            return {"valido": False, "mensaje": msg}

        if not validar_numero(intento):
            return {"valido": False, "mensaje": "Número inválido: debe tener 4 dígitos únicos."}

        # El jugador activo intenta adivinar el secreto del oponente
        secreto_oponente = self.secretos[self.oponente_en_turno]
        resultado = calcular_picas_fijas(secreto_oponente, intento)
        self.intentos[nombre_jugador].append({"intento": intento, "resultado": resultado})

        # Verificar si el jugador ganó
        if es_ganador(resultado):
            self.terminado = True
            self.ganador = nombre_jugador
            self.fase = "fin"
            return {
                "valido": True,
                "resultado": resultado,
                "gano": True,
                "terminado": True,
                "siguiente_turno": None,
                "mensaje": f"¡{nombre_jugador} ganó el juego!",
            }

        # Cambiar el turno al siguiente jugador
        self.turno_actual = 1 - self.turno_actual

        return {
            "valido": True,
            "resultado": resultado,
            "gano": False,
            "terminado": False,
            "siguiente_turno": self.jugador_en_turno,
            "mensaje": (
                f"{resultado['fijas']} fija(s) y {resultado['picas']} pica(s)."
                f" Turno de {self.jugador_en_turno}."
            ),
        }
