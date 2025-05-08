from datetime import datetime
from http.client import BAD_GATEWAY, BAD_REQUEST, INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
import time
from bson import ObjectId
import shutil
from analise import AnaliseParalisia
from yolo import YOLO
import os
from werkzeug.utils import secure_filename
from flask import Flask, make_response, render_template, session, jsonify, request, send_from_directory, url_for, abort, send_file, Response, stream_with_context
from flask_session import Session
from flask_pymongo import PyMongo
import gridfs
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import mimetypes
import hashlib
from datetime import timedelta
from typing import Any, Union
import tensorflow as tf
import threading

import ffmpeg
import requests
import csv
import numpy as np
from pdf import Converter
from drive import GoogleDrive
from concurrent.futures import ThreadPoolExecutor


class Helper:
    def __init__(self):
        pass

    def count_active_threads():
        return len(threading.enumerate())

    @staticmethod
    def allowed_file(filename: str):
        ALLOWED_EXTENSIONS = ["mpg", "mpeg", "webm",
                              "mkv", "ogv", "ogg", "mp4", "avi"]
        for ext in ALLOWED_EXTENSIONS:
            if filename.lower().endswith(ext):
                return ext
        return None

    @staticmethod
    def read_ENV_VARS(arq_config):
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

    @staticmethod
    def get_peso(api: GoogleDrive):
        file_name = "trained_weights_final.h5"
        id = api.get_file_id(file_name)
        bytes_file, _ = api.download_file(id)
        with open(file_name, 'wb') as f:
            f.write(bytes_file)

    @staticmethod
    def enviar_email(mensagem, destino, assunto):
        msg = Message(
            subject=assunto,
            recipients=[destino],  # List of recipients
            body=mensagem
        )
        try:
            mail.send(msg)
            return OK
        except Exception as e:
            return INTERNAL_SERVER_ERROR

    @staticmethod
    def traduzir_diag(diag: str, sep='+'):
        splitado = diag.split(sep)

        esq, dir = splitado
        if esq == "true" and dir == "false":
            string = "Esquerdo"
        elif esq == "false" and dir == "true":
            string = "Direito"
        elif esq == "true" and dir == "true":
            string = "Ambos"
        elif esq == "false" and dir == "false":
            string = "Saudável"
        else:
            raise ValueError("valores incorretos ao traduzir diagnostico!")

        if string != "Ambos":
            string = f"Paralisia no Olho {string}"
        elif string == "Ambos":
            string = f"Paralisia em Ambos Olhos"
        else:
            string = f"Paciente Saudável"
        return string

    @staticmethod
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

    @staticmethod
    def gerar_pdf(path_output, dict_dados):
        """ FUNCAO QUE DEVE PEGAR DADOS DO DIAGNOSTICO E RETORNAR PDF RENDERIZADO

        :param dict_dados dict[str,Any]: keys: [velEsq, nomeMedico, crm, dataAgora, nomePaciente, diagAutom, velDir, diagnosticoMedico, urlGrafico, difVel]
        :param path_output str: path pro output do pdf
        """
        # mapeamento nome no BD -> tag no HTML
        mapeamento = {'crm': "crm", 'velEsq': "vel-esq", 'nomeMedico': "nome-medico",
                      'dataAgora': "data", 'nomePaciente': "nome-paciente", 'diagAutom': "diag-auto",
                      'velDir': "vel-dir",  'diagnosticoMedico': "diag-medico", 'urlGrafico': "img-grafico",
                      'difVel': "dif-vel"}

        # dados com chaves do banco de dados que devem ser mapeados pro pdf
        '''dict_dados = {'velEsq': '2 mm/s', 'crm': "MA-1234", 'nomeMedico': "Dr Fulano de Tal Silva Araujo de Oliveira ThisIsAnExampleOfAReallyLongWordThatNeedsToBreak", 'dataAgora': "11/01/2001",
                    'nomePaciente': "Paciente Doente Silva Junior", 'diagAutom': "Tem Estrabismo",
                    'velDir': '2 mm/s', 'diagnosticoMedico': "Não Tem Estrabismo", 'urlGrafico': "file://../../vite-project/src/assets/grafico.png",
                    'difVel': '20 %'}'''

        # ajeita strings de diagnostico
        str_diag_autom = Helper.traduzir_diag(dict_dados['diagAutom'])
        dict_dados['diagAutom'] = str_diag_autom
        str_diag_medico = Helper.traduzir_diag(dict_dados['diagnosticoMedico'])
        dict_dados['diagnosticoMedico'] = str_diag_medico

        dt_object = datetime.fromtimestamp(dict_dados['dataAgora'])
        formatted_time = dt_object.strftime("%d-%m-%Y")
        dict_dados['dataAgora'] = formatted_time
        print(dict_dados['dataAgora'])

        dict_input_weasy = {}
        for key_dado in dict_dados.keys():
            nomeTag = mapeamento[key_dado]
            dict_input_weasy[nomeTag] = dict_dados[key_dado]
        conv = Converter()
        try:
            filename = os.path.basename(path_output)
            string_html = conv.insert_text_by_class(dict_input_weasy)

            # base_url = 'file://' + app.static_folder
            base_url = app.static_folder
            pdfOK, erro = conv.convert_html_to_pdf(
                string_html, filename, base_url)

            if pdfOK:
                print(base_url)
                if os.path.exists(path_output):
                    os.remove(path_output)

                shutil.move(filename, path_output)
                print("PDF created successfully!")
            else:
                raise erro
        except Exception as e:
            print(e)


