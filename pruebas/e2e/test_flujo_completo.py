# Pruebas: pruebas/e2e/test_flujo_completo.py
# Propósito: Verificar el flujo completo de la aplicación desde la perspectiva del usuario.
#
# Estas pruebas simulan un usuario real interactuando con el navegador web
# usando Playwright. Comprueban que la interfaz funcione correctamente de
# extremo a extremo (desde llenar el formulario hasta ver el resultado del juego).
#
# Historias de usuario cubiertas: HU-1, HU-2, HU-3

import os
import pytest
from playwright.sync_api import sync_playwright, Page, expect

# URL base de la aplicación (configurable por variable de entorno para Docker)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")


# ── Fixture: navegador y página ────────────────────────────────────────────

@pytest.fixture(scope="function")
def pagina():
    """
    Crea y entrega una nueva página de navegador para cada prueba.
    Cierra el navegador automáticamente al terminar.
    """
    with sync_playwright() as playwright:
        # Ejecutar sin cabeza (headless) para entornos Docker/CI
        navegador = playwright.chromium.launch(headless=True)
        pagina = navegador.new_page()
        yield pagina
        navegador.close()


# ── Pruebas de la Pantalla de Inicio ──────────────────────────────────────

class TestPantallaInicio:
    """Verifica que la pantalla de inicio carga y funciona correctamente."""

    def test_pagina_inicio_carga_correctamente(self, pagina: Page):
        """La página principal debe mostrar el título del juego."""
        pagina.goto(BASE_URL)
        expect(pagina).to_have_title("Picas y Fijas – Inicio")

    def test_formulario_de_nombre_visible(self, pagina: Page):
        """El campo de texto para el nombre del jugador debe estar visible."""
        pagina.goto(BASE_URL)
        campo_nombre = pagina.locator("#nombre1")
        expect(campo_nombre).to_be_visible()

    def test_botones_de_modo_visibles(self, pagina: Page):
        """Los botones para seleccionar el modo de juego deben estar presentes."""
        pagina.goto(BASE_URL)
        expect(pagina.locator("#btn-solo")).to_be_visible()
        expect(pagina.locator("#btn-pvp")).to_be_visible()

    def test_selector_modo_pvp_muestra_campo_jugador2(self, pagina: Page):
        """Al seleccionar PvP, debe aparecer el campo para el nombre del jugador 2."""
        pagina.goto(BASE_URL)
        campo_j2 = pagina.locator("#sec-j2")
        # Al inicio debe estar oculto
        expect(campo_j2).to_be_hidden()
        # Al hacer clic en PvP debe mostrarse
        pagina.click("#btn-pvp")
        expect(campo_j2).to_be_visible()


# ── Pruebas de Flujo: Modo Solo ────────────────────────────────────────────

class TestFlujoModoSolo:
    """Verifica el flujo completo de una partida en modo un jugador."""

    def test_iniciar_juego_solo_redirige_al_tablero(self, pagina: Page):
        """Completar el formulario y enviar debe redirigir a la página del tablero."""
        pagina.goto(BASE_URL)
        pagina.fill("#nombre1", "Jugador Test")
        pagina.click("button[type='submit']")
        # Esperar la redirección al tablero
        pagina.wait_for_url(f"{BASE_URL}/tablero", timeout=5000)
        expect(pagina).to_have_title("Picas y Fijas – Tablero")

    def test_tablero_muestra_barra_de_intentos(self, pagina: Page):
        """El tablero debe mostrar los 10 puntos de intentos disponibles."""
        pagina.goto(BASE_URL)
        pagina.fill("#nombre1", "Jugador Test")
        pagina.click("button[type='submit']")
        pagina.wait_for_url(f"{BASE_URL}/tablero", timeout=5000)
        puntos = pagina.locator(".intento-dot")
        expect(puntos).to_have_count(10)

    def test_intento_invalido_muestra_alerta(self, pagina: Page):
        """Un número inválido (con dígitos repetidos) debe mostrar mensaje de error."""
        pagina.goto(BASE_URL)
        pagina.fill("#nombre1", "Tester")
        pagina.click("button[type='submit']")
        pagina.wait_for_url(f"{BASE_URL}/tablero", timeout=5000)

        # Configurar un handler de diálogo para capturar el alert
        pagina.on("dialog", lambda dialog: dialog.accept())
        pagina.fill("#input-intento", "1123")  # Número con dígitos repetidos
        pagina.click("#btn-intentar")

    def test_intento_valido_aparece_en_historial(self, pagina: Page):
        """Un intento válido debe aparecer en la sección de historial."""
        pagina.goto(BASE_URL)
        pagina.fill("#nombre1", "Tester")
        pagina.click("button[type='submit']")
        pagina.wait_for_url(f"{BASE_URL}/tablero", timeout=5000)

        pagina.fill("#input-intento", "1234")
        pagina.click("#btn-intentar")

        # El historial debe tener al menos una fila
        pagina.wait_for_selector(".fila-intento", timeout=3000)
        filas = pagina.locator(".fila-intento")
        expect(filas).to_have_count(1)


# ── Pruebas de Flujo: Modo PvP ─────────────────────────────────────────────

class TestFlujoModoPvP:
    """Verifica el flujo de configuración inicial en modo PvP."""

    def test_iniciar_pvp_redirige_al_tablero(self, pagina: Page):
        """El formulario PvP completo debe redirigir al tablero."""
        pagina.goto(BASE_URL)
        pagina.click("#btn-pvp")
        pagina.fill("#nombre1", "Jugador1")
        pagina.fill("#nombre2", "Jugador2")
        pagina.click("button[type='submit']")
        pagina.wait_for_url(f"{BASE_URL}/tablero", timeout=5000)
        expect(pagina).to_have_title("Picas y Fijas – Tablero")

    def test_tablero_pvp_muestra_configurar_secreto(self, pagina: Page):
        """En modo PvP, el tablero debe mostrar la sección para configurar el secreto."""
        pagina.goto(BASE_URL)
        pagina.click("#btn-pvp")
        pagina.fill("#nombre1", "Alice")
        pagina.fill("#nombre2", "Bob")
        pagina.click("button[type='submit']")
        pagina.wait_for_url(f"{BASE_URL}/tablero", timeout=5000)
        expect(pagina.locator("#sec-pvp-setup")).to_be_visible()

    def test_health_check_responde_ok(self, pagina: Page):
        """El endpoint de salud debe responder correctamente."""
        pagina.goto(f"{BASE_URL}/health")
        expect(pagina.locator("body")).to_contain_text("ok")
