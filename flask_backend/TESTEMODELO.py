from itertools import permutations, product
import traceback
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

BASE_URL = "http://127.0.0.1:5000/api"
URL_ANALISE_WS = f"{BASE_URL}/analise-ws"
URL_STATUS = f"{BASE_URL}/status"
URL_VER_ANALISE = f"{BASE_URL}/ver-analise"


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


def calculaVelocidadeEspacoPercorrido(
    xEsquerdo: list, xDireito: list
) -> tuple[float, float]:
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
        x0 = np.median(input_series[(i - window_size) : (i + window_size)])
        S0 = k * np.median(
            np.abs(input_series[(i - window_size) : (i + window_size)] - x0)
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
            xEsquerdoFinal.append(int((xEsquerdo[j + 1] + xEsquerdo[j - 1]) / 2))
        else:
            xEsquerdoFinal.append(xEsquerdo[j])
        anterior = abs(xDireita[j] - xDireita[j - 1])
        proximo = abs(xDireita[j] - xDireita[j + 1])
        if (anterior > (fator / 7)) and (proximo > (fator / 7)):
            xDireitaFinal.append(int((xDireita[j + 1] + xDireita[j - 1]) / 2))
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


def pegar_lista_paths(PATH: str):
    lista = []
    for root, dirs, lista_arq in os.walk(PATH):
        lista = [os.path.join(root, elem) for elem in lista_arq]
    return lista


def df_videos(PATH_SAUD: str, PATH_PAC: str, PATH_CSV: str):
    """
    Funcao que deve botar info dos pacientes em df
    """

    """LISTAS"""
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
    # ordena listas com base no nome de  arquivo
    for i, elem in enumerate(packed):
        elem.sort(key=lambda x: os.path.basename(x))

    assert len(lista_pessoas) == len(lista_csv), (
        f"{len(lista_pessoas)} != {len(lista_csv)}"
    )

    indices = []
    colunas = ["FRAME", "X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR"]
    for path_pessoa in lista_pessoas:
        id = os.path.splitext(os.path.basename(path_pessoa))[0]
        indices.append(id)

    df_labels = pd.DataFrame(index=indices, columns=["ARRAY_VEL", "DIF", "DOENTE"])

    # povoa df que contem as labels
    for path_pessoa, path_csv in zip(lista_pessoas, lista_csv):
        id = os.path.splitext(os.path.basename(path_pessoa))[0]
        df_csv = pd.read_csv(path_csv, index_col=0, names=colunas, delimiter=",")
        pos_esq = df_csv.loc[:, "X_ESQ"].to_list()
        pos_dir = df_csv.loc[:, "X_DIR"].to_list()
        xEsquerdo, xDireito = getHampel(pos_esq, pos_dir)
        xEsquerdoFinal, xDireitaFinal = removeOutliers(xEsquerdo, xDireito)
        velE, velD = calculaVelocidadeEspacoPercorrido(xEsquerdoFinal, xDireitaFinal)

        percentDif = 1 - min(velE, velD) / max(velE, velD)
        # threshold = 0.1965  # 19.65%, ver artigo
        doente = "doente"
        if path_pessoa in lista_saudavel:
            doente = "saudavel"

        df_labels.loc[id, ("ARRAY_VEL", "DIF", "DOENTE")] = [
            [velE, velD],
            percentDif,
            doente,
        ]

    return df_labels, indices, lista_pessoas


def testar_api_single(video_path: str, timeout: int = 900):
    """
    Testa um único paciente na API e plota o erro L2.
    Função independente que não usa dataframes globais.

    Fluxo:
    1. Autenticar com token via PUT /test-login
    2. POST /api/analise-ws → upload de vídeo + metadados (obtém task_id)
    3. GET /api/status/<task_id> → polling até SUCCESS (a cada 5s)
    4. POST /api/ver-analise/<task_id> → recuperar dados de análise
    5. Calcular erro L2 vs velocidade real
    6. Plotar gráfico comparativo

    Args:
        video_path: Caminho do vídeo (ex: "DADOS/VideosPacientes/1.mp4")
        timeout: Tempo máximo de espera em segundos (padrão: 900s = 15 min)
    """
    import time

    patient_id = os.path.splitext(os.path.basename(video_path))[0]

    print(f"\n=== Testando paciente {patient_id} ===")

    # 0. Criar sessão e autenticar
    print(f"\n✓ Passo 0: Autenticando com token...")

    session = requests.Session()

    try:
        auth_response = session.put(
            f"{BASE_URL}/test-login",
            json={"token": 666, "email": "test@pibiti.local"},
            timeout=10,
        )
        print(f"  Status: {auth_response.status_code}")

        if auth_response.status_code not in [200, 201]:
            print(f"  Aviso: Autenticação retornou status {auth_response.status_code}")
            print(f"  Resposta: {auth_response.text[:200]}")
        else:
            print(f"  ✅ Autenticado com sucesso")

    except Exception as e:
        print(f"  ⚠️  Erro na autenticação: {e}")
        print(f"  Continuando sem autenticação...")

    # 1. Calcula velocidade real a partir do CSV
    csv_path = os.path.join(PATH_CSV, f"{patient_id}.txt")

    if not os.path.exists(csv_path):
        print(f"Erro: Arquivo CSV {csv_path} não encontrado")
        return

    colunas = ["FRAME", "X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR"]
    df_csv = pd.read_csv(csv_path, index_col=0, names=colunas, delimiter=",")

    pos_esq = df_csv.loc[:, "X_ESQ"].to_list()
    pos_dir = df_csv.loc[:, "X_DIR"].to_list()

    xEsquerdo, xDireito = getHampel(pos_esq, pos_dir)
    xEsquerdoFinal, xDireitaFinal = removeOutliers(xEsquerdo, xDireito)

    vel_real_esq, vel_real_dir = calculaVelocidadeEspacoPercorrido(
        xEsquerdoFinal, xDireitaFinal
    )

    print(
        f"Velocidade real - Esquerdo: {vel_real_esq:.4f}, Direito: {vel_real_dir:.4f}"
    )

    # 2. Envia vídeo para análise via /api/analise-ws
    print(f"\n✓ Passo 1: Enviando vídeo para análise...")

    try:
        with open(video_path, "rb") as f:
            files = {"video": (os.path.basename(video_path), f, "video/mp4")}
            data = {
                "nomePaciente": f"Paciente_{patient_id}",
                "stringOlhos": "true+false",  # Ajuste conforme necessário
                "desc": f"Teste automático - Paciente {patient_id}",
            }

            response = session.post(URL_ANALISE_WS, files=files, data=data, timeout=30)
            print(f"  Status: {response.status_code}")

            if response.status_code != 200:
                print(f"  Erro: {response.content}")
                return

            response_data = response.json()
            task_id = response_data.get("task_id")

            if not task_id:
                print(f"  Erro: task_id não encontrado: {response_data}")
                return

            print(f"  Task ID: {task_id}")

    except Exception as e:
        print(f"  Erro ao enviar vídeo: {e}")
        return

    # 3. Polling para verificar status da análise
    print(f"\n✓ Passo 2: Aguardando processamento (máximo {timeout}s)...")
    start_time = time.time()
    elapsed = 0
    analise_completa = False
    tentativas = 0

    while elapsed < timeout:
        elapsed = time.time() - start_time
        tentativas += 1

        try:
            response = session.get(f"{URL_STATUS}/{task_id}", timeout=10)

            if response.status_code == 200:
                try:
                    result = response.json()
                    status_msg = result.get("message", "unknown")

                    if status_msg == "SUCCESS":
                        print(f"  [✓ {elapsed:.1f}s] Status: ✅ Análise concluída!")
                        analise_completa = True
                        break
                    elif status_msg == "PENDING":
                        print(f"  [{elapsed:.1f}s] ⏳ Processando...")
                    elif status_msg == "FAILED":
                        print(f"  [✗ {elapsed:.1f}s] Erro na análise: {result}")
                        return
                    else:
                        print(f"  [{elapsed:.1f}s] Status: {status_msg}")
                except Exception as json_err:
                    print(
                        f"  [✗ {elapsed:.1f}s] Erro ao parsear resposta JSON: {json_err}"
                    )
                    print(f"      Resposta bruta: {response.text[:200]}")

            elif response.status_code == 304:
                # 304 Not Modified também indica ainda processando
                print(f"  [{elapsed:.1f}s] ⏳ Processando (304)...")

            elif response.status_code == 404:
                print(f"  [✗ {elapsed:.1f}s] ❌ Task não encontrada (404)")
                print(f"      Verifique se o task_id está correto: {task_id}")
                print(f"      Resposta: {response.text[:200]}")
                return

            else:
                print(f"  [{elapsed:.1f}s] ⚠️  Status HTTP: {response.status_code}")
                print(f"      Resposta: {response.text[:200]}")

            time.sleep(5)  # Polling a cada 5 segundos

        except requests.exceptions.Timeout:
            print(f"  [⏱ {elapsed:.1f}s] Timeout na requisição de status")
            time.sleep(5)

        except Exception as e:
            print(f"  [✗ {elapsed:.1f}s] Erro na requisição: {type(e).__name__}: {e}")
            time.sleep(5)

    if not analise_completa:
        print(
            f"\n❌ Erro: Análise não foi concluída após {timeout} segundos ({tentativas} tentativas)"
        )
        print(f"   Task ID: {task_id}")
        return

    # 4. Recuperar dados finais da análise
    print(f"\n✓ Passo 3: Recuperando dados de análise...")

    try:
        response = session.post(f"{URL_VER_ANALISE}/{task_id}", timeout=10)

        if response.status_code != 200:
            print(f"  Erro: {response.status_code} - {response.content}")
            return

        dados_analise = response.json()

        vel_pred_esq = float(dados_analise.get("velE", 0))
        vel_pred_dir = float(dados_analise.get("velD", 0))
        percent_dif = float(dados_analise.get("percentDif", 0))
        olho_doente = dados_analise.get("olho_doente", "Desconhecido")

        print(
            f"  Velocidade predita - Esquerdo: {vel_pred_esq:.4f}, Direito: {vel_pred_dir:.4f}"
        )
        print(f"  Diferença: {percent_dif:.2f}%")
        print(f"  Olho doente (predito): {olho_doente}")

    except Exception as e:
        print(f"  Erro ao recuperar dados: {e}")
        return

    # 5. Calcula erros L2 comparando velocidades reais vs preditas
    print(f"\n✓ Passo 4: Calculando erro L2...")

    l2_esq = np.sqrt((vel_real_esq - vel_pred_esq) ** 2)
    l2_dir = np.sqrt((vel_real_dir - vel_pred_dir) ** 2)

    print(f"  Erro L2 - Esquerdo: {l2_esq:.4f}")
    print(f"  Erro L2 - Direito: {l2_dir:.4f}")

    # 6. Gera gráficos de série temporal
    print(f"\n✓ Passo 5: Gerando gráficos de série temporal...")

    # Posições reais do CSV
    pos_esq_real = df_csv.loc[:, "X_ESQ"].to_list()
    pos_dir_real = df_csv.loc[:, "X_DIR"].to_list()

    # Aproximação de posições preditas (extrapolação linear com base nas velocidades)
    # Para uma estimativa mais realista, usamos a velocidade média para interpolar
    frames = np.arange(len(pos_esq_real))

    # Posição predita esquerda: aproximação linear com base na velocidade
    pos_esq_pred = np.array(pos_esq_real) + (vel_pred_esq - vel_real_esq) * frames * 0.1
    pos_dir_pred = np.array(pos_dir_real) + (vel_pred_dir - vel_real_dir) * frames * 0.1

    # Calcular erro L2 frame a frame
    erro_l2_esq_frames = np.sqrt((np.array(pos_esq_real) - pos_esq_pred) ** 2)
    erro_l2_dir_frames = np.sqrt((np.array(pos_dir_real) - pos_dir_pred) ** 2)

    # Gráfico 1: Posição Olho Esquerdo (Real vs Predita)
    fig1, ax1 = plt.subplots(figsize=(14, 5))
    ax1.plot(frames, pos_esq_real, "g-", label="Real", linewidth=2, alpha=0.7)
    ax1.plot(frames, pos_esq_pred, "b--", label="Predita", linewidth=2, alpha=0.7)
    ax1.set_xlabel("Frame", fontsize=11)
    ax1.set_ylabel("Posição X (pixels)", fontsize=11)
    ax1.set_title(
        f"Série Temporal - Posição Olho Esquerdo - Paciente {patient_id}",
        fontsize=12,
        fontweight="bold",
    )
    ax1.legend(loc="best")
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        f"serie_temporal_pos_esq_{patient_id}.png", dpi=150, bbox_inches="tight"
    )
    plt.close()
    print(f"  ✓ Gráfico salvo: serie_temporal_pos_esq_{patient_id}.png")

    # Gráfico 2: Posição Olho Direito (Real vs Predita)
    fig2, ax2 = plt.subplots(figsize=(14, 5))
    ax2.plot(frames, pos_dir_real, "r-", label="Real", linewidth=2, alpha=0.7)
    ax2.plot(
        frames,
        pos_dir_pred,
        "orange",
        linestyle="--",
        label="Predita",
        linewidth=2,
        alpha=0.7,
    )
    ax2.set_xlabel("Frame", fontsize=11)
    ax2.set_ylabel("Posição X (pixels)", fontsize=11)
    ax2.set_title(
        f"Série Temporal - Posição Olho Direito - Paciente {patient_id}",
        fontsize=12,
        fontweight="bold",
    )
    ax2.legend(loc="best")
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        f"serie_temporal_pos_dir_{patient_id}.png", dpi=150, bbox_inches="tight"
    )
    plt.close()
    print(f"  ✓ Gráfico salvo: serie_temporal_pos_dir_{patient_id}.png")

    # Gráfico 3: Erro L2 - Olho Esquerdo
    fig3, ax3 = plt.subplots(figsize=(14, 5))
    ax3.plot(frames, erro_l2_esq_frames, "g-", linewidth=2, alpha=0.8)
    ax3.fill_between(frames, erro_l2_esq_frames, alpha=0.3, color="green")
    ax3.axhline(
        y=np.mean(erro_l2_esq_frames),
        color="darkgreen",
        linestyle="--",
        linewidth=2,
        label=f"Média: {np.mean(erro_l2_esq_frames):.4f}",
    )
    ax3.set_xlabel("Frame", fontsize=11)
    ax3.set_ylabel("Erro L2 (pixels)", fontsize=11)
    ax3.set_title(
        f"Erro L2 de Posição - Olho Esquerdo - Paciente {patient_id}",
        fontsize=12,
        fontweight="bold",
    )
    ax3.legend(loc="best")
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"erro_l2_esq_{patient_id}.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Gráfico salvo: erro_l2_esq_{patient_id}.png")

    # Gráfico 4: Erro L2 - Olho Direito
    fig4, ax4 = plt.subplots(figsize=(14, 5))
    ax4.plot(frames, erro_l2_dir_frames, "r-", linewidth=2, alpha=0.8)
    ax4.fill_between(frames, erro_l2_dir_frames, alpha=0.3, color="red")
    ax4.axhline(
        y=np.mean(erro_l2_dir_frames),
        color="darkred",
        linestyle="--",
        linewidth=2,
        label=f"Média: {np.mean(erro_l2_dir_frames):.4f}",
    )
    ax4.set_xlabel("Frame", fontsize=11)
    ax4.set_ylabel("Erro L2 (pixels)", fontsize=11)
    ax4.set_title(
        f"Erro L2 de Posição - Olho Direito - Paciente {patient_id}",
        fontsize=12,
        fontweight="bold",
    )
    ax4.legend(loc="best")
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"erro_l2_dir_{patient_id}.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Gráfico salvo: erro_l2_dir_{patient_id}.png")

    # 6. Plota gráfico comparativo (barras)
    print(f"\n✓ Passo 6: Gerando gráfico comparativo de velocidades...")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    x_pos = np.arange(2)

    # Gráfico Olho Esquerdo
    axes[0].bar(
        x_pos,
        [vel_real_esq, vel_pred_esq],
        color=["green", "blue"],
        alpha=0.7,
        label=["Real", "Predito"],
    )
    axes[0].set_xticks(x_pos)
    axes[0].set_xticklabels(["Real", "Predito"])
    axes[0].set_title(
        f"Olho Esquerdo - Paciente {patient_id}\nL2 Error: {l2_esq:.4f}",
        fontsize=12,
        fontweight="bold",
    )
    axes[0].set_ylabel("Velocidade (unidades)")
    axes[0].grid(axis="y", alpha=0.3)
    axes[0].legend()

    # Gráfico Olho Direito
    axes[1].bar(
        x_pos,
        [vel_real_dir, vel_pred_dir],
        color=["red", "orange"],
        alpha=0.7,
        label=["Real", "Predito"],
    )
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(["Real", "Predito"])
    axes[1].set_title(
        f"Olho Direito - Paciente {patient_id}\nL2 Error: {l2_dir:.4f}",
        fontsize=12,
        fontweight="bold",
    )
    axes[1].set_ylabel("Velocidade (unidades)")
    axes[1].grid(axis="y", alpha=0.3)
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(f"erro_paciente_{patient_id}.png", dpi=150, bbox_inches="tight")
    plt.close()

    print(f"  ✓ Gráfico salvo: erro_paciente_{patient_id}.png")

    print(f"\n📊 Resumo de Gráficos Gerados:")
    print(
        f"  1. serie_temporal_pos_esq_{patient_id}.png - Série temporal posição olho esquerdo"
    )
    print(
        f"  2. serie_temporal_pos_dir_{patient_id}.png - Série temporal posição olho direito"
    )
    print(f"  3. erro_l2_esq_{patient_id}.png - Erro L2 por frame (olho esquerdo)")
    print(f"  4. erro_l2_dir_{patient_id}.png - Erro L2 por frame (olho direito)")
    print(f"  5. erro_paciente_{patient_id}.png - Comparativo de velocidades (barras)")

    print(f"\n✅ Teste concluído com sucesso!")

    return {
        "patient_id": patient_id,
        "vel_real_esq": vel_real_esq,
        "vel_real_dir": vel_real_dir,
        "vel_pred_esq": vel_pred_esq,
        "vel_pred_dir": vel_pred_dir,
        "l2_esq": l2_esq,
        "l2_dir": l2_dir,
    }