class InterfaceMongo:
    def __init__(self):
        CACHING_NAME = "Caching"
        self.caching_collection = mongo.db.get_collection(CACHING_NAME)

    def cache(self, change_list):
        """
        Funcao responsavel por cachear mudança do Drive para dentro do Banco de Dados\n
        :param dict change_list: Lista que contem dicionario com mudanças. Chaves do dicionario: ['object_id_drive', 'operation', 'time',]
        """
        if len(change_list > 0):
            id_list = []
            try:
                for change_dict in change_list:
                    res = self.caching_collection.insert_one(change_dict)
                    id_list.append(str(res.inserted_id))
                return id_list
            except Exception as e:
                print(f"Exception when caching: {e}\n")
                return None
        else:
            print("NADA PARA FAZER CACHING!\n")
            return None

    def uncache(self, api: GoogleDrive, id_list: list[str] = []):
        if len(id_list) > 0:
            for id in id_list:
                self.caching_collection.find_one({"_id": ObjectId(id)})

        else:
            print("LISTA DE IDS VAZIA AO PEGAR CACHE!")
            return None

    @staticmethod
    def find_one_with_id(collection, id_string):
        return collection.find_one({"_id": ObjectId(id_string)})


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
        str_res, dict_graf = analisador.funcao_metodo(
            path_processamento_arq, path_out, timestamp
        )

        return str_res, dict_graf


# ------------- VARIAVEIS GLOBAIS--------------#
COLLECTION_DIAGS = "Diagnosticos"
COLLECTION_MEDICOS = "Medicos"

PASTA_USUARIO_ANONIMO_GDRIVE = "ANONIMO"

# Read environment variables from CSV
arq_config = "../env.csv"
Helper.read_ENV_VARS(arq_config)


