from http.client import BAD_GATEWAY, BAD_REQUEST, INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
import time
from typing import Collection

from bson import ObjectId
from flask.sessions import SessionMixin
from flask_mail import Mail
from analise import AnaliseParalisia
from yolo import YOLO
import os
from werkzeug.utils import secure_filename
from flask import Flask, make_response, render_template, session, jsonify, request, send_from_directory, url_for, abort
from flask_session import Session

from flask_pymongo import PyMongo
import hashlib
from datetime import timedelta

from flask_cors import CORS, cross_origin
from tensorflow.python.framework.ops import disable_eager_execution
import tensorflow as tf
import threading

import ffmpeg
import requests
import csv


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
        if filename.lower().endswith(ext):
            return ext
    return None


def converter_arq(input: str, output: str):
    """
    Converte video de input em .mp4 
    """
    if not os.path.exists(input):
        raise FileNotFoundError(f"Input file not found: {input}")

    print(f"Converting {input} to {output}")
    stream = ffmpeg.input(input)
    stream = ffmpeg.output(stream, output, vcodec='libx264', acodec='aac')
    print(stream, "\n\n")
    try:
        # Execute the conversion
        ffmpeg.run(stream, cmd='ffmpeg')
        return output
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))


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


def find_user_with_session_mongo(session: SessionMixin, collection):
    return collection.find_one({"_id": ObjectId(session['user_id'])})


# ------------- VARIAVEIS GLOBAIS--------------#
DIAGS = "Diagnosticos"
MEDICOS = "Medicos"

