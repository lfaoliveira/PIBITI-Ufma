# 6NerveTrack

Aplicativo Web projetado para diagnosticar **Paralisia do Nervo Abducente (6º nervo craniano)**, implementando o mesmo modelo utilizado em *Computational method for aid in the diagnosis of sixth optic nerve palsy through digital videos*.

Desenvolvido pelo grupo de pesquisa **VIPLab** no programa **PIBITI** da **UFMA** (Universidade Federal do Maranhão).

## Funcionalidades

- **Upload e análise de vídeo** — o médico faz upload de um vídeo dos movimentos oculares do paciente
- **Detecção de olhos com YOLOv3** — modelo treinado customizado detecta as regiões dos olhos em cada frame
- **Análise de velocidade** — calcula a velocidade de deslocamento de cada olho e compara: se um olho se move ≥19,65% mais lento que o outro, é sinalizado como potencialmente paralisado
- **Geração de relatório PDF** — relatório com gráficos de velocidade, dados do paciente e diagnóstico
- **Armazenamento no Google Drive** — vídeos e resultados são sincronizados automaticamente via conta de serviço
- **Notificações em tempo real** — WebSocket notifica o médico quando a análise é concluída
- **Cadastro de médicos com aprovação** — admin recebe e-mail para aceitar ou recusar novos cadastros
- **Perfil do médico** — histórico paginado de diagnósticos salvos

> ### OBSERVAÇÃO!!!
> ADMINS NÃO PODEM MEXER NA PASTA DO DRIVE QUE CONTÉM VÍDEOS E ARQUIVOS DOS PACIENTES!

---

## Tech Stack

| Camada | Tecnologia |
|---|---|
| **Backend** | Flask 3.1 (ASGI via Starlette + Uvicorn) |
| **Frontend** | Vue 3.4 + Vite 5.4 + Vue Router 4 + Vuex 4 |
| **CSS** | SCSS + Tailwind CSS 4 |
| **Banco de dados** | MongoDB 7.0 (Flask-PyMongo) |
| **Message Broker** | Redis 7 |
| **Fila de tarefas** | Celery 5.5+ (solo pool) |
| **Modelo ML** | TensorFlow 2.8 + Keras (YOLOv3) |
| **Visão computacional** | OpenCV (headless), Pillow, scikit-image |
| **Geração de PDF** | WeasyPrint + BeautifulSoup4 |
| **Armazenamento na nuvem** | Google Drive API v3 (conta de serviço) |
| **E-mail** | Flask-Mail (SMTP Gmail) |
| **WebSocket** | Starlette WebSocketRoute |
| **Processamento de vídeo** | ffmpeg-python |
| **Autenticação** | Flask-Login (sessão, SHA3-256) |
| **Containers** | Docker + Docker Compose |

---

## Arquitetura

```
┌─────────────┐     ┌──────────────────────────────────┐     ┌─────────┐
│  Vue 3 +    │────▶│  Starlette (ASGI)                │────▶│ MongoDB │
│  Vite       │ WS  │  ├── /ws     (WebSocket)         │     └─────────┘
│  :5173      │◀────│  └── /api/*  (Flask WSGI mount)  │
└─────────────┘     │         :5000                    │     ┌─────────┐
                    └──────────┬───────────────────────┘────▶│ Google  │
                               │                             │ Drive   │
                    ┌──────────▼───────────────────────┐     └─────────┘
                    │  Celery Worker                    │
                    │  (envia_diag → YOLOv3 → Drive)   │
                    └──────────┬───────────────────────┘
                               │
                    ┌──────────▼──┐
                    │   Redis 7   │
                    └─────────────┘
```

O Flask (WSGI) é encapsulado pelo `WSGIMiddleware` do Starlette e montado em `/api`. O Starlette cuida do WebSocket em `/ws`. O processamento pesado (detecção YOLO, conversão de vídeo, upload para Drive) é executado em 3 tarefas Celery encadeadas.

---

## Requisitos

- **Python** 3.9 (via Conda) com TensorFlow ≤ 2.8
- **Node.js** ≥ 18
- **MongoDB** 7.0+
- **Redis** 7+
- **ffmpeg** instalado no sistema
- **Docker** + **Docker Compose** (para produção)
- Pango para geração de PDF via WeasyPrint (usar MYSYS2 no Windows para isso)