def testar_api(
    lista_pessoas, df_labels: pd.DataFrame, df_exp: pd.DataFrame, timeout: int = 450
):
    """
    Testa múltiplos pacientes na API com fluxo completo.

    Fluxo para cada paciente:
    1. Autenticar com token (primeira vez apenas)
    2. POST /api/analise-ws → upload de vídeo + metadados
    3. GET /api/status/<task_id> → polling até SUCCESS
    4. POST /api/ver-analise/<task_id> → recuperar dados
    5. Calcular erro L2 vs velocidade real
    6. Gerar gráficos de série temporal

    Args:
        lista_pessoas: Lista de caminhos dos vídeos
        df_labels: DataFrame com labels (ARRAY_VEL, DIF, DOENTE)
        df_exp: DataFrame para armazenar resultados
        timeout: Timeout por análise em segundos (padrão: 900s = 15 min)
    """
    import time

    # 0. Criar sessão única e autenticar uma vez
    print("=" * 80)
    print("🚀 INICIANDO TESTE DE MÚLTIPLOS PACIENTES")
    print("=" * 80)

    session = requests.Session()

    print("\n✓ Autenticando com token...")
    try:
        auth_response = session.put(
            f"{BASE_URL}/test-login",
            json={"token": 666, "email": "test@pibiti.local"},
            timeout=30,
        )
        if auth_response.status_code in [200, 201]:
            print("  ✅ Autenticado com sucesso\n")
        else:
            print(f"  ⚠️  Status: {auth_response.status_code}\n")
    except Exception as e:
        print(f"  ⚠️  Erro na autenticação: {e}\n")

    # Iterar sobre os pacientes
    total_pacientes = len(lista_pessoas)
    pacientes_sucesso = 0
    pacientes_falha = 0

    for idx, video_path in enumerate(lista_pessoas):
        patient_id = os.path.splitext(os.path.basename(video_path))[0]

        print(f"\n{'=' * 80}")
        print(f"📹 Paciente {idx}/{total_pacientes}: {patient_id}")
        print(f"{'=' * 80}")

        # 1. Carregar CSV e calcular velocidade real
        csv_path = os.path.join(PATH_CSV, f"{patient_id}.txt")

        if not os.path.exists(csv_path):
            print(f"❌ Erro: Arquivo CSV {csv_path} não encontrado")
            pacientes_falha += 1
            continue

        colunas = ["FRAME", "X_ESQ", "Y_ESQ", "X_DIR", "Y_DIR"]
        try:
            df_csv = pd.read_csv(csv_path, index_col=0, names=colunas, delimiter=",")
            pos_esq = df_csv.loc[:, "X_ESQ"].to_list()
            pos_dir = df_csv.loc[:, "X_DIR"].to_list()

            xEsquerdo, xDireito = getHampel(pos_esq, pos_dir)
            xEsquerdoFinal, xDireitaFinal = removeOutliers(xEsquerdo, xDireito)

            vel_real_esq, vel_real_dir = calculaVelocidadeEspacoPercorrido(
                xEsquerdoFinal, xDireitaFinal
            )

            print(f"  Vel. real - Esq: {vel_real_esq:.4f}, Dir: {vel_real_dir:.4f}")
        except Exception as e:
            print(f"❌ Erro ao processar CSV: {e}")
            pacientes_falha += 1
            continue

        # 2. Enviar vídeo para análise
        print(f"  ✓ Enviando vídeo para análise...")
        try:
            with open(video_path, "rb") as f:
                files = {"video": (os.path.basename(video_path), f, "video/mp4")}
                data = {
                    "nomePaciente": f"Paciente_{patient_id}",
                    "stringOlhos": "true+false",
                    "desc": f"Análise automática - Paciente {patient_id}",
                }

                response = session.post(
                    URL_ANALISE_WS, files=files, data=data, timeout=30
                )

                if response.status_code != 200:
                    print(f"  ❌ Erro ao enviar: {response.status_code}")
                    pacientes_falha += 1
                    continue

                response_data = response.json()
                task_id = response_data.get("task_id")

                if not task_id:
                    print(f"  ❌ task_id não encontrado")
                    pacientes_falha += 1
                    continue

                print(f"  Task ID: {task_id}")
        except Exception as e:
            print(f"  ❌ Erro ao enviar: {e}")
            pacientes_falha += 1
            continue

        # 3. Polling para status
        print(f"  ✓ Aguardando processamento...")
        start_time = time.time()
        elapsed = 0
        analise_completa = False
        tentativas = 0

        while elapsed < timeout:
            elapsed = time.time() - start_time
            tentativas += 1

            try:
                response = session.get(f"{URL_STATUS}/{task_id}", timeout=10)

                if response.status_code == 200:
                    result = response.json()
                    status_msg = result.get("message", "unknown")

                    if status_msg == "SUCCESS":
                        analise_completa = True
                        print(f"    ✅ Concluída em {elapsed:.1f}s")
                        break
                    elif status_msg == "PENDING":
                        print(f"    [{tentativas}] ⏳ {elapsed:.1f}s...")
                    elif status_msg == "FAILED":
                        print(f"    ❌ Erro: {result}")
                        break
                elif response.status_code == 304:
                    print(f"    [{tentativas}] ⏳ {elapsed:.1f}s...")

                time.sleep(5)
            except Exception as e:
                print(f"    ⚠️  Erro: {e}")
                time.sleep(5)

        if not analise_completa:
            print(f"  ❌ Análise não concluída após {timeout}s")
            pacientes_falha += 1
            continue

        # 4. Recuperar dados da análise
        print(f"  ✓ Recuperando dados...")
        try:
            response = session.post(f"{URL_VER_ANALISE}/{task_id}", timeout=10)

            if response.status_code != 200:
                print(f"  ❌ Erro ao recuperar: {response.status_code}")
                pacientes_falha += 1
                continue

            dados_analise = response.json()

            vel_pred_esq = float(dados_analise.get("velE", 0))
            vel_pred_dir = float(dados_analise.get("velD", 0))
            percent_dif = float(dados_analise.get("percentDif", 0))
            olho_doente = dados_analise.get("olho_doente", "Desconhecido")

            print(f"  Vel. pred - Esq: {vel_pred_esq:.4f}, Dir: {vel_pred_dir:.4f}")
            print(f"  Diferença: {percent_dif:.2f}% | Olho doente: {olho_doente}")

            # Guardar em df_exp
            df_exp.loc[patient_id, "VEL_ESQ"] = vel_pred_esq
            df_exp.loc[patient_id, "VEL_DIR"] = vel_pred_dir
            df_exp.loc[patient_id, "DIF"] = percent_dif
            df_exp.loc[patient_id, "DOENTE"] = olho_doente

        except Exception as e:
            print(f"  ❌ Erro ao recuperar dados: {e}")
            pacientes_falha += 1
            continue

    # Salvar resultados
    print(f"\n{'=' * 80}")
    pacientes_sucesso = total_pacientes - pacientes_falha
    print(
        f"📊 RESUMO: {pacientes_sucesso}/{total_pacientes} pacientes processados com sucesso"
    )
    print(f"{'=' * 80}\n")

    print(df_exp)
    df_exp.to_csv("df_exp.csv", sep=";", decimal=",")
    print("✓ Resultados salvos em df_exp.csv")

    df_res = processar_dfs(df_exp, df_labels)
    return df_res


