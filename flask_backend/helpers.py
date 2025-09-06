import csv
from datetime import datetime
from http.client import INTERNAL_SERVER_ERROR, OK
import json
import os
import subprocess
import threading

from bson import ObjectId
import ffmpeg
from flask_mail import Message
from flask_backend.drive import GoogleDrive
from flask_backend.yolo import YOLO
from flask_backend import PACKAGE_WKDIR


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

    # @staticmethod
    # def enviar_email(mensagem, mail_obj, destino, assunto):
    #     msg = Message(
    #         subject=assunto, recipients=[destino], body=mensagem  # List of recipients
    #     )
    #     try:
    #         mail_obj.send(msg)
    #         return OK
    #     except Exception as e:
    #         return INTERNAL_SERVER_ERROR

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
    def gerar_pdf(path_output: str, workdir: str, dict_dados: dict):
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
        base_url = os.path.join(workdir, "static")

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


def get_modelo():
    kwargs = {
        "model_path": os.path.join(PACKAGE_WKDIR, "trained_weights_final.h5"),
        "anchors_path": os.path.join(PACKAGE_WKDIR, "yolo_anchors.txt"),
        "classes_path": os.path.join(PACKAGE_WKDIR, "classes.txt"),
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "gpu_num": 1,
    }
    modelo = YOLO(**kwargs)
    return modelo
