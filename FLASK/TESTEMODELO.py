from itertools import permutations, product
import requests
import os
import shutil
import pandas as pd
import numpy as np
import cv2
import os
import mimetypes


""" SCRIPT QUE DEVE SER USADO PARA TESTAR EQUIVALÊNCIA ENTRE API E ARTIGO DE POLYANA"""
slicer = pd.IndexSlice

URL_SERVER = "http://127.0.0.1:5000/analise"


""" def video2image(lista_videos):
    for video_path in lista_videos:
        index = os.path.basename(video_path).split(".")[0]
        vid = cv2.VideoCapture(video_path)
        dir_video = str(index)
        # aqui eh criada uma pasta pra cada video, as imagens ficarao nesta pasta
        os.mkdir(dir_video)
        length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        for x in range(length):  # itera sobre imagens do video
            return_value, frame = vid.read()
            if (return_value == True):
                s = os.path.join(dir_video, f"{str(x)}.png")
                cv2.imwrite(s, frame)  # escrevendo a imagem na pasta
        vid.release()
        return
 """


def pegar_lista_paths(PATH):
    lista = []
    for root, dirs, lista_arq in os.walk(PATH):
        lista = [os.path.join(root, elem) for elem in lista_arq]
    return lista


def df_videos(PATH_SAUD: str, PATH_PAC: str, PATH_CSV: str):
    """
    Funcao que deve botar info dos pacientes em df
    """

    '''
    LISTAS
    '''
    lista_saudavel = pegar_lista_paths(PATH_SAUD)

    lista_pac = pegar_lista_paths(PATH_PAC)

    # adiciona todos os pacientes a uma so lista
    lista_pessoas = [elem for elem in lista_saudavel]
    lista_pessoas.extend(lista_pac)

    lista_csv = []
    for root, dirs, lista_arq in os.walk(PATH_CSV):
        for elem in lista_arq:
            if "LEIA" not in elem:
                lista_csv.append(os.path.join(root, elem))

    packed = [lista_saudavel, lista_pac, lista_csv, lista_pessoas]
    # ordena listas com base no arquivo
    for i, elem in enumerate(packed):
        elem.sort(key=lambda x: os.path.basename(x))

    assert len(lista_pessoas) == len(lista_csv)

    tuplas = []
    colunas = ["FRAME", "X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR"]
    for path_pessoa, path_csv in zip(lista_pessoas, lista_csv):
        id = os.path.splitext(path_pessoa)[0]
        df_csv = pd.read_csv(path_csv, index_col=0,
                             names=colunas, delimiter=",")
        lista_frames = list(df_csv.index)
        tuplas.extend(product([id], lista_frames))

    tuplas = tuple(tuplas)
    indices = pd.MultiIndex.from_tuples(tuplas)
    df_labels = pd.DataFrame(index=indices, columns=[
                             "X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR"])
    # povoa df multiindex que contem as labels
    for path_pessoa, path_csv in zip(lista_pessoas, lista_csv):
        id = path_pessoa.split(".")[0]
        df_csv = pd.read_csv(path_csv, index_col=0,
                             names=colunas, delimiter=",")
        for frame in df_csv.index:
            df_labels.loc[(id, frame), ["X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR"]
                          ] = df_csv.loc[frame, ["X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR"]]
    return df_labels, indices


def pegar_dados_resp(resposta: requests.Response):
    pass


def testar_api(lista_saudaveis, lista_pacientes, df_labels, df_res):
    lista_resp = []
    for pac in lista_saudaveis:

        # Open the video file in binary read mode
        with open(pac, 'rb') as video_file:
            # Create a dictionary for the files parameter
            ext = os.path.splitext(pac)[1]
            mimetype = mimetypes.types_map[ext]
            files = {'file': (f'video.{ext}', video_file, mimetype)}

            # Send the POST request with the video file
            response = requests.post(URL_SERVER, files=files)
            video_pac = cv2.VideoCapture(pac)

            lista_resp.append(response.text)
            print(response.text)
            break


# MODE LOCAL == running outside of Google Colab"
MODO = "LOCAL"
if os.path.exists("/content"):
    MODO = "COLAB"
else:
    MODO = "LOCAL"
# --SETTING PATH_DATASET-- #

CWD = os.getcwd()
PATH_DADOS = os.path.join(CWD, "DADOS")

# raise error when dataset not present
if not os.path.exists(PATH_DADOS):
    os.mkdir(PATH_DADOS)

PATH_PACIENTES = os.path.join(PATH_DADOS, "VideosPacientes")
PATH_SAUDAVEIS = os.path.join(PATH_DADOS, "VideosSaudaveis")
PATH_CSV = os.path.join(PATH_DADOS, "CSV")

if any(not os.path.exists(elem) for elem in [PATH_PACIENTES, PATH_SAUDAVEIS,  PATH_CSV]):
    raise SystemError("dados para teste nao existem")

#### LOOP PRINCIPAL ####
df_labels, multi_index = df_videos(PATH_SAUDAVEIS, PATH_PACIENTES, PATH_CSV)
df_res = pd.DataFrame(columns=["X_ESQ", "Y_ESQ", "X_DIR",
                      "Y_DIR", "DIF_VEL", "DIAG", "TEMP_PROC"], index=multi_index)


# TODO: criar loop  pra fazer teste da API com a lista de videos que ja existe
lista_saudavel = pegar_lista_paths(PATH_SAUDAVEIS)
lista_pac = pegar_lista_paths(PATH_PACIENTES)

testar_api(lista_saudavel, lista_pac, df_labels, df_res)

# TODO: criar nova rota no Flask pra lidar com teste da API (precisa de mais dados)