app = Flask(__name__)
app.config.from_object(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/PARALISIA6_NERVO"
app.config["SESSION_TYPE"] = "filesystem"
mongo = PyMongo(app)

# objeto que vai fazer logica de armazenamento de arquivos no MongoDB
fs = gridfs.GridFS(mongo.db)


def upload_file(file_path):
    with open(file_path, "rb") as file_data:
        file_id = fs.put(file_data, filename=os.path.basename(file_path))
        print(f"File uploaded successfully with ID: {file_id}")


# SEGURANÇA
app.secret_key = os.environ.get('SECRET_KEY')
if app.secret_key is None:
    exit(1)
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
"""ALERTA!!!!!!!!!! somente usar CORS em producao, ja que isso habilita requisicoes de qualquer origem
Possível risco de segurança!
"""
CORS(app, supports_credentials=True)
# path para arquivos temporarios

print("WeasyPrint: se Aparecer erro: 'Fontconfig error: Cannot load default config file: No such file: (null)', testar se pdfs estao sendo gerados corretamente para ter deploy garantido\n")
print("APP INICIADO")

os.makedirs("tmp", exist_ok=True)

PATH_PIBITI = os.getcwd()
PATH_FLASK = os.path.join(PATH_PIBITI, "FLASK")


if "WKDIR" not in app.config.keys():
    app.config["WKDIR"] = PATH_FLASK
if "PIBITI" == os.path.basename(PATH_PIBITI):
    os.chdir(app.config["WKDIR"])
app.config["WKDIR"] = os.getcwd()

PATH_CRED = os.path.join(
    app.config["WKDIR"], "permalink-googleDrive-pibiti6-nervo.json")

# PASTA NO DRIVE QUE VAI CONTER TODOS OS ARQVUISO DE COLLECTION_MEDICOS
ROOT_DRIVE = "ROOT_DADOS"
drive = GoogleDrive(PATH_CRED, ROOT_DRIVE)
print("\nGOOGLE DRIVE:", end=" ")
if not drive.file_state.empty:
    for name in drive.file_state.loc[:, "name"]:
        print(f"{name},", end=" ")
print(
    f"Initial drive state captured with {len(drive.file_state.index)} Objects.")

print(f"\nHOME: {app.config['WKDIR']}\n\n")

path_pesos_yolo = os.path.join(app.config["WKDIR"], "trained_weights_final.h5")
if not os.path.exists(path_pesos_yolo):
    print(" NÃO REINICIE O SERVIDOR!!!!!!!\nBaixando pesos do modelo YOLOv3...")
    Helper.get_peso(app.config["WKDIR"])

app.config["TEMP_FOLDER"] = os.path.join(app.config["WKDIR"], "tmp")
os.makedirs(app.config["TEMP_FOLDER"], exist_ok=True)
video_demo = os.path.join(app.config["WKDIR"], "demoInput.mp4")

# --------------------- MODELO --------------------------#
modelo = get_modelo()
# NOTE: MODELO DEVE TER FUNCAO detect_image implementada
analisador = AnaliseParalisia(modelo, app.config["TEMP_FOLDER"])


@app.route("/teste_pdf")
def teste_pdf():
    """ FUNCAO QUE DEVE PEGAR DADOS DO DIAGNOSTICO E RETORNAR PDF renderizado

    dict_dados: keys: `
    [logoApp, velEsq, nomeMedico, dataAgora, nomePaciente, diagAutom, 
    velDir, diagnosticoMedico, urlGrafico, logoVip, logoUfma, logoNca, difVel]
    `
    """
    # mapeamento input da funcao -> tag no HTML
    mapeamento = {'crm': "crm", 'velEsq': "vel-esq", 'nomeMedico': "nome-medico",
                  'dataAgora': "data", 'nomePaciente': "nome-paciente", 'diagAutom': "diag-auto",
                  'velDir': "vel-dir",  'diagnosticoMedico': "diag-medico", 'urlGrafico': "img-grafico",
                  'difVel': "dif-vel"}

    dict_dados = {'velEsq': '2 mm/s', 'crm': "MA-1234", 'nomeMedico': "Dr Fulano de Tal Silva Araujo de Oliveira ThisIsAnExampleOfAReallyLongWordThatNeedsToBreak", 'dataAgora': "11/01/2001",
                  'nomePaciente': "Paciente Doente Silva Junior", 'diagAutom': "Tem Estrabismo",
                  'velDir': '2 mm/s', 'diagnosticoMedico': "Não Tem Estrabismo", 'urlGrafico': "file://../../vite-project/src/assets/grafico.png",
                  'difVel': '20 %'}

    dict_input_weasy = {}
    for key_dado in dict_dados.keys():
        nomeTag = mapeamento[key_dado]
        dict_input_weasy[nomeTag] = dict_dados[key_dado]
    conv = Converter()
    try:
        filename = "diagnostico.pdf"
        # TODO: ARMAZENAR PDF NO GOOGLE DRIVE
        string_html = conv.insert_text_by_class(dict_input_weasy)

        # base_url = 'file://' + app.static_folder
        base_url = app.static_folder
        pdfOK, erro = conv.convert_html_to_pdf(
            string_html, filename, base_url)

        if pdfOK:
            print(base_url)
            if os.path.exists(os.path.join(
                    app.config["TEMP_FOLDER"], filename)):
                os.remove(os.path.join(
                    app.config["TEMP_FOLDER"], filename))

            shutil.move(filename, os.path.join(
                app.config["TEMP_FOLDER"], filename))
            print("PDF created successfully!")
        else:
            raise erro
        return make_response("PDF created successfully!", OK)
    except Exception as e:
        print(e)
        return make_response("An error occurred during PDF creation.", INTERNAL_SERVER_ERROR)


@app.route("/deletar_tudo")
def deletar_tudo():
    # drive.upload_to_drive("requirements.txt", ROOT_DRIVE)
    files = drive.fetch_drive_files().copy()
    # print(f"{file.get('name')} deleted in folder {file.get('parents')}\n")
    print("ARQUIVOS DO FETCH")
    for id in files.index:
        if id == drive.ID_ROOT_DADOS:
            continue
        file = files.loc[id]
        print(f"ID:{id} NOME:{file.get('name')} in {file.get('parents')}")
        if drive.delete_file(id):
            print(f"DELETOU {file.get('name')}")
        else:
            print(f"NAO CONSEGUI: {file.get('name')}")
    print(drive.fetch_drive_files())
    return make_response("OK", OK)


@app.route("/teste_arq")
def teste_folder():
    try:
        file_path = "requirements.txt"
        if os.path.exists(file_path):
            drive.upload_to_drive(file_path, nomes_parents=[
                                  "TESTE", "DENTRO"], resumable=False)
        else:
            print(f"File '{file_path}' does not exist.")
        print(drive.fetch_drive_files())
        return make_response("OK", OK)

    except Exception as e:
        raise e
        return make_response("DEU ALGUMA COISA ERRADA", INTERNAL_SERVER_ERROR)


@app.route("/teste_mongo")
def teste2():
    diags = mongo.db.get_collection(COLLECTION_DIAGS)
    for diag in diags.find():
        print(diag)


@app.route("/")
def index():
    return "Hello World"


@app.route('/get-file-drive/<id_file>', methods=['GET'])
@cross_origin(supports_credentials=True)
# usando esse decorator pra evitar erros de TLS
def get_file_drive(id_file):
    """
    Serves files using file_id from Google Drive.
    """
    print("FILE ID: ", id_file)
    try:
        limite_mega = 20*1024*1024  # (20 MB)
        print("PEGANDO ARQUIVO!")
        file_generator, filename = drive.download_file(id_file)
        # TODO: IMPLEMENTAR LOGICA DE STREAM AO ENVIAR ARQUIVOS MUITO GRANDES!!!!
        print("DEPOIS DOWNLOAD")
        return Response(
            stream_with_context(file_generator),
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            }
        )
    except Exception as e:
        print(f"ERRO AO PEGAR ARQUIVO: {e}")
        return make_response({"error": f"{str(e)}", "file_url": 'None'}, INTERNAL_SERVER_ERROR)


