# -*- coding: utf-8 -*-
import colorsys
import os
from timeit import default_timer as timer
import numpy as np
import sys

# TensorFlow 2.x - usar tensorflow.keras em vez de keras standalone
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Input
from PIL import Image, ImageFont, ImageDraw

from flask_backend import PACKAGE_WKDIR
from flask_backend.yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
from flask_backend.yolo3.utils import letterbox_image

# Fallback seguro para multi_gpu_model - API interna do TensorFlow pode quebrar em versoes diferentes
try:
    from tensorflow.python.keras.utils.multi_gpu_utils import multi_gpu_model
except (ImportError, AttributeError):
    # Fallback: se importacao quebrar, criar dummy function que retorna modelo como esta
    def multi_gpu_model(model, gpus=None):
        """Fallback para multi_gpu_model quando import falha. Retorna modelo sem modificacao."""
        print(
            "[YOLO] multi_gpu_model indisponivel (versao TensorFlow incompativel). Usando modelo em CPU/GPU single."
        )
        return model


import matplotlib.pyplot as plt
from skimage import io


class YOLO(object):
    _defaults = {
        "model_path": "trained_weights_final.h5",
        "anchors_path": "yolo_anchors.txt",
        "classes_path": "classes.txt",
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),  # (384, 384)
        "gpu_num": 0,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        print(kwargs)
        self.__dict__.update(kwargs)
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        # TensorFlow 2.x - nao precisa de sessao
        # Removido: self.sess = K.get_session()
        self.yolo_model = self.generate()

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(",")]
        return np.array(anchors).reshape(-1, 2)

    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith(".h5"), "Keras model or weights must be a .h5 file."

        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        is_tiny_version = num_anchors == 6  # default setting
        try:
            yolo_model = load_model(model_path, compile=False)
        except:
            yolo_model = (
                tiny_yolo_body(
                    Input(shape=(None, None, 3)), num_anchors // 2, num_classes
                )
                if is_tiny_version
                else yolo_body(
                    Input(shape=(None, None, 3)), num_anchors // 3, num_classes
                )
            )
            yolo_model.load_weights(
                self.model_path
            )  # make sure model, anchors and classes match
        else:
            assert yolo_model.layers[-1].output_shape[-1] == num_anchors / len(
                yolo_model.output
            ) * (num_classes + 5), (
                "Mismatch between model and given anchor and class sizes"
            )

        # print('{} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [
            (x / len(self.class_names), 1.0, 1.0) for x in range(len(self.class_names))
        ]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(
                lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors,
            )
        )
        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(
            self.colors
        )  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default.

        # TensorFlow 2.x - multi_gpu_model soh funciona com 2+ GPUs
        if self.gpu_num >= 2:
            yolo_model = multi_gpu_model(yolo_model, gpus=self.gpu_num)

        # Nao chamamos yolo_eval aqui - faremos isso em detect_image
        return yolo_model

    def detect_image(self, image):
        area = []
        classes = []
        start = timer()
        if self.model_image_size != (None, None):
            assert self.model_image_size[0] % 32 == 0, "Multiples of 32 required"
            assert self.model_image_size[1] % 32 == 0, "Multiples of 32 required"
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (
                image.width - (image.width % 32),
                image.height - (image.height % 32),
            )
            boxed_image = letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype="float32")

        image_data /= 255.0
        image_data = np.expand_dims(image_data, 0)

        # TensorFlow 2.x - usar predict() em vez de sess.run com feed_dict
        # Primeiro, obter as saidas do modelo
        model_output = self.yolo_model.predict(image_data, verbose=0)

        # yolo_eval espera (image_shape) como segundo argumento
        # Converter para formato correto: (height, width)
        input_image_shape = np.array([image.size[1], image.size[0]], dtype=np.float32)

        # Chamar yolo_eval com as saidas do modelo
        out_boxes, out_scores, out_classes = yolo_eval(
            model_output,
            self.anchors,
            len(self.class_names),
            input_image_shape,
            score_threshold=self.score,
            iou_threshold=self.iou,
        )

        # Converter tensores para numpy arrays
        out_boxes = out_boxes.numpy() if hasattr(out_boxes, 'numpy') else out_boxes
        out_scores = out_scores.numpy() if hasattr(out_scores, 'numpy') else out_scores
        out_classes = out_classes.numpy() if hasattr(out_classes, 'numpy') else out_classes

        font = ImageFont.truetype(
            font=os.path.join(PACKAGE_WKDIR, "font/FiraMono-Medium.otf"),
            size=np.floor(3e-2 * image.size[1] + 0.5).astype("int32"),
        )
        thickness = (image.size[0] + image.size[1]) // 300
        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            label = "{} {:.2f}".format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textlength(label, font)

            # as coordenadas sao dadas em top (y min), left(x min), bottom(y max) e right(x max)
            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype("int32"))
            left = max(0, np.floor(left + 0.5).astype("int32"))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype("int32"))
            right = min(image.size[0], np.floor(right + 0.5).astype("int32"))

            if top - label_size >= 0:
                text_origin = np.array([left, top - label_size])
            else:
                text_origin = np.array([left, top + 1])

            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i], outline=self.colors[c]
                )

                areaAux = (left + i, top + i, right - i, bottom - i)
            area.append(areaAux)
            classes.append((predicted_class, score))
            draw.text(text_origin, label, font=font, fill="black")
            del draw

        end = timer()
        return image, area, classes

    def close_session(self):
        # TensorFlow 2.x - Keras gerencia a memoria automaticamente
        # Nao precisa fechar sessao
        pass