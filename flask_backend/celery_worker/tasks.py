from http.client import (
    BAD_GATEWAY,
    BAD_REQUEST,
    INTERNAL_SERVER_ERROR,
    OK,
    UNAUTHORIZED,
)
from json import dumps
import json
import time
from traceback import print_exc
from bson import ObjectId
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
import tensorflow as tf
from celery import Task
import numpy as np

from pymongo import MongoClient
import posixpath


from flask_backend.analise import AnaliseParalisia
from flask_backend import (
    BASE_URL,
    COLLECTION_DIAGS,
    COLLECTION_MEDICOS,
    PASTA_USUARIO_ANONIMO_GDRIVE,
)

from .celery import app
from flask_backend.drive import GoogleDrive
from flask_backend.helpers import Helper, get_modelo


# PASTA_USUARIO_ANONIMO_GDRIVE = "ANONIMO"
DB_PARALISIA = "PARALISIA6_NERVO"


# classe abstrata pra instanciar GoogleDrive e Mongo
class MainTask(Task):
    _drive = None
    _mongo = None

    _coll_diags = None
    _coll_meds = None

    @property
    def coll_diags(self):
        if self._coll_diags is None:
            self._coll_diags = COLLECTION_DIAGS
        return self._coll_diags

    @property
    def coll_meds(self):
        if self._coll_meds is None:
            self._coll_meds = COLLECTION_MEDICOS
        return self._coll_meds

    @property
    def drive(self):
        if self._drive is None:
            from flask_backend import PATH_CRED, ROOT_DRIVE

            self._drive = GoogleDrive(PATH_CRED, ROOT_DRIVE)
        return self._drive

    @property
    def mongo(self):
        if self._mongo is None:
            self._mongo = MongoClient(os.environ.get("MONGO_URI"))
        return self._mongo


# @tf.function
def predict(analisador: AnaliseParalisia, path_processamento_arq, path_out, timestamp):
    # modelo = analisador.modelo

    str_res, dict_graf = analisador.funcao_metodo(
        path_processamento_arq, path_out, timestamp
    )
    str_res = tf.convert_to_tensor(str_res)

    # essa parte transforma qualquer elemento que nao seja int em int
    dict_graf["vel_esq"] = list(
        map(lambda x: x.item() if type(x) == np.int64 else x, dict_graf["vel_esq"])
    )
    dict_graf["vel_dir"] = list(
        map(lambda x: x.item() if type(x) == np.int64 else x, dict_graf["vel_dir"])
    )
    dict_graf = dumps(dict_graf)
    print(f"DICT GRAF DUMP: {dict_graf}\n")
    dict_graf = tf.convert_to_tensor(dict_graf)

    return str_res, dict_graf


# WARNING: Tasks foram criadas para serem executadas em sequencia, mas fora do FLASK!!!!!!!
class EnviaDiagTask(MainTask):
    # name = "envia_diag_task"
    pass

class AnaliseTask(MainTask):
    """TASK PRINCIPAL DO CELERY PARA PROCESSAMENTO PESADO E ASSINCRONO!"""

    _helper = None
    _analisador = None

    # name = "processamento_analise"

    def __init__(self):
        super().__init__()

    @property
    def helper(self):
        if self._helper is None:
            self._helper = Helper()
        return self._helper

    @property
    def analisador(self):
        if self._analisador is None:
            modelo = get_modelo()
            # NOTE: MODELO DEVE TER FUNCAO detect_image implementada
            self._analisador = AnaliseParalisia(modelo, None)
        return self._analisador

    

# NOTE: ARGUMENTOS DEVEM SER APENAS OBJETOS SERIALIZAVEIS (SEM SER OBJETOS COMPLEXOS)
class SyncDriveTask(MainTask):
    # name = "sync_google_drive"
    pass
    

