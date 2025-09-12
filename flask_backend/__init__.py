import os

COLLECTION_DIAGS = "Diagnosticos"
COLLECTION_MEDICOS = "Medicos"
DB_PARALISIA = "PARALISIA6_NERVO"
PASTA_USUARIO_ANONIMO_GDRIVE = "ANONIMO"
ROOT_DRIVE = "ROOT_DADOS"

BASE_URL = os.environ["FLASK_BASE_URL"]

PACKAGE_WKDIR = os.path.join(
    os.path.join(
        os.getcwd(),
        __package__,
    )
)

PATH_CRED = os.path.join(PACKAGE_WKDIR, "permalink-googleDrive-pibiti6-nervo.json")
