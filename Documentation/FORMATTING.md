# 🎨 Configuración de Formateo de Código

## Para Python: Black + isort

### Instalación

```bash
pip install -r dev-requirements.txt
```

Esto instalará:
- **Black** - Formateador de código Python (equivalente a Prettier)
- **isort** - Ordenador de imports
- **flake8** - Linter de código
- **autopep8** - Formateador automático PEP8

### Uso Manual

**Formatear todo el proyecto:**
```bash
# Con Black
black src/ tests/ *.py

# Ordenar imports
isort src/ tests/ *.py

# Verificar estilo (sin modificar)
flake8 src/ tests/
```

**Formatear archivo específico:**
```bash
black src/validators/quality_scorer.py
isort src/validators/quality_scorer.py
```

### Configuración de VS Code

**Extensiones recomendadas:**
1. **Black Formatter** (ms-python.black-formatter)
2. **isort** (ms-python.isort)
3. **Prettier** (esbenp.prettier-vscode) - Para JSON/Markdown

**Configuración manual:**

1. Abre VS Code Settings (Ctrl+,)
2. Busca "Python Formatting Provider"
3. Selecciona "black"
4. Activa "Format On Save"

**O crea `.vscode/settings.json` manualmente:**

```json
{
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "isort.args": ["--profile", "black"]
}
```

## Para JSON/Markdown/YAML: Prettier

### Instalación (opcional)

Si quieres usar Prettier para archivos JSON, Markdown, etc.:

```bash
npm install --save-dev prettier
```

### Configuración Prettier

Crea `.prettierrc.json`:

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": false,
  "trailingComma": "es5",
  "bracketSpacing": true,
  "arrowParens": "always"
}
```

### Uso

```bash
# Formatear archivos JSON/Markdown
npx prettier --write "**/*.{json,md,yml,yaml}"

# Solo verificar
npx prettier --check "**/*.{json,md,yml,yaml}"
```

## Configuración del Proyecto

### pyproject.toml

El archivo `pyproject.toml` ya está configurado con:

```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']

[tool.isort]
profile = "black"
line_length = 100
```

### Pre-commit Hook (opcional)

Para formatear automáticamente antes de cada commit:

**Instalar pre-commit:**
```bash
pip install pre-commit
```

**Crear `.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
```

**Activar:**
```bash
pre-commit install
```

## Atajos de Teclado en VS Code

- **Formatear documento:** `Shift + Alt + F`
- **Formatear selección:** `Ctrl + K, Ctrl + F`
- **Organizar imports:** `Shift + Alt + O`

## Comandos Rápidos

```bash
# Formatear todo el proyecto
black . && isort .

# Verificar sin modificar
black --check . && isort --check .

# Ver diferencias
black --diff src/

# Formatear solo archivos modificados
git diff --name-only | grep '\.py$' | xargs black
```

## Integración con CI/CD

Agregar a `.github/workflows/api-tests.yml`:

```yaml
- name: Check code formatting
  run: |
    pip install black isort flake8
    black --check src/ tests/
    isort --check src/ tests/
    flake8 src/ tests/
```

---

**¡Código limpio y consistente!** ✨
