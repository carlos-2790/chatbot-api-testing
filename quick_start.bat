@echo off
echo ========================================
echo Chatbot API Testing Framework
echo Quick Start Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo [1/4] Virtual environment already exists
)

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo [3/4] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [4/4] Running smoke tests...
set PYTHONPATH=.
pytest -v -m smoke
if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed. Check the output above.
) else (
    echo.
    echo ✓ All smoke tests passed!
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo   - Run all tests:        pytest -v
echo   - Run quality tests:    pytest -v -m quality
echo   - Generate HTML report: pytest --html=reports/report.html --self-contained-html
echo   - View README.md for more options
echo.
pause
