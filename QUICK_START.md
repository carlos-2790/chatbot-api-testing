# 🚀 Inicio Rápido

## Opción 1: Script Automático (Recomendado)

Simplemente haz doble clic en:
```
quick_start.bat
```

Este script automáticamente:
1. ✅ Crea el entorno virtual
2. ✅ Instala todas las dependencias
3. ✅ Ejecuta los smoke tests
4. ✅ Te muestra los próximos pasos

---

## Opción 2: Manual

### 1. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar tests
```bash
# Smoke tests (rápidos)
pytest -v -m smoke

# Tests de calidad
pytest -v -m quality

# Todos los tests
pytest -v
```

---

## 📊 Ver Resultados Detallados

### Generar reporte HTML
```bash
pytest --html=reports/report.html --self-contained-html
```

Luego abre `reports/report.html` en tu navegador.

### Ver scores de calidad
```bash
python test_quality.py
```

---

## ⚙️ Configuración

### Cambiar threshold de calidad

Crea un archivo `.env` (copia de `.env.example`):
```bash
copy .env.example .env
```

Edita `.env` y cambia:
```
QUALITY_THRESHOLD=0.90
```

---

## 📖 Documentación Completa

- **README.md** - Documentación completa del proyecto
- **test_questions.json** - Dataset de preguntas de prueba
- **pytest.ini** - Configuración de pytest

---

## 🆘 Solución de Problemas

### Error: "No module named 'sentence_transformers'"
```bash
pip install sentence-transformers
```

### Error: "API timeout"
Edita `.env` y aumenta:
```
API_TIMEOUT=20
```

### Tests muy lentos
La primera vez que ejecutas los tests, Sentence Transformers descarga el modelo (~80MB). Las siguientes ejecuciones serán mucho más rápidas.

---

## 📞 Ayuda

Para más información, consulta el [README.md](README.md) completo.
