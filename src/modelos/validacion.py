# Módulo: src/modelos/validacion.py
# Propósito: Validar que un número cumple las reglas del juego Picas y Fijas.
#
# Reglas del juego:
#   - Debe tener exactamente 4 dígitos
#   - Solo debe contener caracteres numéricos
#   - Todos los dígitos deben ser diferentes entre sí


def validar_numero(numero: str) -> bool:
    """
    Valida que un número de entrada cumple con las reglas del juego.

    Parámetros:
        numero: Cadena de texto a validar.

    Retorna:
        True si el número es válido para jugar, False en caso contrario.
    """
    # Regla 1: Debe tener exactamente 4 caracteres
    if len(numero) != 4:
        return False

    # Regla 2: Todos los caracteres deben ser dígitos numéricos
    if not numero.isdigit():
        return False

    # Regla 3: Todos los dígitos deben ser únicos (sin repeticiones)
    if len(set(numero)) != 4:
        return False

    return True
