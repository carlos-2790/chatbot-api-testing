# 🧪 Guía para Ejecutar Tests Localmente

Aquí tienes las instrucciones paso a paso para ejecutar los tests en tu máquina local.

## Opción 1: Script Automático (Más Fácil)

Si estás en Windows (PowerShell), simplemente ejecuta:

```powershell
.\quick_start.bat
```

Este script se encargará de configurar el entorno y correr los tests básicos.

## Opción 2: Ejecución Manual (Más Control)

Si prefieres ejecutar comandos manualmente, sigue estos pasos en tu terminal:

### 1. Activar el Entorno Virtual

```powershell
.\venv\Scripts\Activate.ps1
```

*(Verás `(venv)` al principio de tu línea de comandos si se activó correctamente)*

### 2. Ejecutar Tests

#### Correr TODOS los tests:
```powershell
pytest -v
```

#### Correr solo Smoke Tests (Rápido):
```powershell
pytest -v -m smoke
```

#### Correr solo Quality Tests (Verifica puntajes):
```powershell
pytest -v -m quality
```

### 3. Generar Reportes

Para generar un archivo HTML con los resultados:

```powershell
pytest --html=reports/report.html --self-contained-html
```

El reporte se guardará en la carpeta `reports/`.

## Opción 3: Usando Docker (Recomendado)

Si configuraste Docker, esta es la forma más limpia de correr los tests, ya que usa un entorno aislado idéntico al de CI/CD.

#### Correr todos los tests:
```powershell
docker-compose run --rm chatbot-tests pytest -v
```

#### Correr Smoke Tests:
```powershell
docker-compose run --rm chatbot-tests pytest -v -m smoke
```