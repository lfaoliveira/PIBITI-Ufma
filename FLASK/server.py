import time
from analise import AnaliseParalisia
from yolo import YOLO
import base64
import os
from werkzeug.utils import secure_filename
import numpy as np
from flask import Flask, render_template, jsonify, request, send_from_directory, url_for, abort

from flask_pymongo import PyMongo
import hashlib

from flask_cors import CORS
from tensorflow.python.framework.ops import disable_eager_execution
import tensorflow as tf
import threading
import logging
import ffmpeg


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


def converter_arq(input: str, output: str):
    """
    Converte video de input em .mp4 
    """
    print(f"Converting {input} to {output}")
    stream = ffmpeg.input(input)
    stream = ffmpeg.output(stream, output, vcodec='libx264', acodec='aac')
    print(stream, "\n\n")
    # Execute the conversion
    ffmpeg.run(stream)
    return output


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
def predict(analisador: AnaliseParalisia, path_processamento_arq, path_out, timestamp):
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
app.config["MONGO_URI"] = "mongodb://localhost:27017/PARALISIA6_NERVO"
mongo = PyMongo(app)
alg_hash = hashlib.sha3_256

print("APP INICIADO")
# path para arquivos temporarios

os.makedirs("tmp", exist_ok=True)

PATH_PIBITI = os.getcwd()
PATH_FLASK = os.path.join(PATH_PIBITI, "FLASK")

if "WKDIR" not in app.config.keys():
    app.config["WKDIR"] = PATH_FLASK
if "PIBITI" == os.path.basename(PATH_PIBITI):
    os.chdir(app.config["WKDIR"])


app.config["WKDIR"] = os.getcwd()
print(f"\nHOME: {app.config['WKDIR']}\n\n")

path_pesos_yolo = os.path.join(app.config["WKDIR"], "trained_weights_final.h5")
if not os.path.exists(path_pesos_yolo):
    download_peso(app.config["WKDIR"])

app.config["TEMP_FOLDER"] = os.path.join(app.config["WKDIR"], "tmp")
video_demo = os.path.join(app.config["WKDIR"], "demoInput.mp4")

# --------------------- MODELO --------------------------#

modelo = get_modelo()
# OBS: MODELO DEVE TER FUNCAO detect_image implementada
analisador = AnaliseParalisia(modelo, app.config["TEMP_FOLDER"])


@app.route("/")
def index():
    return "Hello World"