@app.task(base=EnviaDiagTask, bind=True)
def envia_diag_task(
    self,
    video_data,
    filename,
    nomePaciente,
    stringOlhos,
    desc,
    user_id,
    TEMP_FOLDER: str,
    timestamp,
):

    print(f"\nCONEXAO MONGO: {self.mongo.get_database(DB_PARALISIA)}\n")
    diagnosticoMedico = stringOlhos

    if user_id:
        db = self.mongo.get_database(DB_PARALISIA)
        medicos = db.get_collection(self.coll_meds)
        medico_atual = medicos.find_one({"email": user_id})
        print(f"\nUSER ID: {user_id}\n")
        print(f"\nCOLLECTION MEDICOS: {medicos} \n")
        print(f"\nTODOS OS MEDICOS: {list(medicos.find({'email': user_id}))} \n")
        print(f"\nMEDICO ATUAL: {medico_atual}\n")

        if medico_atual is None:
            raise Exception("MEDICO LOGADO NAO ENCONTRADO")
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

    diags = db.get_collection(self.coll_diags)
    print(f"DIAGS: {diags}")
    result = diags.insert_one(dados)
    id_diag_mongo = str(result.inserted_id)

    nome_local = f"{str(round(timestamp, 4))}_{filename}"
    path_temp_videoLabel = os.path.join(TEMP_FOLDER, nome_local)

    with open(path_temp_videoLabel, "wb") as f:
        f.write(video_data)
    print("ENVIA DIAG TERMINADO\n")
    return {
        "mensagem": "CARREGADO",
        "id_diag": id_diag_mongo,
        "nome_input": nome_local,
    }


