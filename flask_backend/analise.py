import traceback
import matplotlib.pyplot as plt
from PIL import Image
import os
import numpy as np
import cv2
from tensorflow.python.framework.ops import disable_eager_execution
from traceback import print_exc

disable_eager_execution()

# from yolo import YOLO


class AnaliseParalisia:
    """
    Classe wrapper que contem todas as funcoes necessarias pra produzir resultados relevantes
    pro diagnostico de paralisia
    """

    def __init__(self, modelo, path_temp):
        self.path_temp = path_temp
        self.modelo = modelo

    def funcao_metodo(self, videoEntrada, videoSaida, timestamp):
        # olhoEsquerdo e  olhoDireito são listas de pontos com as posições (x,y) dos respectivos olhos em cada frame
        # frames é uma lista com os indices dos frames que foram usados

        try:
            olhoEsquerdo, olhoDireito, frames = self.detectaOlhos(
                videoEntrada, videoSaida
            )
            print("DETECCAO DOS OLHOS OK")
        except Exception as e:
            print(f"ERRO:FALHA NA DETECÇÃO DOS OLHOS: {e}")
            print_exc()
            return "ERRO:FALHA NA DETECÇÃO DOS OLHOS", "None"
        # self.escrever_olhos([olhoEsquerdo, olhoDireito], frames, videoEntrada)
        try:
            leftEye = np.array(olhoEsquerdo)
            rightEye = np.array(olhoDireito)
            xE = leftEye[:, 0] - min(leftEye[:, 0])
            xD = rightEye[:, 0] - min(rightEye[:, 0])
            xEsquerdo, xDireito = self.getHampel(xE, xD)
            xEsquerdoFinal, xDireitaFinal = self.removeOutliers(xEsquerdo, xDireito)
            # print("\n\nXESQUERDO: ", xEsquerdoFinal, "\n\n")
            print("FILTRAGEM DE PONTOS OK")
        except Exception as e:
            print("ERRO:FALHA NA MANIPULAÇÃO DO GRÁFICO DE POSIÇÃO: ", e)
            return "ERRO:FALHA NA MANIPULAÇÃO DO GRÁFICO DE POSIÇÃO", "None"

        try:
            titulo = "Grafico de Velocidade dos Olhos"
            dict_graf = {
                "vel_esq": xEsquerdoFinal.astype(int),
                "vel_dir": xDireitaFinal.astype(int),
                "titulo": titulo,
                "time": timestamp,
            }

            """ path_graf = self.plotHampelFinal(
                xEsquerdoFinal,
                xDireitaFinal, titulo, timestamp,
            ) """

            velE, velD = self.calculaVelocidadeEspacoPercorrido(
                xEsquerdoFinal, xDireitaFinal
            )

            velE2, velD2 = self.calculaVelocidade(
                xEsquerdoFinal, xDireitaFinal, frames, timestamp
            )
            print(
                f"Velocidade do olho esquerdo: {velE:.2f}\nVelocidade do olho direito: {velD:.2f}"
            )

            percentDif = 1 - min(velE, velD) / max(velE, velD)
            threshold = 0.1965  # 19.65%, ver artigo
            olho_doente = ""

            if velE < velD:
                print(
                    f"O olho esquerdo se move {percentDif*100:.2f}% mais devagar que o olho direito."
                )
                olho_doente = "Esquerdo"
            else:
                print(
                    f"O olho direito se move {percentDif*100:.2f}% mais devagar que o olho esquerdo."
                )
                olho_doente = "Direito"

            if percentDif < threshold:
                olho_doente = "None"
            return f"{velE},{velD},{percentDif},{olho_doente}", dict_graf
        except Exception as e:
            print("ERRO:FALHA NO CALCULO DA VELOCIDADE: ", e)
            return "ERRO:FALHA NO CALCULO DA VELOCIDADE", "None"

    def detectaOlhos(self, path_inputVideo, path_outputVideo):
        vid = cv2.VideoCapture(path_inputVideo)
        length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        if not vid.isOpened():
            print("FRAME COUNT: ", length)
            raise IOError("Nao foi possivel abrir o video indicado.")

        fps = vid.get(cv2.CAP_PROP_FPS)
        frame_width = int(vid.get(3))
        frame_height = int(vid.get(4))

        if frame_width > 416 and frame_height > 416:
            auxV = max(frame_width, frame_height)
            factor = np.trunc(auxV / 416)
            frame_width = int(frame_width / factor)
            frame_height = int(frame_height / factor)

        videoFinal = cv2.VideoWriter(
            path_outputVideo,
            cv2.VideoWriter_fourcc("M", "J", "P", "G"),
            fps / 2,
            (frame_width, frame_height),
        )
        olhoEsquerdo = []
        olhoDireito = []
        frames = []
        try:

            for x in range(0, length - 1):
                image = []
                return_value, frame = vid.read()

                if x % 5 == 0:
                    if return_value:
                        rows, cols, ch = frame.shape
                        dim = (frame_width, frame_height)
                        resized = cv2.resize(frame, dim)
                        image = Image.fromarray(resized)
                        image, area, classes = self.modelo.detect_image(image)
                        pontosCentro = []

                        if len(area) > 1:
                            numbers = selectBoundingBoxes(area)
                            if len(numbers) > 0:
                                angle = round(numbers[1], 2)
                                numbers = numbers[0]
                                if len(numbers) == 2:
                                    for index in numbers:
                                        a = area[index]
                                        start_point = (a[0], a[1])
                                        end_point = (a[2], a[3])
                                        center = getCenter(a)
                                        pontosCentro.append(center)
                                        cv2.rectangle(
                                            resized,
                                            start_point,
                                            end_point,
                                            (0, 0, 255),
                                            3,
                                        )
                                        cv2.circle(resized, center, 5, (0, 255, 0), -1)
                                    cv2.putText(
                                        resized,
                                        text="Olhos " + str(len(numbers)),
                                        org=(3, 15),
                                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                        fontScale=0.50,
                                        color=(255, 0, 0),
                                        thickness=2,
                                    )
                                    videoFinal.write(resized)
                                    frames.append(x)

                                    if len(pontosCentro) == 2:
                                        if pontosCentro[0][0] < pontosCentro[1][0]:
                                            olhoEsquerdo.append(pontosCentro[0])
                                            olhoDireito.append(pontosCentro[1])
                                        else:
                                            olhoEsquerdo.append(pontosCentro[1])
                                            olhoDireito.append(pontosCentro[0])

            vid.release()
            videoFinal.release()
            return olhoEsquerdo, olhoDireito, frames

        except Exception as e:
            print(e)
            print_exc()
            raise

    def escrever_olhos(self, olhos, frames, videoEntrada):
        for idx_olho, olho in enumerate(olhos):
            ordem = "Esquerdo" if idx_olho == 0 else "Direito"
            pupilaOlho = open(videoEntrada.split(".")[0] + f"{ordem}.txt", "w+")
            for i in range(len(olho)):
                pupilaOlho.write("\n%d," % (frames[i]))
                pupilaOlho.write("%d," % (olho[i][0]))
                pupilaOlho.write("%d\n" % (olho[i][1]))
            pupilaOlho.close()

    def hampel_filter_forloop(self, input_series, window_size, n_sigmas):
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

    def getHampel(self, x1, x2) -> tuple:
        lent = min(len(x1), len(x2))
        x1 = x1[:lent]
        x2 = x2[:lent]
        resultEsquerdo, _ = self.hampel_filter_forloop(x1, 5, 2)
        resultDireito, _ = self.hampel_filter_forloop(x2, 5, 2)
        return resultEsquerdo, resultDireito

    def removeOutliers(self, xEsquerdo, xDireita):

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

    def plotHampelFinal(
        self,
        xEsquerdoFinal,
        xDireitaFinal,
        titulo,
        timestamp,
    ):
        plt.figure(num=1, figsize=(10, 5))
        plt.title(titulo)
        # plt.plot(xEsquerda, 'b', label='Esq.')
        # plt.plot(xEsquerdoHampel, 'salmon', label='Esq. Hampel')
        plt.plot(xEsquerdoFinal, "darkred", label="Esq. Final")
        # plt.plot(xDireita, 'g', label='Dir.')
        # plt.plot(xDireitaHampel, 'grey', label='Dir. Hampel')
        plt.plot(xDireitaFinal, "k", label="Dir. Final")
        plt.xlabel("Frames")
        plt.ylabel("Pixels")
        plt.legend()
        path_graf = os.path.join(self.path_temp, f"GRAF_{timestamp}.jpg")
        plt.savefig(path_graf)
        # plt.show()
        plt.close()
        return path_graf

    def calculaVelocidadeEspacoPercorrido(self, xEsquerdo, xDireito):
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

    def calculaVelocidade(self, olhoEsquerdo, olhoDireito, frames, timestamp):
        posicaoOlhoEsquerdo = [x for x in olhoEsquerdo]
        posicaoOlhoDireito = [x for x in olhoDireito]
        esquerdaHampel, direitaHampel = self.getHampel(
            posicaoOlhoEsquerdo, posicaoOlhoDireito
        )
        olhoEsquerdoFinal, olhoDireitoFinal = self.removeOutliers(
            esquerdaHampel, direitaHampel
        )
        """ self.plotHampelFinal(
            posicaoOlhoEsquerdo,
            posicaoOlhoDireito,
            esquerdaHampel,
            olhoEsquerdoFinal,
            direitaHampel,
            olhoDireitoFinal,
            "Posição em relacao aos frames",
            timestamp,
        ) """
        velEsquerda, velDireita = self.calculaVelocidadeEspacoPercorrido(
            olhoEsquerdoFinal, olhoDireitoFinal
        )
        return velEsquerda, velDireita


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