@app.route('/get-file-local/<filename>', methods=['GET'])
@cross_origin(supports_credentials=True)
# usando esse decorator pra evitar erros de TLS
def get_file_local(filename):
    """
    NOTE: USAR ^APENAS^ BASENAME DO ARQUVIO QUE ESTEJA NO TMP
    Serves files from '/tmp' using filename.
    """
    try:
        if len(filename) > 0:
            # limite_mega = 20*1024*1024
            filename = os.path.join(
                app.config["TEMP_FOLDER"], secure_filename(filename))
            print("FILE NAME: ", filename)

            chunk_size = 1024*1024

            def file_generator(file_path):
                with open(file_path, "rb") as f:
                    # ':=' walrus operator, designa e avalia variavel 'chunk'
                    while chunk := f.read(chunk_size):  # Read in chunks of 8KB
                        yield chunk
            print(f"BAIXANDO ARQUIVO {filename}")
            return Response(
                stream_with_context(file_generator(filename)),
                headers={
                    'Content-Disposition': f'attachment; filename="{os.path.basename(filename)}"',
                    'Content-Type': mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                }
            )
    except Exception as e:
        print(f"ERRO AO PEGAR ARQUIVO: {e}")
        return make_response({"error": f"{str(e)}", "file_url": 'None'}, INTERNAL_SERVER_ERROR)


