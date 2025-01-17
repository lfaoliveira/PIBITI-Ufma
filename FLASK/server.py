import time
from analise import AnaliseParalisia
from yolo import YOLO
import base64
import os
from werkzeug.utils import secure_filename
import numpy as np
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
from tensorflow.python.framework.ops import disable_eager_execution
import tensorflow as tf
import threading
import logging

# disable_eager_execution()


"""import tensorflow as tf
from keras.models import load_model

global graph
graph = tf.get_default_graph()"""


def download_peso(PATH_FLASK):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    import io

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    PATH_CRED = os.path.join(PATH_FLASK, "permalink-modelo.json")
    credentials = service_account.Credentials.from_service_account_file(
        PATH_CRED, scopes=SCOPES
    )

    service = build("drive", "v3", credentials=credentials)
    file_id = "10hdULWG2n7F8jjUbebcB2lMeiUUnh6rq"
    file_name = "trained_weights_final.h5"

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, "wb")
    downloader = MediaIoBaseDownload(fh, request, chunksize=1024 * 1024)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")


def count_active_threads():
    return len(threading.enumerate())


def allowed_file(filename: str):
    ALLOWED_EXTENSIONS = ["mpg", "mpeg", "webm",
                          "mkv", "ogv", "ogg", "mp4", "avi"]
    for ext in ALLOWED_EXTENSIONS:
        if filename.endswith(ext):
            return ext
    return None


def get_modelo():
    kwargs = {
        "model_path": "trained_weights_final.h5",
        "anchors_path": "yolo_anchors.txt",
        "classes_path": "classes.txt",
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "gpu_num": 1,
    }
    modelo = YOLO(**kwargs)
    return modelo

@tf.function
def predict(analisador:AnaliseParalisia, path_processamento_arq, path_out, timestamp):
    modelo = analisador.modelo
    with modelo.sess.graph.as_default():
        str_res, path_graf = analisador.funcao_metodo(
            path_processamento_arq, path_out, timestamp
        )
        return str_res, path_graf


# ------------- VARIAVEIS GLOBAIS--------------#


app = Flask(__name__)
"""ALERTA!!!!!!!!!! somente usar isso em producao, ja que isso habilita requisicoes de qualquer origem
Possível risco de segurança!
"""
CORS(app)

print("APP INICIADO")
# path para arquivos temporarios
app.config["TEMP_FOLDER"] = "tmp"
os.makedirs("tmp", exist_ok=True)

PATH_PIBITI = os.getcwd()
PATH_FLASK = os.path.join(PATH_PIBITI, "FLASK")

if "WKDIR" not in app.config.keys():
    app.config["WKDIR"] = PATH_FLASK
if "PIBITI" == os.path.basename(PATH_PIBITI):
    os.chdir(app.config["WKDIR"])


app.config["WKDIR"] = os.getcwd()
print(f"\nHOME: { os.getcwd()}\n\n")

path_pesos_yolo = os.path.join(app.config["WKDIR"], "trained_weights_final.h5")
if not os.path.exists(path_pesos_yolo):
    download_peso(app.config["WKDIR"])

video_demo = os.path.join(app.config["WKDIR"], "demoInput.mp4")

# --------------------- MODELO --------------------------#

modelo = get_modelo()
# OBS: MODELO DEVE TER FUNCAO detect_image implementada
analisador = AnaliseParalisia(modelo, app.config["TEMP_FOLDER"])

@app.route("/")
def index():
    # send_assets("/assets/style.css")
    return "Hello World"


@app.before_request
def before_request():
    logging.info(f"Before request: {count_active_threads()} active threads.")


@app.after_request
def after_request(response):
    logging.info(f"After request: {count_active_threads()} active threads.")
    return response


# Rota que recupera arquivos da pasta "assets"
@app.route("/assets/<path:path>")
def send_assets(path):
    print("ARQUIVO!" + str(path))
    return send_from_directory("assets", path)


# TODO: utilizar Gunicorn pra spawn de novas threads no servidor Flask (talvez seja desnecessario por conta do Kubernetes)
# TODO: utilizar kubernetes pra criar 1 container por requisicao (provavelmente desnecessario ja que Flask cria 1 thread por req.)
@app.route("/analise", methods=["POST"])
def analisar():
    """
    Pega video de input, executa método e retorna resultado como requisicao HTTP
    """
    timestamp = time.time()
    print(f"\nTHREADS: {count_active_threads()}\n\n")
    # timestamp do momento em que o servidor foi chamado
    """ resultado, path_graf = analisador.funcao_metodo(
        videoInput, f"{timestamp}.mp4", timestamp
    ) """
    arq = request.files["file"]
    # user = request.args.get("user")
    user = "EU"
    ext = allowed_file(str(arq.filename))
    if ext is None:
        print("Tipo incorreto de arq!\n\n")
        return SystemError

    nome_local = f"{user}_{str(round(timestamp, 4))}.{ext}"
    filename_local = secure_filename(f"INPUT_{nome_local}")
    # video deve ser armazenado usando ID do usuario e timestamp, pra garantir multiplicidade
    path_processamento_arq = os.path.join(
        app.config["TEMP_FOLDER"], filename_local)
    save = True
    if save:
        arq.save(path_processamento_arq)

    # se eu nao me engano, logica utilizada para fazer streaming de arquivos grandes
    """arq_stream = arq.stream"""
    path_out = os.path.join(app.config["TEMP_FOLDER"], f"OUT_{nome_local}")

    res_tensor, graf_tensor = predict(
        analisador, path_processamento_arq, path_out, timestamp
    )
    with tf.compat.v1.Session() as sess:
        # Run the session to get the tensor's value
        res_np = sess.run(res_tensor)
        graf_np = sess.run(graf_tensor)
    # Decode bytes to string since predict returns all output as tensor
    str_res, path_graf = res_np.decode('utf-8'), graf_np.decode('utf-8')

    with open(path_out, "rb") as file:
        video_base64 = base64.b64encode(file.read()).decode('utf-8')

    with open(path_graf, "rb") as file:
        grafico_base64 = base64.b64encode(file.read()).decode('utf-8')

    result = {"string": str_res, "grafico": grafico_base64, "video": video_base64}
    # servidor DEVE retorna JSON com string contendo as métricas, VIDEO DE SAIDA e grafico
    return jsonify(result)


@app.route("/demo", methods=["POST"])
def demo_func():
    """
    Pega video de demonstracao do servidor, finge processamento e retorna resultados
    """
    return analisar(video_demo)
    # servidor retorna string contando os resultados e grafico como respsotas HTTP


if __name__ == "__main__":
    # para poder adicionar um sheduler de tasks de background,
    # adicionar use_reloader=False
    app.run(debug=True, threaded=False)
