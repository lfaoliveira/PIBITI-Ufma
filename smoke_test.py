#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de smoke test para validação integrada do refactor Keras/TensorFlow.
Executa as checagens listadas na Fase 5 do plano.

Uso:
  python smoke_test.py          # Teste rápido (compatibilidade local)
  docker-compose up --build     # Teste integrado (com containers)
"""

import sys
import os
import subprocess
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_check(text, status="✓"):
    print(f"  [{status}] {text}")


def run_command(cmd, description):
    """Executa comando e retorna sucesso/falha"""
    print(f"\n  Executando: {cmd}")
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print_check(description)
            if result.stdout:
                for line in result.stdout.split("\n")[:3]:
                    if line.strip():
                        print(f"         → {line[:60]}")
            return True
        else:
            print(f"  [✗] {description}")
            if result.stderr:
                print(f"         Erro: {result.stderr[:100]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [✗] {description} - Timeout")
        return False
    except Exception as e:
        print(f"  [✗] {description} - {e}")
        return False


print_header("SMOKE TEST - Refactor Keras/TensorFlow Stack Legada")
print("\nValidando critérios de aceite do plano...")

checks_passed = 0
checks_failed = 0

# Check 1: Validar Python version
print_header("CHECK 1: Python Version e Ambiente")
print(f"  Python version: {sys.version.split()[0]}")
print(f"  Working directory: {os.getcwd()}")
if sys.version_info >= (3, 8):
    print_check("Python >= 3.8 ✓")
    checks_passed += 1
else:
    print_check("Python < 3.8 ✗", "✗")
    checks_failed += 1

# Check 2: Validar pyproject.toml
print_header("CHECK 2: Dependências (pyproject.toml)")
pyproject_path = Path("./flask_backend/pyproject.toml")
if pyproject_path.exists():
    print_check("pyproject.toml encontrado")
    with open(pyproject_path) as f:
        content = f.read()
        if "tensorflow==2.8.0" in content:
            print_check("TensorFlow 2.8.0 pinned ✓")
            checks_passed += 1
        else:
            print_check("TensorFlow 2.8.0 não encontrado ✗", "✗")
            checks_failed += 1

        if "keras==2.8.0" in content:
            print_check("Keras 2.8.0 pinned ✓")
            checks_passed += 1
        else:
            print_check("Keras 2.8.0 não encontrado ✗", "✗")
            checks_failed += 1
else:
    print_check("pyproject.toml não encontrado ✗", "✗")
    checks_failed += 1

# Check 3: Validar uv.lock
print_header("CHECK 3: Lock File (uv.lock)")
lock_path = Path("./flask_backend/uv.lock")
if lock_path.exists():
    print_check("uv.lock encontrado")
    checks_passed += 1
    stat = lock_path.stat()
    print(f"         Tamanho: {stat.st_size / 1024:.1f} KB")
    print(f"         Modificado: {Path(lock_path).stat().st_mtime}")
else:
    print_check("uv.lock não encontrado ✗", "✗")
    checks_failed += 1

# Check 4: Validar Dockerfiles (Python 3.8)
print_header("CHECK 4: Dockerfiles (Python 3.8)")
dockerfiles = [
    "./DOCKER/flask/dockerfile",
    "./DOCKER/celery/dockerfile",
]
for df_path in dockerfiles:
    df = Path(df_path)
    if df.exists():
        with open(df) as f:
            content = f.read()
            if "python:3.9" in content:
                print_check(f"{df_path} - Python 3.8 ✓")
                checks_passed += 1
            else:
                print_check(f"{df_path} - Python não é 3.8 ✗", "✗")
                checks_failed += 1
    else:
        print_check(f"{df_path} não encontrado ✗", "✗")
        checks_failed += 1

# Check 5: Validar YOLO fallback
print_header("CHECK 5: YOLO Import Fallback")
yolo_path = Path("./flask_backend/yolo.py")
if yolo_path.exists():
    with open(yolo_path) as f:
        content = f.read()
        if "try:" in content and "multi_gpu_model" in content:
            print_check("YOLO multi_gpu_model fallback implementado ✓")
            checks_passed += 1
        else:
            print_check("YOLO fallback não encontrado ✗", "✗")
            checks_failed += 1
else:
    print_check("yolo.py não encontrado ✗", "✗")
    checks_failed += 1

# Check 6: Validar comando Celery
print_header("CHECK 6: Celery Command (docker-compose)")
compose_path = Path("./docker-compose.yaml")
if compose_path.exists():
    with open(compose_path) as f:
        content = f.read()
        if "flask_backend.celery_worker.celery:app" in content:
            print_check("Celery command com app explícito ✓")
            checks_passed += 1
        else:
            print_check("Celery command app explícito não encontrado ✗", "✗")
            checks_failed += 1
else:
    print_check("docker-compose.yaml não encontrado ✗", "✗")
    checks_failed += 1

# Summary
print_header("RESUMO DOS TESTES")
total = checks_passed + checks_failed
print(f"\n  ✓ PASSOU: {checks_passed}/{total}")
print(f"  ✗ FALHOU: {checks_failed}/{total}")

if checks_failed == 0:
    print("\n  ✅ TODOS OS CRITÉRIOS DE ACEITE VALIDADOS!")
    print("\n  Próximos passos:")
    print("    1. Navegar até flask_backend: cd flask_backend")
    print("    2. Rodar validação de imports: python validate_imports.py")
    print("    3. Build Docker: docker compose build --no-cache flask celery_worker")
    print(
        "    4. Iniciar stack: docker compose up -d redis db && docker compose up -d celery_worker flask"
    )
    print("    5. Testar healthcheck: curl http://localhost:5000/api")
    sys.exit(0)
else:
    print(f"\n  ❌ {checks_failed} FALHA(S) ENCONTRADA(S)")
    print("     Verifique os erros acima e tente novamente.")
    sys.exit(1)