@app.route('/get-file/<resource_url>', methods=['GET'])
@cross_origin(supports_credentials=True)
# usando esse decorator pra evitar erros de TLS
def get_file(resource_uri) -> Union[Any, Response]:
    """
    Serves files depending on storage
    """
    print("URI: ", resource_uri)
    try:
        print("PEGANDO ARQUIVO!")
        tipo, uri = split_storage_url(resource_uri)
        if tipo == "local":
            return get_file_local(uri)
        else:
            return get_file_drive(uri)

    except Exception as e:
        print(f"ERRO AO PEGAR ARQUIVO: {e}")
        return make_response({"error": f"{str(e)}", "file_url": 'None'}, INTERNAL_SERVER_ERROR)


def make_storage_url(local=True, filename=None):
    """
    Cria uma string em duas partes: primeira eh flag indicando onde arquivo esta armazenado, segunda eh url para o arquivo
    """
    storage_string = ""
    sep = ":"
    if local:
        temp_folder = os.path.basename(app.config["TEMP_FOLDER"])
        filename = secure_filename(os.path.basename(filename))
        relpath = os.path.relpath(os.path.join(
            temp_folder, filename), app.config["WKDIR"])
        storage_string = f"local{sep}{relpath}"
    else:
        # arquivo pro google drive, filename eh hash do drive
        id_drive = filename
        storage_string = f"cloud{sep}{id_drive}"

    return storage_string


def split_storage_url(string: str):
    sep = ":"
    tipo, uri = string.split(sep)
    return tipo, uri


def sync_google_drive(storage_strings: dict, id_diag: str, email: str):
    print(f"STORAGE: {storage_strings}, ID: {id_diag}")
    str_video_in = storage_strings["video_in"]
    tipo, path_video_in = split_storage_url(str_video_in)

    str_video_out = storage_strings["video_out"]
    tipo, path_video_out = split_storage_url(str_video_out)

    id_in = drive.upload_to_drive(path_video_in)
    id_out = drive.upload_to_drive(path_video_out)

    url_in = make_storage_url(local=False, filename=id_in)
    url_out = make_storage_url(local=False, filename=id_out)

    modif = {"video_in": url_in, "video": url_out}
    mongo.db.get_collection(COLLECTION_DIAGS).update_one(
        {"_id": ObjectId(id_diag)},
        {"$set": modif}
    )
    print("UPLOAD COMPLETO! ANÁLISE TERMINADA")


