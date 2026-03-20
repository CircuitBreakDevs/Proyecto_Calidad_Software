# Picas y Fijas

Juego de adivinar un número de 4 dígitos únicos. Una **fija** es un dígito en la posición correcta; una **pica** es un dígito que existe pero en otra posición.

## Requisitos

- Docker y Docker Compose instalados. No se necesita Python local.

## Ejecutar la aplicación

```bash
docker compose up --build webapp
```

Abrir en el navegador: http://localhost:8000

## Pruebas

```bash
# Pruebas unitarias + BDD con cobertura
docker compose run --rm unitests

# Pruebas End-to-End (Playwright)
docker compose up --abort-on-container-exit e2e

# Pruebas de Carga y Rendimiento (K6)
# 1. Asegúrate de que la aplicación esté corriendo:
# docker compose up -d webapp
# 2. Ejecuta una de las pruebas de K6 (smoke, stress, spike o soak):
# En PowerShell (Windows):
Get-Content pruebas\carga\smoke.js | docker run --rm -i grafana/k6 run -
# O en CMD / Git Bash / Mac / Linux:
docker run --rm -i grafana/k6 run - < pruebas/carga/smoke.js

```

## Tecnologias usadas en pruebas

| Herramienta | Uso |
|---|---|
| pytest | Framework de pruebas |
| pytest-bdd | Pruebas BDD con Gherkin (.feature) |
| pytest-cov | Cobertura de codigo (minimo 80%) |
| playwright | Pruebas E2E en navegador real |
| k6 | Pruebas de carga y rendimiento (Smoke, Stress, Spike, Soak) |

## SonarQube

[Picas y Fijas](https://sonarcloud.io/project/overview?id=CircuitBreakDevs_Proyecto_Calidad_Software)
