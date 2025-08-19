from datetime import datetime
from http.client import (
    BAD_GATEWAY,
    BAD_REQUEST,
    INTERNAL_SERVER_ERROR,
    OK,
    UNAUTHORIZED,
)
import time
from bson import ObjectId
import shutil
from analise import AnaliseParalisia
from yolo import YOLO
import os
from werkzeug.utils import secure_filename
import subprocess
import json
from flask import (
    Flask,
    make_response,
    redirect,
    session,
    jsonify,
    request,
    url_for,
    abort,
    Response,
    stream_with_context,
    send_file,
)
from dotenv import load_dotenv
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message

import mimetypes
import hashlib
from datetime import timedelta
from typing import Any, Union
import tensorflow as tf
import threading

import ffmpeg
from celery import Celery

import csv
import numpy as np
from pdf import Converter
from drive import GoogleDrive
from _email import MailHandler
from user import User
import logging

from celery_worker.tasks import (
    envia_diag_task,
    processamento_analise,
    sync_google_drive,
)


class Helper:
    def __init__(self):
        pass

    def count_active_threads():
        return len(threading.enumerate())

    @staticmethod
    def allowed_file(filename: str):
        ALLOWED_EXTENSIONS = ["mpg", "mpeg", "webm", "mkv", "ogv", "ogg", "mp4", "avi"]
        for ext in ALLOWED_EXTENSIONS:
            if filename.lower().endswith(ext):
                return ext
        return None

    @staticmethod
    def read_ENV_VARS(arq_config):
        try:
            with open(arq_config, "r") as file:
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
        print("PEGANDO ID DO ARQUIVO A BAIXAR")
        id = api.get_file_id(file_name)
        bytes_file, _ = api.download_file(id)
        print("BYTES BAIXADOS")
        with open(file_name, "wb") as f:
            f.write(bytes_file)

    @staticmethod
    def enviar_email(mensagem, destino, assunto):
        msg = Message(
            subject=assunto, recipients=[destino], body=mensagem  # List of recipients
        )
        try:
            mail.send(msg)
            return OK
        except Exception as e:
            return INTERNAL_SERVER_ERROR

    @staticmethod
    def traduzir_diag(diag: str, sep="+"):
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
        stream = ffmpeg.output(stream, output, vcodec="libx264", acodec="aac")
        print(stream, "\n\n")
        try:
            # Execute the conversion
            ffmpeg.run(stream, cmd="ffmpeg")
            return output
        except ffmpeg.Error as e:
            print("stdout:", e.stdout.decode("utf8"))
            print("stderr:", e.stderr.decode("utf8"))

    @staticmethod
    def gerar_pdf(path_output, dict_dados):
        """FUNCAO QUE DEVE PEGAR DADOS DO DIAGNOSTICO E RETORNAR PDF RENDERIZADO

        :param dict_dados dict[str,Any]: keys: [velEsq, nomeMedico, crm, dataAgora, nomePaciente, diagAutom, velDir, diagnosticoMedico, urlGrafico, difVel]
        :param path_output str: path pro output do pdf
        """
        # mapeamento nome no BD -> tag no HTML
        mapeamento = {
            "crm": "crm",
            "velEsq": "vel-esq",
            "nomeMedico": "nome-medico",
            "dataAgora": "data",
            "nomePaciente": "nome-paciente",
            "diagAutom": "diag-auto",
            "velDir": "vel-dir",
            "diagnosticoMedico": "diag-medico",
            "urlGrafico": "img-grafico",
            "difVel": "dif-vel",
        }

        print(f"DICT DADOS PDF: {dict_dados}\n")
        # ajeita strings de diagnostico
        str_diag_autom = Helper.traduzir_diag(dict_dados["diagAutom"])
        dict_dados["diagAutom"] = str_diag_autom
        str_diag_medico = Helper.traduzir_diag(dict_dados["diagnosticoMedico"])
        dict_dados["diagnosticoMedico"] = str_diag_medico

        dt_object = datetime.fromtimestamp(dict_dados["dataAgora"])
        formatted_time = dt_object.strftime("%d-%m-%Y")
        dict_dados["dataAgora"] = formatted_time
        print(dict_dados["dataAgora"])

        dict_input_weasy = {}
        for key_dado in dict_dados.keys():
            nomeTag = mapeamento[key_dado]
            dict_input_weasy[nomeTag] = dict_dados[key_dado]

        # Serialize data to pass to the external process
        args_pdf = {"path_output": path_output, "dict_input_weasy": dict_input_weasy}
        base_url = os.path.join(app.config["WKDIR"], "static")

        try:
            # Execute the PDF generation as an external process
            process = subprocess.run(
                [
                    "python",
                    "pdf.py",
                    json.dumps(dict_input_weasy),
                    path_output,
                    base_url,
                ],
                text=True,
                capture_output=True,
            )

            if process.returncode == 0:
                print("PDF created successfully!")
            else:
                raise Exception(
                    f"PDF generation failed in external process {process.stderr}"
                )
        except Exception as e:
            print(e)

    @staticmethod
    def find_one_with_id(collection, id_string):
        return collection.find_one({"_id": ObjectId(id_string)})


class CeleryTaskWrapper:
    def __init__(
        self, mongo: Any, COLLECTION_DIAGS: str, COLLECTION_MEDICOS: str, app, drive
    ) -> None:

        self.mongo_inst = mongo
        self.coll_diags = COLLECTION_DIAGS
        self.coll_meds = COLLECTION_MEDICOS
        self.flask_app = app
        self.drive_inst = drive
        print("CELERY WRAPPER INICIADO")

    def sync_google_drive(
        storage_strings: dict,
        id_diag: str,
        email: str,
        drive_inst,
        mongo_inst,
        coll_diags,
    ):
        return sync_google_drive.apply_async(
            args=[storage_strings, id_diag, email, drive_inst, mongo_inst, coll_diags]
        )

    def processamento_analise(
        self,
        id_diag,
        nome_input,
        filename,
    ):
        return processamento_analise.apply_async(
            args=[
                id_diag,
                nome_input,
                filename,
                self.mongo_inst,
                self.coll_diags,
                self.coll_meds,
                self.flask_app,
                predict,
                analisador,
                Helper,
            ]
        )

    def envia_diag_task(
        self,
        video_data,
        filename,
        nomePaciente,
        stringOlhos,
        desc,
        user_id,
    ):

        return envia_diag_task.apply_async(
            args=[
                video_data,
                filename,
                nomePaciente,
                stringOlhos,
                desc,
                user_id,
                self.mongo_inst,
                self.flask_app,
                self.coll_diags,
                self.coll_meds,
            ]
        )


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
# arq_config = "./env.csv"
# Helper.read_ENV_VARS(arq_config) NOTE: DEPRECATED
load_dotenv()

