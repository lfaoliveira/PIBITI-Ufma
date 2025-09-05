from http.client import (
    BAD_GATEWAY,
    BAD_REQUEST,
    INTERNAL_SERVER_ERROR,
    OK,
    UNAUTHORIZED,
    NOT_MODIFIED,
    NOT_FOUND,
)
import time
import uuid
from bson import ObjectId
import shutil
from flask_backend.analise import AnaliseParalisia
import os

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


### IMPORTS PRA WEBSOCKET
from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.responses import PlainTextResponse


import mimetypes
import hashlib
from datetime import timedelta
from typing import Any, Union
import tensorflow as tf
import numpy as np


from flask_backend.pdf import Converter
from flask_backend.drive import GoogleDrive
from flask_backend._email import MailHandler
from flask_backend.user import User

import logging

from flask_backend.celery_worker.tasks import envia_diag_task, processamento_analise


@tf.function
def predict(analisador: AnaliseParalisia, path_processamento_arq, path_out, timestamp):
    modelo = analisador.modelo
    with modelo.sess.graph.as_default():
        str_res, dict_graf = analisador.funcao_metodo(
            path_processamento_arq, path_out, timestamp
        )

        return str_res, dict_graf


# ------------- VARIAVEIS GLOBAIS--------------#
from flask_backend import (
    COLLECTION_DIAGS,
    COLLECTION_MEDICOS,
    PASTA_USUARIO_ANONIMO_GDRIVE,
)

# Read environment variables from CSV
# arq_config = "./env.csv"
# Helper.read_ENV_VARS(arq_config) NOTE: DEPRECATED
# load_dotenv()

app = Flask(__name__)
app.config.from_object(__name__)

app.config["MONGO_URI"] = os.environ["MONGO_URI"]

# Flask app config example:
# app.config.update()
mongo = PyMongo(app)


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
PATH_flask_backend = os.path.join(PATH_PIBITI, "flask_backend")
EMAIL_ADMIN = "viplab.psno@nca.ufma.br"
DOMINIO_SITE = "http://localhost:5000"
# DOMINIO_FRONT_VUE = "http://localhost:5173"
DOMINIO_FRONT_VUE = os.environ.get("VUE_FRONT_URL")

if "WKDIR" not in app.config.keys():
    app.config["WKDIR"] = PATH_flask_backend
    print("SETTING WKDIR TO APP.CONFIG")
if "PIBITI" == os.path.basename(PATH_PIBITI):
    os.chdir(app.config["WKDIR"])
    print(f"CHANGING DIR TO {os.getcwd()}")

# app.config["WKDIR"] = os.getcwd()

PATH_CRED = os.path.join(
    app.config["WKDIR"], "permalink-googleDrive-pibiti6-nervo.json"
)
if not os.path.exists(PATH_CRED):
    raise FileNotFoundError(f"\n\nSEM CHAVE DE API DO GOOGLE DRIVE {PATH_CRED}!\n\n")
    exit(1)

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

path_pesos_yolo = os.path.join(app.config["WKDIR"], "trained_weights_final.h5")
if not os.path.exists(path_pesos_yolo):
    raise Exception(
        f"PESO YOLOv3 NAO EXISTE!!! BAIXE O ARQUIVO: trained_weights_final.h5 PARA PROSSEGUIR"
    )


app.config["TEMP_FOLDER"] = os.path.join(app.config["WKDIR"], "tmp")
os.makedirs(app.config["TEMP_FOLDER"], exist_ok=True)
video_demo = os.path.join(app.config["WKDIR"], "demoInput.mp4")

# --------------------- MODELO --------------------------#


@app.route("/teste_pdf")
def teste_pdf():
    """FUNCAO DE TESTE QUE DEVE PEGAR DADOS DO DIAGNOSTICO E RETORNAR PDF renderizado

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


@app.route("/analise", methods=["PUT"])
@cross_origin(supports_credentials=True)
def analisar():
    data = request.form
    id_diag = data.get("id_diag", None)
    nome_input = data.get("nome_input", None)
    filename = data.get("filename", None)

    if id_diag is None:
        return make_response("INPUT NULO!", BAD_REQUEST)

    # Enqueue the celery task
    task = processamento_analise.delay(
        id_diag, nome_input, filename, app.config["TEMP_FOLDER"]
    )

    return jsonify({"task_id": task.id, "status": "Processing started"})


from celery.result import AsyncResult


@app.route("/status/<task_id>", methods=["GET"])
def task_status(task_id):
    try:
        task = AsyncResult(task_id)
        if task.state == "PENDING":
            return make_response(
                jsonify({"dados": "", "message": "PENDING"}), NOT_MODIFIED
            )
        elif task.state == "SUCCESS":
            return make_response(
                jsonify({"dados": task.result, "message": "SUCCESS"}), OK
            )
        else:
            return make_response(
                jsonify({"dados": task.result, "message": "FAILED"}),
                INTERNAL_SERVER_ERROR,
            )
    except Exception as e:
        print(f"EXCEPTION NO STATUS DA TASK: {e}\n")
        return make_response(
            f"TASK DOESNT EXIST! OR SOMETHING ELSE FAILED!:\n",
            NOT_FOUND,
        )


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

        Helper.gerar_pdf(relpath_output, app.config["WKDIR"], dados_pdf)

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

    # Instantiate the analyzer from the task to access its methods
    analisador = processamento_analise.analisador
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
    """ task = celery_wrapper.envia_diag(
        video_data, filename, nomePaciente, stringOlhos, desc, user_id
    ) """
    task = envia_diag_task.delay(
        video_data,
        filename,
        nomePaciente,
        stringOlhos,
        desc,
        user_id,
        app.config["TEMP_FOLDER"],
    )

    return jsonify({"task_id": task.id, "status": "Upload queued"})


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


# -----------------------------------------------#
# -----------------------------------------------#
# ------------------WEBSOCKETS-------------------#
# -----------------------------------------------#
# -----------------------------------------------#


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    data = request.json or {}
    print(data)
    form_id = str(uuid.uuid4())
    record = {"_id": form_id, "data": data}
    # forms_coll.insert_one(record)
    return jsonify({"uuid": form_id})


async def ws_handler(ws):
    await ws.accept()
    msg = await ws.receive_text()
    # Expect the UUID
    await ws.send_json({"status": "processing started", "uuid": msg})
    time.sleep(30)  # simulate long task
    # Return dummy response
    resp = {
        "uuid": msg,
        "video_url": "http://example.com/video.mp4",
        "text": "Processing complete!",
    }
    await ws.send_json(resp)
    await ws.close()


# Starlette app for WebSockets
starlette_app = Starlette(
    routes=[
        Route("/ping", lambda request: PlainTextResponse("Pong!")),  # test route
        WebSocketRoute("/ws", ws_handler),
    ]
)
from starlette.middleware.cors import CORSMiddleware

starlette_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ != "__main__":
    # NOTE: para poder adicionar um sheduler de tasks de background, adicionar use_reloader=False
    # app.run(host="0.0.0.0")
    from flask_backend.helpers import Helper

    print("\n\n SERVIDOR INICIADO!\n\n")
    # LEGACY: GUnicorn nao sendo mais usado
    from asgiref.wsgi import WsgiToAsgi
    from starlette.middleware.wsgi import WSGIMiddleware

    # --- Combine both ---
    # Mount Flask under /api, WebSockets under /
    flask_app = app
    starlette_app.mount("/api", WSGIMiddleware(flask_app))
    asgi_app = starlette_app

    # gunicorn_logger = logging.getLogger("gunicorn.error")
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)
