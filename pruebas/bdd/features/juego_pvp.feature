# Archivo: pruebas/bdd/features/juego_pvp.feature
# Propósito: Escenarios BDD para el modo dos jugadores (PvP).

Feature: Juego en modo dos jugadores (PvP)
  Como dos jugadores que quieren competir
  Quiero que cada uno pueda configurar su número secreto y turnarse para adivinar
  Para poder jugar un duelo de picas y fijas

  Scenario: Crear una sesión PvP con dos jugadores
    Given dos jugadores llamados "Alice" y "Bob"
    When crean una nueva sesión PvP
    Then la sesión debe crearse exitosamente

  Scenario: Configurar el número secreto de un jugador
    Given una sesión PvP activa entre "Alice" y "Bob"
    When "Alice" configura su secreto con "1234"
    Then el secreto de "Alice" queda registrado

  Scenario: Ambos jugadores configuran su secreto e inicia el juego
    Given una sesión PvP activa entre "Alice" y "Bob"
    When "Alice" configura su secreto con "1234"
    And "Bob" configura su secreto con "5678"
    Then el juego entra en fase de juego

  Scenario: Un jugador juega en su turno
    Given una sesión PvP lista para jugar entre "Alice" y "Bob"
    When "Alice" intenta adivinar con "5123"
    Then el sistema retorna picas y fijas
    And el siguiente turno es de "Bob"

  Scenario: Un jugador adivina el número y gana
    Given una sesión PvP lista para jugar entre "Alice" y "Bob" con secreto de "Bob" siendo "5678"
    When "Alice" intenta adivinar con "5678"
    Then "Alice" ha ganado la partida PvP

  Scenario: Intento fuera de turno es rechazado
    Given una sesión PvP lista para jugar entre "Alice" y "Bob"
    When "Bob" intenta adivinar antes de que sea su turno
    Then el sistema rechaza el intento con un mensaje de error
