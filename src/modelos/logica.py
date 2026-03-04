# Módulo: src/modelos/logica.py
# Propósito: Calcular el resultado (picas y fijas) de un intento del jugador.
#
# Definiciones:
#   - FIJA:  Dígito correcto en la posición correcta
#   - PICA:  Dígito que existe en el número secreto, pero en posición incorrecta


def calcular_picas_fijas(secreto: str, intento: str) -> dict:
    """
    Calcula cuántas picas y fijas tiene un intento respecto al número secreto.

    Parámetros:
        secreto: El número de 4 dígitos que se debe adivinar.
        intento: El número de 4 dígitos que el jugador propuso.

    Retorna:
        Un diccionario con las claves 'picas' y 'fijas', cada una con un
        entero entre 0 y 4.

    Ejemplo:
        secreto = "1234", intento = "1356"
        → fijas=1 (el '1' está en posición 0), picas=1 (el '3' existe pero en pos. 2→1)
        → {"picas": 1, "fijas": 1}
    """
    fijas = 0
    picas = 0

    for i in range(4):
        if intento[i] == secreto[i]:
            # Dígito correcto en la posición exacta
            fijas += 1
        elif intento[i] in secreto:
            # Dígito existe en el número, pero en posición diferente
            picas += 1

    return {"picas": picas, "fijas": fijas}


def es_ganador(resultado: dict) -> bool:
    """
    Determina si un resultado significa que el jugador adivinó el número.

    Parámetros:
        resultado: Diccionario retornado por calcular_picas_fijas.

    Retorna:
        True si el jugador acertó los 4 dígitos en su posición correcta.
    """
    return resultado["fijas"] == 4