@app.route("/analise", methods=["POST"])
@cross_origin(supports_credentials=True)
def analisar():
    """
    Takes video  input, executa the model e and returns result as JSON
    # servidor DEVE retorna JSON com string contendo as métricas, pdf de res, VIDEO DE SAIDA e grafico
    """
    timestamp = time.time()
    print(f"KEYS FORM: {request.form.keys()}\n")
    id_diag = request.form.get("id_diag", None)
    nome_input = request.form.get("nome_input", None)
    filename = request.form.get("filename", None)
    diag = None

    if id_diag != None:
        print(request.form)
        diag = mongo.db.get_collection(
            COLLECTION_DIAGS).find_one({"_id": ObjectId(id_diag)})
    else:
        return make_response("INPUT NULO!", BAD_REQUEST)
    # VERSÃO LOGADO
    if "user_id" in session:
        user = session["user_id"]
    else:
        user = "TEMP"
    ext = Helper.allowed_file(filename)
    if ext is None:
        print("Incorrect file type!\n\n")
        return SystemError

    nome_video = f"{user}_{str(round(timestamp, 4))}"
    nome_local = f"{nome_video}.{ext}"
    filename_arq_input = secure_filename(f"INPUT_{nome_input}")
    os.rename(os.path.join(app.config["TEMP_FOLDER"], nome_input), os.path.join(
        app.config["TEMP_FOLDER"], filename_arq_input))

    # video deve ser armazenado usando ID do usuario e timestamp, pra garantir multiplicidade
    path_arq_input = os.path.join(
        app.config["TEMP_FOLDER"], filename_arq_input)

    """ se eu nao me engano, logica utilizada para fazer streaming de arquivos grandes
    arq_stream = arq.stream"""

    EXT_OUT = "mp4"
    nome_local = f"{nome_video}.{EXT_OUT}"
    # path cujo unico proposito eh servir de temporario pras conversoes de video
    path_aux_conv = os.path.join(
        app.config["TEMP_FOLDER"], f"CONVERT_{nome_local}")

    path_arq_input_conv = Helper.converter_arq(
        path_arq_input, path_aux_conv)
    print("\nDEPOIS PRIMEIRA CONVER\n")
    nome_local = f"{nome_video}.{EXT_OUT}"
    path_out_antes_conv = os.path.join(
        app.config["TEMP_FOLDER"], f"OUT_PRE_{nome_local}")

    # executando predicao
    res_tensor, dict_graf_tensor = predict(
        analisador, path_arq_input_conv, path_out_antes_conv, timestamp
    )

    with tf.compat.v1.Session() as sess:
        # Run the session to get the tensor's value
        res_np = sess.run(res_tensor)
        if "ERRO" in res_np.decode('utf-8'):
            return make_response(res_np, BAD_REQUEST)
        graf_np = sess.run(dict_graf_tensor)
    # Decode bytes to string since predict returns all output as tensor
    str_res, dict_graf_tensor = res_np.decode('utf-8'), graf_np

    dict_graf_tensor['vel_esq'] = np.array(
        dict_graf_tensor['vel_esq']).tolist()
    dict_graf_tensor['vel_dir'] = np.array(
        dict_graf_tensor['vel_dir']).tolist()
    dict_graf_tensor['time'] = float(dict_graf_tensor['time'])

    path_out = os.path.join(app.config["TEMP_FOLDER"], f"OUT_{nome_local}")
    print("ULTIMA CONVERSAO")
    path_out = Helper.converter_arq(
        path_out_antes_conv, path_out)

    '''Removendo APENAS arquivos auxiliares'''
    os.remove(path_out_antes_conv)
    os.remove(path_aux_conv)

    # TODO: ARMAZENAR DADOS PDF NO DB
    # path_pdf = os.path.join(
    #     app.config["TEMP_FOLDER"], f"RELATORIO_{nome_video}.pdf")

    # str_res no formato "velE,velD,percentDif,olho_doente"
    split_res = str_res.split(",")
    olho_doente = str_res.split(",")[3]

    if olho_doente == "Esquerdo":
        str_diag = "true+false"
    elif olho_doente == "Direito":
        str_diag = "false+true"
    else:
        str_diag = "false+false"

    id_medico = diag.get('id_medico', None)
    # NOTE: NAO GERA PDF PRA USUARIOS ANONIMOS!
    if id_medico:
        diag_medico = diag.get('diagnosticoMedico')  # string codificada
        nome_paciente = diag.get('nomePaciente')

        medico = InterfaceMongo.find_one_with_id(mongo.db.get_collection(
            COLLECTION_MEDICOS), id_medico)
        nome_medico = medico.get('nome')
        crm = medico.get('crm')
        email_medico = medico.get('email')
        dict_dados_pdf = {"velEsq": split_res[0], "velDir": split_res[1], "difVel": split_res[2], "crm": crm,
                          "diagAutom": str_diag, "dataAgora": timestamp, "nomePaciente": nome_paciente,
                          "nomeMedico": nome_medico, "diagnosticoMedico": diag_medico, "dadosGrafico": dict_graf_tensor}
    else:
        email_medico = PASTA_USUARIO_ANONIMO_GDRIVE
        dict_dados_pdf = None

    print("PEGANDO URLS")

    local_url_video_out = make_storage_url(local=True, filename=path_out)
    local_url_video_in = make_storage_url(local=True, filename=path_arq_input)

    result = {"diagAutom": str_diag, "dados_grafico": dict_graf_tensor, "dados_pdf": dict_dados_pdf,
              "dataDiag": timestamp, "video": local_url_video_out, "ultimaModif": timestamp}
    mongo.db.get_collection(COLLECTION_DIAGS).update_one(
        {"_id": ObjectId(id_diag)},
        {"$set": result}
    )

    result["diagAutom"] = str_res

    storage_dict = {"video_in": local_url_video_in,
                    "video_out": local_url_video_out}

    def after_analise():
        # cria nova thread pra sincronizar com google drive
        thread = threading.Thread(
            target=sync_google_drive, args=(storage_dict, id_diag, email_medico))
        thread.start()

    result.pop('dados_grafico')
    result.pop('dados_pdf')
    result["grafico"] = url_for(
        'gerar_relatorio', id_diag=id_diag, _external=True)
    result["pdf"] = url_for('gerar_relatorio', id_diag=id_diag, _external=True)
    resp = jsonify(result)
    resp.call_on_close(after_analise)
    print("\nANALISE FINALZIADA!")
    return resp


