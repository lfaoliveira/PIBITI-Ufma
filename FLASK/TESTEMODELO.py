from itertools import permutations, product
import requests
import os
import shutil
import pandas as pd
import numpy as np
import cv2
import os

""" SCRIPT QUE DEVE SER USADO PARA TESTAR EQUIVALÊNCIA ENTRE API E ARTIGO DE POLYANA"""
slicer = pd.IndexSlice


def video2image(lista_videos):
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


def df_videos(PATH_SAUD, PATH_PAC, PATH_CSV):
    """
    Funcao que deve botar info dos pacientes em df 
    """

    """
    LISTAS
    """
    lista_saudavel = os.listdir(PATH_SAUD)
    lista_pac = os.listdir(PATH_PAC)
    # adiciona todos os pacientes a uma so lista
    lista_pessoas = lista_saudavel.extend(lista_pac)
    lista_csv = [elem for elem in os.listdir(PATH_CSV) if "LEIA" not in elem]
    packed = [lista_saudavel, lista_pac, lista_csv, lista_pessoas]
    # ordena listas com base no arquivo
    for elem in packed:
        elem.sort(lambda x: os.path.basename(x))
    assert len(lista_pessoas) == len(lista_csv)
    """
    LOGICA QUE PEGA TUPLAS DE ID E FRAME E BOTA COMO INDICE DO DF
    """
    tuplas = []
    for path_pessoa, path_csv in zip(lista_pessoas, lista_csv):
        id = path_pessoa.split(".")[0]
        df_csv = pd.read_csv(path_csv, index_col=0, delimiter=",")
        lista_frames = list(df_csv.index)
        tuplas.extend(product([id], lista_frames))
    tuplas = tuple(tuplas)
    indices = pd.MultiIndex.from_tuples(tuplas)
    df_labels = pd.DataFrame(
        {"X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR"}, index=indices)
    return df_labels, indices


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
    raise SystemError("Dataset not found")

PATH_PACIENTES = os.path.join(PATH_DADOS, "VideosPacientes")
PATH_SAUDAVEIS = os.path.join(PATH_DADOS, "VideosSaudaveis")
PATH_CSV = os.path.join(PATH_DADOS, "CSV")

if any(not os.path.exists(elem) for elem in [PATH_PACIENTES, PATH_SAUDAVEIS,  PATH_CSV]):
    raise SystemError

#### LOOP PRINCIPAL ####
df_labels, multi_index = df_videos(PATH_SAUDAVEIS, PATH_PACIENTES, PATH_CSV)
df_res = pd.DataFrame({"X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR",
                      "DIF_VEL", "DIAG", "TEMP_PROC"}, index=multi_index)
# TODO: criar loop  pra fazer teste da API com a lista de videos que ja existe
# TODO: criar nova rota no Flask pra lidar com teste da API (precisa de mais dados)