# Read environment variables from CSV
arq_config = "../env.csv"
try:
    with open(arq_config, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:  # Ensure row has key and value
                key, value = row[0], row[1]
                os.environ[key] = value
except FileNotFoundError:
    print(f"Warning: Config file {arq_config} not found")
except Exception as e:
    print(f"{e}")


app = Flask(__name__)
app.config.from_object(__name__)

"""ALERTA!!!!!!!!!! somente usar CORS em producao, ja que isso habilita requisicoes de qualquer origem
Possível risco de segurança!
"""

app.config["MONGO_URI"] = "mongodb://localhost:27017/PARALISIA6_NERVO"
app.config["SESSION_TYPE"] = "filesystem"
mongo = PyMongo(app)

# SEGURANÇA
app.secret_key = os.environ.get('SECRET_KEY')
alg_hash = hashlib.sha3_256

# TODO: MUDAR SEGURANCÇA DOS COOKIES QUANO FOR PRO DEPLOY
"""-------CONFIGS DE SESSAO---------------"""
app.config.update(
    SESSION_COOKIE_SECURE=True,  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)
)
Session(app)
# CONFIGS DE EMAIL
app.config.update(
    MAIL_SERVER=os.environ.get('MAIL_SERVER', 'smtp.example.com'),
    MAIL_PORT=int(os.environ.get('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true',
    MAIL_USE_SSL=os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true',
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER')
)

mail = Mail(app)
CORS(app, supports_credentials=True)
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
    print(" NÃO REINICIE O SERVIDOR!!!!!!!\nBaixando pesos do modelo YOLOv3...")
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


def get_pdf() -> str:
    # FUNCAO QUE DEVE PEGAR DADOS DO DIAGNOSTICO E RETORNAR URL EXTERNA DO PDF
    pass


@app.route("/analise", methods=["POST"])
@cross_origin(supports_credentials=True)
def analisar():
    import base64

    """
    Takes video  input, executa the model e and returns result as JSON
    """
    timestamp = time.time()
    id_diag = request.form.get("id_diag", None)
    filename = request.form.get("filename", None)
    diag = None

    if id_diag != None:
        print(request.form)
        diag = mongo.db.get_collection(
            DIAGS).find_one({"_id": ObjectId(id_diag)})
    else:
        return make_response("INPUT NULO!", BAD_REQUEST)
    # VERSÃO LOGADO
    if "user_id" in session:
        user = session["user_id"]
    else:
        user = "TEMP"
    ext = allowed_file(filename)
    if ext is None:
        print("Incorrect file type!\n\n")
        return SystemError

    nome_video = f"{user}_{str(round(timestamp, 4))}"
    nome_local = f"{nome_video}.{ext}"
    filename_arq_input = secure_filename(f"INPUT_{nome_local}")

    # video deve ser armazenado usando ID do usuario e timestamp, pra garantir multiplicidade
    path_arq_input = os.path.join(
        app.config["TEMP_FOLDER"], filename_arq_input)

    with open(path_arq_input, 'wb') as f:
        video_base64 = diag["videoLabel"]
        video_bin = base64.b64decode(video_base64, validate=True)
        f.write(video_bin)

    """ se eu nao me engano, logica utilizada para fazer streaming de arquivos grandes
    arq_stream = arq.stream"""

    EXT_OUT = "mp4"
    nome_local = f"{nome_video}.{EXT_OUT}"
    # path cujo unico proposito eh servir de temporario pras conversoes de video
    path_aux_conv = os.path.join(
        app.config["TEMP_FOLDER"], f"CONVERT_{nome_local}")

    path_arq_input_conv = converter_arq(
        path_arq_input, path_aux_conv)
    print("\nDEPOIS PRIMEIRA CONV\n")
    nome_local = f"{nome_video}.{EXT_OUT}"
    path_out_antes_conv = os.path.join(
        app.config["TEMP_FOLDER"], f"OUT_PRE_{nome_local}")

    # executando predicao
    res_tensor, graf_tensor = predict(
        analisador, path_arq_input_conv, path_out_antes_conv, timestamp
    )

    with tf.compat.v1.Session() as sess:
        # Run the session to get the tensor's value
        res_np = sess.run(res_tensor)
        if "ERRO" in res_np.decode('utf-8'):
            return make_response(res_np, BAD_REQUEST)
        graf_np = sess.run(graf_tensor)
    # Decode bytes to string since predict returns all output as tensor
    str_res, path_graf = res_np.decode('utf-8'), graf_np.decode('utf-8')

    path_out = os.path.join(app.config["TEMP_FOLDER"], f"OUT_{nome_local}")
    print("ULTIMA CONVERSAO")
    path_out = converter_arq(
        path_out_antes_conv, path_out)

    # Remover APENAS arquivos auxiliares
    os.remove(path_out_antes_conv)
    os.remove(path_aux_conv)
    """ with open(path_out, "rb") as file:
        video_base64 = base64.b64encode(file.read()).decode('utf-8')

    with open(path_graf, "rb") as file:
        grafico_base64 = base64.b64encode(file.read()).decode('utf-8') """

    url_pdf = get_pdf()

    print("PEGANDO URLS")

    resposta_json = get_file(os.path.basename(path_graf))[0].get_json()
    url_graf = resposta_json["file_url"]

    resposta_json = get_file(os.path.basename(path_out))[0].get_json()
    url_video_out = resposta_json["file_url"]
    olho_doente = str_res.split(",")[3]

    if olho_doente == "Esquerdo":
        str_diag = "true+false"
    elif olho_doente == "Direito":
        str_diag = "false+true"
    else:
        str_diag = "false+false"

    result = {"diagAutom": str_diag, "grafico": url_graf, "pdf": url_pdf,
              "dataDiag": timestamp, "video": url_video_out, "ultimaModif": timestamp}
    mongo.db.get_collection(DIAGS).update_one(
        {"_id": ObjectId(id_diag)},
        {"$set": result}
    )

    result["diagAutom"] = str_res
    # servidor DEVE retorna JSON com string contendo as métricas, pdf de res, VIDEO DE SAIDA e grafico
    return jsonify(result)


@app.route("/pega_perfil", methods=["GET"])
@cross_origin(supports_credentials=True)
def pega_perfil():
    dados_diag = [
        "nomePaciente",
        "diagMedico",
        "diagAutom",
        "desc",
        "dataDiag",
        "ultimaModif",
        "linkRelatorio",
    ]
    medicos = mongo.db.get_collection(MEDICOS)
    usuario = find_user_with_session_mongo(session, medicos)


@app.route("/envia_diag", methods=["POST"])
@cross_origin(supports_credentials=True)
def envia_diag():
    video = request.files.get("video", None)
    # Convert video to base64
    # TODO: MONGO TEM LIMITE DE ARMAZENAMENTO DE 16MB. PRA ARQUIVOS MAIORES USAR GOOGLE DRIVE
    import base64
    video_data = video.read()
    video_b64 = base64.b64encode(video_data)
    nomePaciente = request.form.get("nomePaciente", None)
    stringOlhos = request.form.get("stringOlhos", None)

    desc = request.form.get("desc", None)
    a = [video, nomePaciente]
    if any(elem is None for elem in a):
        return make_response("INPUT NULO!", BAD_REQUEST)

    filename = video.filename
    diagnosticoMedico = stringOlhos
    response = requests.get(
        url_for('val_login', _external=True),
        cookies=request.cookies
    )

    if response.text == 'True':
        # caso pra usuario logado
        id_medico = session['user_id']
        medicos = mongo.db.get_collection(MEDICOS)
        medico_atual = medicos.find_one({"_id": ObjectId(id_medico)})
        nomeMedico = medico_atual.get("nome") if medico_atual else None
        if nomeMedico is None:
            return make_response("MEDICO LOGADO NAO ENCONTRADO", INTERNAL_SERVER_ERROR)
    else:
        id_medico = None

    diags = mongo.db.get_collection(DIAGS)
    dados = {"videoLabel": video_b64, "nomePaciente": nomePaciente, "id_medico": id_medico,
             "diagnosticoMedico": diagnosticoMedico, "desc": desc}
    for key, value in dados.items():
        if value is None:
            dados[key] = "None"

    result = diags.insert_one(dados)
    id_diag = str(result.inserted_id)
    if result.acknowledged:
        return make_response({"mensagem": "CARREGADO", "id_diag": id_diag, "filename": filename}, OK)
    else:
        return make_response("Erro ao registrar diagnostico", INTERNAL_SERVER_ERROR)


@app.route("/auth", methods=["POST"])
@cross_origin(supports_credentials=True)
def autenticar():
    """
    Handles user authentication for login and registration.
        Data received through request.form 
            email (str): User's email
            senha (str): password
            nome (str): User's name (registration only)
            crm (str): Medical license (registration only)

        Data received through request.args:
        tipo (str): 'login' or 'cadastro'

        Uses session authentication and MongoDB for storage.
        Passwords are hashed. Sessions last 7 days.
    Notes:
        - Passwords are hashed before storage and comparison
        - Sessions are set to be permanent (7 days)
        - User ID and creation time are stored in session for logged users
    """
    email, senha = request.form.get(
        "email", None), request.form.get("senha", None)
    if email is None or senha is None:
        print("EMAIL OU SENHA INVALIDOS")
        return make_response('SEM EMAIL OU SENHA', BAD_REQUEST)

    medicos = mongo.db.get_collection(MEDICOS)
    usuario = medicos.find_one({"email": email})
    senha = alg_hash(senha.encode('utf-8')).hexdigest()
    tipo = request.args['tipo']
    # ---------LOGIN--------#
    if tipo == "login":
        # sessao 'permanente', com duracao de 7 dias
        session.permanent = True
        if not email or not senha:
            print("EMAIL OU SENHA INVALIDOS")
            return abort(UNAUTHORIZED)

        """logica de cookies de sessao"""
        response = requests.get(
            url_for('val_login', _external=True),
            cookies=request.cookies
        )
        if response.text == 'True':
            return "OK"
        else:
            print("\nSEM SESSAO\n")
        if usuario != None and senha == usuario['senha']:
            session['user_id'] = str(usuario['_id'])
            # Add session creation timestamp
            session['_creation_time'] = time.time()
            session.modified = True  # Ensure session is saved
            print(session)
            return "OK"
        else:
            return make_response('INCORRETO', UNAUTHORIZED)
    # ------CADASTRO--------#
    elif (tipo == "cadastro"):
        nome = request.form.get("nome")
        crm = request.form.get("crm")
        if usuario != None:
            return "JA_EXISTE"

        medicos.insert_one({"email": email, "nome": nome,
                            "crm": crm, "senha": senha})
        return "CADASTRADO"

    else:
        return make_response('TIPO DE AUTENTICACAO ERRADO', BAD_REQUEST)


@app.route("/esqueci_senha", methods=["POST"])
def esqueci():
    emailDestino = request.form.get('email', None)
    if emailDestino:
        pass
        # TODO:  codigo para enviar email de recuperacao para medico


@app.route("/mudar_senha", methods=["PUT"])
def mudar_senha():
    email = request.form.get('email', None)
    novaSenha = request.form.get('novaSenha', None)
    if novaSenha is None or email is None:
        return make_response("", UNAUTHORIZED)
    novaSenha = alg_hash(novaSenha.encode('utf-8')).hexdigest()
    # TODO: codigo pra atulizar senha do usuario


@app.route("/val_login", methods=["GET"])
@cross_origin(supports_credentials=True)
def val_login():
    """
    Valida cookies de sessao do usuario
    """
    if 'user_id' not in session.keys():
        print("SESSAO NAO INICIADA")
        return make_response("False", UNAUTHORIZED)
    else:
        # Check if user exists in database
        medicos = mongo.db.get_collection(MEDICOS)
        usuario = find_user_with_session_mongo(session, medicos)
        if usuario != None:
            # Check if session cookie has expired based on PERMANENT_SESSION_LIFETIME
            if session.get('_creation_time', 0) + app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() <= time.time():
                session.clear()
                print("SESSAO EXPIRADA")
                return make_response("False", UNAUTHORIZED)
            else:
                return make_response("True", OK)
        else:
            print("ID DA SESSAO TA ERRADO")
            return make_response("False", INTERNAL_SERVER_ERROR)

    # Optional: Add additional security checks
    # - Check if session is expired
    # - Verify user still exists in database
    # - Check if session token is valid


@app.route("/logout", methods=["GET"])
def logout():
    try:
        session.pop('user_id', None)
        return make_response('', OK)
    except Exception as e:
        return abort(INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    # para poder adicionar um sheduler de tasks de background,
    # adicionar use_reloader=False
    app.run(debug=True)