@app.route("/pega_perfil", methods=["GET"])
@cross_origin(supports_credentials=True)
def pega_perfil():
    maxItensPag = 16
    pagAtual = request.args.get('pagAtual', None)
    if pagAtual != None:
        pagAtual = int(pagAtual)
        id_medico = session['user_id']
        res = mongo.db.get_collection(COLLECTION_DIAGS).aggregate([
            {
                '$match': {
                    "id_medico": id_medico
                }
            },

            {
                '$facet': {
                    'metadata': [{'$count': 'totalCount'}],
                    'data': [{'$skip': (pagAtual - 1) * maxItensPag}, {'$limit': maxItensPag}],
                },
            },
        ], allowDiskUse=True)
        lista_res = list(res)[0]['data']
        print(f"\n\n{lista_res}\n\n")

        medico = InterfaceMongo.find_one_with_id(
            mongo.db.get_collection(COLLECTION_MEDICOS), id_medico)
        # res = list(mongo.db.get_collection(COLLECTION_DIAGS).find())
        return jsonify({"nomeMedico": medico["nome"], "crm": medico["crm"], "lista": lista_res})

    else:
        return make_response("INPUT NULO!", BAD_REQUEST)


@app.route("/gerar_relatorio/<id_diag>", methods=["GET"])
def gerar_relatorio(id_diag):
    """
    Gera pdf com grafico e outros dados importantes e retorna url do pdf
    """

    diag = InterfaceMongo.find_one_with_id(
        mongo.db.get_collection(COLLECTION_DIAGS), id_diag)
    dados_pdf = diag.get('dados_pdf')
    output = os.path.relpath(os.path.join(
        app.config["TEMP_FOLDER"], dados_pdf["nomePaciente"]), app.config["WKDIR"])
    dados_pdf["urlGrafico"] = gerar_grafico(id_diag, external=False)

    Helper.gerar_pdf(output, dados_pdf)
    uri_pdf = make_storage_url(output)
    return get_file(uri_pdf)


