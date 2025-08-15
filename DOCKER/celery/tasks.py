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
import logging


@celery.task(bind=True)
# NAO RETIRAR SELF!
def processamento_analise(self, id_diag, nome_input, filename):

    timestamp = time.time()
    diag = mongo.db.get_collection(COLLECTION_DIAGS).find_one(
        {"_id": ObjectId(id_diag)}
    )

    ext = Helper.allowed_file(filename)
    if ext is None:
        return {"error": "Incorrect file type"}

    paciente = diag.get("nomePaciente", None)
    nome_video = f"{paciente}_{str(round(timestamp, 4))}"
    nome_local = f"{nome_video}.{ext}"
    filename_arq_input = f"INPUT_{nome_local}"
    # renomeia arquivo de input na pasta temporaria para filename_arq_input
    os.rename(
        os.path.join(app.config["TEMP_FOLDER"], nome_input),
        os.path.join(app.config["TEMP_FOLDER"], filename_arq_input),
    )

    # video deve ser armazenado usando ID do usuario e timestamp, pra garantir multiplicidade
    path_arq_input = os.path.join(app.config["TEMP_FOLDER"], filename_arq_input)

    """ se eu nao me engano, logica utilizada para fazer streaming de arquivos grandes
    arq_stream = arq.stream"""

    EXT_OUT = "mp4"
    nome_local = f"{nome_video}.{EXT_OUT}"
    # path cujo unico proposito eh servir de temporario pras conversoes de video
    path_aux_conv = os.path.join(app.config["TEMP_FOLDER"], f"CONVERT_{nome_local}")

    path_arq_input_conv = Helper.converter_arq(path_arq_input, path_aux_conv)
    print("\nDEPOIS PRIMEIRA CONVER\n")

    path_out_antes_conv = os.path.join(
        app.config["TEMP_FOLDER"], f"OUT_PRE_{nome_local}"
    )

    # executando predicao
    res_tensor, dict_graf_tensor = predict(
        analisador, path_arq_input_conv, path_out_antes_conv, timestamp
    )

    with tf.compat.v1.Session() as sess:
        # Run the session to get the tensor's value
        res_np = sess.run(res_tensor)
        if "ERRO" in res_np.decode("utf-8"):
            return make_response(res_np, BAD_REQUEST)
        graf_np = sess.run(dict_graf_tensor)

    # Decode bytes to string since predict returns all output as tensor
    str_res, dict_graf = res_np.decode("utf-8"), graf_np

    dict_graf["vel_esq"] = np.array(dict_graf["vel_esq"]).tolist()
    dict_graf["vel_dir"] = np.array(dict_graf["vel_dir"]).tolist()
    dict_graf["time"] = float(dict_graf["time"])
    dict_graf["titulo"] = str(dict_graf["titulo"])

    path_out = os.path.join(app.config["TEMP_FOLDER"], f"OUT_{nome_local}")
    print("ULTIMA CONVERSAO")
    path_out = Helper.converter_arq(path_out_antes_conv, path_out)

    """Removendo APENAS arquivos auxiliares"""
    os.remove(path_out_antes_conv)
    os.remove(path_aux_conv)

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

    id_medico = diag.get("id_medico", None)
    # NOTE: NAO GERA PDF PRA USUARIOS ANONIMOS!
    if str(id_medico) != "None":
        diag_medico = diag.get("diagnosticoMedico")  # string codificada
        nome_paciente = diag.get("nomePaciente")

        medico = find_one_with_id(
            mongo.db.get_collection(COLLECTION_MEDICOS), id_medico
        )
        nome_medico = medico.get("nome")
        crm = medico.get("crm")
        email_medico = medico.get("email")
        dict_dados_pdf = {
            "velEsq": split_res[0],
            "velDir": split_res[1],
            "difVel": split_res[2],
            "crm": crm,
            "diagAutom": str_diag,
            "dataAgora": timestamp,
            "nomePaciente": nome_paciente,
            "nomeMedico": nome_medico,
            "diagnosticoMedico": diag_medico,
        }
    else:
        email_medico = PASTA_USUARIO_ANONIMO_GDRIVE
        dict_dados_pdf = None

    print("PEGANDO URLS")

    local_url_video_out = url_for(
        "get_file", resource_uri=os.path.basename(path_out), _external=True
    )
    print(f"LOCAL URL VIDEO OUT: {local_url_video_out}")
    local_url_video_in = url_for(
        "get_file", resource_uri=os.path.basename(path_arq_input), _external=True
    )

    result = {
        "diagAutom": str_diag,
        "dados_grafico": dict_graf,
        "dados_pdf": dict_dados_pdf,
        "dataDiag": timestamp,
        "video": local_url_video_out,
        "ultimaModif": timestamp,
    }
    # seta resultado no BD
    mongo.db.get_collection(COLLECTION_DIAGS).update_one(
        {"_id": ObjectId(id_diag)}, {"$set": result}
    )

    result["diagAutom"] = str_res

    storage_dict = {"video_in": path_arq_input, "video_out": path_out}

    sync_google_drive.delay(storage_dict, id_diag, email_medico)

    result.pop("dados_grafico")
    result.pop("dados_pdf")
    result["grafico"] = url_for(
        "gerar_grafico", external=True, id_diag=id_diag, _external=True
    )
    result["pdf"] = url_for(
        "gerar_relatorio", id_diag=id_diag, download=True, _external=True
    )
    result["video"] = local_url_video_out
    print("\nANALISE FINALZIADA!")

    return {
        "result": result,
        "grafico_url": url_for(
            "gerar_grafico", external=True, id_diag=id_diag, _external=True
        ),
        "pdf_url": url_for(
            "gerar_relatorio", id_diag=id_diag, download=True, _external=True
        ),
        "video_url": local_url_video_out,
    }


@celery.task
def envia_diag_task(video_data, filename, nomePaciente, stringOlhos, desc, user_id):
    import os
    from bson import ObjectId

    timestamp = time.time()

    diagnosticoMedico = stringOlhos
    if user_id:
        medicos = mongo.db.get_collection(COLLECTION_MEDICOS)
        medico_atual = medicos.find_one({"email": user_id})
        if medico_atual is None:
            return {"error": "MEDICO LOGADO NAO ENCONTRADO"}
        id_medico = medico_atual.get("_id", None)
    else:
        id_medico = None

    dados = {
        "nomePaciente": nomePaciente,
        "id_medico": str(id_medico),
        "diagnosticoMedico": diagnosticoMedico,
        "desc": desc,
    }

    # Convert None to string "None"
    for key, value in dados.items():
        if value is None:
            dados[key] = "None"

    diags = mongo.db.get_collection(COLLECTION_DIAGS)
    result = diags.insert_one(dados)
    id_diag_mongo = str(result.inserted_id)

    nome_local = f"{str(round(timestamp, 4))}_{filename}"
    path_temp_videoLabel = os.path.join(app.config["TEMP_FOLDER"], nome_local)

    with open(path_temp_videoLabel, "wb") as f:
        f.write(video_data)

    return {
        "mensagem": "CARREGADO",
        "id_diag": id_diag_mongo,
        "nome_input": nome_local,
        "filename": filename,
    }
