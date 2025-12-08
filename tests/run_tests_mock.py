#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ejecutar tests en modo mock mientras se configura Magic Loops
"""

import os
import subprocess
import sys
from pathlib import Path

def run_tests_with_mock():
    """Ejecuta los tests con cliente en modo mock"""
    
    print("\n" + "=" * 80)
    print("EJECUTANDO TESTS EN MODO MOCK")
    print("=" * 80 + "\n")
    
    # Cambiar al directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    env = os.environ.copy()
    env["USE_MOCK"] = "true"
    
    # Ejecutar solo tests de salud de la API
    cmd = [
        sys.executable, 
        "-m", 
        "pytest",
        "tests/test_api_health.py::TestAPIHealth",
        "-v",
        "--tb=short"
    ]
    
    print(f"Directorio: {project_root}")
    print(f"Comando: {' '.join(cmd)}")
    print(f"Modo Mock: USE_MOCK=true\n")
    
    result = subprocess.run(cmd, env=env)
    
    print("\n" + "=" * 80)
    if result.returncode == 0:
        print("[OK] TODOS LOS TESTS PASARON EN MODO MOCK")
    else:
        print("[ERROR] ALGUNOS TESTS FALLARON")
    print("=" * 80)
    print("\nNota: Estos tests usan respuestas simuladas.")
    print("Para usar la API real, ejecuta sin la variable USE_MOCK o configurala en false")
    print("=" * 80 + "\n")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests_with_mock())
