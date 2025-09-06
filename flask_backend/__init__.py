import os

COLLECTION_DIAGS = "Diagnosticos"
COLLECTION_MEDICOS = "Medicos"
PASTA_USUARIO_ANONIMO_GDRIVE = "ANONIMO"

PACKAGE_WKDIR = os.path.join(
    os.path.join(
        os.getcwd(),
        __package__,
    )
)
