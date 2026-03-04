# Módulo: src/servicios/juego_solo.py
# Propósito: Gestionar el estado de una partida en modo un solo jugador.
#
# Responsabilidades:
#   - Guardar el número secreto generado por el sistema
#   - Registrar cada intento del jugador y su resultado
#   - Controlar el límite de intentos (máximo: 10)
#   - Determinar si el jugador ganó o perdió

import random
from src.modelos.logica import calcular_picas_fijas, es_ganador
from src.modelos.validacion import validar_numero

# Número máximo de intentos que tiene el jugador en modo solo
MAX_INTENTOS = 10


def generar_numero_secreto() -> str:
    """
    Genera aleatoriamente un número de 4 dígitos únicos para que el jugador adivine.

    Retorna:
        Una cadena de texto de 4 dígitos todos diferentes (ej: "4827").
    """
    digitos = random.sample("0123456789", 4)
    return "".join(digitos)


class JuegoSolo:
    """
    Representa y gestiona el estado de una partida en modo un jugador.
    El sistema genera el número secreto y el jugador tiene MAX_INTENTOS para adivinarlo.
    """

    def __init__(self, nombre_jugador: str, numero_secreto: str = None):
        """
        Inicializa una nueva partida en modo solo.

        Parámetros:
            nombre_jugador: Nombre del jugador que identifica la sesión.
            numero_secreto: Opcional. Si no se provee, se genera uno aleatorio.
        """
        self.nombre_jugador = nombre_jugador
        self.numero_secreto = numero_secreto or generar_numero_secreto()
        self.intentos_realizados = []   # Lista de {"intento": str, "resultado": dict}
        self.terminado = False
        self.gano = False

    @property
    def intentos_restantes(self) -> int:
        """Retorna cuántos intentos le quedan al jugador."""
        return MAX_INTENTOS - len(self.intentos_realizados)

    def realizar_intento(self, intento: str) -> dict:
        """
        Procesa un intento del jugador y actualiza el estado de la partida.

        Parámetros:
            intento: El número de 4 dígitos que propone el jugador.

        Retorna:
            Diccionario con:
                - 'valido': bool — si el número cumple las reglas del juego
                - 'resultado': dict — picas y fijas (si el intento es válido)
                - 'gano': bool — si el jugador acertó
                - 'terminado': bool — si la partida finalizó
                - 'intentos_restantes': int — intentos que quedan
                - 'mensaje': str — mensaje descriptivo del resultado

        Lanza:
            ValueError: Si la partida ya había terminado.
        """
        if self.terminado:
            raise ValueError("La partida ya ha terminado.")

        # Validar que el intento cumple las reglas del juego
        if not validar_numero(intento):
            return {
                "valido": False,
                "mensaje": "Número inválido: debe tener 4 dígitos únicos.",
            }

        # Calcular resultado del intento
        resultado = calcular_picas_fijas(self.numero_secreto, intento)
        self.intentos_realizados.append({"intento": intento, "resultado": resultado})

        # Verificar si el jugador ganó
        if es_ganador(resultado):
            self.terminado = True
            self.gano = True
            return {
                "valido": True,
                "resultado": resultado,
                "gano": True,
                "terminado": True,
                "intentos_restantes": self.intentos_restantes,
                "mensaje": (
                    f"¡{self.nombre_jugador} ganó"
                    f" en {len(self.intentos_realizados)} intentos!"
                ),
            }

        # Verificar si se agotaron los intentos
        if self.intentos_restantes == 0:
            self.terminado = True
            return {
                "valido": True,
                "resultado": resultado,
                "gano": False,
                "terminado": True,
                "intentos_restantes": 0,
                "mensaje": f"Sin intentos. El número era: {self.numero_secreto}",
            }

        return {
            "valido": True,
            "resultado": resultado,
            "gano": False,
            "terminado": False,
            "intentos_restantes": self.intentos_restantes,
            "mensaje": f"{resultado['fijas']} fija(s) y {resultado['picas']} pica(s).",
        }
