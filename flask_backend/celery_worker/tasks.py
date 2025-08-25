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
from typing import Any, Union
import tensorflow as tf
from celery import Task
import numpy as np

from pymongo import MongoClient

from analise import AnaliseParalisia
from flask_backend import (
    COLLECTION_DIAGS,
    COLLECTION_MEDICOS,
    PASTA_USUARIO_ANONIMO_GDRIVE,
)

from .celery import app
from drive import GoogleDrive
from server import Helper, get_modelo


PASTA_USUARIO_ANONIMO_GDRIVE = "ANONIMO"


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
            self._drive = GoogleDrive(PATH_CRED, ROOT_DRIVE)
        return self._drive

    @property
    def mongo(self):
        if self._mongo is None:
            self._mongo = MongoClient(os.environ.get("MONGO_URI"))
        return self._mongo


@tf.function
def predict(analisador: AnaliseParalisia, path_processamento_arq, path_out, timestamp):
    modelo = analisador.modelo
    with modelo.sess.graph.as_default():
        str_res, dict_graf = analisador.funcao_metodo(
            path_processamento_arq, path_out, timestamp
        )

        return str_res, dict_graf


# TODO: ARGUMENTOS DEVEM SER APENAS OBJETOS SERIALIZAVEIS (SEM SER OBJETOS COMPLEXOS)
class SyncDriveTask(MainTask):
    def run(self, storage_strings: dict, id_diag: str, email: str):
        print(f"STORAGE: {storage_strings}, ID: {id_diag}")
        path_video_in = storage_strings["video_in"]
        path_video_out = storage_strings["video_out"]
        id_in = self.drive.upload_to_drive(path_video_in, [email])
        id_out = self.drive.upload_to_drive(path_video_out, [email])

        # Update the document in the database with the new Google Drive file IDs
        self.mongo.db.get_collection("diagnosticos").update_one(
            {"_id": ObjectId(id_diag)}, {"$set": {"video_in": id_in, "video": id_out}}
        )

        print("UPLOAD COMPLETO! ANÁLISE TERMINADA")
        return None


class AnaliseTask(MainTask):

    _helper = None
    _analisador = None

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

    def run(
        self,
        id_diag,
        nome_input,
        filename,
        TEMP_FOLDER,
    ):

        timestamp = time.time()
        diag = self.mongo.db.get_collection(self.coll_diags).find_one(
            {"_id": ObjectId(id_diag)}
        )
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

        # executando predicao
        res_tensor, dict_graf_tensor = predict(
            self.analisador, path_arq_input_conv, path_out_antes_conv, timestamp
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

        path_out = os.path.join(TEMP_FOLDER, f"OUT_{nome_local}")
        print("ULTIMA CONVERSAO")
        path_out = self.helper.converter_arq(path_out_antes_conv, path_out)

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
                self.mongo.db.get_collection(self.coll_meds), id_medico
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
        self.mongo.db.get_collection(self.coll_diags).update_one(
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


class EnviaDiagTask(MainTask):
    def run(
        self,
        video_data,
        filename,
        nomePaciente,
        stringOlhos,
        desc,
        user_id,
        TEMP_FOLDER: str,
    ):
        import os

        timestamp = time.time()

        diagnosticoMedico = stringOlhos
        if user_id:
            medicos = self.mongo.db.get_collection(self.coll_meds)
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

        diags = self.mongo.db.get_collection(self.coll_diags)
        result = diags.insert_one(dados)
        id_diag_mongo = str(result.inserted_id)

        nome_local = f"{str(round(timestamp, 4))}_{filename}"
        path_temp_videoLabel = os.path.join(TEMP_FOLDER, nome_local)

        with open(path_temp_videoLabel, "wb") as f:
            f.write(video_data)

        return {
            "mensagem": "CARREGADO",
            "id_diag": id_diag_mongo,
            "nome_input": nome_local,
            "filename": filename,
        }


sync_google_drive = SyncDriveTask()
processamento_analise = AnaliseTask()
envia_diag_task = EnviaDiagTask()

app.tasks.register(sync_google_drive)
app.tasks.register(processamento_analise)
app.tasks.register(envia_diag_task)


# from celery import Celery

# app = Celery(
#     "tasks",
#     backend=os.environ["CELERY_RESULT_BACKEND"],
#     broker=os.environ["CELERY_BROKER_URL"],
# )
