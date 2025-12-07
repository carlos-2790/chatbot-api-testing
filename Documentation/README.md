# Chatbot API Testing Framework

[![API Tests](https://github.com/YOUR_USERNAME/chatbot-api-testing/actions/workflows/api-tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/chatbot-api-testing/actions/workflows/api-tests.yml)

Framework de testing automatizado para validar respuestas de una API de chatbot sobre buenas prácticas de testing, con sistema de scoring multi-dimensional que garantiza calidad **>0.85**.

## 🎯 Características

- ✅ **Validación Multi-dimensional**: Combina validación estructural (20%), de contenido (40%) y semántica (40%)
- 🤖 **Validación Semántica con IA**: Usa Sentence Transformers para medir relevancia de respuestas
- 📊 **Sistema de Scoring Configurable**: Threshold ajustable vía variables de entorno
- 🔄 **Retry Logic**: Reintentos automáticos con backoff exponencial
- 📈 **Reportes Detallados**: Reportes HTML con métricas de calidad y coverage
- 🚀 **CI/CD Integrado**: GitHub Actions con ejecución automática
- 🧪 **Suite Completa de Tests**: Health checks, validación estructural, calidad de contenido y escenarios

## 📋 Requisitos

- Python 3.8+
- pip

## 🚀 Instalación

1. **Clonar el repositorio** (o crear uno nuevo):
```bash
git clone <your-repo-url>
cd chatbot-api-testing
```

2. **Crear entorno virtual** (recomendado):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno** (opcional):
```bash
copy .env.example .env
# Editar .env con tus configuraciones
```

## 🐳 Instalación con Docker

**Opción alternativa**: Usa Docker para un setup más rápido y portable.

1. **Asegúrate de tener Docker instalado**:
   - [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **Configurar variables de entorno**:
```bash
copy .env.example .env
# Editar .env con tus configuraciones
```

3. **Construir y ejecutar con Docker Compose**:
```bash
# Construir la imagen
docker-compose build

# Ejecutar todos los tests
docker-compose run --rm chatbot-tests

# Ejecutar smoke tests
docker-compose run --rm chatbot-tests pytest -v -m smoke
```

📖 **Ver [Documentation/DOCKER.md](Documentation/DOCKER.md) para guía completa de Docker**

## 🎮 Uso

### Ejecutar todos los tests

```bash
pytest -v
```

### Ejecutar tests por categoría

```bash
# Smoke tests (rápidos)
pytest -v -m smoke

# Tests de regresión
pytest -v -m regression

# Tests de calidad
pytest -v -m quality
```

### Generar reporte HTML

```bash
pytest --html=reports/report.html --self-contained-html
```

### Ejecutar con coverage

```bash
pytest --cov=src --cov-report=html --cov-report=term
```

### Ajustar threshold de calidad

```bash
# Windows PowerShell
$env:QUALITY_THRESHOLD="0.90"; pytest -v

# Linux/Mac
QUALITY_THRESHOLD=0.90 pytest -v
```

### Con Docker

```bash
# Ejecutar todos los tests
docker-compose run --rm chatbot-tests pytest -v

# Smoke tests
docker-compose run --rm chatbot-tests pytest -v -m smoke

# Con reporte HTML
docker-compose run --rm chatbot-tests pytest --html=reports/report.html --self-contained-html

# Con threshold personalizado
docker-compose run --rm -e QUALITY_THRESHOLD=0.90 chatbot-tests pytest -v
```

📖 **Más comandos Docker en [Documentation/DOCKER.md](Documentation/DOCKER.md)**

## 📊 Sistema de Scoring

El framework evalúa cada respuesta con un score de **0.0 a 1.0** basado en:

### 1. Validación Estructural (20%)
- ✓ Formato JSON válido
- ✓ Campo "answer" presente
- ✓ Respuesta no vacía
- ✓ Longitud mínima (>100 caracteres)

### 2. Validación de Contenido (40%)
- ✓ Contiene ejemplos de código
- ✓ Menciona frameworks/herramientas (pytest, unittest, etc.)
- ✓ Incluye mejores prácticas numeradas
- ✓ Estructura organizada (listas, bullets)
- ✓ Keywords relevantes (assert, mock, test, etc.)

### 3. Validación Semántica (40%)
- ✓ Relevancia a la pregunta (similarity score con Sentence Transformers)
- ✓ Coherencia del contenido
- ✓ Profundidad técnica

**Threshold por defecto**: 0.85 (configurable)

## 📁 Estructura del Proyecto

```
chatbot-api-testing/
├── src/
│   ├── api/
│   │   └── chatbot_client.py      # Cliente HTTP con retry logic
│   ├── validators/
│   │   ├── response_validator.py  # Validación de estructura
│   │   ├── content_validator.py   # Validación de contenido
│   │   └── quality_scorer.py      # Sistema de scoring
│   └── utils/
│       └── config.py               # Configuración centralizada
├── tests/
│   ├── conftest.py                 # Fixtures compartidas
│   ├── test_api_health.py          # Tests de disponibilidad
│   ├── test_response_structure.py  # Tests de estructura
│   ├── test_content_quality.py     # Tests de calidad
│   └── test_scenarios.py           # Tests parametrizados
├── data/
│   └── test_questions.json         # Dataset de preguntas
├── Documentation/
│   └── DOCKER.md                   # Guía de Docker
├── .github/workflows/
│   └── api-tests.yml               # CI/CD con GitHub Actions
├── Dockerfile                      # Configuración Docker
├── docker-compose.yml              # Orquestación de contenedores
├── .dockerignore                   # Exclusiones para Docker
└── reports/                        # Reportes generados
```

## 🔧 Configuración

Variables de entorno disponibles en `.env`:

```bash
# URL de la API
API_URL=https://magicloops.dev/api/loop/7e391b7e-f45a-49ec-bd71-bd23b9ad711e/run

# Threshold de calidad (0.0 - 1.0)
QUALITY_THRESHOLD=0.85

# Timeouts
API_TIMEOUT=10
REQUEST_RETRY_COUNT=3

# Logging
LOG_LEVEL=INFO
```

## 🧪 Ejemplos de Uso

### Uso Programático

```python
from src.api.chatbot_client import ChatbotClient
from src.validators.quality_scorer import QualityScorer

# Crear cliente
client = ChatbotClient()

# Hacer pregunta
response = client.ask("¿Cómo escribir tests unitarios en Python?")

# Evaluar calidad
scorer = QualityScorer()
score = scorer.calculate_overall_score(response, "¿Cómo escribir tests unitarios en Python?")

print(f"Quality Score: {score:.2f}")

# Obtener detalles
details = scorer.get_detailed_scores(response, "¿Cómo escribir tests unitarios en Python?")
print(f"Structural: {details['structural_score']:.2f}")
print(f"Content: {details['content_score']:.2f}")
print(f"Semantic: {details['semantic_score']:.2f}")
print(f"Passes: {details['passes_threshold']}")
```

### Agregar Nuevas Preguntas de Test

Edita `data/test_questions.json`:

```json
{
  "question": "Tu nueva pregunta aquí",
  "expected_topics": ["keyword1", "keyword2"]
}
```

## 📈 CI/CD

El proyecto incluye GitHub Actions que:

- ✅ Ejecuta tests automáticamente en push/PR
- ✅ Corre tests diariamente (9 AM UTC)
- ✅ **Tests con Python tradicional** (matriz 3.9-3.12) con `PYTHONPATH` configurado
- ✅ **Tests con Docker** para consistencia con desarrollo local
- ✅ Genera reportes HTML y coverage
- ✅ Publica artifacts
- ✅ Comenta resultados en PRs

**Configuración de PYTHONPATH**: Todos los jobs de test incluyen `PYTHONPATH: ${{ github.workspace }}` para asegurar que Python encuentre el módulo `src`.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🙏 Agradecimientos

- [Sentence Transformers](https://www.sbert.net/) - Para validación semántica
- [Pytest](https://pytest.org/) - Framework de testing
- [MagicLoops](https://magicloops.dev/) - API de chatbot

---

**¿Preguntas o sugerencias?** Abre un issue en GitHub.
