# Picas y Fijas 🎯

Juego de lógica para adivinar un número de 4 dígitos únicos. Proyecto académico para la asignatura de Calidad del Software.

## Reglas del juego

- **Fija** 🟩: Dígito correcto en la posición correcta
- **Pica** 🟡: Dígito que existe en el número, pero en otra posición
- El número secreto tiene **4 dígitos, todos diferentes**

## Modos de juego

- **Solo**: El sistema genera el número secreto. El jugador tiene **10 intentos**.
- **PvP**: Dos jugadores se turnan para adivinar el número del oponente. Gana quien adivine primero.

---

## 🚀 Cómo ejecutar (solo requiere Docker)

### Levantar la aplicación

```bash
docker compose up --build webapp db
```

Luego abre tu navegador en: **http://localhost:8000**

### Ejecutar pruebas unitarias y BDD (con coverage)

```bash
docker compose run --rm unitests
```

### Ejecutar pruebas End-to-End (Playwright)

```bash
docker compose up --abort-on-container-exit e2e
```

### Ejecutar análisis estático (flake8)

```bash
docker compose run --rm webapp flake8 src/
```

---

## 📁 Estructura del proyecto

```
proyecto/
├── src/
│   ├── modelos/        # Lógica pura: validación y cálculo de picas/fijas
│   ├── servicios/      # Gestión de estado: modo solo y PvP
│   └── interfaz/       # API FastAPI + plantillas HTML
├── pruebas/
│   ├── unitarias/      # Pruebas por función, una clase por categoría
│   ├── bdd/            # Escenarios Gherkin + step definitions
│   └── e2e/            # Flujos completos con Playwright
├── .github/workflows/  # CI: análisis estático + pruebas + coverage ≥ 80%
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 📋 Historias de Usuario

| ID | Historia |
|----|----------|
| HU-1 | El jugador puede ingresar su nombre para identificarse |
| HU-2 | El jugador puede jugar solo contra el sistema con 10 intentos |
| HU-3 | Dos jugadores pueden jugar PvP turnándose; gana quien adivine primero |
| HU-4 | El sistema calcula correctamente picas y fijas por cada intento |

---

## ✅ Requerimientos de calidad implementados

- [x] Historias de usuario con criterios de aceptación
- [x] Pruebas unitarias (`pruebas/unitarias/`)
- [x] Coverage configurado (mínimo 80%, via `--cov-fail-under=80`)
- [x] Pruebas BDD con Gherkin (`pruebas/bdd/`)
- [x] Pruebas E2E con Playwright (`pruebas/e2e/`)
- [x] Análisis estático con flake8 (`.flake8`)
- [x] CI automatizado con GitHub Actions (`.github/workflows/ci.yml`)
