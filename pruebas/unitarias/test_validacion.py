# Pruebas: pruebas/unitarias/test_validacion.py
# Propósito: Verificar que la función validar_numero cumple todas las reglas del juego.
#
# Historia de Usuario cubierta: HU-4 (Motor de Lógica del Juego)
# Función bajo prueba: src.modelos.validacion.validar_numero

import pytest
from src.modelos.validacion import validar_numero


# ── Pruebas de Longitud ─────────────────────────────────────────────────────

class TestValidacionLongitud:
    """Verifica que el número tenga exactamente 4 dígitos."""

    def test_numero_de_4_digitos_es_valido(self):
        assert validar_numero("1234") is True

    def test_numero_de_3_digitos_es_invalido(self):
        assert validar_numero("123") is False

    def test_numero_de_5_digitos_es_invalido(self):
        assert validar_numero("12345") is False

    def test_cadena_vacia_es_invalida(self):
        assert validar_numero("") is False

    def test_un_solo_digito_es_invalido(self):
        assert validar_numero("7") is False


# ── Pruebas de Contenido (solo dígitos) ─────────────────────────────────────

class TestValidacionContenido:
    """Verifica que el número no contenga letras ni caracteres especiales."""

    def test_numero_solo_con_digitos_es_valido(self):
        assert validar_numero("5678") is True

    def test_numero_con_letras_es_invalido(self):
        assert validar_numero("12a4") is False

    def test_numero_con_espacios_es_invalido(self):
        assert validar_numero("12 4") is False

    def test_numero_con_guion_es_invalido(self):
        assert validar_numero("1-23") is False

    def test_numero_completamente_alfanumerico_es_invalido(self):
        assert validar_numero("abcd") is False


# ── Pruebas de Unicidad de Dígitos ───────────────────────────────────────────

class TestValidacionUnicidad:
    """Verifica que todos los dígitos sean diferentes entre sí."""

    def test_digitos_todos_unicos_es_valido(self):
        assert validar_numero("9876") is True

    def test_primer_y_segundo_digito_repetidos_es_invalido(self):
        assert validar_numero("1134") is False

    def test_ultimo_digito_repetido_es_invalido(self):
        assert validar_numero("1233") is False

    def test_todos_los_digitos_iguales_es_invalido(self):
        assert validar_numero("1111") is False

    def test_digito_repetido_no_adyacente_es_invalido(self):
        # El 2 aparece en posición 0 y 2
        assert validar_numero("2123") is False


# ── Pruebas de Casos Borde ───────────────────────────────────────────────────

class TestValidacionCasosBorde:
    """Casos especiales y límites del rango de dígitos."""

    def test_numero_con_el_cero_es_valido(self):
        # El cero debe ser aceptado como dígito válido
        assert validar_numero("0123") is True

    def test_todos_los_digitos_del_0_al_3(self):
        assert validar_numero("0123") is True

    def test_numero_maximos_digitos_diferentes(self):
        assert validar_numero("9876") is True

    @pytest.mark.parametrize("numero", [
        "1234", "5678", "0123", "9876", "2468", "1357"
    ])
    def test_numeros_validos_parametrizados(self, numero):
        """Múltiples números válidos probados con un solo test parametrizado."""
        assert validar_numero(numero) is True

    @pytest.mark.parametrize("numero", [
        "1123", "1233", "1223", "0001", "9999", "1111"
    ])
    def test_numeros_con_repeticion_parametrizados(self, numero):
        """Múltiples números con dígitos repetidos, todos deben ser inválidos."""
        assert validar_numero(numero) is False