### Arquivos obrigatórios

- `flask_backend/permalink-googleDrive-pibiti6-nervo.json` — credenciais da conta de serviço do Google Drive
- `flask_backend/trained_weights_final.h5` — pesos treinados do modelo YOLOv3
- `env.csv` — variáveis de ambiente (na raiz do projeto)

---

## Variáveis de Ambiente

### Backend (Flask / Celery)

| Variável | Descrição |
|---|---|
| `MONGO_URI` | String de conexão do MongoDB |
| `SECRET_KEY` | Chave secreta da sessão Flask |
| `FLASK_BASE_URL` | URL pública do backend Flask |
| `VUE_FRONT_URL` | URL do frontend (para links em e-mails) |
| `CELERY_BROKER_URL` | URL do Redis como broker do Celery |
| `CELERY_RESULT_BACKEND` | URL do Redis para resultados do Celery |
| `ID_ROOT_FOLDER_GDRIVE` | ID da pasta raiz no Google Drive |
| `MAIL_SERVER` | Servidor SMTP (ex: `smtp.gmail.com`) |
| `MAIL_PORT` | Porta SMTP (ex: `587`) |
| `MAIL_USE_TLS` | Habilitar TLS (`True`) |
| `MAIL_USERNAME` | Usuário da conta de e-mail |
| `MAIL_PASSWORD` | Senha de aplicativo do e-mail |
| `MAIL_DEFAULT_SENDER` | E-mail remetente padrão |

### Frontend (Vite)

| Variável | Descrição |
|---|---|
| `VITE_BACKEND_URL` | URL da API backend (ex: `http://localhost:5000`) |
| `VITE_BACKEND_WS` | URL do WebSocket (ex: `ws://localhost:5000`) |

---

## Instalação e Execução

### Opção 1 — Desenvolvimento Local (Windows)

1. Clone o repositório:
   ```bash
   git clone https://github.com/lfaoliveira/PIBITI-Ufma
   cd PIBITI-Ufma
   ```

2. Execute o script automatizado que instala dependências, inicia MongoDB, frontend e backend:
   ```powershell
   .\run.ps1
   ```

   O script `run.ps1` realiza automaticamente:
   - Verifica e inicia o serviço MongoDB
   - Instala `ffmpeg` via winget (se necessário)
   - Valida a presença das credenciais do Google Drive
   - Instala MSYS2 + Pango (para WeasyPrint/PDF)
   - Instala pacotes Node em `vite-project/`
   - Cria o ambiente Conda `env-pibiti` a partir de `conda.yml`
   - Inicia o frontend Vue (porta 5173) e o backend Flask

#### Ou manualmente:

1. Crie e ative o ambiente Conda:
   ```bash
   conda env create --prefix ./env-pibiti --file conda.yml
   conda activate ./env-pibiti
   ```

2. Instale os pacotes do frontend:
   ```bash
   cd vite-project
   npm install
   cd ..
   ```

3. Inicie o frontend Vue:
   ```bash
   cd vite-project
   npm run dev
   ```

4. Inicie o backend Flask (em outro terminal):
   ```bash
   cd flask_backend
   python server.py
   ```

5. Inicie o Celery worker (em outro terminal):
   ```bash
   celery -A flask_backend.celery_worker worker --pool=solo
   ```

### Opção 2 — Docker (Produção)

```bash
docker-compose up --build
```

Isso inicia 5 serviços:

| Serviço | Porta | Descrição |
|---|---|---|
| `flask` | 5000 | Backend Flask + Uvicorn |
| `frontend` | 5173 | Frontend Vue + Vite |
| `celery_worker` | — | Worker Celery (limite 400MB RAM) |
| `redis` | 6379 | Broker / Result backend |
| `db` | 27017 | MongoDB |

Todos os serviços compartilham a rede bridge `projeto`. Os dados do MongoDB são persistidos em um volume nomeado `db`.

Consulte [DOCKER/DOCKER.md](DOCKER/DOCKER.md) para mais detalhes sobre a configuração dos containers.

