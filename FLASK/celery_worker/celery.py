from celery import Celery
import os

app = Celery(
    "celery_worker",  # DEVE SER O NOME DA PASTA QUE ESTAO OS ARQUIVOS
    backend=os.environ["CELERY_RESULT_BACKEND"],
    broker=os.environ["CELERY_BROKER_URL"],
    include=["celery_worker.tasks"],  # pasta.tasks
)

if __name__ == "__main__":
    app.start()
