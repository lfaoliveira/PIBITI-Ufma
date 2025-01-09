import numpy as np
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS

import requests
from werkzeug.utils import secure_filename
import os
import sys
from yolo import YOLO
from analise import AnaliseParalisia
import time
import glob
import zipfile
import h5py


def uniao_pesos(extract_dir, nome_base, testar=True):
    """
    Une partes dos pesos em 1 unico arquivo zip e depois concatena e extrai em um arquivo .h5
    `extract_dir`: diretorio onde pesos vao ser extraidos. Cria se nao houver
    `nome_base`: nome no estilo 'myfile.zip.'
    `testar`: bool, se deve testar integridade do arquivo ou nao

    Retorna `output_file`, path dos pesos finais
    """

    zip_prefix = f"trained_weights_final.zip."
    parts = glob.glob(zip_prefix + "*")
    n = len(parts)

    # Directory to extract files
    os.makedirs(extract_dir, exist_ok=True)
    path_zip_completo = os.path.join(extract_dir, nome_base)

    # Concatena partes em um unico arquivo
    with open(path_zip_completo, "wb") as outfile:
        for i in range(1, n + 1):
            filename = f"{zip_prefix}{str(i).zfill(3)}"
            # essa parte le parte do zip e escreve no zip total
            with open(filename, "rb") as infile:
                outfile.write(infile.read())

    # Extract
    with zipfile.ZipFile(path_zip_completo, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    if testar:

        try:
            with h5py.File(output_file, "r") as h5file:
                print("File reconstructed successfully and is readable.")
        except Exception as e:
            print(f"An error occurred: {e}")

    output_file = path_zip_completo.replace("zip", "h5")
    return output_file
    # print(output_file, "\n\n")


# quando partir pra deploy, rodar servidor usando bash pra garantir cwd correto
# TODO: ou seja, trocar esse path absoluto
PATH_PIBITI = os.path.join("C:\\", "Users", "Eu", "Desktop", "PIBITI")

# path para arquivos temporarios
PATH_FLASK = os.path.join(PATH_PIBITI, "FLASK")

if not os.getcwd() == PATH_FLASK:
    os.chdir(PATH_FLASK)

path_pesos_yolo = os.path.join(PATH_FLASK, "trained_weights_final.h5")
if not os.path.exists(path_pesos_yolo):
    uniao_pesos(os.getcwd(), "trained_weights_final.zip")

video_demo = os.path.join(os.getcwd(), "demoInput.mp4")

app = Flask(__name__)
"""ALERTA!!!!!!!!!! somente usar isso em producao, ja que isso habilita requisicoes de qualquer origem
Possível risco de segurança!
"""
CORS(app)

app.config["UPLOAD_FOLDER"] = "tmp"
os.makedirs("tmp", exist_ok=True)

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
modelo = YOLO(**kwargs)
analisador = AnaliseParalisia(modelo, app.config["UPLOAD_FOLDER"])

ALLOWED_EXTENSIONS = ["mpg", "mpeg", "webm", "mkv", "ogv", "ogg", "mp4"]


def allowed_file(filename: str):
    for ext in ALLOWED_EXTENSIONS:
        if filename.endswith(ext):
            return ext
    return None


@app.route("/")
def index():
    # send_assets("/assets/style.css")
    return "Hello World"


# Rota que recupera arquivos da pasta "assets"
@app.route("/assets/<path:path>")
def send_assets(path):
    print("ARQUIVO!" + str(path))
    return send_from_directory("assets", path)


# TODO: utilizar Gunicorn pra spawn de novas threads no servidor Flask (talvez seja desnecessario por conta do Kubernetes)
# TODO: utilizar kubernetes pra criar 1 container por requisicao
@app.route("/analise", methods=["POST"])
def analisar():
    """
    Pega video de input, executa método e retorna resultado como requisicao HTTP
    """
    # timestamp do momento em que o servidor foi chamado

    timestamp = time.time()
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
    path_processamento_arq = os.path.join(app.config["UPLOAD_FOLDER"], filename_local)
    save = True
    if save:
        arq.save(path_processamento_arq)

    # se eu nao me engano, logica utilizada para fazer streaming de arquivos grandes
    """arq_stream = arq.stream"""
    path_out = os.path.join(app.config["UPLOAD_FOLDER"], f"OUT_{nome_local}")
    str_res, path_graf = analisador.funcao_metodo(
        path_processamento_arq, path_out, timestamp
    )

    videoOut = open(path_out, "r")
    grafico = open(path_graf, "r")
    result = {"string": str_res, "grafico": grafico, "video": videoOut}
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
    app.run(debug=True)