def processar_dfs(df_exp: pd.DataFrame, df_label: pd.DataFrame):
    def classifc_resp(label, pred):
        if label == "saudavel" and pred == "saudavel":
            return "TP"
        elif label == "saudavel" and pred == "doente":
            return "FP"
        elif label == "doente" and pred == "saudavel":
            return "FN"
        elif label == "doente" and pred == "doente":
            return "TN"
        else:
            print(label, pred)
            traceback.print_exc()
            raise Exception("Deu merda aqui")

    print("Processando df...")

    # erro entre velocidade e medição real / diganostico correto ou nao
    df_res = pd.DataFrame(
        index=df_exp.index, columns=["ERRO_VEL_ESQ", "ERRO_VEL_DIR", "DOENTE"]
    )

    for id in df_exp.index:
        serie_res = df_res.loc[id]
        serie_exp = df_exp.loc[id]
        serie_label = df_label.loc[id]

        for i, lado in enumerate(["ESQ", "DIR"]):
            vel_exp = np.array(serie_exp.loc[f"VEL_{lado}"], dtype=np.float64).item()

            vel_true = np.array(serie_label.loc[f"ARRAY_VEL"], dtype=np.float64)[i]

            serie_res.loc[f"ERRO_VEL_{lado}"] = np.abs(np.subtract(vel_exp, vel_true))

        classif = classifc_resp(serie_label.at["DOENTE"], serie_exp.at["DOENTE"])
        serie_res["DOENTE"] = classif

    print(df_res.head)
    sens, spec, acc = calculate_metrics(df_res)

    medias_erro_vel = [
        df_res.loc[:, "ERRO_VEL_ESQ"].median(),
        df_res.loc[:, "ERRO_VEL_DIR"].median(),
    ]
    dp_erro_vel = [
        df_res.loc[:, "ERRO_VEL_ESQ"].std(),
        df_res.loc[:, "ERRO_VEL_DIR"].std(),
    ]
    with open("out.txt", "w") as f:
        lista_str = []
        lista_str.append(f"SENS: {sens} SPEC: {spec} ACURACIA: {acc}\n")
        lista_str.append("----ERRO MEDIO DE VELOCIDADE-----\n")
        lista_str.append(
            f"ERRO VELOCIDADE ESQUERDA: {medias_erro_vel[0]}+-{dp_erro_vel[0]}\n"
        )
        lista_str.append(
            f"ERRO VELOCIDADE ESQUERDA: {medias_erro_vel[1]}+-{dp_erro_vel[1]}\n"
        )
        f.writelines(lista_str)
    df_res.to_csv(
        "df_res.csv", sep=";", decimal=",", compression=None, float_format="%.5f"
    )

    return df_res


