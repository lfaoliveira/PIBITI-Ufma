import numpy as np
from flask import Flask, render_template, jsonify, request, send_from_directory
import requests
import os

#  from yolo import YOLO

from analise import AnaliseParalisia
import time

# path para arquivos temporarios

PATH_TEMP = os.path.join(os.getcwd(), "TEMP")
video_demo = os.path.join(os.getcwd(), "demoInput.mp4")

kwargs = {
    "model_path": "trained_weights_final.h5",
    "anchors_path": "yolo_anchors.txt",
    "classes_path": "classes.txt",
    "score": 0.3,
    "iou": 0.45,
    "model_image_size": (416, 416),
    "gpu_num": 1,
}
# OBS: MODELO DEVE TER FUNCAO detect_image implementada
# modelo = YOLO(**kwargs)

# analisador = AnaliseParalisia(modelo, PATH_TEMP)
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello Wrold"


# Rota que recupera arquivos da pasta "assets"
@app.route("/assets/<path:path>")
def send_assets(path):
    print("ARQUIVO!" + str(path))
    return send_from_directory("assets", path)


# ROTA PRINCIPAL que mostra a página "resultado.html"
@app.route("/analise", methods=["POST"])
def analisar(videoInput):
    """
    Pega video de input, executa método e retorna resultado como requisicao HTTP
    """
    # timestamp do momento em que o servidor foi chamado

    timestamp = time.gmtime()
    resultado, path_graf = analisador.funcao_metodo(
        videoInput, f"{timestamp}.mp4", timestamp
    )
    # servidor retorna string contando os resultados e grafico como respsotas HTTP
    return


@app.route("/demo", methods=["POST"])
def demo_func():
    """
    Pega video de demonstracao do servidor, finge processamento e retorna resultados
    """
    analisar(video_demo)
    # servidor retorna string contando os resultados e grafico como respsotas HTTP
    return


if __name__ == "__main__":
    # para poder adicionar um sheduler de tasks de background,
    # adicionar use_reloader=False
    app.run(debug=True)
