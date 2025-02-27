from itertools import permutations, product
import requests
import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
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


def pegar_lista_paths(PATH: str):
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

    indices = []
    colunas = ["FRAME", "X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR"]
    for path_pessoa in lista_pessoas:
        id = os.path.splitext(os.path.basename(path_pessoa))[0]
        indices.append(id)

    df_labels = pd.DataFrame(index=indices, columns=[
                             "ARRAY_VEL", "DIF", "DOENTE"])

    # povoa df que contem as labels
    for path_pessoa, path_csv in zip(lista_pessoas, lista_csv):
        id = os.path.splitext(os.path.basename(path_pessoa))[0]
        df_csv = pd.read_csv(path_csv, index_col=0,
                             names=colunas, delimiter=",")
        pos_esq = df_csv.loc[:, "X_ESQ"].to_list()
        pos_dir = df_csv.loc[:, "X_DIR"].to_list()
        xEsquerdo, xDireito = getHampel(pos_esq, pos_dir)
        xEsquerdoFinal, xDireitaFinal = removeOutliers(xEsquerdo, xDireito)
        velE, velD = calculaVelocidadeEspacoPercorrido(
            xEsquerdoFinal, xDireitaFinal)

        percentDif = 1 - min(velE, velD) / max(velE, velD)
        # threshold = 0.1965  # 19.65%, ver artigo

        if path_pessoa in lista_saudavel:
            doente = False
        elif (path_pessoa in lista_pac):
            doente = True
        else:
            a = 1/0

        df_labels.loc[id, ("ARRAY_VEL", "DIF", "DOENTE")] = [
            [velE, velD], percentDif, doente]

    return df_labels, indices, lista_pessoas


def calculaVelocidadeEspacoPercorrido(xEsquerdo: list, xDireito: list) -> tuple[float, float]:
    assert type(xDireito) == type(xEsquerdo) == list
    somaEsquerda = 0
    somaDireita = 0
    if sum(xEsquerdo) > sum(xDireito):
        maxIndex = np.where(xEsquerdo == np.amax(xEsquerdo))
        minIndex = np.where(xEsquerdo == np.amin(xEsquerdo))
        mE = min(minIndex[0][0], maxIndex[0][0])
        mxE = max(minIndex[0][0], maxIndex[0][0])
        length = abs(mxE - mE)
        for i in range(mE + 1, mxE + 1):
            somaEsquerda += abs(xEsquerdo[i] - xEsquerdo[i - 1])
            somaDireita += abs(xDireito[i] - xDireito[i - 1])
        velE = somaEsquerda / length
        velD = somaDireita / length
    else:
        maxIndex = np.where(xDireito == np.amax(xDireito))
        minIndex = np.where(xDireito == np.amin(xDireito))
        mE = min(minIndex[0][0], maxIndex[0][0])
        mxE = max(minIndex[0][0], maxIndex[0][0])
        length = abs(mxE - mE)
        for i in range(mE + 1, mxE + 1):
            somaEsquerda += abs(xEsquerdo[i] - xEsquerdo[i - 1])
            somaDireita += abs(xDireito[i] - xDireito[i - 1])
        velE = somaEsquerda / length
        velD = somaDireita / length
    return velE, velD


def hampel_filter_forloop(input_series, window_size, n_sigmas):
    n = len(input_series)
    new_series = input_series.copy()
    k = 1.4826
    indices = []
    for i in range((window_size), (n - window_size)):
        x0 = np.median(input_series[(i - window_size): (i + window_size)])
        S0 = k * np.median(
            np.abs(input_series[(i - window_size): (i + window_size)] - x0)
        )
        if np.abs(input_series[i] - x0) > n_sigmas * S0:
            new_series[i] = x0
            indices.append(i)
    return new_series, indices


def getHampel(x1, x2):
    lent = min(len(x1), len(x2))
    x1 = x1[:lent]
    x2 = x2[:lent]
    resultEsquerdo, _ = hampel_filter_forloop(x1, 5, 2)
    resultDireito, _ = hampel_filter_forloop(x2, 5, 2)
    return resultEsquerdo, resultDireito


def removeOutliers(xEsquerdo, xDireita):

    fator = max(xEsquerdo) - min(xEsquerdo)
    fatorD = max(xDireita) - min(xDireita)
    xDireitaFinal = []
    xEsquerdoFinal = []
    xEsquerdoFinal.append(xEsquerdo[0])
    xDireitaFinal.append(xDireita[0])

    for j in range(1, len(xEsquerdo) - 1):
        anterior = abs(xEsquerdo[j] - xEsquerdo[j - 1])
        proximo = abs(xEsquerdo[j] - xEsquerdo[j + 1])
        if (anterior > (fator / 7)) and (proximo > (fator / 7)):
            xEsquerdoFinal.append(
                int((xEsquerdo[j + 1] + xEsquerdo[j - 1]) / 2))
        else:
            xEsquerdoFinal.append(xEsquerdo[j])
        anterior = abs(xDireita[j] - xDireita[j - 1])
        proximo = abs(xDireita[j] - xDireita[j + 1])
        if (anterior > (fator / 7)) and (proximo > (fator / 7)):
            xDireitaFinal.append(
                int((xDireita[j + 1] + xDireita[j - 1]) / 2))
        else:
            xDireitaFinal.append(xDireita[j])
    xDireitaFinal.append(xDireita[len(xDireita) - 1])
    xEsquerdoFinal.append(xEsquerdo[len(xEsquerdo) - 1])

    return xEsquerdoFinal, xDireitaFinal