---

## Endpoints da API

Todas as rotas Flask estão montadas em `/api` via Starlette.

### Autenticação

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/auth?tipo=login` | Login com e-mail/senha |
| POST | `/api/auth?tipo=cadastro` | Cadastro de novo médico |
| GET | `/api/val_login` | Validar sessão/cookies |
| GET | `/api/logout` | Logout |
| POST | `/api/esqueci_senha` | Enviar e-mail de recuperação de senha |
| POST | `/api/mudar_senha` | Alterar senha |

### Gerenciamento de Cadastro (Admin)

| Método | Rota | Descrição |
|---|---|---|
| GET/POST | `/api/aceitaCadastro/<email>` | Aceitar cadastro de médico |
| GET/POST | `/api/recusaCadastro/<email>` | Recusar cadastro de médico |

### Diagnóstico e Análise

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/analise-ws` | Enviar vídeo para análise (Celery chain) |
| PUT | `/api/analise` | Endpoint alternativo de análise |
| POST | `/api/envia_diag` | Upload de dados diagnósticos |
| GET | `/api/status/<task_id>` | Consultar status da tarefa Celery |
| POST | `/api/ver-analise/<task_uuid>` | Recuperar resultados de análise concluída |

### Arquivos

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/get-file/<resource_uri>` | Serve arquivo (local → Google Drive) |
| GET | `/api/get-file-local/<filename>` | Stream de arquivo local (`tmp/`) |
| GET | `/api/get-file-drive/<id_file>` | Stream de arquivo do Google Drive |

### Relatórios

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/gerar_relatorio/<id_diag>` | Gerar relatório PDF (`?download=true` para baixar) |
| GET | `/api/gerar_grafico/<id_diag>` | Gerar imagem do gráfico de velocidade |

### Perfil

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/pega_perfil?pagAtual=N` | Perfil do médico + diagnósticos paginados |

### WebSocket

| Rota | Descrição |
|---|---|
| `/ws` | Cliente envia `{taskId}`, servidor retorna resultado quando concluído |

---

## Rotas do Frontend

| Caminho | Componente | Descrição |
|---|---|---|
| `/` | `HomePage` | Página inicial |
| `/acesso` | `Acesso` | Login / Cadastro |
| `/ficha` | `FichaDiag` | Formulário de diagnóstico + upload de vídeo |
| `/analise?uuid=...` | `AnaliseVideo` | Visualizar resultados da análise |
| `/perfil` | `Perfil` | Perfil do médico com histórico |
| `/termos` | `Termos` | Termos de uso |
| `/metodo` | `Metodo` | Metodologia |
| `/duvidas` | `Duvidas` | Perguntas frequentes |
| `/equipe` | `Equipe` | Equipe do projeto |
| `/esqueceuSenha` | `EsqueciSenha` | Recuperação de senha |
| `/mudarSenha` | `MudarSenha` | Alteração de senha |

---

## Estrutura do Projeto

```
├── flask_backend/          # Backend Flask + lógica de análise
│   ├── server.py           # App principal (Starlette + Flask WSGI)
│   ├── analise.py          # Pipeline de processamento YOLOv3
│   ├── user.py             # Rotas de autenticação e usuário
│   ├── drive.py            # Integração com Google Drive API
│   ├── _email.py           # Envio de e-mails (Flask-Mail)
│   ├── pdf.py              # Geração de relatórios PDF
│   ├── helpers.py          # Funções auxiliares
│   ├── yolo.py             # Carregamento do modelo YOLO
│   ├── yolo3/              # Implementação do modelo YOLOv3
│   └── celery_worker/      # Configuração e tarefas Celery
├── vite-project/           # Frontend Vue 3 + Vite
│   └── src/
│       ├── components/     # Componentes Vue organizados por função
│       ├── store/          # Vuex store (modal, websocket)
│       └── router.js       # Rotas da aplicação
├── DOCKER/                 # Dockerfiles (flask, celery, frontend)
├── docker-compose.yaml     # Orquestração dos 5 serviços
├── conda.yml               # Ambiente Conda (Python 3.9 + TF)
└── run.ps1                 # Script de inicialização (Windows)
```
