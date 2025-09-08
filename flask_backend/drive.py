import traceback
from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import mimetypes
import os
import time
import pandas as pd

# NOTE!!!!!!!!! SE NECESSARIO, CRIAR FORMA DE MANTER ROOT_DRIVE AUTALIZADO, SENAO APLCIACAO PODE QUEBRAR


class GoogleDrive:
    """Classe que lidara com logica relacionada a interacoes com API do Google Drive\n
    :param pd.DataFrame file_state: Dataframe que ira conter todas as informacoes sobre os arquivos e folders no Drive
    """

    def __init__(self, PATH_CRED, ROOT_DRIVE):
        """NAO MUDAR!!!!!! E NAO CONFUNDIR ID'S DE ROOT!!!!!!!"""
        # TODO: mudar para '0AHIxAncewr_KUk9PVA' em PRODUCAO
        self.ID_ROOT_CONTA_SERVICO = "root"

        self.emailOwner = "viplab.psno@nca.ufma.br"
        self.emailService = "teste-drive@pibiti6-nervo.iam.gserviceaccount.com"
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        CREDENTIALS = service_account.Credentials.from_service_account_file(
            PATH_CRED,
            scopes=SCOPES,
            subject=self.emailService,
        )
        self.drive_service = build("drive", "v3", credentials=CREDENTIALS)
        self.first_fetch = True
        self.startPageToken = None
        """ self.file_state: dict[str, dict[str, str]] """

        # dict que vai mapear nomes de arquivos a lista de id's desses arquivos
        self.hash_nomes = {}
        self.ROOT_DRIVE = ROOT_DRIVE
        self.ID_ROOT_DADOS = os.environ.get("ID_ROOT_FOLDER_GDRIVE", None)
        if not self.ID_ROOT_DADOS:
            raise ValueError(
                "ID ROOT NAO SETADO!!!!!! (CHECAR SE env.csv ESTA PRESENTE NO FOLDER DO SERVIDOR!!)"
            )
        print(f"ID ROOT: {self.ID_ROOT_DADOS}")
        self.fetch_drive_files()

    def initial_fetch(self):
        # Get initial state and start page token

        page_token = None
        files = []

        # First, get the starting page token for future changes
        response = self.drive_service.changes().getStartPageToken().execute()
        self.startPageToken = response.get("startPageToken")

        while True:
            response = (
                self.drive_service.files()
                .list(
                    pageSize=100,
                    fields="nextPageToken, files(id, name, mimeType, modifiedTime, parents)",
                    pageToken=page_token,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                    q="trashed=false",
                )
                .execute()
            )

            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

        self.file_state = {}
        for file in files:

            if file.get("name") not in self.hash_nomes.keys():
                self.hash_nomes[file.get("name")] = []
            # self.hash_nomes[file.get('name')].append(file['id'])
            id_parent = file.get("parents")
            if id_parent != None and len(id_parent) > 1:
                raise Exception("INITIAL FETCH ERROR: ID_PARENT LENGTH TOO BIG")
            # id_parent None significa que parent eh ROOT_DADOS
            id_parent = id_parent[0] if id_parent != None else self.ID_ROOT_DADOS
            if id_parent == self.ID_ROOT_CONTA_SERVICO:
                raise Exception("PEGAR ARQUIVOS DA CONTA DE SERVIÇO É PROBIDO!!!!!")
            self.file_state[file["id"]] = {
                "name": file.get("name"),
                "modified": file.get("modifiedTime"),
                "parents": [id_parent],
                "mimeType": file.get("mimeType"),
            }
        self.file_state = pd.DataFrame.from_dict(self.file_state, orient="index")
        # more options can be specified also
        with pd.option_context("display.max_rows", None, "display.max_columns", 3):
            print(f"DF FILE STATE: \n{self.file_state}")
        self.first_fetch = False

    def update_state(self, changes, verbose=False):
        """
        Atualiza dataframe com estado local do drive\n
        :param Any changes: objeto que contera mudanças vindas da change API
        """
        aux_file_state = {}
        for change in changes:
            if verbose:
                print("CHANGE: ", change)
            file_id = change.get("fileId")
            trashed = change.get("file", {}).get("trashed", False)
            if change.get("removed", False) or trashed:
                if file_id in self.file_state.index:
                    # tira arquivo do registro SE NAO FOI DELETADO ANTES
                    self.file_state.drop(index=file_id, inplace=True)
            else:
                # atualiza arquivo no registro
                file = change.get("file")
                id_parent = file.get("parents")
                if id_parent != None and len(id_parent) > 1:
                    raise Exception("INITIAL FETCH ERROR: ID_PARENT LENGTH TOO BIG")

                # id_parent None significa que parent eh ROOT_DADOS
                id_parent = id_parent[0] if id_parent != None else self.ID_ROOT_DADOS
                if id_parent == self.ID_ROOT_CONTA_SERVICO:
                    raise Exception("PEGAR ARQUIVOS DA CONTA DE SERVIÇO É PROBIDO!!!!!")

                aux_file_state[file_id] = {
                    "name": file.get("name"),
                    "modified": file.get("modifiedTime"),
                    "parents": [id_parent],
                    "mimeType": file.get("mimeType"),
                }
        modificacoes = pd.DataFrame.from_dict(aux_file_state, orient="index")
        if verbose:
            with pd.option_context("display.max_rows", None, "display.max_columns", 2):
                print(f"DF MODIFICACOES: \n{modificacoes}\n")

        if not self.file_state.empty:
            self.file_state.update(modificacoes)
            new_ids = modificacoes.index.difference(self.file_state.index)
            to_append = modificacoes.loc[new_ids]
            self.file_state = pd.concat([self.file_state, to_append], axis=0)

            print("update_state: ATUALIZOU")
            if verbose:
                with pd.option_context(
                    "display.max_rows", None, "display.max_columns", 2
                ):
                    print(f"DF FILE STATE DEPOIS DAS MODIF: \n{self.file_state}\n")
        else:
            self.file_state = modificacoes.copy()

    def fetch_drive_files(self, changed_file_id=None):
        """
        Query Google Drive to fetch a list of all files (INCLUDES FOLDERS) THAT HAVE BEEN CHANGED.
        NOTE: if needing sync, specify changed_file_id after EACH operation
        Returns:
            the file_state
        """
        # contador para evitar loops infinitos
        cont = 0
        delay = 0.5
        if self.first_fetch:
            self.initial_fetch()
            return self.file_state
        # NOTE!!!! USUÁRIO NÃO PODE MODIFICAR PASTAS NO ROOT DA CONTA DE USUÁRIO SENÃO PODE QUEBRAR SINCRONIA!!!!!!
        page_token = self.startPageToken
        while page_token is not None:
            try:
                # se tiver delay, refaz chamadas ate haver mudancas
                while True:
                    response = (
                        self.drive_service.changes()
                        .list(
                            pageToken=page_token,
                            includeRemoved=True,
                            includeItemsFromAllDrives=True,
                            supportsAllDrives=True,
                            pageSize=50,
                            fields="nextPageToken, newStartPageToken, changes(fileId, file(trashed, modifiedTime, name, parents, mimeType), removed)",
                        )
                        .execute()
                    )
                    if "newStartPageToken" in response.keys():
                        # Save this token for the next polling interval
                        a = self.startPageToken
                        self.startPageToken = response.get("newStartPageToken")

                    changes = response.get("changes", [])
                    if changed_file_id != None and len(changes) > 0:
                        ids = [change.get("fileId") for change in changes]
                        print("Changes detected.")
                        self.update_state(changes)

                        if changed_file_id in ids:
                            print("ACHOU MUDANÇA!")
                            break
                        else:
                            print("NAO ACHOU!")
                            time.sleep(1)
                            cont += 1

                    elif changed_file_id != None:
                        print("No changes detected...")
                        time.sleep(1)
                        cont += 1
                        if cont > 20:
                            print("PASSOU DO LIMITE!")
                            break
                    else:
                        # sem mudança e sem espera nao faz nada e continua no while externo
                        break

                page_token = response.get("nextPageToken", None)

            except HttpError as error:
                print(f"An error occurred: {error}")
                if delay:
                    time.sleep(delay)  # Retry after a delay
                else:
                    return error

        return self.file_state

    def check_id(self, id_drive):
        try:
            file = (
                self.drive_service.files()
                .get(fileId=id_drive, fields="id", supportsAllDrives=True)
                .execute()
            )
            return file is not None
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def get_file_id(self, file_name, folder_name=None):
        if self.file_state.empty:
            return None

        if folder_name:
            id_folder = self.get_folder_id(folder_name)

        existe = file_name in self.file_state["name"].values

        if not existe:
            # print("ARQUIVO NAO EXISTE!")
            return None
        if folder_name:
            cond_extra = self.file_state["parents"].apply(lambda x: x == [id_folder])
        else:
            cond_extra = True
        matching_files = self.file_state[
            (self.file_state["mimeType"] != "application/vnd.google-apps.folder")
            & (self.file_state["name"] == file_name)
            & cond_extra
        ]
        if not matching_files.empty:
            return matching_files.index[0]

        return None

    def get_folder_id(self, folder_name):
        # partindo do principio que ROOT_DRIVE sempre existe e ja esta configurado ;)
        if folder_name == self.ROOT_DRIVE:
            return self.ID_ROOT_DADOS

        if self.file_state.empty:
            print("FILE STATE VAZIO")
            return None

        existe = folder_name in self.file_state["name"].values

        if not existe:
            print("FOLDER NAO EXISTE!")
            return None

        matching_files = self.file_state[
            (self.file_state["mimeType"] == "application/vnd.google-apps.folder")
            & (self.file_state["name"] == folder_name)
        ]
        if not matching_files.empty:
            # print(f"\nMATCHED FILES FOR {folder_name}:{matching_files}")
            return matching_files.index[0]

        # print(f"MATCHED FILES :{matching_files}")
        return None

    def create_folder(self, nomes_parents: list = [], wait=False):
        """
        Criacao de Folder. PRECISA SEMPRE GARANTIR QUE NAO HAJAM DUPLICATAS!!!!
        (NUNCA INCLUIR O NOME DO ROOT DENTRO)
        """
        folder_name = nomes_parents[-1]
        # print(f"\nFOLDER_NAME: {folder_name}")
        # print(f"CAMINHO: {nomes_parents}\n")

        if folder_name == self.ROOT_DRIVE:
            print(f"TENTANDO CRIAR ROOT_DRIVE '{self.ROOT_DRIVE}'. Abortando...")
            return None
        if self.ROOT_DRIVE not in nomes_parents:
            # so pra garantir que o primeiro eh o ROOT_DRIVE
            nomes_parents.insert(0, self.ROOT_DRIVE)
        elif nomes_parents[0] != self.ROOT_DRIVE:
            nomes_parents.remove(self.ROOT_DRIVE)
            nomes_parents.insert(0, self.ROOT_DRIVE)

        folder_novo = nomes_parents[-1]
        id_novo = self.get_folder_id(folder_novo)
        if id_novo != None:
            # nome de folder ja existe, logo nao pode criar
            return id_novo

        folder_list = []
        folder_list.extend(nomes_parents)

        id_parents = [self.ID_ROOT_DADOS]
        # pula primeiro ja que eh sempre ROOT_DRIVE
        # self.fetch_drive_files()
        for i in range(1, len(folder_list)):
            # da fecth para atualizar estado local
            id = self.get_folder_id(folder_list[i])
            if id == None:
                # id nulo, cria folder com parents ja criados
                folder_metadata = {
                    "name": folder_list[i],
                    "parents": [id_parents[i - 1]],
                    "mimeType": "application/vnd.google-apps.folder",
                }
                folder_drive = (
                    self.drive_service.files()
                    .create(body=folder_metadata, fields="id")
                    .execute()
                )
                print(
                    f"FOLDER CRIADO: {folder_list[i]}, FOLDER METADATA: NAME AND PARENT:{folder_metadata['name'], folder_metadata['parents']}"
                )
                folder_id = folder_drive.get("id")
                id_parents.append(folder_id)
                if wait:
                    self.fetch_drive_files(changed_file_id=folder_id)
            else:
                folder_id = id
                # print(f"FOLDER {folder_list[i]} JA EXISTE!")
            id_parents.append(folder_id)

        return folder_id

    def upload_to_drive(self, file_path, nomes_parents=[], wait=False, resumable=False):
        """
        Faz upload de arquivo para o drive; Cria folder de destino se folder nao existir \n

        :param list[str] nomes_parents: contem nomes dos folders-pai do arquivo (NUNCA INCLUIR O NOME DO ROOT DENTRO)
        Returns: id do arquivo criado
        """
        # self.fetch_drive_files()
        try:

            nomes_parents.insert(0, self.ROOT_DRIVE)

            print(f"NO UPLOAD: FILE: {file_path} PARENTS: {nomes_parents}\n\n")
            if len(nomes_parents) >= 2:
                # quer inserir em um diretorio mais profundo que ROOT_DRIVE
                parent = nomes_parents[-2]

                # pega id do folder mais profundo
                print(f"INNER FOLDER: {nomes_parents[-1]} PARENT: {parent}")
                id_folder = self.get_folder_id(nomes_parents[-1])
            else:
                print(f"AVISO!! INSERINDO em {self.ROOT_DRIVE}!")
                # quer inserir no ROOT
                id_folder = self.get_folder_id(nomes_parents[0])

            # checa se ja existe arquivo igual naquele diretorio
            filename = os.path.basename(file_path)
            id_file = self.get_file_id(filename, nomes_parents[-1])
            if id_file != None:
                return id_file

            # cria parentes, se nao existirem, e folder
            if id_folder == None:
                print(f"ESPERANDO DIRETORIO {nomes_parents[-1]}")

            mime = mimetypes.guess_type(file_path)
            if mime[0]:
                media = MediaFileUpload(
                    file_path, mimetype=mime[0], resumable=resumable
                )

                file_metadata = {
                    "name": filename,
                    "parents": [id_folder],
                }
                """NOTE: SEMPRE QUE ESPECIFICAR 'parents' BOTAR COMO UM ARRAY!!!!!!! SENAO API VAI DAR BUG SILENCIOSO!!!!!!!!"""
                try:
                    print("FAZENDO UPLOAD")
                    if resumable == False:
                        # upload simples
                        response = (
                            self.drive_service.files()
                            .create(
                                body=file_metadata,
                                media_body=media,
                                fields="id",
                                supportsAllDrives=True,
                            )
                            .execute()
                        )
                        file_id = response.get("id")
                        # self.fetch_drive_files(changed_file_id=file_id)
                    else:
                        # UPLOAD EM PARTES (NECESSARIO PARA ARQUIVOS > 5MB)
                        request = self.drive_service.files().create(
                            body=file_metadata,
                            media_body=media,
                            fields="id",
                            supportsAllDrives=True,
                        )

                        response = None
                        while response is None:
                            status, response = request.next_chunk()
                            if status:
                                print(f"Uploaded {int(status.progress() * 100)}%.")
                        file_id = response.get("id")

                        if wait:
                            self.fetch_drive_files(changed_file_id=file_id)
                    return file_id
                except Exception as e:
                    print("PROBLEMA NO UPLOAD: \n\n", e)
                    raise
            else:
                """ERRO NO MIME"""
                raise Exception("ERRO AO PEGAR MIMETYPE")
                return None

        except Exception as e:
            print("ERRO NO UPLOAD: ", e)
            traceback.print_exc()

    def update_file(self, new_data, filename, folder):
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
            folder_id = self.get_folder_id(folder)
            file_id = self.get_file_id(filename, folder)

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
                updated_file = (
                    self.drive_service.files()
                    .update(fileId=file_id, media_body=media)
                    .execute()
                )

                # self.fetch_drive_files()   #Update local state
                return updated_file.get("id")

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
            self.drive_service.files().delete(
                fileId=file_id, supportsAllDrives=True
            ).execute()

            # self.fetch_drive_files()

            return True

        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    def download_file(self, file_id):
        # self.fetch_drive_files()
        filename = str(self.file_state.loc[file_id, "name"])
        request = self.drive_service.files().get_media(fileId=file_id)
        print(request)
        import io

        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request, chunksize=1024 * 1024)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
        return file.getvalue(), filename