def parse_response(resposta: requests.Response):

    dict_resp = resposta.json()
    str_res = dict_resp["string"]
    url_video = dict_resp["video"]
    # TODO: VERIFICAR PORQUE MATRIZ DE CONFUSAO ESTA SENDO CALCULADA ERRADO
    velE, velD, difPercent, olho_doente = str_res.split(",")
    if olho_doente.lower() == "esquerdo" or olho_doente.lower() == "direito":
        doente = "doente"
    else:
        print("ELSE olho_doente: ", olho_doente)
        doente = "saudavel"
    print("DOENTE PRED:", doente)
    return [velE, velD, difPercent, doente], url_video


def calculate_metrics(df_res):
    """Calculate sensitivity, specificity, and accuracy from results dataframe"""

    # Count true/false positives/negatives
    tp = len(df_res[df_res["DOENTE"] == "TP"])
    tn = len(df_res[df_res["DOENTE"] == "TN"])
    fp = len(df_res[df_res["DOENTE"] == "FP"])
    fn = len(df_res[df_res["DOENTE"] == "FN"])

    # Calculate metrics
    sensitivity = round(tp / (tp + fn), 3) if (tp + fn) > 0 else 0
    specificity = round(tn / (tn + fp), 3) if (tn + fp) > 0 else 0
    accuracy = round((tp + tn) / (tp + tn + fp + fn), 3)

    return sensitivity, specificity, accuracy


### AVISO: COMO TESTAR:
# Criar pastas VideosPacientes, VideosSaudaveis, CSV (marcacoes de olhos para cada frame do video) em uma pasta qualquer
# JOgar esse script e esperar calcular performance da API


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

if any(not os.path.exists(elem) for elem in [PATH_PACIENTES, PATH_SAUDAVEIS, PATH_CSV]):
    raise SystemError("dados para teste nao existem")


#### LOOP PRINCIPAL ####
# Testa um único paciente com visualização gráfica do erro L2
# lista_saudavel = pegar_lista_paths(PATH_SAUDAVEIS)
# lista_pac = pegar_lista_paths(PATH_PACIENTES)
# lista_pessoas = lista_saudavel + lista_pac
# lista_pessoas.sort(key=lambda x: os.path.basename(x))

df_labels, index, lista_pessoas = df_videos(PATH_SAUDAVEIS, PATH_PACIENTES, PATH_CSV)
coluna_exp = ["VEL_ESQ", "VEL_DIR", "DIF", "DOENTE"]

df_exp = pd.DataFrame(columns=coluna_exp, index=index)


print("COMECANDO TESTE")
resultado = testar_api(lista_pessoas, df_labels, df_exp)
