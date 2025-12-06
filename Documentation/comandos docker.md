# Ejecutar todos los tests
docker-compose run --rm chatbot-tests

# Smoke tests
docker-compose run --rm chatbot-tests pytest -v -m smoke

# Quality tests
docker-compose run --rm chatbot-tests pytest -v -m quality

# Con reporte HTML
docker-compose run --rm chatbot-tests pytest --html=reports/report.html --self-contained-html

# Ver tamaño de imagen
docker images chatbot-api-tests