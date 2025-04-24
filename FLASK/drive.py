from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import mimetypes
import os
import itertools
import time
import pandas as pd

# NOTE!!!!!!!!! SE NECESSARIO, CRIAR FORMA DE MANTER ROOT_DRIVE AUTALIZADO, SENAO APLCIACAO PODE QUEBRAR
# TODO: ADAPTAR LOGICA PARA QUE TODO_ E QUALQUER FOLDER E ARQUIVO SEJA CRIADO DENTRO DE ID_ROOT_DADOS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class GoogleDrive:
    """Classe que lidara com logica relacionada a interacoes com API do Google Drive\n
    :param pd.DataFrame file_state: Dataframe que ira conter todas as informacoes sobre os arquivos e folders no Drive
    """

    def __init__(self, PATH_CRED, ROOT_DRIVE):
        """NAO MUDAR!!!!!! E NAO CONFUNDIR ID'S DE ROOT!!!!!!!"""
        # TODO: mudar para '0AHIxAncewr_KUk9PVA' em PRODUCAO
        self.ID_ROOT_CONTA_SERVICO = 'root'

        self.emailOwner = 'viplab.psno@nca.ufma.br'
        self.emailService = 'teste-drive@pibiti6-nervo.iam.gserviceaccount.com'
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        CREDENTIALS = service_account.Credentials.from_service_account_file(
            PATH_CRED, scopes=SCOPES, subject=self.emailService,
        )
        self.drive_service = build("drive", "v3", credentials=CREDENTIALS)
        self.first_fetch = True
        self.startPageToken = None
        """ self.file_state: dict[str, dict[str, str]] """

        # dict que vai mapear nomes de arquivos a lista de id's desses arquivos
        self.hash_nomes = {}
        self.ROOT_DRIVE = ROOT_DRIVE
        self.ID_ROOT_DADOS = os.environ.get('ID_ROOT_FOLDER_GDRIVE', None)
        if not self.ID_ROOT_DADOS:
            raise ValueError(
                "ID ROOT NAO SETADO!!!!!! (CHECAR SE env.csv ESTA PRESENTE NO FOLDER DO SERVIDOR!!)")
        print(f"ID ROOT: {self.ID_ROOT_DADOS}")
        self.fetch_drive_files()

    def initial_fetch(self):
        # Get initial state and start page token

        page_token = None
        files = []

        # First, get the starting page token for future changes
        response = self.drive_service.changes().getStartPageToken().execute()
        self.startPageToken = response.get('startPageToken')

        while True:
            response = self.drive_service.files().list(
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime, parents)",
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                q="trashed=false",
            ).execute()

            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        # TODO: ADPATAR PRA DF: Clear existing state before updating
        self.file_state = {}
        for file in files:

            if file.get('name') not in self.hash_nomes.keys():
                self.hash_nomes[file.get('name')] = []
            # self.hash_nomes[file.get('name')].append(file['id'])
            id_parent = file.get('parents')
            if id_parent != None and len(id_parent) > 1:
                raise Exception(
                    "INITIAL FETCH ERROR: ID_PARENT LENGTH TOO BIG")
            # id_parent None significa que parent eh ROOT_DADOS
            id_parent = id_parent[0] if id_parent != None else self.ID_ROOT_DADOS
            if id_parent == self.ID_ROOT_CONTA_SERVICO:
                raise Exception(
                    "PEGAR ARQUIVOS DA CONTA DE SERVIÇO É PROBIDO!!!!!")
            self.file_state[file['id']] = {
                "name": file.get('name'),
                "modified": file.get('modifiedTime'),
                "parents":  [id_parent],
                "mimeType": file.get('mimeType')
            }
        self.file_state = pd.DataFrame.from_dict(
            self.file_state, orient='index')
        print(f"DF FILE STATE: \n{self.file_state}")
        self.first_fetch = False

    def fetch_drive_files(self):
        """
        Query Google Drive to fetch a list of all files (INCLUDES FOLDERS).
        Returns:
            A dictionary mapping file IDs to their modified times (or any other metadata you want).
        """
        if self.first_fetch:
            self.initial_fetch()
            return self.file_state
        # NOTE!!!! USUÁRIO NÃO PODE MODIFICAR PASTAS NO ROOT DA CONTA DE USUÁRIO SENÃO PODE QUEBRAR SINCRONIA!!!!!!
        page_token = self.startPageToken
        while page_token is not None:
            response = self.drive_service.changes().list(
                pageToken=page_token,
                includeRemoved=True,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageSize=50,
                fields="nextPageToken, newStartPageToken, changes(fileId, file(trashed, modifiedTime, name, parents, mimeType), removed)"
            ).execute()
            print("")
            aux_file_state = {}
            for change in response.get('changes', []):
                print("CHANGE: ", change)
                file_id = change.get('fileId')
                trashed = change.get('file', {}).get('trashed', False)
                if change.get('removed', False) or trashed:
                    # tira arquivo do registro
                    self.file_state.drop(index=file_id, inplace=True)
                else:
                    # atualiza arquivo no registro
                    file = change.get('file')

                    # tem que botar so id na lista do hash de nomes!!!!!!!!!!!!!!!!!!!!
                    id_parent = file.get('parents')
                    if id_parent != None and len(id_parent) > 1:
                        raise Exception(
                            "INITIAL FETCH ERROR: ID_PARENT LENGTH TOO BIG")

                    # id_parent None significa que parent eh ROOT_DADOS
                    id_parent = id_parent[0] if id_parent != None else self.ID_ROOT_DADOS
                    if id_parent == self.ID_ROOT_CONTA_SERVICO:
                        raise Exception(
                            "PEGAR ARQUIVOS DA CONTA DE SERVIÇO É PROBIDO!!!!!")

                    aux_file_state[file_id] = {
                        "name": file.get('name'),
                        "modified": file.get('modifiedTime'),
                        "parents": [id_parent],
                        "mimeType": file.get('mimeType'),
                    }

            if 'newStartPageToken' in response.keys():
                # Save this token for the next polling interval
                self.startPageToken = response.get('newStartPageToken')
            page_token = response.get('nextPageToken')

        modificacoes = pd.DataFrame.from_dict(aux_file_state, orient='index')
        self.file_state.update(modificacoes)
        return self.file_state

    def get_file_id(self, file_name, folder_name=None, id_parent_folder=None):
        if folder_name:
            id_folder = self.get_folder_id(folder_name, id_parent_folder)

        existe = folder_name in self.file_state['name'].values()
        if not existe:
            return None
        lista_ids = self.hash_nomes.get(file_name, None)

        file_id = None
        if lista_ids:
            for id in lista_ids.items():
                file = self.file_state.loc[id]
                name = file.get('name')
                parent_id = file.get('parents')[0]
                if name == file_name:
                    # se especificar nome do folder, compara com id do folder
                    if folder_name:
                        if id_folder == parent_id:
                            file_id = id
                            break
                    else:
                        file_id = id
                        break
        # sem lista ou nao achou
        if file_id:
            print("ACHOU FILE_ID")
        return file_id

    def get_folder_id(self, folder_name, id_parent):
        # partindo do principio que ROOT_DRIVE sempre existe e ja esta configurado ;)
        if folder_name == self.ROOT_DRIVE:
            return self.ID_ROOT_DADOS

        existe = folder_name in self.file_state['name'].values
        if not existe:
            return None

        matching_files = self.file_state[
            (self.file_state['parents'][0] == id_parent) &
            (self.file_state['mimeType'] == 'application/vnd.google-apps.folder') &
            (self.file_state['name'] == folder_name)
        ]
        print(f"TYPE MATCHED FILES: {type(matching_files)}")
        if not matching_files.empty:
            return matching_files.index[0]

        """ for id in self.file_state.index:
            file = self.file_state[id]
            mime = file.get('mimeType')
            name = file.get('name')
            parent_arq = file.get('parents', None)
            print(
                f"NAME: {name} PARENTS_ARQ: {parent_arq} PARENTS_ARG: {id_parent}\n")
            if (id_parent == parent_arq):
                return id """
        return None

    def create_folder(self, nomes_parents: list = []):
        """
        Criacao de Folder
        """
        folder_name = nomes_parents[-1]
        print(f"\nFOLDER_NAME: {folder_name}")
        print(f"CAMINHO: {nomes_parents}\n")

        if folder_name == self.ROOT_DRIVE:
            print(
                f"TENTANDO CRIAR ROOT_DRIVE '{self.ROOT_DRIVE}'. Abortando...")
            return None
        if self.ROOT_DRIVE not in nomes_parents:
            # so pra garantir que o primeiro eh o ROOT_DRIVE
            nomes_parents.insert(0, self.ROOT_DRIVE)

        folder_list = []
        folder_list.extend(nomes_parents)

        id_parents = [self.ID_ROOT_DADOS]
        # pula primeiro ja que eh sempre ROOT_DRIVE
        for i in range(1, len(folder_list)):
            # da fecth para atualizar estado local
            self.fetch_drive_files()
            print(
                f"PARENTS NIVEL {i} (O QUE ERA PRA SER): {folder_list[0:i]}\n")
            id = self.get_folder_id(
                folder_list[i], id_parent=folder_list[i - 1])
            if (id == None):
                # id nulo, cria folder com parents ja criados
                folder_metadata = {
                    'name': folder_list[i],
                    'parents': [id_parents[i - 1]],
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                print(f"ID PARENTS: {id_parents}")
                print(
                    f"CRIANDO FOLDER {folder_list[i]}, FOLDER METADATA: NAME AND PARENT:{folder_metadata['name'], folder_metadata['parents']}")
                folder_drive = self.drive_service.files().create(
                    body=folder_metadata, fields='id').execute()
                folder_id = folder_drive.get('id')
                id_parents.append(folder_id)
            else:
                folder_id = id
            id_parents.append(folder_id)

        return folder_id

    def upload_to_drive(self, file_path, nomes_parents=[], resumable=False):
        """
        Faz upload de arquivo para o drive; Cria folder de destino se folder nao existir \n

        :param list[str] nomes_parents: contem nomes dos folders-pai do arquivo (NUNCA INCLUIR O NOME DO ROOT DENTRO)
        NOTE: SEMPRE QUE ESPECIFICAR 'parents' BOTAR COMO UM ARRAY!!!!!!! SENAO VAI MANDAR PRO ROOT DA CONTA DE SERVIÇO
        Returns: id do arquivo criado
        """
        self.fetch_drive_files()
        nomes_parents.insert(0, self.ROOT_DRIVE)

        print(
            f"NO UPLOAD: FILE: {file_path} PARENTS: {nomes_parents}\n\n")
        if len(nomes_parents) >= 2:
            # quer inserir em um diretorio mais profundo que ROOT_DRIVE
            parent = nomes_parents[-2]
            print(f"INSERINDO MAIS FUNDO QUE {self.ROOT_DRIVE}")

            # pega id do folder mais profundo
            id_folder = self.get_folder_id(nomes_parents[-1], parent)
        else:
            print("AVISO!! INSERINDO NO ROOT_DRIVE!")
            # quer inserir no ROOT
            id_folder = self.get_folder_id(nomes_parents[0], None)

        # cria parentes, se nao existirem, e folder
        if (id_folder == None):
            print("CRIANDO DIRETORIO")
            id_folder = self.create_folder(nomes_parents)
            if id_folder == None:
                return None

        mime = mimetypes.guess_type(file_path)
        if mime:
            media = MediaFileUpload(
                file_path, mimetype=mime[0], resumable=resumable)

            file_metadata = {
                'name': os.path.basename(file_path),
                'parents': [id_folder],
            }
            try:
                print("FAZENDDO UPLOAD")
                if resumable == False:
                    # upload simples
                    response = self.drive_service.files().create(
                        body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
                    file_id = response.get('id')
                else:
                    # UPLOAD EM PARTES (NECESSARIO PARA ARQUIVOS > 5MB)
                    request = self.drive_service.files().create(
                        body=file_metadata, media_body=media, fields='id', supportsAllDrives=True)

                    response = None
                    while response is None:
                        status, response = request.next_chunk()
                        if status:
                            print(f"Uploaded {int(status.progress() * 100)}%.")
                    file_id = response.get('id')
                return file_id
            except Exception as e:
                print("PROBLEMA NO UPLOAD: \n\n", e)
                raise e
        else:
            """ ERRO NO MIME"""
            print(Exception("ERRO AO PEGAR MIMETYPE"))
            return None

    def update_file(self, new_data, filename, folder, parents):
        """
        Updates a file in Google Drive with new data

        Args:
            new_data: Path to the new file data
            filename: Name of the file to update
            folder: Name of the folder containing the file

        Returns:
            str: ID of updated file or None if update fails
        """
        try:
            # Get folder and file IDs
            folder_id = self.get_folder_id(folder, parents)
            file_id = self.get_file_id(filename)

            if not folder_id:
                print("Folder not found")
                return None
            elif not file_id:
                print("File not found")
                return None

            # Create media object for new file
            mime = mimetypes.guess_type(new_data)
            if mime:
                media = MediaFileUpload(new_data, mimetype=mime[0])

                # Update the file
                updated_file = self.drive_service.files().update(
                    fileId=file_id,
                    media_body=media
                ).execute()

                self.fetch_drive_files()  # Update local state
                return updated_file.get('id')

            return None

        except Exception as e:
            print(f"Error updating file: {e}")
            return None

    def delete_file(self, file_id):
        """
        Delete a file from a specific folder in Google Drive

        Args:
            file_id: ID of the file to delete
            folder_id: ID of the folder containing the file

        Returns:
            bool: True if deletion successful, False otherwise
        """
        print("\n")
        try:
            if file_id == self.ID_ROOT_DADOS:
                raise ValueError("NAO PODE DELETAR ROOT_DADOS!!!!!!!")
            # Delete the file
            self.drive_service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
            time.sleep(1)
            self.fetch_drive_files()
            return True

        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    def download_file(self, file_id):
        self.fetch_drive_files()

        request = self.drive_service.files(
            fields="file(name)").get_media(fileId=file_id)
        import io
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request, chunksize=1024 * 1024)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
        return file.getvalue(), request.get('file').get('name', None)
