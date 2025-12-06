# 🚀 Guía de CI/CD

## Workflows Configurados

El proyecto incluye 3 workflows de GitHub Actions:

### 1. 📋 API Tests & Quality Checks (`api-tests.yml`)

**Triggers:**
- Push a `main` o `develop`
- Pull requests a `main`
- Schedule diario (9 AM UTC)
- Manual dispatch

**Jobs:**

#### Code Quality Checks
- ✅ Black formatting check
- ✅ isort import sorting check
- ✅ flake8 linting

#### Tests (Matrix: Python 3.9, 3.10, 3.11, 3.12)
- ✅ Smoke tests
- ✅ Quality tests
- ✅ Full test suite con coverage
- 📊 Upload de reportes HTML
- 📈 Upload de coverage a Codecov

#### Quality Gate
- ✅ Validación de threshold >0.85
- ✅ Test de calidad completo

#### PR Comments
- 💬 Comenta automáticamente en PRs con resultados

---

### 2. 🌙 Nightly Quality Report (`nightly-report.yml`)

**Triggers:**
- Schedule nocturno (2 AM UTC)
- Manual dispatch

**Funcionalidad:**
- Ejecuta tests de calidad
- Guarda respuestas de la IA
- Genera resumen de calidad
- Upload de artifacts (retención: 90 días)

**Uso:** Monitorear calidad de la API a lo largo del tiempo

---

### 3. 🎁 Release (`release.yml`)

**Triggers:**
- Push de tags `v*` (ej: `v1.0.0`)
- Manual dispatch

**Funcionalidad:**
- Ejecuta suite completa de tests
- Crea GitHub Release
- Genera changelog automático

---

## Configuración Inicial

### 1. Crear Repositorio en GitHub

```bash
cd C:\Users\crlsy\OneDrive\Escritorio\repo\chatbot-api-testing

# Inicializar git (si no está inicializado)
git init

# Agregar archivos
git add .
git commit -m "Initial commit: API testing framework"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/chatbot-api-testing.git
git branch -M main
git push -u origin main
```

### 2. Configurar Secrets (Opcional)

Para funcionalidades avanzadas, agrega secrets en GitHub:

**Settings → Secrets and variables → Actions → New repository secret**

Secrets útiles:
- `CODECOV_TOKEN` - Para reportes de coverage
- `SLACK_WEBHOOK` - Para notificaciones
- `API_KEY` - Si tu API requiere autenticación

### 3. Activar GitHub Actions

Los workflows se activan automáticamente al hacer push. Verifica en:
**Actions tab** de tu repositorio

---

## Badges para README

Agrega estos badges a tu `README.md`:

```markdown
[![API Tests](https://github.com/TU_USUARIO/chatbot-api-testing/actions/workflows/api-tests.yml/badge.svg)](https://github.com/TU_USUARIO/chatbot-api-testing/actions/workflows/api-tests.yml)
[![codecov](https://codecov.io/gh/TU_USUARIO/chatbot-api-testing/branch/main/graph/badge.svg)](https://codecov.io/gh/TU_USUARIO/chatbot-api-testing)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

---

## Flujo de Trabajo Recomendado

### Para Desarrollo

```bash
# 1. Crear rama feature
git checkout -b feature/nueva-funcionalidad

# 2. Hacer cambios
# ... editar código ...

# 3. Formatear código localmente
black src/ tests/
isort src/ tests/

# 4. Ejecutar tests localmente
pytest -v -m smoke

# 5. Commit y push
git add .
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad

# 6. Crear Pull Request en GitHub
# CI/CD se ejecutará automáticamente
```

### Para Release

```bash
# 1. Asegurar que main está actualizado
git checkout main
git pull

# 2. Crear tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 3. GitHub Actions creará el release automáticamente
```

---

## Monitoreo y Reportes

### Ver Resultados de CI/CD

1. Ve a **Actions** tab en GitHub
2. Selecciona el workflow
3. Ve los logs detallados
4. Descarga artifacts (reportes HTML, coverage)

### Artifacts Disponibles

- `test-reports-py3.X` - Reportes HTML de tests
- `coverage-report-py3.X` - Reportes de coverage
- `nightly-responses-X` - Respuestas guardadas (nightly)
- `nightly-summary-X` - Resumen de calidad (nightly)

### Codecov Integration

Si configuras Codecov:
1. Crea cuenta en [codecov.io](https://codecov.io)
2. Conecta tu repositorio
3. Agrega `CODECOV_TOKEN` a secrets
4. Los reportes se subirán automáticamente

---

## Personalización

### Cambiar Schedule

Edita `.github/workflows/api-tests.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Diario a las 9 AM UTC
  # Formato: minuto hora día mes día-semana
  # Ejemplos:
  # - cron: '0 */6 * * *'  # Cada 6 horas
  # - cron: '0 0 * * 1'    # Cada lunes
```

### Agregar Notificaciones

#### Slack

```yaml
- name: Send Slack notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

#### Email (usando GitHub)

```yaml
- name: Send email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: CI/CD Results
    body: Tests completed!
    to: tu@email.com
```

### Agregar Deployment

Para deployar a un servidor:

```yaml
deploy:
  name: Deploy to Production
  runs-on: ubuntu-latest
  needs: quality-gate
  if: github.ref == 'refs/heads/main'
  
  steps:
  - name: Deploy via SSH
    uses: appleboy/ssh-action@master
    with:
      host: ${{ secrets.SERVER_HOST }}
      username: ${{ secrets.SERVER_USER }}
      key: ${{ secrets.SSH_PRIVATE_KEY }}
      script: |
        cd /path/to/app
        git pull
        pip install -r requirements.txt
        systemctl restart app
```

---

## Troubleshooting

### Tests fallan en CI pero pasan localmente

**Causa:** Diferencias de entorno

**Solución:**
```bash
# Ejecutar en contenedor Docker localmente
docker run -it python:3.11 bash
pip install -r requirements.txt
pytest -v
```

### Timeouts en tests de calidad

**Causa:** API lenta

**Solución:** Aumentar timeout en workflow:
```yaml
- name: Run quality tests
  run: pytest -v -m quality
  timeout-minutes: 15  # Aumentar de 10 a 15
```

### Coverage muy bajo

**Causa:** Faltan tests

**Solución:** Agregar más tests o excluir archivos:
```ini
# pytest.ini
[coverage:run]
omit = 
    */tests/*
    */setup.py
```

---

## Comandos Útiles

```bash
# Ver status de workflows
gh workflow list

# Ejecutar workflow manualmente
gh workflow run api-tests.yml

# Ver runs recientes
gh run list

# Ver logs de un run
gh run view <run-id> --log

# Descargar artifacts
gh run download <run-id>
```

---

**¡CI/CD configurado y listo!** 🚀
