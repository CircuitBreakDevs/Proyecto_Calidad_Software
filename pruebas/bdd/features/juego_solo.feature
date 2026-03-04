# Archivo: pruebas/bdd/features/juego_solo.feature
# Propósito: Escenarios BDD (Behavior Driven Development) para el modo un jugador.
#
# Estos escenarios describen el comportamiento esperado del sistema
# desde la perspectiva del usuario, siguiendo el formato Gherkin.

Feature: Juego en modo un jugador
  Como jugador que quiere jugar solo
  Quiero que el sistema genere un número secreto y me permita adivinarlo
  Para poder disfrutar del juego de picas y fijas

  Scenario: Iniciar una partida en modo solo con nombre válido
    Given un jugador con nombre "Carlos"
    When inicia una partida en modo solo
    Then la partida debe crearse exitosamente
    And el jugador tiene 10 intentos disponibles

  Scenario: Realizar un intento inválido (número repetido) en modo solo
    Given un jugador con nombre "Maria"
    And tiene una partida en modo solo activa
    When el jugador intenta con el número "1123"
    Then el sistema debe responder que el número es inválido

  Scenario: Realizar un intento válido y recibir picas y fijas
    Given un jugador con nombre "Pedro"
    And tiene una partida en modo solo activa con secreto "5678"
    When el jugador intenta con el número "5123"
    Then el resultado debe tener al menos "1" fija
    And el número de intentos restantes disminuye

  Scenario: Adivinar el número correctamente en modo solo
    Given un jugador con nombre "Juan"
    And tiene una partida en modo solo activa con secreto "1234"
    When el jugador intenta con el número "1234"
    Then el jugador ha ganado
    And la partida está terminada

  Scenario: Agotar los intentos sin adivinar en modo solo
    Given un jugador con nombre "Ana"
    And tiene una partida en modo solo activa con secreto "9876"
    When el jugador realiza 10 intentos incorrectos
    Then la partida está terminada
    And el jugador no ha ganado
