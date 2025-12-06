# 🐳 Docker Guide - Chatbot API Testing Framework

Esta guía proporciona instrucciones detalladas para usar Docker y Docker Compose con el framework de testing.

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Inicio Rápido](#inicio-rápido)
- [Comandos Comunes](#comandos-comunes)
- [Configuración Avanzada](#configuración-avanzada)
- [Arquitectura Docker](#arquitectura-docker)
- [Troubleshooting](#troubleshooting)

## 🔧 Requisitos Previos

- Docker Desktop instalado ([Descargar aquí](https://www.docker.com/products/docker-desktop))
- Docker Compose (incluido con Docker Desktop)
- Archivo `.env` configurado (copiar desde `.env.example`)

## 🚀 Inicio Rápido

### 1. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
# Asegúrate de configurar API_URL y QUALITY_THRESHOLD
```

### 2. Construir la Imagen Docker

```bash
docker-compose build
```

### 3. Ejecutar Tests

```bash
# Ejecutar todos los tests
docker-compose run --rm chatbot-tests

# Ver los resultados en ./reports/
```

## 📦 Comandos Comunes

### Ejecutar Tests

```bash
# Todos los tests
docker-compose run --rm chatbot-tests pytest -v

# Solo smoke tests
docker-compose run --rm chatbot-tests pytest -v -m smoke

# Solo quality tests
docker-compose run --rm chatbot-tests pytest -v -m quality

# Tests con reporte HTML
docker-compose run --rm chatbot-tests pytest --html=reports/report.html --self-contained-html

# Tests con coverage
docker-compose run --rm chatbot-tests pytest --cov=src --cov-report=html
```

### Gestión de Contenedores

```bash
# Construir/reconstruir imagen
docker-compose build

# Forzar reconstrucción sin cache
docker-compose build --no-cache

# Ver logs
docker-compose logs

# Limpiar contenedores y volúmenes
docker-compose down -v
```

### Ejecutar Scripts Personalizados

```bash
# Ejecutar test_quality.py
docker-compose run --rm chatbot-tests python test_quality.py

# Ver responses guardadas
docker-compose run --rm chatbot-tests python view_responses.py

# Shell interactivo
docker-compose run --rm chatbot-tests bash
```

## ⚙️ Configuración Avanzada

### Variables de Entorno

Puedes sobrescribir variables de entorno directamente:

```bash
# Cambiar threshold temporalmente
docker-compose run --rm -e QUALITY_THRESHOLD=0.90 chatbot-tests pytest -v -m quality

# Cambiar timeout
docker-compose run --rm -e API_TIMEOUT=20 chatbot-tests pytest -v
```

### Volúmenes Persistentes

Los siguientes directorios se montan como volúmenes:

- `./reports` - Reportes HTML y de cobertura
- `./responses` - Respuestas guardadas del API
- `./data` - Datos de configuración

Estos archivos persisten entre ejecuciones del contenedor.

### Modo Desarrollo

Para desarrollo activo, puedes montar el código fuente:

```yaml
# Agregar a docker-compose.yml bajo volumes:
- ./src:/app/src
- ./tests:/app/tests
```

Esto permite editar código sin reconstruir la imagen.

## 🏗️ Arquitectura Docker

### Dockerfile Multi-Stage

El Dockerfile usa un build multi-stage para optimizar el tamaño:

1. **Builder Stage**: Instala dependencias del sistema y Python
2. **Runtime Stage**: Copia solo lo necesario para ejecutar

Beneficios:
- ✅ Imagen final más pequeña
- ✅ Menos vulnerabilidades de seguridad
- ✅ Build más rápido en CI/CD

### Estructura de la Imagen

```
/app
├── src/              # Código fuente
├── tests/            # Tests
├── reports/          # Reportes (volumen)
├── responses/        # Responses (volumen)
├── data/             # Datos (volumen)
├── requirements.txt
└── pytest.ini
```

## 🔍 Troubleshooting

### Problema: "Cannot connect to Docker daemon"

**Solución**: Asegúrate de que Docker Desktop esté ejecutándose.

```bash
# Windows
# Iniciar Docker Desktop desde el menú de inicio

# Verificar que Docker está corriendo
docker --version
```

### Problema: "Port already in use"

**Solución**: Este proyecto no expone puertos, pero si modificas docker-compose.yml:

```bash
# Ver qué está usando el puerto
netstat -ano | findstr :8000

# Detener contenedores
docker-compose down
```

### Problema: Tests fallan pero funcionan localmente

**Solución**: Verifica las variables de entorno

```bash
# Ver variables en el contenedor
docker-compose run --rm chatbot-tests env

# Verificar que .env existe y tiene los valores correctos
cat .env
```

### Problema: Imagen muy grande

**Solución**: Limpiar cache de Docker

```bash
# Limpiar imágenes no usadas
docker image prune -a

# Ver tamaño de la imagen
docker images chatbot-api-tests
```

### Problema: Cambios en código no se reflejan

**Solución**: Reconstruir la imagen

```bash
# Reconstruir sin cache
docker-compose build --no-cache

# O usar volúmenes para desarrollo (ver Modo Desarrollo)
```

## 📊 Comparación: Docker vs Setup Tradicional

| Aspecto | Docker | Setup Tradicional |
|---------|--------|-------------------|
| **Setup inicial** | `docker-compose build` | `python setup.py` |
| **Dependencias** | Aisladas en contenedor | Instaladas globalmente/venv |
| **Portabilidad** | ✅ Alta | ⚠️ Depende del sistema |
| **Reproducibilidad** | ✅ Garantizada | ⚠️ Puede variar |
| **Velocidad** | ⚠️ Overhead inicial | ✅ Más rápido |
| **Uso de recursos** | ⚠️ Mayor | ✅ Menor |

## 🎯 Mejores Prácticas

1. **Siempre usa `.env`** para configuración sensible
2. **Reconstruye la imagen** después de cambiar `requirements.txt`
3. **Usa `--rm`** para limpiar contenedores automáticamente
4. **Monta volúmenes** para datos que deben persistir
5. **Revisa los logs** si algo falla: `docker-compose logs`

## 🔗 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Python Docker Images](https://docs.docker.com/language/python/build-images/)

---

**¿Preguntas?** Consulta el [README.md](../README.md) principal o abre un issue.
