from celery import Celery
import os

app = Celery(
    "flask_backend",  # DEVE SER O NOME DA PASTA QUE ESTAO OS ARQUIVOS
    backend=os.environ["CELERY_RESULT_BACKEND"],
    broker=os.environ["CELERY_BROKER_URL"],
    include=["flask_backend.celery_worker.tasks"],  # <-- corrigido
)

app.autodiscover_tasks(["flask_backend.celery_worker"])


if __name__ == "__main__":
    app.start()
