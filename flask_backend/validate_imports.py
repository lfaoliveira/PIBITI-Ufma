#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de validação de imports críticos do projeto.
Executa verificações de compatibilidade e estabilidade dos módulos principais.
Deve rodar em ambiente Docker ou local para validar stack legada.
"""

import sys
import os

print("[VALIDATION] Iniciando validação de imports críticos...")
print(f"[VALIDATION] Python version: {sys.version}")
print(f"[VALIDATION] Working directory: {os.getcwd()}")

errors = []
warnings = []

# Test 1: TensorFlow e Keras
print("\n[1/7] Testando TensorFlow/Keras...")
try:
    import tensorflow as tf

    print(f"  ✓ TensorFlow {tf.__version__}")

    from keras import backend as K

    print(f"  ✓ Keras backend: {K.backend()}")

    from keras.models import load_model
    from keras.layers import Input

    print("  ✓ Keras utils (load_model, Input)")
except Exception as e:
    errors.append(f"TensorFlow/Keras: {e}")
    print(f"  ✗ Erro: {e}")

# Test 2: YOLO multi_gpu fallback
print("\n[2/7] Testando YOLO multi_gpu_model fallback...")
try:
    try:
        from tensorflow.python.keras.utils.multi_gpu_utils import multi_gpu_model

        print("  ✓ multi_gpu_model disponível (API nativa)")
    except (ImportError, AttributeError):
        print("  ⚠ multi_gpu_model não disponível - será usado fallback")
        warnings.append("multi_gpu_model não disponível - fallback ativado")
except Exception as e:
    errors.append(f"YOLO multi_gpu fallback: {e}")
    print(f"  ✗ Erro: {e}")

# Test 3: Flask setup
print("\n[3/7] Testando Flask...")
try:
    from flask import Flask

    print(f"  ✓ Flask importado com sucesso")

    # Test basic app instantiation
    app = Flask("test")
    print("  ✓ Flask app instantiação funciona")
except Exception as e:
    errors.append(f"Flask: {e}")
    print(f"  ✗ Erro: {e}")

# Test 4: Celery setup
print("\n[4/7] Testando Celery...")
try:
    # Set up environment variables se não estiverem definidas
    if "CELERY_BROKER_URL" not in os.environ:
        os.environ["CELERY_BROKER_URL"] = "redis://redis:6379/0"
    if "CELERY_RESULT_BACKEND" not in os.environ:
        os.environ["CELERY_RESULT_BACKEND"] = "redis://redis:6379/0"

    from flask_backend.celery_worker.celery import app as celery_app

    print(f"  ✓ Celery app importado: {celery_app.main}")
    print(f"  ✓ Broker: {celery_app.conf.broker_url}")
except Exception as e:
    warnings.append(f"Celery: {e} (pode ser esperado se Redis não está disponível)")
    print(f"  ⚠ Aviso: {e}")

# Test 5: Core modules
print("\n[5/7] Testando módulos core...")
try:
    import numpy as np

    print(f"  ✓ NumPy {np.__version__}")

    import cv2

    print(f"  ✓ OpenCV {cv2.__version__}")

    from PIL import Image

    print("  ✓ Pillow")

    import pandas as pd

    print(f"  ✓ Pandas {pd.__version__}")
except Exception as e:
    errors.append(f"Core modules: {e}")
    print(f"  ✗ Erro: {e}")


# Test 6: Environment variables (.env)
print("\n[6/7] Testando carregamento de variáveis de ambiente (.env)...")
try:
    from dotenv import load_dotenv

    # Try to load .env from current directory or parent
    env_loaded = False
    env_files = [".env", "../.env", "../../.env"]

    for env_file in env_files:
        if os.path.exists(env_file):
            dotenv_path = os.path.abspath(env_file)
            load_dotenv(dotenv_path)
            print(f"  ✓ .env carregado de: {env_file}")
            env_loaded = True
            break

    if not env_loaded:
        print("  ⚠ Nenhum arquivo .env encontrado (esperado em produção)")
        warnings.append(".env não encontrado - usar variáveis de ambiente do sistema")

    # Check critical env vars
    critical_vars = ["CELERY_BROKER_URL", "CELERY_RESULT_BACKEND", "MONGO_URI"]
    missing_vars = []

    for var in critical_vars:
        if var in os.environ:
            print(f"     • {var}: carregado ✓")
        else:
            missing_vars.append(var)

    if missing_vars:
        warnings.append(f"Variáveis de ambiente ausentes: {', '.join(missing_vars)}")
        print(f"  ⚠ Variáveis não definidas: {', '.join(missing_vars)}")

except Exception as e:
    errors.append(f"Environment (.env): {e}")
    print(f"  ✗ Erro: {e}")


# Test 7: YOLO initialization test (sem modelo)
print("\n[7/7] Testando estrutura YOLO...")
try:
    from flask_backend.yolo3.model import yolo_body, tiny_yolo_body

    print("  ✓ YOLO model builders importados")

    from flask_backend.yolo3.utils import letterbox_image

    print("  ✓ YOLO utils importados")
except Exception as e:
    errors.append(f"YOLO structure: {e}")
    import traceback

    print(f"  ✗ Erro: {e}, {traceback.print_exc()}")


# Summary
print("\n" + "=" * 60)
print("RESUMO DA VALIDAÇÃO")
print("=" * 60)

if errors:
    print(f"\n❌ {len(errors)} erro(s) crítico(s) encontrado(s):")
    for i, error in enumerate(errors, 1):
        print(f"   {i}. {error}")
    sys.exit(1)
else:
    print("\n✅ Todos os imports críticos validados com sucesso!")

if warnings:
    print(f"\n⚠️  {len(warnings)} aviso(s):")
    for i, warning in enumerate(warnings, 1):
        print(f"   {i}. {warning}")

print("\n[OK] Validação completa. Stack legada está estável para uso.")
sys.exit(0)