""" 
Nao uso essa funcao pq ja faz Hampel e outliers nas posicoes

def calculaVelocidade(self, olhoEsquerdo, olhoDireito, frames, timestamp):
    posicaoOlhoEsquerdo = [x for x in olhoEsquerdo]
    posicaoOlhoDireito = [x for x in olhoDireito]
    esquerdaHampel, direitaHampel = self.getHampel(
        posicaoOlhoEsquerdo, posicaoOlhoDireito
    )
    olhoEsquerdoFinal, olhoDireitoFinal = self.removeOutliers(
        esquerdaHampel, direitaHampel
    )
    self.plotHampelFinal(
        posicaoOlhoEsquerdo,
        posicaoOlhoDireito,
        esquerdaHampel,
        olhoEsquerdoFinal,
        direitaHampel,
        olhoDireitoFinal,
        "Posição em relacao aos frames",
        timestamp,
    )
    velEsquerda, velDireita = self.calculaVelocidadeEspacoPercorrido(
        olhoEsquerdoFinal, olhoDireitoFinal
    )
    return velEsquerda, velDireita

"""


def getCenter(bbox):
    """Função auxiliar para calcular o centro da bounding box."""
    centerX = (bbox[2] + bbox[0]) // 2
    centerY = (bbox[3] + bbox[1]) // 2
    return centerX, centerY


def selectBoundingBoxes(boxes):
    """Função auxiliar para selecionar as bounding boxes dos olhos."""
    # Exemplo de lógica para retornar as bounding boxes dos olhos
    return [
        0,
        1,
    ], 45  # Mock da seleção das bounding boxes e ângulo (substituir com lógica real)

# --------------------------------------------#
# --------------------------------------------#
# --------------------------------------------#
# --------------------------------------------#
# ---------------#-#-#-#-#-#-#----------------#
# --------------#----O--O----#----------------#
# -------------#    --     #-----------------#
# --------------#-#-#-#-#-#------------------#
# --------------------------------------------#
# --------------------------------------------#
# --------------------------------------------#


def testar_api(lista_pessoas, df_labels, df_exp):
    # testa 3 pacientes na API
    cont = 0
    url_video = ""
    for pac in lista_pessoas:
        # Open the video file in binary read mode
        with open(pac, 'rb') as video_file:
            id, ext = os.path.splitext(os.path.basename(pac))
            print(id, ext)
            mimetype = mimetypes.types_map[ext]
            # Create a dictionary for the files parameter
            files = {'file': (f'video.{ext}', video_file, mimetype)}
            # Send the POST request with the video file
            response = requests.post(URL_SERVER, files=files)
            [velE, velD, difPercent,
                olho_doente], url_video = parse_response(response)
            df_exp.loc[id, ["ARRAY_VEL", "DIF", "DOENTE"]] = [
                [velE, velD], difPercent, olho_doente]
            print(response.json())
        cont += 1
        nome = os.path.basename(url_video)
        response = requests.get(url_video)
        """ if response.status_code == 200:
            with open(f'{nome}.mp4', 'wb') as file:
                file.write(response.content) """

    processar_dfs(df_exp, df_labels)


def processar_dfs(df_exp: pd.DataFrame, df_label: pd.DataFrame):
    print("Processando df...")
    colunas_exp = list(df_exp.columns)
    colunas_exp.remove("DOENTE")
    colunas_exp.append("DOENTE")
    # erro entre velocidade e medição real / diganostico correto  ou nao
    df_res = pd.DataFrame(index=df_exp.index, columns=["ERRO_VEL", "DOENTE"])

    for id in df_exp.index:
        serie_res = df_res.loc[id]
        serie_exp = df_exp.loc[id]
        serie_label = df_label.loc[id]

        array_exp = np.array(serie_exp.loc["ARRAY_VEL"], dtype=np.float32)
        array_true = np.array(serie_label.loc["ARRAY_VEL"])
        serie_res.loc["ERRO_VEL"] = np.abs(array_exp - array_true).tolist()
        cond = serie_exp["DOENTE"] == serie_label["DOENTE"]
        serie_res["DOENTE"] = True if cond else False
    print(df_res.head)
    df_res.to_csv("df_res.csv", sep=",")


def parse_response(resposta: requests.Response):
    dict_resp = resposta.json()
    str_res = dict_resp["string"]
    url_video = dict_resp["video"]
    velE, velD, difPercent, olho_doente = str_res.split(",")
    return [velE, velD, difPercent, olho_doente], url_video


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
df_labels, index, lista_pessoas = df_videos(
    PATH_SAUDAVEIS, PATH_PACIENTES, PATH_CSV)
# df do experimento
df_labels.to_csv("df_labels.csv")
df_exp = pd.DataFrame(columns=df_labels.columns, index=index)

print("COMECANDO TESTE")
testar_api(lista_pessoas, df_labels, df_exp)
# TODO: criar nova rota no Flask pra lidar com teste da API (precisa de mais dados)
