@echo off
REM Script para ejecutar comandos comunes de testing

setlocal enabledelayedexpansion

if "%1"=="" (
    echo.
    echo =============================================================================
    echo  ChatBot API Testing - Commands
    echo =============================================================================
    echo.
    echo Usage:
    echo   run.bat [command]
    echo.
    echo Available Commands:
    echo.
    echo   mock         - Run tests with mock responses (fast)
    echo   test         - Run tests with real API
    echo   verify       - Verify Magic Loops connection
    echo   verify-mock  - Verify connection with mock
    echo   debug        - Run single test with debug output
    echo   all          - Run all tests
    echo   health       - Run health checks only
    echo.
    echo Examples:
    echo   run.bat mock         - Run tests in mock mode
    echo   run.bat verify       - Check if Magic Loops is working
    echo   run.bat test         - Run real API tests
    echo.
    exit /b 0
)

if "%1"=="mock" (
    echo Running tests with MOCK responses...
    python tests\run_tests_mock.py
    exit /b !errorlevel!
)

if "%1"=="test" (
    echo Running tests with REAL API...
    python -m pytest tests/test_api_health.py::TestAPIHealth -v
    exit /b !errorlevel!
)

if "%1"=="verify" (
    echo Verifying Magic Loops connection...
    python verify_magic_loop.py
    exit /b !errorlevel!
)

if "%1"=="verify-mock" (
    echo Verifying connection with MOCK...
    set USE_MOCK=true
    python verify_magic_loop.py
    exit /b !errorlevel!
)

if "%1"=="debug" (
    echo Running tests with debug output...
    python -m pytest tests/test_api_health.py::TestAPIHealth -v -s
    exit /b !errorlevel!
)

if "%1"=="all" (
    echo Running ALL tests...
    python -m pytest tests/ -v
    exit /b !errorlevel!
)

if "%1"=="health" (
    echo Running HEALTH tests...
    python -m pytest tests/test_api_health.py -v
    exit /b !errorlevel!
)

echo Unknown command: %1
echo Use 'run.bat' without arguments to see available commands
exit /b 1
