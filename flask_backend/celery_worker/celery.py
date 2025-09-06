from celery import Celery
import os

app = Celery(
    "flask_backend",  # DEVE SER O NOME DA PASTA QUE ESTAO OS ARQUIVOS
    backend=os.environ["CELERY_RESULT_BACKEND"],
    broker=os.environ["CELERY_BROKER_URL"],
    include=["flask_backend.celery_worker.tasks"],  # <-- corrigido
)

app.autodiscover_tasks(["flask_backend.celery_worker"])

CELERY_CONFIG = {
    "worker_log_format": "[%(levelname)s/%(processName)s] %(message)s",
    "worker_task_log_format": "[%(levelname)s/%(processName)s] %(task_name)s[%(task_id)s]: %(message)s",
}
config_preparada = app.prepare_config(CELERY_CONFIG)
app.config_from_object(config_preparada)

if __name__ == "__main__":
    app.start()
