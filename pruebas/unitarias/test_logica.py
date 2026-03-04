# Pruebas: pruebas/unitarias/test_logica.py
# Propósito: Verificar que el cálculo de picas y fijas es correcto en todos los casos posibles.
#
# Historia de Usuario cubierta: HU-4 (Motor de Lógica del Juego)
# Funciones bajo prueba:
#   - src.modelos.logica.calcular_picas_fijas
#   - src.modelos.logica.es_ganador

import pytest
from src.modelos.logica import calcular_picas_fijas, es_ganador


# ── Pruebas de Fijas ─────────────────────────────────────────────────────────

class TestFijas:
    """Verifica la detección de dígitos correctos en la posición correcta."""

    def test_cuatro_fijas_es_numero_exacto(self):
        resultado = calcular_picas_fijas("1234", "1234")
        assert resultado == {"fijas": 4, "picas": 0}

    def test_primera_posicion_fija(self):
        resultado = calcular_picas_fijas("1234", "1567")
        assert resultado["fijas"] == 1
        assert resultado["picas"] == 0

    def test_ultima_posicion_fija(self):
        resultado = calcular_picas_fijas("1234", "5674")
        assert resultado["fijas"] == 1

    def test_dos_fijas(self):
        # '1' en pos 0 = fija, '2' en pos 1 = fija, '7' no existe, '8' no existe
        resultado = calcular_picas_fijas("1234", "1278")
        assert resultado["fijas"] == 2

    def test_tres_fijas(self):
        resultado = calcular_picas_fijas("1234", "1235")
        assert resultado["fijas"] == 3


# ── Pruebas de Picas ─────────────────────────────────────────────────────────

class TestPicas:
    """Verifica la detección de dígitos correctos en posición incorrecta."""

    def test_una_pica_digito_en_posicion_erronea(self):
        resultado = calcular_picas_fijas("1234", "2000")
        assert resultado["picas"] == 1
        assert resultado["fijas"] == 0

    def test_cuatro_picas_todos_presentes_pero_rotados(self):
        resultado = calcular_picas_fijas("1234", "2341")
        assert resultado["picas"] == 4
        assert resultado["fijas"] == 0

    def test_dos_picas(self):
        resultado = calcular_picas_fijas("1234", "2156")
        assert resultado["picas"] == 2

    def test_una_pica_y_una_fija(self):
        resultado = calcular_picas_fijas("1234", "1560")
        assert resultado["fijas"] == 1   # solo el '1'
        assert resultado["picas"] == 0


# ── Pruebas de Cero Resultados ───────────────────────────────────────────────

class TestSinCoincidencias:
    """Verifica el caso donde no hay ningún dígito en común."""

    def test_cero_picas_cero_fijas(self):
        resultado = calcular_picas_fijas("1234", "5678")
        assert resultado == {"fijas": 0, "picas": 0}

    def test_ninguna_coincidencia_con_ceros(self):
        resultado = calcular_picas_fijas("1234", "5609")
        assert resultado["fijas"] == 0
        assert resultado["picas"] == 0


# ── Pruebas de la función es_ganador ─────────────────────────────────────────

class TestEsGanador:
    """Verifica que es_ganador detecta correctamente el acierto total."""

    def test_cuatro_fijas_es_ganador(self):
        resultado = {"fijas": 4, "picas": 0}
        assert es_ganador(resultado) is True

    def test_tres_fijas_no_es_ganador(self):
        resultado = {"fijas": 3, "picas": 1}
        assert es_ganador(resultado) is False

    def test_cero_fijas_no_es_ganador(self):
        resultado = {"fijas": 0, "picas": 4}
        assert es_ganador(resultado) is False

    def test_ninguna_coincidencia_no_es_ganador(self):
        resultado = {"fijas": 0, "picas": 0}
        assert es_ganador(resultado) is False


# ── Pruebas Parametrizadas ───────────────────────────────────────────────────

@pytest.mark.parametrize("secreto, intento, fijas_esperadas, picas_esperadas", [
    ("1234", "1234", 4, 0),  # Acierto total
    ("1234", "5678", 0, 0),  # Sin coincidencias
    ("1234", "1357", 1, 1),  # 1 fija (el '1'), 1 pica (el '3')
    ("0987", "9870", 0, 4),  # Todos bien, todos en posición incorrecta
    ("1234", "4321", 0, 4),  # Todos presentes, invertidos
])
def test_calcular_picas_fijas_parametrizado(secreto, intento, fijas_esperadas, picas_esperadas):
    """Tabla de verdad de picas y fijas para múltiples combinaciones."""
    resultado = calcular_picas_fijas(secreto, intento)
    assert resultado["fijas"] == fijas_esperadas
    assert resultado["picas"] == picas_esperadas
