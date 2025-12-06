# Contributing to Chatbot API Testing Framework

## 🎯 Cómo Contribuir

¡Gracias por tu interés en contribuir! Este documento te guiará en el proceso.

## 📋 Proceso de Contribución

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU_USUARIO/chatbot-api-testing.git
cd chatbot-api-testing
```

### 2. Crear Rama

```bash
git checkout -b feature/mi-nueva-funcionalidad
# o
git checkout -b fix/corregir-bug
```

### 3. Configurar Entorno

```bash
# Instalar dependencias
pip install -r requirements.txt
pip install -r dev-requirements.txt

# Instalar pre-commit hooks (opcional)
pip install pre-commit
pre-commit install
```

### 4. Hacer Cambios

- Escribe código limpio y bien documentado
- Sigue las convenciones de estilo (Black, isort)
- Agrega tests para nuevas funcionalidades
- Actualiza documentación si es necesario

### 5. Formatear Código

```bash
# Formatear con Black
black src/ tests/ *.py

# Ordenar imports
isort src/ tests/ *.py

# Verificar linting
flake8 src/ tests/
```

### 6. Ejecutar Tests

```bash
# Tests rápidos
pytest -v -m smoke

# Tests completos
pytest -v

# Con coverage
pytest --cov=src --cov-report=term
```

### 7. Commit

```bash
git add .
git commit -m "tipo: descripción breve

Descripción más detallada si es necesario.

Fixes #123"
```

**Tipos de commit:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formateo, sin cambios de código
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento

### 8. Push y Pull Request

```bash
git push origin feature/mi-nueva-funcionalidad
```

Luego crea un Pull Request en GitHub con:
- Título descriptivo
- Descripción de cambios
- Referencias a issues relacionados
- Screenshots si aplica

## 🎨 Estándares de Código

### Python Style Guide

- Seguir PEP 8
- Usar Black para formateo (line-length: 100)
- Usar isort para imports
- Máximo 100 caracteres por línea
- Docstrings en formato Google

### Ejemplo de Docstring

```python
def calculate_score(text: str, question: str) -> float:
    """
    Calculate quality score for a response.
    
    Args:
        text: The response text to analyze
        question: The original question
        
    Returns:
        Quality score between 0.0 and 1.0
        
    Raises:
        ValueError: If text is empty
        
    Example:
        >>> score = calculate_score("Good answer", "What is testing?")
        >>> print(f"{score:.2f}")
        0.85
    """
    pass
```

### Tests

- Usar pytest
- Nombrar tests descriptivamente: `test_should_return_high_score_for_quality_response`
- Usar fixtures para setup común
- Aim for >80% coverage
- Marcar tests apropiadamente (`@pytest.mark.smoke`, etc.)

## 📝 Documentación

- Actualizar README.md si cambias funcionalidad principal
- Agregar docstrings a funciones y clases
- Comentar código complejo
- Actualizar CHANGELOG.md

## 🐛 Reportar Bugs

Usa GitHub Issues con:
- Título claro
- Pasos para reproducir
- Comportamiento esperado vs actual
- Versión de Python
- Output de error completo

## 💡 Sugerir Features

Usa GitHub Issues con:
- Descripción clara del problema que resuelve
- Propuesta de solución
- Ejemplos de uso
- Alternativas consideradas

## ✅ Checklist de PR

Antes de crear un PR, verifica:

- [ ] Código formateado con Black e isort
- [ ] Tests pasan localmente
- [ ] Agregaste tests para nueva funcionalidad
- [ ] Documentación actualizada
- [ ] Commit messages descriptivos
- [ ] Sin archivos innecesarios (`.pyc`, `__pycache__`, etc.)
- [ ] CI/CD pasa en GitHub Actions

## 🙏 Código de Conducta

- Sé respetuoso y profesional
- Acepta críticas constructivas
- Enfócate en lo mejor para el proyecto
- Ayuda a otros contribuidores

## 📞 Contacto

- GitHub Issues: Para bugs y features
- Pull Requests: Para contribuciones de código
- Discussions: Para preguntas generales

---

**¡Gracias por contribuir!** 🎉
