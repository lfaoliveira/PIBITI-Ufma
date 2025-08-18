from celery import Celery
import os

app = Celery(
    "celery",
    backend=os.environ["CELERY_RESULT_BACKEND"],
    broker=os.environ["CELERY_BROKER_URL"],
    include=["celery.tasks"],
)

if __name__ == "__main__":
    app.start()