@app.route("/gerar_grafico/<id_diag>", methods=["GET"])
def gerar_grafico(id_diag, external=True):
    """
    Gera grafico e retorna ele como stream
    """

    diag = InterfaceMongo.find_one_with_id(
        mongo.db.get_collection(COLLECTION_DIAGS), id_diag)
    dados_grafico = diag.get('dados_grafico')
    vel_esq, vel_dir, titulo, time = dados_grafico["vel_esq"], dados_grafico[
        "vel_dir"], dados_grafico["titulo"], dados_grafico["time"]

    path_graf = analisador.plotHampelFinal(vel_esq, vel_dir, titulo, time)
    uri_graf = make_storage_url(path_graf)
    if external:
        return get_file(uri_graf)
    else:
        return uri_graf


@app.route("/envia_diag", methods=["POST"])
@cross_origin(supports_credentials=True)
def envia_diag():
    """
    Rota responsavel por receber formulario com diagnostico do medico e guardar dados no BD e no Drive
    """
    print("ENVIO DO DIAG")
    timestamp = time.time()
    video = request.files.get("video", None)

    nomePaciente = request.form.get("nomePaciente", None)
    stringOlhos = request.form.get("stringOlhos", None)

    desc = request.form.get("desc", None)
    a = [video, nomePaciente]
    if any(elem is None for elem in a):
        return make_response("INPUT NULO!", BAD_REQUEST)

    diagnosticoMedico = stringOlhos
    response = requests.get(
        url_for('val_login', _external=True),
        cookies=request.cookies
    )

    if response.text == 'True':
        # caso pra usuario logado
        id_medico = session['user_id']
        medicos = mongo.db.get_collection(COLLECTION_MEDICOS)
        medico_atual = medicos.find_one({"_id": ObjectId(id_medico)})
        nomeMedico = medico_atual.get("nome") if medico_atual else None
        if nomeMedico is None:
            return make_response("MEDICO LOGADO NAO ENCONTRADO", INTERNAL_SERVER_ERROR)
    else:
        # padronizar dados nulos no BD como None e erros de preenchimento como null
        id_medico = None

    diags = mongo.db.get_collection(COLLECTION_DIAGS)
    dados = {"nomePaciente": nomePaciente, "id_medico": id_medico,
             "diagnosticoMedico": diagnosticoMedico, "desc": desc}

    # transforma qualquer valor None em string
    for key, value in dados.items():
        if value is None:
            dados[key] = "None"

    result = diags.insert_one(dados)
    id_diag_mongo = str(result.inserted_id)
    print("RESULTADO INSERT: ", result)

    # escreve dados no video em \tmp e usa timestamp pra evitar duplicatas
    filename = video.filename
    nome_local = f"{str(round(timestamp, 4))}_{filename}"
    video_data = video.read()
    path_temp_videoLabel = os.path.join(app.config["TEMP_FOLDER"], nome_local)
    with open(path_temp_videoLabel, "wb") as f:
        f.write(video_data)

    print("DIAG ENVIADO!\n")
    return make_response({"mensagem": "CARREGADO", "id_diag": id_diag_mongo, "nome_input": nome_local, "filename": filename}, OK)


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

    medicos = mongo.db.get_collection(COLLECTION_MEDICOS)
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
        # cria sessão para o usuario logado
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
        drive.create_folder([email], wait=False)
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
        usuario = InterfaceMongo.find_one_with_id(
            mongo.db.get_collection(COLLECTION_MEDICOS), session['user_id'])
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
    # NOTE: para poder adicionar um sheduler de tasks de background, adicionar use_reloader=False
    app.run(debug=True)
