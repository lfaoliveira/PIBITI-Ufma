#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de validação de imports críticos do projeto.
Executa verificações de compatibilidade e estabilidade dos módulos principais.
Deve rodar em ambiente Docker ou local para validar stack legada.
"""

from pathlib import Path
import sys
import os


print("[VALIDATION] Iniciando validação de imports críticos...")
print(f"[VALIDATION] Python version: {sys.version}")
print(f"[VALIDATION] Working directory: {os.getcwd()}")

# ⭐ LOAD .ENV FIRST - antes de qualquer import de flask_backend!
print("\n[0/7] Carregando variáveis de ambiente (.env)...")
try:
    from dotenv import load_dotenv

    env_loaded = False
    env_file = Path("flask_backend", ".env")

    if os.path.exists(env_file):
        dotenv_path = os.path.abspath(env_file)
        load_dotenv(dotenv_path)
        print(f"  ✓ .env carregado de: {env_file}")
        env_loaded = True

    if not env_loaded:
        print("  ⚠ Nenhum arquivo .env encontrado (será usado variáveis do sistema)")
        exit(1)
except Exception as e:
    print(f"  ⚠ Aviso ao carregar .env: {e}")

errors = []
warnings = []

# Test 1: TensorFlow e Keras
print("\n[1/6] Testando TensorFlow/Keras...")
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
print("\n[2/6] Testando YOLO multi_gpu_model fallback...")
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
print("\n[3/6] Testando Flask...")
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
print("\n[4/6] Testando Celery...")
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
print("\n[5/6] Testando módulos core...")
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


# Test 6: YOLO initialization test (sem modelo)
print("\n[6/6] Testando estrutura YOLO...")
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
