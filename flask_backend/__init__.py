import os

COLLECTION_DIAGS = "Diagnosticos"
COLLECTION_MEDICOS = "Medicos"
PASTA_USUARIO_ANONIMO_GDRIVE = "ANONIMO"

BASE_URL = os.getenv("FLASK_BASE_URL")

PACKAGE_WKDIR = os.path.join(
    os.path.join(
        os.getcwd(),
        __package__,
    )
)