app = Flask(__name__)
app.config.from_object(__name__)

app.config["MONGO_URI"] = os.environ["MONGO_URI"]
app.config["CELERY_RESULT_BACKEND"] = os.environ["CELERY_RESULT_BACKEND"]
app.config["CELERY_BROKER_URL"] = os.environ["CELERY_BROKER_URL"]

# Flask app config example:
# app.config.update()
mongo = PyMongo(app)

# objeto que vai fazer logica de armazenamento de arquivos no MongoDB


def make_celery(app):
    celery = Celery(
        "tasks",
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


# celery = make_celery(app)


# @celery.task
# def sync_google_drive(self, storage_strings: dict, id_diag: str, email: str):
#     print(f"STORAGE: {storage_strings}, ID: {id_diag}")
#     path_video_in = storage_strings["video_in"]
#     path_video_out = storage_strings["video_out"]
#     id_in = self.drive_inst.upload_to_drive(path_video_in, [email])
#     id_out = self.drive_inst.upload_to_drive(path_video_out, [email])

#     # Update the document in the database with the new Google Drive file IDs
#     self.mongo_inst.db.get_collection(self.coll_diags).update_one(
#         {"_id": ObjectId(id_diag)}, {"$set": {"video_in": id_in, "video": id_out}}
#     )

#     print("UPLOAD COMPLETO! ANÁLISE TERMINADA")


# @celery.task(bind=True)
# def processamento_analise(self, id_diag, nome_input, filename):

#     timestamp = time.time()
#     diag = mongo.db.get_collection(COLLECTION_DIAGS).find_one(
#         {"_id": ObjectId(id_diag)}
#     )

#     ext = Helper.allowed_file(filename)
#     if ext is None:
#         return {"error": "Incorrect file type"}

#     paciente = diag.get("nomePaciente", None)
#     nome_video = f"{paciente}_{str(round(timestamp, 4))}"
#     nome_local = f"{nome_video}.{ext}"
#     filename_arq_input = f"INPUT_{nome_local}"
#     # renomeia arquivo de input na pasta temporaria para filename_arq_input
#     os.rename(
#         os.path.join(app.config["TEMP_FOLDER"], nome_input),
#         os.path.join(app.config["TEMP_FOLDER"], filename_arq_input),
#     )

#     # video deve ser armazenado usando ID do usuario e timestamp, pra garantir multiplicidade
#     path_arq_input = os.path.join(app.config["TEMP_FOLDER"], filename_arq_input)

#     """ se eu nao me engano, logica utilizada para fazer streaming de arquivos grandes
#     arq_stream = arq.stream"""

#     EXT_OUT = "mp4"
#     nome_local = f"{nome_video}.{EXT_OUT}"
#     # path cujo unico proposito eh servir de temporario pras conversoes de video
#     path_aux_conv = os.path.join(app.config["TEMP_FOLDER"], f"CONVERT_{nome_local}")

#     path_arq_input_conv = Helper.converter_arq(path_arq_input, path_aux_conv)
#     print("\nDEPOIS PRIMEIRA CONVER\n")

#     path_out_antes_conv = os.path.join(
#         app.config["TEMP_FOLDER"], f"OUT_PRE_{nome_local}"
#     )

#     # executando predicao
#     res_tensor, dict_graf_tensor = predict(
#         analisador, path_arq_input_conv, path_out_antes_conv, timestamp
#     )

#     with tf.compat.v1.Session() as sess:
#         # Run the session to get the tensor's value
#         res_np = sess.run(res_tensor)
#         if "ERRO" in res_np.decode("utf-8"):
#             return make_response(res_np, BAD_REQUEST)
#         graf_np = sess.run(dict_graf_tensor)

#     # Decode bytes to string since predict returns all output as tensor
#     str_res, dict_graf = res_np.decode("utf-8"), graf_np

#     dict_graf["vel_esq"] = np.array(dict_graf["vel_esq"]).tolist()
#     dict_graf["vel_dir"] = np.array(dict_graf["vel_dir"]).tolist()
#     dict_graf["time"] = float(dict_graf["time"])
#     dict_graf["titulo"] = str(dict_graf["titulo"])

#     path_out = os.path.join(app.config["TEMP_FOLDER"], f"OUT_{nome_local}")
#     print("ULTIMA CONVERSAO")
#     path_out = Helper.converter_arq(path_out_antes_conv, path_out)

#     """Removendo APENAS arquivos auxiliares"""
#     os.remove(path_out_antes_conv)
#     os.remove(path_aux_conv)

#     # path_pdf = os.path.join(
#     #     app.config["TEMP_FOLDER"], f"RELATORIO_{nome_video}.pdf")

#     # str_res no formato "velE,velD,percentDif,olho_doente"
#     split_res = str_res.split(",")
#     olho_doente = str_res.split(",")[3]

#     if olho_doente == "Esquerdo":
#         str_diag = "true+false"
#     elif olho_doente == "Direito":
#         str_diag = "false+true"
#     else:
#         str_diag = "false+false"

#     id_medico = diag.get("id_medico", None)
#     # NOTE: NAO GERA PDF PRA USUARIOS ANONIMOS!
#     if str(id_medico) != "None":
#         diag_medico = diag.get("diagnosticoMedico")  # string codificada
#         nome_paciente = diag.get("nomePaciente")

#         medico = Helper.find_one_with_id(
#             mongo.db.get_collection(COLLECTION_MEDICOS), id_medico
#         )
#         nome_medico = medico.get("nome")
#         crm = medico.get("crm")
#         email_medico = medico.get("email")
#         dict_dados_pdf = {
#             "velEsq": split_res[0],
#             "velDir": split_res[1],
#             "difVel": split_res[2],
#             "crm": crm,
#             "diagAutom": str_diag,
#             "dataAgora": timestamp,
#             "nomePaciente": nome_paciente,
#             "nomeMedico": nome_medico,
#             "diagnosticoMedico": diag_medico,
#         }
#     else:
#         email_medico = PASTA_USUARIO_ANONIMO_GDRIVE
#         dict_dados_pdf = None

#     print("PEGANDO URLS")

#     local_url_video_out = url_for(
#         "get_file", resource_uri=os.path.basename(path_out), _external=True
#     )
#     print(f"LOCAL URL VIDEO OUT: {local_url_video_out}")
#     local_url_video_in = url_for(
#         "get_file", resource_uri=os.path.basename(path_arq_input), _external=True
#     )

#     result = {
#         "diagAutom": str_diag,
#         "dados_grafico": dict_graf,
#         "dados_pdf": dict_dados_pdf,
#         "dataDiag": timestamp,
#         "video": local_url_video_out,
#         "ultimaModif": timestamp,
#     }
#     # seta resultado no BD
#     mongo.db.get_collection(COLLECTION_DIAGS).update_one(
#         {"_id": ObjectId(id_diag)}, {"$set": result}
#     )

#     result["diagAutom"] = str_res

#     storage_dict = {"video_in": path_arq_input, "video_out": path_out}

#     sync_google_drive.delay(storage_dict, id_diag, email_medico)

#     result.pop("dados_grafico")
#     result.pop("dados_pdf")
#     result["grafico"] = url_for(
#         "gerar_grafico", external=True, id_diag=id_diag, _external=True
#     )
#     result["pdf"] = url_for(
#         "gerar_relatorio", id_diag=id_diag, download=True, _external=True
#     )
#     result["video"] = local_url_video_out
#     print("\nANALISE FINALZIADA!")

#     return {
#         "result": result,
#         "grafico_url": url_for(
#             "gerar_grafico", external=True, id_diag=id_diag, _external=True
#         ),
#         "pdf_url": url_for(
#             "gerar_relatorio", id_diag=id_diag, download=True, _external=True
#         ),
#         "video_url": local_url_video_out,
#     }


print("DEPOIS DO CELERY")


# SEGURANÇA
app.secret_key = os.environ.get("SECRET_KEY", None)
if app.secret_key is None:
    exit(1)
alg_hash = hashlib.sha3_256

# TODO: MUDAR SEGURANÇA DOS COOKIES QUANO FOR PRO DEPLOY
# SESSÃO PADRÃO DO FLASK
# NOTE: FLASK < 3.1 não tem suporte pra cookies Partitioned
"""-------CONFIGS DE SESSAO---------------"""
app.config.update(
    SESSION_PERMANENT=True,
    SESSION_COOKIE_SECURE=True,  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="None",
    SESSION_USE_SIGNER=True,
    SESSION_COOKIE_PARTITIONED=True,
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
    SESSION_TYPE="filesystem",
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "basic"


# CONFIGS DE EMAIL
app.config.update(
    MAIL_SERVER=os.environ.get("MAIL_SERVER", "smtp.example.com"),
    MAIL_PORT=int(os.environ.get("MAIL_PORT", 587)),
    MAIL_USE_TLS=os.environ.get("MAIL_USE_TLS", "True").lower() == "true",
    MAIL_USE_SSL=os.environ.get("MAIL_USE_SSL", "False").lower() == "true",
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.environ.get("MAIL_DEFAULT_SENDER"),
)

"""ALERTA!!!!!!!!!! somente usar CORS em producao, ja que isso habilita requisicoes de qualquer origem
Possível risco de segurança!
"""
CORS(app, supports_credentials=True, expose_headers=["Set-Cookie"])
# path para arquivos temporarios

"""WeasyPrint: se Aparecer erro: 
'Fontconfig error: Cannot load default config file: No such file: (null)', 
testar se pdfs estao sendo gerados corretamente para ter deploy garantido\n")"""

os.makedirs("tmp", exist_ok=True)

PATH_PIBITI = os.getcwd()
print(f"PATH_PIBITI: {PATH_PIBITI}\n")
PATH_FLASK = os.path.join(PATH_PIBITI, "FLASK")
EMAIL_ADMIN = "viplab.psno@nca.ufma.br"
DOMINIO_SITE = "http://localhost:5000"
DOMINIO_FRONT_VUE = "http://localhost:5173"

if "WKDIR" not in app.config.keys():
    app.config["WKDIR"] = PATH_FLASK
    print("SETTING WKDIR TO APP.CONFIG")
if "PIBITI" == os.path.basename(PATH_PIBITI):
    os.chdir(app.config["WKDIR"])
    print(f"CHANGING DIR TO {os.getcwd()}")

app.config["WKDIR"] = os.getcwd()

PATH_CRED = os.path.join(
    app.config["WKDIR"], "permalink-googleDrive-pibiti6-nervo.json"
)

# OBJETO DO FLASK_MAIL
mail = Mail(app)
# HANDLER DE EMAILS
MAILHANDLER = MailHandler(mail)


print("APP INICIADO")
# PASTA NO DRIVE QUE VAI CONTER TODOS OS ARQVUISO DE COLLECTION_MEDICOS
ROOT_DRIVE = "ROOT_DADOS"
drive = GoogleDrive(PATH_CRED, ROOT_DRIVE)
print("\nGOOGLE DRIVE:", end=" ")
if not drive.file_state.empty:
    for name in drive.file_state.loc[:, "name"]:
        print(f"{name},", end=" ")
print(f"Initial drive state captured with {len(drive.file_state.index)} Objects.")

print(f"\nHOME: {app.config['WKDIR']}\n\n")

celery_wrapper = CeleryTaskWrapper(
    mongo, COLLECTION_DIAGS, COLLECTION_MEDICOS, app, drive
)


path_pesos_yolo = os.path.join(app.config["WKDIR"], "trained_weights_final.h5")
if not os.path.exists(path_pesos_yolo):
    raise Exception(
        f"PESO YOLOv3 NAO EXISTE!!! BAIXE O ARQUIVO: trained_weights_final.h5 PARA PROSSEGUIR"
    )


app.config["TEMP_FOLDER"] = os.path.join(app.config["WKDIR"], "tmp")
os.makedirs(app.config["TEMP_FOLDER"], exist_ok=True)
video_demo = os.path.join(app.config["WKDIR"], "demoInput.mp4")

# --------------------- MODELO --------------------------#
modelo = get_modelo()
# NOTE: MODELO DEVE TER FUNCAO detect_image implementada
analisador = AnaliseParalisia(modelo, app.config["TEMP_FOLDER"])


@app.route("/teste_pdf")
def teste_pdf():
    """FUNCAO QUE DEVE PEGAR DADOS DO DIAGNOSTICO E RETORNAR PDF renderizado

    dict_dados: keys: `
    [logoApp, velEsq, nomeMedico, dataAgora, nomePaciente, diagAutom,
    velDir, diagnosticoMedico, urlGrafico, logoVip, logoUfma, logoNca, difVel]
    `
    """
    # mapeamento input da funcao -> tag no HTML
    mapeamento = {
        "crm": "crm",
        "velEsq": "vel-esq",
        "nomeMedico": "nome-medico",
        "dataAgora": "data",
        "nomePaciente": "nome-paciente",
        "diagAutom": "diag-auto",
        "velDir": "vel-dir",
        "diagnosticoMedico": "diag-medico",
        "urlGrafico": "img-grafico",
        "difVel": "dif-vel",
    }

    dict_dados = {
        "velEsq": "2 mm/s",
        "crm": "MA-1234",
        "nomeMedico": "Dr Fulano de Tal Silva Araujo de Oliveira ThisIsAnExampleOfAReallyLongWordThatNeedsToBreak",
        "dataAgora": "11/01/2001",
        "nomePaciente": "Paciente Doente Silva Junior",
        "diagAutom": "Tem Estrabismo",
        "velDir": "2 mm/s",
        "diagnosticoMedico": "Não Tem Estrabismo",
        "urlGrafico": "file://../../vite-project/src/assets/grafico.png",
        "difVel": "20 %",
    }

    dict_input_weasy = {}
    for key_dado in dict_dados.keys():
        nomeTag = mapeamento[key_dado]
        dict_input_weasy[nomeTag] = dict_dados[key_dado]
    conv = Converter()
    try:
        filename = "diagnostico.pdf"
        string_html = conv.insert_text_by_class(dict_input_weasy)

        # base_url = 'file://' + app.static_folder
        base_url = app.static_folder
        pdfOK, erro = conv.convert_html_to_pdf(string_html, filename, base_url)

        if pdfOK:
            print(base_url)
            if os.path.exists(os.path.join(app.config["TEMP_FOLDER"], filename)):
                os.remove(os.path.join(app.config["TEMP_FOLDER"], filename))

            shutil.move(filename, os.path.join(app.config["TEMP_FOLDER"], filename))
            print("PDF created successfully!")
        else:
            raise erro
        return make_response("PDF created successfully!", OK)
    except Exception as e:
        print(e)
        return make_response(
            "An error occurred during PDF creation.", INTERNAL_SERVER_ERROR
        )


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
        if drive.get_folder_id(file.get("name")):
            # eh folder, logo nao deleta
            continue
        if drive.delete_file(id):
            print(f"DELETOU {file.get('name')}")
        else:
            print(f"NAO CONSEGUI: {file.get('name')}")
    print(drive.fetch_drive_files())
    return make_response("OK", OK)


@app.route("/teste_email")
def teste_folder():
    try:
        # MAILHANDLER.enviar_email_usuario(
        #     "recuperar", "luisfelipearaujo503@gmail.com", "TESTE TESTE", "http://localhost:5173/")
        MAILHANDLER.enviar_email_admin(
            "luisfelipearaujo503@gmail.com",
            "FULANO",
            "MA-1234",
            "http://localhost:5173/",
            "http://localhost:5173/",
        )
        return make_response("OK", OK)

    except Exception as e:
        raise e
        return make_response("DEU ALGUMA COISA ERRADA", INTERNAL_SERVER_ERROR)


@app.route("/teste_esquecer")
def teste2():
    diags = mongo.db.get_collection(COLLECTION_DIAGS)
    for diag in diags.find():
        print(diag)


@app.route("/")
def index():
    return "Hello World"


@app.route("/get-file-drive/<id_file>", methods=["GET"])
@cross_origin(supports_credentials=True)
# usando esse decorator pra evitar erros de TLS
def get_file_drive(id_file):
    """
    Serves files using file_id from Google Drive.
    """
    print("FILE ID: ", id_file)
    try:
        limite_mega = 20 * 1024 * 1024  # (20 MB)
        print("PEGANDO ARQUIVO!")
        file_generator, filename = drive.download_file(id_file)
        print("DEPOIS DOWNLOAD")
        return Response(
            stream_with_context(file_generator),
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": mimetypes.guess_type(filename)[0]
                or "application/octet-stream",
            },
        )
    except Exception as e:
        print(f"ERRO AO PEGAR ARQUIVO: {e}")
        return make_response(
            {"error": f"{str(e)}", "file_url": "None"}, INTERNAL_SERVER_ERROR
        )


@app.route("/get-file-local/<filename>", methods=["GET"])
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
            filename = os.path.join(app.config["TEMP_FOLDER"], filename)
            print("FILE NAME GET_LOCAL: ", filename)

            chunk_size = 1024 * 1024

            def file_generator(file_path):
                with open(file_path, "rb") as f:
                    # ':=' walrus operator, designa e avalia variavel 'chunk'
                    while chunk := f.read(chunk_size):  # Read in chunks of 8KB
                        yield chunk

            print(f"BAIXANDO ARQUIVO {filename}")
            return Response(
                stream_with_context(file_generator(filename)),
                headers={
                    "Content-Disposition": f'attachment; filename="{os.path.basename(filename)}"',
                    "Content-Type": mimetypes.guess_type(filename)[0]
                    or "application/octet-stream",
                },
            )
    except Exception as e:
        print(f"ERRO AO PEGAR ARQUIVO: {e}")
        return make_response(
            {"error": f"{str(e)}", "file_url": "None"}, INTERNAL_SERVER_ERROR
        )


@app.route("/get-file/<resource_uri>", methods=["GET"])
@cross_origin(supports_credentials=True)
# usando esse decorator pra evitar erros de TLS
def get_file(resource_uri) -> Union[Any, Response]:
    """
    Serves files depending on storage, prioritizing local storage, then DB, and finally cloud.
    """
    print("URI: ", resource_uri)
    try:
        if resource_uri:
            print("PEGANDO ARQUIVO!")
            # Check local storage first
            local_path = os.path.join(
                app.config["TEMP_FOLDER"], os.path.basename(resource_uri)
            )
            if os.path.exists(local_path):
                print("RETORNANDO ARQUIVO LOCAL")
                return get_file_local(os.path.basename(resource_uri))
            elif drive.check_id(resource_uri):
                print("RETORNANDO ARQUIVO DO DRIVE")
                return get_file_drive(resource_uri)
            else:
                raise Exception("Arquivo não encontrado em nenhuma fonte!")
        else:
            raise Exception("RECURSO NULO!")
    except Exception as e:
        print(f"ERRO AO PEGAR ARQUIVO: {e}")
        return make_response(
            {"error": f"{str(e)}", "file_url": "None"}, INTERNAL_SERVER_ERROR
        )


@app.route("/analise", methods=["POST"])
@cross_origin(supports_credentials=True)
def analisar():
    id_diag = request.form.get("id_diag", None)
    nome_input = request.form.get("nome_input", None)
    filename = request.form.get("filename", None)

    ext = Helper.allowed_file(filename)
    if ext is None:
        print("Incorrect file type!\n\n")
        return make_response("TIPO de ARQUIVO INCORRETO!", BAD_REQUEST)

    if id_diag is None:
        return make_response("INPUT NULO!", BAD_REQUEST)

    task = celery_wrapper.processamento_analise(id_diag, nome_input, filename)

    return jsonify({"task_id": task.id, "status": "Processing started"})


from celery.result import AsyncResult


@app.route("/status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = AsyncResult(task_id)
    if task.state == "PENDING":
        return "Task is still pending"
    elif task.state == "SUCCESS":
        return f"Task completed successfully: {task.result}"
    else:
        return f"Task failed with state: {task.state}"


# @app.route("/analise", methods=["POST"])
# @cross_origin(supports_credentials=True)
# def analisar():
#     """
#     Pega video  input, executa o model e and retorna JSON
#     ### servidor DEVE retorna JSON com string contendo as métricas, pdf de res, VIDEO DE SAIDA e grafico
#     """
#     timestamp = time.time()
#     print(f"KEYS FORM: {request.form.keys()}\n")
#     id_diag = request.form.get("id_diag", None)
#     nome_input = request.form.get("nome_input", None)
#     filename = request.form.get("filename", None)
#     diag = None

#     if id_diag != None:
#         print(request.form)
#         diag = mongo.db.get_collection(COLLECTION_DIAGS).find_one(
#             {"_id": ObjectId(id_diag)}
#         )
#     else:
#         return make_response("INPUT NULO!", BAD_REQUEST)

#     ext = Helper.allowed_file(filename)
#     if ext is None:
#         print("Incorrect file type!\n\n")
#         return make_response("TIPO de ARQUIVO INCORRETO!", BAD_REQUEST)

#     paciente = diag.get("nomePaciente", None)
#     nome_video = f"{paciente}_{str(round(timestamp, 4))}"
#     nome_local = f"{nome_video}.{ext}"
#     filename_arq_input = f"INPUT_{nome_local}"
#     # renomeia arquivo de input na pasta temporaria para filename_arq_input
#     os.rename(
#         os.path.join(app.config["TEMP_FOLDER"], nome_input),
#         os.path.join(app.config["TEMP_FOLDER"], filename_arq_input),
#     )

#     # video deve ser armazenado usando ID do usuario e timestamp, pra garantir multiplicidade
#     path_arq_input = os.path.join(app.config["TEMP_FOLDER"], filename_arq_input)

#     """ se eu nao me engano, logica utilizada para fazer streaming de arquivos grandes
#     arq_stream = arq.stream"""

#     EXT_OUT = "mp4"
#     nome_local = f"{nome_video}.{EXT_OUT}"
#     # path cujo unico proposito eh servir de temporario pras conversoes de video
#     path_aux_conv = os.path.join(app.config["TEMP_FOLDER"], f"CONVERT_{nome_local}")

#     path_arq_input_conv = Helper.converter_arq(path_arq_input, path_aux_conv)
#     print("\nDEPOIS PRIMEIRA CONVER\n")

#     path_out_antes_conv = os.path.join(
#         app.config["TEMP_FOLDER"], f"OUT_PRE_{nome_local}"
#     )

#     # executando predicao
#     res_tensor, dict_graf_tensor = predict(
#         analisador, path_arq_input_conv, path_out_antes_conv, timestamp
#     )

#     with tf.compat.v1.Session() as sess:
#         # Run the session to get the tensor's value
#         res_np = sess.run(res_tensor)
#         if "ERRO" in res_np.decode("utf-8"):
#             return make_response(res_np, BAD_REQUEST)
#         graf_np = sess.run(dict_graf_tensor)

#     # Decode bytes to string since predict returns all output as tensor
#     str_res, dict_graf = res_np.decode("utf-8"), graf_np

#     dict_graf["vel_esq"] = np.array(dict_graf["vel_esq"]).tolist()
#     dict_graf["vel_dir"] = np.array(dict_graf["vel_dir"]).tolist()
#     dict_graf["time"] = float(dict_graf["time"])
#     dict_graf["titulo"] = str(dict_graf["titulo"])

#     path_out = os.path.join(app.config["TEMP_FOLDER"], f"OUT_{nome_local}")
#     print("ULTIMA CONVERSAO")
#     path_out = Helper.converter_arq(path_out_antes_conv, path_out)

#     """Removendo APENAS arquivos auxiliares"""
#     os.remove(path_out_antes_conv)
#     os.remove(path_aux_conv)

#     # path_pdf = os.path.join(
#     #     app.config["TEMP_FOLDER"], f"RELATORIO_{nome_video}.pdf")

#     # str_res no formato "velE,velD,percentDif,olho_doente"
#     split_res = str_res.split(",")
#     olho_doente = str_res.split(",")[3]

#     if olho_doente == "Esquerdo":
#         str_diag = "true+false"
#     elif olho_doente == "Direito":
#         str_diag = "false+true"
#     else:
#         str_diag = "false+false"

#     id_medico = diag.get("id_medico", None)
#     # NOTE: NAO GERA PDF PRA USUARIOS ANONIMOS!
#     if str(id_medico) != "None":
#         diag_medico = diag.get("diagnosticoMedico")  # string codificada
#         nome_paciente = diag.get("nomePaciente")

#         medico = Helper.find_one_with_id(
#             mongo.db.get_collection(COLLECTION_MEDICOS), id_medico
#         )
#         nome_medico = medico.get("nome")
#         crm = medico.get("crm")
#         email_medico = medico.get("email")
#         dict_dados_pdf = {
#             "velEsq": split_res[0],
#             "velDir": split_res[1],
#             "difVel": split_res[2],
#             "crm": crm,
#             "diagAutom": str_diag,
#             "dataAgora": timestamp,
#             "nomePaciente": nome_paciente,
#             "nomeMedico": nome_medico,
#             "diagnosticoMedico": diag_medico,
#         }
#     else:
#         email_medico = PASTA_USUARIO_ANONIMO_GDRIVE
#         dict_dados_pdf = None

#     print("PEGANDO URLS")

#     local_url_video_out = url_for(
#         "get_file", resource_uri=os.path.basename(path_out), _external=True
#     )
#     print(f"LOCAL URL VIDEO OUT: {local_url_video_out}")
#     local_url_video_in = url_for(
#         "get_file", resource_uri=os.path.basename(path_arq_input), _external=True
#     )

#     result = {
#         "diagAutom": str_diag,
#         "dados_grafico": dict_graf,
#         "dados_pdf": dict_dados_pdf,
#         "dataDiag": timestamp,
#         "video": local_url_video_out,
#         "ultimaModif": timestamp,
#     }
#     mongo.db.get_collection(COLLECTION_DIAGS).update_one(
#         {"_id": ObjectId(id_diag)}, {"$set": result}
#     )

#     result["diagAutom"] = str_res

#     storage_dict = {"video_in": path_arq_input, "video_out": path_out}

#     def after_analise():
#         # cria nova thread pra sincronizar com google drive
#         thread = threading.Thread(
#             target=sync_google_drive, args=(storage_dict, id_diag, email_medico)
#         )
#         thread.start()

#     result.pop("dados_grafico")
#     result.pop("dados_pdf")
#     result["grafico"] = url_for(
#         "gerar_grafico", external=True, id_diag=id_diag, _external=True
#     )
#     result["pdf"] = url_for(
#         "gerar_relatorio", id_diag=id_diag, download=True, _external=True
#     )
#     result["video"] = local_url_video_out
#     resp = jsonify(result)
#     resp.call_on_close(after_analise)
#     print("\nANALISE FINALZIADA!")
#     return resp


@app.route("/pega_perfil", methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required
def pega_perfil():
    maxItensPag = 16
    pagAtual = request.args.get("pagAtual", None)
    if pagAtual != None:
        pagAtual = int(pagAtual)

        email_medico = str(current_user.id)
        medico = mongo.db.get_collection(COLLECTION_MEDICOS).find_one(
            {"email": email_medico}
        )
        validado = bool(medico.get("validado", None))
        if not validado:
            print("MEDICO NAO VALIDADADO!")
            return make_response("MEDICO NAO VALIDADO!", UNAUTHORIZED)
        id_medico = str(medico["_id"])
        print("ID MEDICO: ", id_medico)
        res = mongo.db.get_collection(COLLECTION_DIAGS).aggregate(
            [
                {"$match": {"id_medico": id_medico}},
                {
                    "$facet": {
                        "metadata": [{"$count": "totalCount"}],
                        "data": [
                            {"$skip": (pagAtual - 1) * maxItensPag},
                            {"$limit": maxItensPag},
                        ],
                    },
                },
            ],
            allowDiskUse=True,
        )
        lista_res = list(res)[0]["data"]
        # print(f"DIAGS: \n\n{lista_res}\n\n")

        medico = Helper.find_one_with_id(
            mongo.db.get_collection(COLLECTION_MEDICOS), id_medico
        )
        # res = list(mongo.db.get_collection(COLLECTION_DIAGS).find())
        return jsonify(
            {
                "nomeMedico": medico["nome"],
                "crm": medico["crm"],
                "lista": lista_res,
                "maxItensPag": maxItensPag,
            }
        )

    else:
        print("INPUT NULO!")

        return make_response("INPUT NULO!", BAD_REQUEST)


@app.route("/gerar_relatorio/<id_diag>", methods=["GET"])
def gerar_relatorio(id_diag):
    """
    Gera pdf com grafico e outros dados importantes e retorna url do pdf
    """
    download = request.args.get("download", default=False, type=bool)

    diag = Helper.find_one_with_id(mongo.db.get_collection(COLLECTION_DIAGS), id_diag)
    dados_pdf = diag.get("dados_pdf", None)
    if str(dados_pdf) == "None":
        return make_response("NAO TEM PDF!", BAD_REQUEST)

    path_out_pdf = os.path.join(
        app.config["TEMP_FOLDER"], f"{dados_pdf['nomePaciente']}.pdf"
    )
    relpath_output = os.path.relpath(path_out_pdf, app.config["WKDIR"])
    try:
        dados_pdf["urlGrafico"] = gerar_grafico(id_diag, external=False)

        Helper.gerar_pdf(relpath_output, dados_pdf)

        uri_pdf = relpath_output
        if download:
            print(f"BAIXANDO PDF {relpath_output}...")
            return send_file(
                path_out_pdf, as_attachment=True, download_name="Relatorio.pdf"
            )
        else:
            return get_file(uri_pdf)
    except Exception as e:
        print(f"EXCEPTION AO GERAR PDF: {e}")
        return make_response("NAO TEM PDF!", INTERNAL_SERVER_ERROR)


@app.route("/gerar_grafico/<id_diag>", methods=["GET"])
def gerar_grafico(id_diag, external=True):
    """
    Gera grafico e retorna ele como stream
    """

    diag = Helper.find_one_with_id(mongo.db.get_collection(COLLECTION_DIAGS), id_diag)
    dados_grafico = diag.get("dados_grafico", None)
    if str(dados_grafico) == "None":
        return make_response("NAO TEM GRAFICO!", BAD_REQUEST)

    vel_esq, vel_dir, titulo, time = (
        dados_grafico["vel_esq"],
        dados_grafico["vel_dir"],
        dados_grafico["titulo"],
        dados_grafico["time"],
    )

    path_graf = analisador.plotHampelFinal(vel_esq, vel_dir, titulo, time)
    print(f"PATH_GRAF: {path_graf}\n\n")
    uri_graf = path_graf
    print(f"URI DO GRAF: {uri_graf}\n\n")
    if external:
        return get_file(uri_graf)
    else:
        return uri_graf


@app.route("/envia_diag", methods=["POST"])
@cross_origin(supports_credentials=True)
def envia_diag():
    video = request.files.get("video", None)
    nomePaciente = request.form.get("nomePaciente", None)
    stringOlhos = request.form.get("stringOlhos", None)
    desc = request.form.get("desc", None)

    if any(elem is None for elem in [video, nomePaciente]):
        return make_response("INPUT NULO!", BAD_REQUEST)

    filename = video.filename
    video_data = video.read()
    user_id = current_user.id if current_user.is_authenticated else None

    # Enqueue the Celery task
    task = celery_wrapper.envia_diag_task(
        video_data, filename, nomePaciente, stringOlhos, desc, user_id
    )

    return jsonify({"task_id": task.id, "status": "Upload queued"})


# @app.route("/envia_diag", methods=["POST"])
# @cross_origin(supports_credentials=True)
# def envia_diag():
#     """
#     Rota responsavel por receber formulario com diagnostico do medico e guardar dados no BD e no Drive
#     """
#     print("ENVIO DO DIAG")
#     timestamp = time.time()
#     video = request.files.get("video", None)

#     nomePaciente = request.form.get("nomePaciente", None)
#     stringOlhos = request.form.get("stringOlhos", None)

#     desc = request.form.get("desc", None)
#     a = [video, nomePaciente]
#     if any(elem is None for elem in a):
#         return make_response("INPUT NULO!", BAD_REQUEST)

#     diagnosticoMedico = stringOlhos
#     # Check if user is authenticated directly
#     if current_user.is_authenticated:
#         # caso pra usuario logado
#         email_medico = current_user.id
#         medicos = mongo.db.get_collection(COLLECTION_MEDICOS)
#         medico_atual = medicos.find_one({"email": email_medico})
#         if medico_atual is None:
#             return make_response("MEDICO LOGADO NAO ENCONTRADO", INTERNAL_SERVER_ERROR)
#         id_medico = medico_atual.get("_id", None)
#     else:
#         # padronizar dados nulos no BD como None e erros de preenchimento como null
#         id_medico = None

#     print("ID MEDICO: ", id_medico)
#     diags = mongo.db.get_collection(COLLECTION_DIAGS)
#     dados = {
#         "nomePaciente": nomePaciente,
#         "id_medico": str(id_medico),
#         "diagnosticoMedico": diagnosticoMedico,
#         "desc": desc,
#     }

#     # transforma qualquer valor None em string
#     for key, value in dados.items():
#         if value is None:
#             dados[key] = "None"

#     result = diags.insert_one(dados)
#     id_diag_mongo = str(result.inserted_id)
#     print("RESULTADO INSERT: ", result)

#     # escreve dados no video em \tmp e usa timestamp pra evitar duplicatas
#     filename = video.filename
#     nome_local = f"{str(round(timestamp, 4))}_{filename}"
#     video_data = video.read()
#     path_temp_videoLabel = os.path.join(app.config["TEMP_FOLDER"], nome_local)
#     with open(path_temp_videoLabel, "wb") as f:
#         f.write(video_data)

#     print("DIAG ENVIADO!\n")
#     return make_response(
#         {
#             "mensagem": "CARREGADO",
#             "id_diag": id_diag_mongo,
#             "nome_input": nome_local,
#             "filename": filename,
#         },
#         OK,
#     )


@login_manager.user_loader
def load_user(user_id):
    return User.get_user(user_id)


@app.route("/auth", methods=["POST"])
@cross_origin(supports_credentials=True)
def autenticar():
    tipo = request.args.get("tipo", "login")
    email = request.form.get("email")
    senha = request.form.get("senha")
    medicos = mongo.db.get_collection(COLLECTION_MEDICOS)

    if tipo == "login":
        session.permanent = True
        if not email or not senha:
            return make_response("Email ou senha ausentes", BAD_REQUEST)
        usuario = medicos.find_one({"email": email})
        if (
            usuario
            and usuario.get("senha") == alg_hash(senha.encode("utf-8")).hexdigest()
        ):
            user_obj = User(email)
            login_user(user_obj, remember=True)
            return make_response("LOGADO", OK)
        else:
            return make_response("Credenciais inválidas", UNAUTHORIZED)

    elif tipo == "cadastro":
        nome = request.form.get("nome")
        crm = request.form.get("crm")
        # checando valores
        if not any(valor for valor in [email, senha, nome, crm]):
            return make_response("Dados de cadastro ausentes", BAD_REQUEST)

        # Usuario ja existe
        if medicos.find_one({"email": email}):
            return make_response("JA_EXISTE", OK)

        senha_hash = alg_hash(senha.encode("utf-8")).hexdigest()
        medicos.insert_one(
            {
                "email": email,
                "nome": nome,
                "crm": crm,
                "senha": senha_hash,
                "validado": False,
            }
        )

        # loga usuario
        user_obj = User(email)
        login_user(user_obj, remember=True)

        # TODO: ENVIAR EMAIL DE CADASTRO PARA ADMIN
        urlAceita = url_for("aceitar_cadastro", email_medico=email, _external=True)
        urlRecusa = url_for("recusar_cadastro", email_medico=email, _external=True)
        MAILHANDLER.enviar_email_admin(email, nome, crm, urlAceita, urlRecusa)
        drive.create_folder([email])

        return make_response("CADASTRADO", OK)
    else:
        return make_response("Tipo inválido", BAD_REQUEST)


@app.route("/aceitaCadastro/<email_medico>", methods=["GET", "POST"])
def aceitar_cadastro(email_medico):
    try:
        mongo.db.get_collection(COLLECTION_MEDICOS).update_one(
            {"email": email_medico}, {"$set": {"validado": True}}
        )

        a = MAILHANDLER.enviar_email_usuario(
            "cadastroOK", email_medico, "Cadastro Validado!", DOMINIO_FRONT_VUE
        )
        if not a:
            raise Exception("Não foi possível enviar email!!!")

        return make_response(f"EMAIL ENVIADO!", OK)
    except Exception as e:
        print(f"ERRO AO ENVIAR EMIAL DE CADASTRO: {e}")
        return make_response(f"{e}", INTERNAL_SERVER_ERROR)


@app.route("/recusaCadastro/<email_medico>", methods=["GET", "POST"])
def recusar_cadastro(email_medico):
    try:
        a = MAILHANDLER.enviar_email_usuario(
            "cadastroInvalido", email_medico, "Cadastro Inválido!", EMAIL_ADMIN
        )
        if not a:
            raise Exception("Não foi possível enviar email!!!")
        mongo.db.get_collection(COLLECTION_MEDICOS).delete_one({"email": email_medico})

        return make_response(f"EMAIL ENVIADO!", OK)
    except Exception as e:
        print(f"ERRO AO ENVIAR EMIAL DE CADASTRO: {e}")
        return make_response(f"{e}", INTERNAL_SERVER_ERROR)


@app.route("/esqueci_senha", methods=["POST"])
def esqueci():
    emailDestino = request.form.get("email", None)
    url_front = request.form.get("url_front", None)

    print(f"URL FRONT: {url_front}")
    if emailDestino:
        # TODO:  codigo para enviar email de recuperacao para medico
        medicos = mongo.db.get_collection(COLLECTION_MEDICOS)
        medico = medicos.find_one({"email": emailDestino})
        if medico is None:
            return make_response("Email Inválido!", UNAUTHORIZED)

        assunto = "Recuperação de Senha"
        MAILHANDLER.enviar_email_usuario("recuperar", emailDestino, assunto, url_front)

        return make_response("OK", OK)
    else:
        return make_response("Email Inválido!", BAD_REQUEST)


@app.route("/mudar_senha", methods=["POST"])
def mudar_senha():
    email = request.form.get("email", None)
    novaSenha = request.form.get("novaSenha", None)
    print("COMECANDO MUDANCA")
    if novaSenha is None or email is None:
        print("INPUT NULO")
        return make_response(f"INPUT NULO!", UNAUTHORIZED)
    novaSenha = alg_hash(novaSenha.encode("utf-8")).hexdigest()

    medicos = mongo.db.get_collection(COLLECTION_MEDICOS)
    medico = medicos.find_one({"email": email})

    if medico == None:
        return make_response("EMAIL NAO EXISTE", BAD_REQUEST)
    else:
        medicos.update_one({"email": email}, {"$set": {"senha": novaSenha}})
        print("SENHA ATUALIZADA")
        return make_response("SENHA ATUALIZADA!", OK)


@app.route("/val_login", methods=["GET"])
@cross_origin(supports_credentials=True)
def val_login():
    """
    Valida cookies de sessao do usuario usando flask-login
    """
    print(current_user)
    if not current_user.is_authenticated:
        print("USUÁRIO NÃO AUTENTICADO OU SESSÃO EXPIRADA")
        return make_response("False", UNAUTHORIZED)
    else:
        """
        # Check if user exists in database
        usuario = Helper.find_one_with_id(
            mongo.db.get_collection(COLLECTION_MEDICOS), str(current_user.id))
        if usuario is not None and current_user.is_authenticated:

        else:
            print("USUARIO INEXISTE OU SESSAO EXPIRADA!!!!!")
            return make_response("False", INTERNAL_SERVER_ERROR)
        """
        print("LOGADO")

        return make_response("LOGADO", OK)


@app.route("/logout")
@cross_origin(supports_credentials=True)
@login_required
def logout():
    try:
        logout_user()
        response = make_response(redirect(url_for("val_login")))
        # Overwrite cookie with expired date to remove it from browser
        response.set_cookie(
            "session",
            "",
            expires=0,
            path="/",
            secure=True,
            httponly=True,
            samesite="None",
            partitioned=True,
        )
        response.delete_cookie("remember_token")
        return response

    except Exception as e:
        print(f"EXCEPTION!!!: {e}")
        return make_response(f"{e}", INTERNAL_SERVER_ERROR)


if __name__ != "__main__":
    # NOTE: para poder adicionar um sheduler de tasks de background, adicionar use_reloader=False
    # app.run(host="0.0.0.0")
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
