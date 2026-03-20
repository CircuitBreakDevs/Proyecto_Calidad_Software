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


# Pruebas de Carga (K6)
# NOTA: Usar host.docker.internal para que K6 encuentre el puerto 8000 en Windows

# En PowerShell (para correr cada prueba individualmente):
Get-Content pruebas\carga\smoke.js | docker run --rm -i -e API_URL=http://host.docker.internal:8000 grafana/k6 run -
Get-Content pruebas\carga\stress.js | docker run --rm -i -e API_URL=http://host.docker.internal:8000 grafana/k6 run -
Get-Content pruebas\carga\spike.js | docker run --rm -i -e API_URL=http://host.docker.internal:8000 grafana/k6 run -
Get-Content pruebas\carga\soak.js | docker run --rm -i -e API_URL=http://host.docker.internal:8000 grafana/k6 run -

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