@app.route('/get-file/<filename>', methods=['GET'])
def get_file(filename):
    """
    Serves files from the /tmp directory.
    """
    print("filename: ", filename)
    try:
        file_path = os.path.join(app.config["TEMP_FOLDER"], filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404

        # Generate the URL for the file
        file_url = url_for('serve_file', filename=filename, _external=True)

        return jsonify({"file_url": file_url}), 200
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/serve-file/<filename>', methods=['GET'])
def serve_file(filename):
    """
    Serves the file when the generated URL is accessed.
    """
    try:
        return send_from_directory(app.config["TEMP_FOLDER"], filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

# TODO: utilizar Gunicorn pra spawn de novas threads no servidor Flask (talvez seja desnecessario por conta do Kubernetes)


@app.route("/analise", methods=["POST"])
def analisar():
    """
    Takes video  input, executa the model e and returns result as JSON
    """
    timestamp = time.time()

    arq = request.files["file"]

    # user = request.args.get("user")
    user = "TESTE"
    ext = allowed_file(str(arq.filename))
    if ext is None:
        print("Incorrect file type!\n\n")
        return SystemError

    nome_local = f"{user}_{str(round(timestamp, 4))}.{ext}"
    filename_local = secure_filename(f"INPUT_{nome_local}")

    # video deve ser armazenado usando ID do usuario e timestamp, pra garantir multiplicidade
    path_processamento_arq = os.path.join(
        app.config["TEMP_FOLDER"], filename_local)
    arq.save(path_processamento_arq)

    """ se eu nao me engano, logica utilizada para fazer streaming de arquivos grandes
    arq_stream = arq.stream"""

    EXT_OUT = "mp4"
    nome_local = f"{user}_{str(round(timestamp, 4))}.{EXT_OUT}"
    path_convert = os.path.join(
        app.config["TEMP_FOLDER"], f"CONVERT_{nome_local}")

    path_processamento_arq = converter_arq(
        path_processamento_arq, path_convert)

    nome_local = f"{user}_{str(round(timestamp, 4))}.{EXT_OUT}"
    path_out_pre = os.path.join(
        app.config["TEMP_FOLDER"], f"OUT_PRE_{nome_local}")

    # executando predicao
    res_tensor, graf_tensor = predict(
        analisador, path_processamento_arq, path_out_pre, timestamp
    )
    with tf.compat.v1.Session() as sess:
        # Run the session to get the tensor's value
        res_np = sess.run(res_tensor)
        graf_np = sess.run(graf_tensor)
    # Decode bytes to string since predict returns all output as tensor
    str_res, path_graf = res_np.decode('utf-8'), graf_np.decode('utf-8')

    path_out = os.path.join(app.config["TEMP_FOLDER"], f"OUT_{nome_local}")

    path_out = converter_arq(
        path_out_pre, path_out)

    os.remove(path_out_pre)
    os.remove(path_convert)
    """ with open(path_out, "rb") as file:
        video_base64 = base64.b64encode(file.read()).decode('utf-8')

    with open(path_graf, "rb") as file:
        grafico_base64 = base64.b64encode(file.read()).decode('utf-8') """

    resposta_json = get_file(os.path.basename(path_graf))[0].get_json()
    path_graf = resposta_json["file_url"]

    resposta_json = get_file(os.path.basename(path_out))[0].get_json()
    path_out = resposta_json["file_url"]

    result = {"string": str_res, "grafico": path_graf,
              "video": path_out, "extVideo": EXT_OUT}
    # servidor DEVE retorna JSON com string contendo as métricas, VIDEO DE SAIDA e grafico

    return jsonify(result)


@app.route("/demo", methods=["POST"])
def demo_func():
    """
    Pega video de demonstracao do servidor, finge processamento e retorna resultados
    """
    return analisar(video_demo)
    # servidor retorna string contando os resultados e grafico como respsotas HTTP


@app.route("/cadastro", methods=["POST"])
def cad_func():
    dict_valores = request.form.to_dict()
    email = dict_valores["email"]
    nome = dict_valores["nome"]
    crm = dict_valores["crm"]
    senha_utf8 = dict_valores["senha"].encode('utf-8')
    senha = alg_hash(senha_utf8).hexdigest()

    medicos = mongo.db.get_collection("Medicos")
    res = medicos.find_one({"email": email})
    if res != None:
        return "JA_EXISTE"

    # print(f"\n\nVALORES CAD: {email, senha, nome, crm}\n\n")

    medicos.insert_one({"email": email, "nome": nome,
                       "crm": crm, "senha": senha})
    return "CADASTRADO"


@app.route("/val_login", methods=["GET"])
def val_login():
    """
    Validates user registration by checking email and password from form submission.
    Gets email and password values from submitted form data to process user registration.
    Returns:
        None
    Raises:
        None
    """
    email, senha = request.form.get("email"), request.form.get("senha")
    senha = alg_hash(senha.encode('utf-8')).hexdigest()
    medicos = mongo.db.get_collection("Medicos")
    res = medicos.find_one({"email": email, "senha": senha})
    if res != None:
        return "OK"
    else:
        raise ValueError("Email e/ou Senha incorreto(s)!")


if __name__ == "__main__":
    # para poder adicionar um sheduler de tasks de background,
    # adicionar use_reloader=False
    app.run(debug=True, threaded=False)
