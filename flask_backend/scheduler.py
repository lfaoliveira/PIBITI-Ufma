# Classe de scheduler que vai organizar threads de CPU e utilizacao de GPU

# utilizar Gunicorn pra spawn de novas threads no servidor Flask (talvez seja desnecessario por conta do Kubernetes)
# utilizar kubernetes pra criar 1 container por requisicao


class Scheduler:
    def __init__(self):
        self.fila_jobs = []