@app.task(base=AnaliseTask, bind=True)
def processamento_analise(self, res_anterior, **kwargs):
    """
    Funcao deve: registrar dados no BD, pegar o que tiver que pegar pra processar, processar e guardar dados no BD
    """
    # ------------INPUT----------------#
    filename = kwargs.get("filename")
    TEMP_FOLDER = kwargs.get("TEMP_FOLDER")
    timestamp = kwargs.get("timestamp")

    id_diag = res_anterior.get("id_diag")
    nome_input = res_anterior.get("nome_input")
    mensagem = res_anterior.get("mensagem")
    print(f"ESTADO ATUAL TASKS: {mensagem}\n")

    db = self.mongo.get_database(DB_PARALISIA)

    # --------PREPARANDO PROCESSAMENTO---------#
    print(f"COLLECTION: {db.get_collection(self.coll_diags)}\n")
    diag = db.get_collection(self.coll_diags).find_one({"_id": ObjectId(id_diag)})
    self.analisador.path_temp = TEMP_FOLDER
    ext = self.helper.allowed_file(filename)

    if ext is None:
        return {"error": "Incorrect file type"}

    paciente = diag.get("nomePaciente", None)
    nome_video = f"{paciente}_{str(round(timestamp, 4))}"
    nome_local = f"{nome_video}.{ext}"
    filename_arq_input = f"INPUT_{nome_local}"
    # renomeia arquivo de input na pasta temporaria para filename_arq_input
    os.rename(
        os.path.join(TEMP_FOLDER, nome_input),
        os.path.join(TEMP_FOLDER, filename_arq_input),
    )

    # video deve ser armazenado usando ID do usuario e timestamp, pra garantir multiplicidade
    path_arq_input = os.path.join(TEMP_FOLDER, filename_arq_input)

    """ se eu nao me engano, logica utilizada para fazer streaming de arquivos grandes
    arq_stream = arq.stream"""

    EXT_OUT = "mp4"
    nome_local = f"{nome_video}.{EXT_OUT}"
    # path cujo unico proposito eh servir de temporario pras conversoes de video
    path_aux_conv = os.path.join(TEMP_FOLDER, f"CONVERT_{nome_local}")

    path_arq_input_conv = self.helper.converter_arq(path_arq_input, path_aux_conv)
    print("\nDEPOIS PRIMEIRA CONVER\n")

    path_out_antes_conv = os.path.join(TEMP_FOLDER, f"OUT_PRE_{nome_local}")

    # --------- executando predicao ------------
    res_tensor, dict_graf_tensor = predict(
        self.analisador, path_arq_input_conv, path_out_antes_conv, timestamp
    )

    # --------- executando predicao ------------
    print(res_tensor, type(res_tensor))
    print(dict_graf_tensor, type(dict_graf_tensor))
    with tf.compat.v1.Session() as sess:
        # Run the session to get the tensor's value
        res_np = sess.run(res_tensor)
        if "ERRO" in res_np.decode("utf-8"):
            raise Exception("DEU ERRO: ", BAD_REQUEST)
        graf_np = sess.run(dict_graf_tensor)

    # Decode bytes to string since predict returns all output as tensor
    str_res = res_np.decode("utf-8")
    dict_graf_string = graf_np.decode("utf-8")
    dict_graf = json.loads(dict_graf_string)

    dict_graf["vel_esq"] = np.array(dict_graf["vel_esq"]).tolist()
    dict_graf["vel_dir"] = np.array(dict_graf["vel_dir"]).tolist()
    dict_graf["time"] = float(dict_graf["time"])
    dict_graf["titulo"] = str(dict_graf["titulo"])

    path_out = os.path.join(TEMP_FOLDER, f"OUT_{nome_local}")
    path_out = self.helper.converter_arq(path_out_antes_conv, path_out)
    print("ULTIMA CONVERSAO")

    """Removendo APENAS arquivos auxiliares"""
    os.remove(path_out_antes_conv)
    os.remove(path_aux_conv)

    # path_pdf = os.path.join(
    #     TEMP_FOLDER, f"RELATORIO_{nome_video}.pdf")

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

        medico = self.helper.find_one_with_id(
            db.get_collection(self.coll_meds),
            id_medico,
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
    local_url_video_out = (
        posixpath.join(BASE_URL, "get_file", os.path.basename(path_out))
    )

    local_url_video_in = (
        posixpath.join(BASE_URL, "get_file", os.path.basename(path_arq_input))
    )
    print(f"LOCAL URL VIDEO OUT: {local_url_video_out}")

    result = {
        "diagAutom": str_diag,
        "dados_grafico": dict_graf,
        "dados_pdf": dict_dados_pdf,
        "dataDiag": timestamp,
        "video": local_url_video_out,
        "ultimaModif": timestamp,
    }
    # seta resultado no BD
    db.get_collection(self.coll_diags).update_one(
        {"_id": ObjectId(id_diag)}, {"$set": result}
    )

    result["diagAutom"] = str_res

    storage_dict = {"video_in": path_arq_input, "video_out": path_out}

    result.pop("dados_grafico")
    result.pop("dados_pdf")
    print(f"BASE_URL: {BASE_URL}\n")
    result["grafico"] = posixpath.join(BASE_URL, "gerar_grafico", id_diag)
    result["pdf"] = posixpath.join(BASE_URL, "gerar_relatorio", id_diag)

    result["video"] = local_url_video_out
    print("ANALISE FINALZIADA!")

    return {
        "result": result,
        "grafico_url": posixpath.join(BASE_URL, "gerar_grafico", id_diag),
        "pdf_url": posixpath.join(BASE_URL, "gerar_relatorio", id_diag),
        "video_url": local_url_video_out,
        "storage_strings": storage_dict,
        "id_diag": id_diag,
        "email": email_medico,
    }
    # sync_google_drive.delay(storage_dict, id_diag, email_medico)


@app.task(base=SyncDriveTask, bind=True)
def sync_google_drive(self, res_anterior):
    # -----INPUT--------#
    try:

        storage_strings = res_anterior.get("storage_strings")
        id_diag = res_anterior.get("id_diag")
        email = res_anterior.get("email")

        print(f"STORAGE: {storage_strings}, ID: {id_diag}")
        # --------SYNC---------#
        path_video_in = storage_strings["video_in"]
        path_video_out = storage_strings["video_out"]
        print(f"ANTES ID_IN: INSTANCIA DRIVE: {self.drive}")
        id_in = self.drive.upload_to_drive(path_video_in, [email])
        print("ANTES ID_OUT")
        id_out = self.drive.upload_to_drive(path_video_out, [email])
        print("ANTES DEPOIS ID_OUT")

        db = self.mongo.get_database(DB_PARALISIA)
        print("ANTES DB")
        # Update the document in the database with the new Google Drive file IDs
        db.get_collection("diagnosticos").update_one(
            {"_id": ObjectId(id_diag)}, {"$set": {"video_in": id_in, "video": id_out}}
        )

        print("UPLOAD COMPLETO! ANÁLISE TERMINADA!\n\n")
        res_anterior.pop("storage_strings")
        res_anterior.pop("id_diag")
        res_anterior.pop("email")
        return res_anterior
    except Exception as e:
        print(f"ERRO NA PARTE DE UPLOAD: {e}")
        print_exc()
        raise
